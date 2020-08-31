from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order
from msa_sdk.device import Device
from msa_sdk import util

from datetime import datetime
from msa_sdk import constants
import re
import json
import xmltodict
import sys

#New Variables object
task_variables = Variables()

#Add new variables
task_variables.add('site', var_type = 'String')

#Add vars to context
context = Variables.task_call(task_variables)

process_id = context['SERVICEINSTANCEID']
ms_ipam_tenant = context['ipam_ms_aliases']['IPAM Tenants']
ms_ipam_site = context['ipam_ms_aliases']['IPAM Sites']
ms_ipam_device = context['ipam_ms_aliases']['IPAM Devices']
ipam_device_id = context['ipam_device_id']
customer_name = context['customer_name']
fail_comment = str()
success_string = str()
fail_string = f'{{"wo_status": "FAIL", "wo_comment": "{fail_comment}"}}'

#Create order object
IpamOrderObject = Order(ipam_device_id)


#Find site ID
objects_list = IpamOrderObject.command_objects_instances(ms_ipam_site)

#Collect cusromer sites object_id for future use 
for site in objects_list:
    site_object = IpamOrderObject.command_objects_instances_by_id(ms_ipam_site, 
                                                                  site)[ms_ipam_site][site]
    if site_object['object_id'] == site:
      context['site_id'] = site_object['id']

#Find all devices on the site
site_device_list = list()
for device in context['customer_details']['devices_list'].values():
    device_object = IpamOrderObject.command_objects_instances_by_id(ms_ipam_device, 
                                                                    device)[ms_ipam_device][device]
    try:
        if device_object['site'] == context['site']:
            site_device_list.append(device)
    except:
      pass

#Find staged devices on the site
for device in site_device_list:
    device_object = IpamOrderObject.command_objects_instances_by_id(ms_ipam_device, 
                                                            device)[ms_ipam_device][device]
    if not ((device_object['role'] == 'CE') and (device_object['status'] == 'staged')):
        site_device_list.remove(device)

#Finish if no single CE device in staged state in the site
if len(site_device_list) > 1:
    fail_comment = 'More then 1 CE device on the site in \'staged\' state'
    print(fail_string)

if len(site_device_list) == 0:
    fail_comment = 'No CE devices on the site in \'staged\' state'
    print(fail_string)

ce_device = IpamOrderObject.command_objects_instances_by_id(ms_ipam_device, 
                                                        site_device_list[0])[ms_ipam_device][site_device_list[0]]
ce_device_local_context = json.loads(json.dumps(xmltodict.parse(ce_device['local_context_data'])))['local_context_data']

CeDeviceObject = Device(customer_id = re.match('^\D+?(\d+?)$',context['UBIQUBEID']).group(1), 
                        name = ce_device['object_id'], 
                        device_external = ce_device['object_id'],
                        manufacturer_id = ce_device_local_context['msa_specific']['manufacture_id'],
                        password_admin = ce_device_local_context['enable_password'],
                        model_id = ce_device_local_context['msa_specific']['model_id'],
                        login = ce_device_local_context['username'], 
                        password = ce_device_local_context['password'], 
                        management_address = ce_device['primary_ip'].split('/')[0],
                        management_port = ce_device_local_context['port']
                        )

CeDeviceObject.create()
context['ce_device_details'] = dict()

context['ce_device_details']['local_context']       = ce_device_local_context
context['ce_device_details']['device_id']           = CeDeviceObject.device_id
context['ce_device_details']['external_reference']  = ce_device['object_id']

success_string = 'New CE device has been created successfully'
print(CeDeviceObject.process_content('ENDED', success_string, context, True))






