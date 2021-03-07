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


"""

#New Variables object
TaskVariables = Variables()

#Add vars to context
context = Variables.task_call(TaskVariables)

#Udate exchange file
with open(context['exchange_file'], 'r') as exchange_file:
    exchange_dict = json.load(exchange_file)

process_id                   = context['SERVICEINSTANCEID']
site_ip_plan			 	 = exchange_dict['site_ip_plan']
ms_router_dns_records		 = context['ms_aliases']['Router DNS host records']

#Variables to finish the task properlly
fail_comment = str()
success_comment = str()
fail_string = f'{{"wo_status": "FAIL", "wo_comment": "{fail_comment}"}}'
success_string = f'{{"wo_status": "ENDED", "wo_comment": "{success_comment}"}}'

#Create Orchestration object to update GUI dynamically
Orchestration = Orchestration(context['UBIQUBEID'])
async_update_list = (context['PROCESSINSTANCEID'], context['TASKID'], context['EXECNUMBER'])


#Create site router Order object
RouterOrderObject = Order(context['dns_server_device_id'])
RouterOrderObject.command_synchronize(300)

#Create DNS record for each host in site_ip_plan
objects_list = RouterOrderObject.command_objects_instances(ms_router_dns_records)

for host_record_object in objects_list:
   ms_dict = {ms_router_dns_records: {host_record_object: dict()}}
   RouterOrderObject.command_execute('DELETE', ms_dict)

result = MSA_API.process_content('ENDED', 'DNS Records have been updated', context, True)
print(result)

