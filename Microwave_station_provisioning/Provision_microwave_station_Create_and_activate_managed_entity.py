from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order
from msa_sdk.device import Device
from msa_sdk.orchestration import Orchestration
from datetime import datetime
from msa_sdk import constants
from msa_sdk import lookup
from msa_sdk import util
import ipaddress
import time
import re
import json
import sys
import os

"""
The proposals of the task are:
 - Create and activate NEC iPasolink managed entity
"""


#New Variables object
TaskVariables = Variables()

#Add vars to context
context = Variables.task_call(TaskVariables)

process_id = context['SERVICEINSTANCEID']
nec_ipasolink_manufacture_id = '70000'
nec_ipasolink_model_id = '7000123'
nec_ipasolink_default_password = '12345678'
nec_ipasolink_default_username = 'Admin'
nec_ipasolink_profile_name = 'nec_ipasolink_profile'


#Variables to finish the task properlly
fail_comment = str()
success_comment = str()
fail_string = f'{{"wo_status": "FAIL", "wo_comment": "{fail_comment}"}}'
success_string = f'{{"wo_status": "ENDED", "wo_comment": "{success_comment}"}}'

#Create Orchestration object to update GUI dynamically
Orchestration = Orchestration(context['UBIQUBEID'])
async_update_list = (context['PROCESSINSTANCEID'], context['TASKID'], context['EXECNUMBER'])


#Create microwave station object
StationDeviceObject = Device(customer_id = re.match('^\D+?(\d+?)$',context['UBIQUBEID']).group(1), 
                      		 name = '{}[{}]'.format(context['hostname'], context['ip_address']), 
                      		 device_external = re.sub(r'[\.\[\]-]', "_", context['hostname']),
                      		 manufacturer_id = nec_ipasolink_manufacture_id,
                      		 password_admin = nec_ipasolink_default_password,
                      		 model_id = nec_ipasolink_model_id,
                      		 login = nec_ipasolink_default_username, 
                      		 password = nec_ipasolink_default_password, 
                      		 management_address = context['ip_address'],
                      		 management_port = '22'
                            )

StationDeviceObject.create()

pretty_formatted_bar = list('-'*12)
Orchestration.update_asynchronous_task_details(*async_update_list, 'Creating managed entity for the station... [{}]'.format(''.join(pretty_formatted_bar)))


#Provision device
StationDeviceObject.initial_provisioning()

#Create station device order object
context['station_device_id'] = StationDeviceObject.device_id
StationOrderObject = Order(context['station_device_id'])

#Wait until provisioning is done
while StationDeviceObject.provision_status()['status'] != 'OK':
    pretty_formatted_bar.insert(0,'*')
    Orchestration.update_asynchronous_task_details(*async_update_list, 'Creating managed entity for the station... [{}]'.format(''.join(pretty_formatted_bar)))
    time.sleep(5)
    
#Attach configuration profile
Orchestration.update_asynchronous_task_details(*async_update_list, 'Attaching configuration deployment settings profile... ') 
StationDeviceObject.profile_attach(nec_ipasolink_profile_name)
Orchestration.update_asynchronous_task_details(*async_update_list, 'Attaching configuration deployment settings profile... OK') 

for counter in range(0, 12):
    pretty_formatted_bar.insert(0,'*')
    pretty_formatted_bar.pop()
    Orchestration.update_asynchronous_task_details(*async_update_list, 'Creating managed entity for the station... [{}]'.format(''.join(pretty_formatted_bar)))
    time.sleep(5)

#Sync up microservices
response = StationOrderObject.command_synchronize(300)
    
Orchestration.update_asynchronous_task_details(*async_update_list, 'Creating managed entity for the station... [{}] OK'.format(''.join(pretty_formatted_bar)))
time.sleep(3) 


success_comment = 'Microwave station managed entity created sucessfully.'
print(StationDeviceObject.process_content('ENDED', success_comment, context, True))


