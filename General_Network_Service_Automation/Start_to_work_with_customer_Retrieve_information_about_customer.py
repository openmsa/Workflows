from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order
from msa_sdk.orchestration import Orchestration
from datetime import datetime
from msa_sdk import constants
from msa_sdk import util
import json
import sys
import time


"""
The proposals of the tasks are:
  - Check whether is the customer defined in IPAM system;
  - Retrive usefull infomration about the customer:
     - Sites;
     - Devices
  - Put information in context as customer_details (dict)

"""


#Create Variables() object and retrieve useful variables
TaskVariables = Variables()
context = Variables.task_call(TaskVariables)

ms_ipam_tenant = context['ipam_ms_aliases']['IPAM Tenants']
ms_ipam_site = context['ipam_ms_aliases']['IPAM Sites']
ms_ipam_device = context['ipam_ms_aliases']['IPAM Devices']
ms_ipam_vrf = context['ipam_ms_aliases']['IPAM VRFs']
ipam_device_id = context['ipam_device_id']
customer_name = context['customer_name']

#Variables to finish the task properlly
fail_comment = str()
success_comment = str()
fail_string = f'{{"wo_status": "FAIL", "wo_comment": "{fail_comment}"}}'
success_string = f'{{"wo_status": "ENDED", "wo_comment": "{success_comment}"}}'

#Create Orchestration object to update GUI dynamically
Orchestration = Orchestration(context['UBIQUBEID'])
async_update_list = (context['PROCESSINSTANCEID'], context['TASKID'], context['EXECNUMBER'])


#Create order object
IpamOrderObject = Order(ipam_device_id)
IpamOrderObject.command_synchronize(300)

#Retrieve info about tenants
Orchestration.update_asynchronous_task_details(*async_update_list, 'Retrieving information about customer... ')
objects_list = IpamOrderObject.command_objects_instances(ms_ipam_tenant)

#Check if customer exists in IPAM system
does_tenant_exists = False
counter = 0
while not does_tenant_exists and counter < len(objects_list):
    tenant_object = IpamOrderObject.command_objects_instances_by_id(ms_ipam_tenant, 
                                                                    objects_list[counter])[ms_ipam_tenant][objects_list[counter]]
    if tenant_object['object_id'] == customer_name:
        does_tenant_exists = True
        customer_id = tenant_object['id']
    counter += 1

#If the customer does not exist in IPAM system, finish the task as fail
if not does_tenant_exists:
    fail_comment = f'Customer {customer_name} has not been found'
    print(fail_string)



#If we here, cusotmer exists. Extract customer sites
Orchestration.update_asynchronous_task_details(*async_update_list, 'Retrieving information about customer... OK')
Orchestration.update_asynchronous_task_details(*async_update_list, 'Retrieving customer details... ')

objects_list = IpamOrderObject.command_objects_instances(ms_ipam_site)

#Collect cusromer sites object_id for future use 
sites_list = list()
for site in objects_list:
    site_object = IpamOrderObject.command_objects_instances_by_id(ms_ipam_site, 
                                                            site)[ms_ipam_site][site]
    try:
        if site_object['tenant'] == customer_name:
            sites_list.append(site)
    except:
      pass

#Extract customer devices
objects_list = IpamOrderObject.command_objects_instances(ms_ipam_device)

#Collect cusromer sites object_id for future use 
devices_list = list()
for device in objects_list:
    device_object = IpamOrderObject.command_objects_instances_by_id(ms_ipam_device, 
                                                                    device)[ms_ipam_device][device]
    try:
        if device_object['tenant'] == customer_name:
            devices_list.append(device)
    except:
      pass

#Extract customer devices
objects_list = IpamOrderObject.command_objects_instances(ms_ipam_vrf)

#Collect cusromer sites object_id for future use 
vrf_list = list()
for vrf in objects_list:
    vrf_object = IpamOrderObject.command_objects_instances_by_id(ms_ipam_vrf, 
                                                                 vrf)[ms_ipam_vrf][vrf]
    try:
        if vrf_object['tenant'] == customer_name:
            vrf_list.append(vrf)
    except:
      pass

Orchestration.update_asynchronous_task_details(*async_update_list, 'Retrieving customer details... OK')

success_comment = 'Customer {} exists in IPAM system. It has {} sites and {} devices'.format(customer_name, len(sites_list), len(devices_list))

context['customer_details'] = {
                               "name": customer_name,
                               "object_id": tenant_object,
                               "customer_id": customer_id,
                               "sites_list": sites_list,
                               "devices_list": devices_list
                              }
if len(vrf_list) > 0:
  context['customer_details']['vrf'] = vrf_list[0].replace(' ', '_')


#Finish the task correctlly
print(MSA_API.process_content('ENDED', success_comment , context, True))