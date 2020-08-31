from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order
from msa_sdk.device import Device
from datetime import datetime
from msa_sdk import constants
from msa_sdk import util
import time
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

process_id                   = context['SERVICEINSTANCEID']
ce_device_id                 = context['ce_device_details']['device_id']
ce_device_external_reference = context['ce_device_details']['external_reference']
ce_device_name 				 = context['ce_device_details']['external_reference']
ce_local_context             = context['ce_device_details']['local_context']
ms_ipam_device 				 = context['ipam_ms_aliases']['IPAM Devices']
customer_name                = context['customer_name']
ipam_device_id               = context['ipam_device_id']
fail_comment                 = str()
success_string               = str()
fail_string                  = f'{{"wo_status": "FAIL", "wo_comment": "{fail_comment}"}}'


#IPAM order object
IpamOrderObject = Order(ipam_device_id)

#Create CE device object
CeDeviceObject = Device(device_id = ce_device_id,
                        device_external = ce_device_external_reference)

#If the device mgmt interface is REST-based, add required configuration variables
if 'rest' in ce_local_context['interface'].lower():
    for variable, value in ce_local_context['msa_specific']['rest_headers'].items():
        CeDeviceObject.create_configuration_variable(name = variable, value = value)

#Provision device
CeDeviceObject.initial_provisioning()

#Wait until provisioning is done
while json.loads(CeDeviceObject.provision_status())['status'] != 'OK':
    time.sleep(10)

time.sleep(120)

#Attach configuration profile
CeDeviceObject.profile_attach(ce_local_context['msa_specific']['deployment_settings_ref'])


#Create CE device irder object
CeOrderObject = Order(ce_device_id)
response = CeOrderObject.command_synchronize(300)


device_object = IpamOrderObject.command_objects_instances_by_id(ms_ipam_device, 
                                                                ce_device_name)[ms_ipam_device][ce_device_name.replace('.', '_')]
#Mark the device as Active in IPAM
ms_dict = {ms_ipam_device: 
                       {ce_device_name: {'object_id': ce_device_name,
                                    	 'status':   'active',
                                    	 'site': device_object['site'],
                                    	 'role': device_object['role'],
                                    	 'model': device_object['model']
                                    }
                        }
        }
util.log_to_process_file(process_id, 'MS DICT {}'.format(ms_dict))
IpamOrderObject.command_execute('UPDATE', ms_dict)


#Clean up context
context.pop('ce_device_details')


success_string = 'New CE device has been proviosioned successfully'
print(CeDeviceObject.process_content('ENDED', success_string, context, True))
