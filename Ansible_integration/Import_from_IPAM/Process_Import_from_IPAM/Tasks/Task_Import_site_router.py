from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order
from msa_sdk.device import Device
from msa_sdk.orchestration import Orchestration
from datetime import datetime
from msa_sdk import constants
from msa_sdk import lookup
from msa_sdk import util
import json
import sys
import time


"""
The proposals of the tasks are:

"""


#Create Variables() object and retrieve useful variables
TaskVariables = Variables()
context = Variables.task_call(TaskVariables)

ms_ipam_tenant = context['ipam_ms_aliases']['IPAM Tenants']
ms_ipam_site = context['ipam_ms_aliases']['IPAM Sites']
ms_ipam_device = context['ipam_ms_aliases']['IPAM Devices']
ipam_device_id = context['ipam_device_id']
customer_name = context['tenant']
site_name = context['site']
process_id = context['SERVICEINSTANCEID']

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

if context['site'] not in sites_list:
    fail_comment = f'Site {site_name} has not been found'
    print(fail_string)
    
#Extract customer devices
objects_list = IpamOrderObject.command_objects_instances(ms_ipam_device)

#Collect cusromer sites object_id for future use 
site_router = None
for device in objects_list:
    device_object = IpamOrderObject.command_objects_instances_by_id(ms_ipam_device, 
                                                                    device)[ms_ipam_device][device]
    try:
        if device_object['tenant'] == customer_name and device_object['site'] == context['site']:
            site_router = device_object
    except:
      pass

if not site_router:
    fail_comment = f'There is no router on site {site_name}'
    print(fail_string)

Orchestration.update_asynchronous_task_details(*async_update_list, 'Retrieving customer details... OK')

#Find out device_id for all PE what the CE connected to
MsaLookup = lookup.Lookup()
MsaLookup.look_list_device_ids()
devices = json.loads(MsaLookup.content)
counter = 0
site_router_device_id = None

while site_router_device_id is None and counter < len(devices):
    if devices[counter]['name'] == site_router['object_id']:
        site_router_device_id = devices[counter]['id']
    counter +=1

if not site_router_device_id:
    fail_comment = 'Can not find MSA ME for router {}'.format(site_router['name'])
    print(fail_string)
else:
  context['site_router'] = site_router_device_id

success_comment = 'Sie router has been identified'

#Finish the task correctlly
print(MSA_API.process_content('ENDED', success_comment , context, True))