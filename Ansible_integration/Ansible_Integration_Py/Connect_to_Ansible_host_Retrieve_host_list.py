import hashlib
import zlib
import json
import sys
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk import constants
from msa_sdk.orchestration import Orchestration
from msa_sdk.order import Order
from msa_sdk.device import Device
from msa_sdk.customer import Customer

dev_var = Variables()
context = Variables.task_call(dev_var)

context['test1'] = "valeur1"
context.update(test2="valeur2")
#Grab variable from context
device_id = context['device_id']

#Instantiate Order object.
order = Order(device_id)
    
#Retrieve variables from context and define the new ones
Orchestration = Orchestration(context['UBIQUBEID'])
async_update_list = (context['PROCESSINSTANCEID'],
                     context['TASKID'], context['EXECNUMBER'])

if __name__ == "__main__":
    
    #Extract numeric customer ID
    customer_db_ext_ref = context['UBIQUBEID']
    
    context['customer_db_id'] = customer_db_ext_ref
    
    if context['do_import_hosts'] == True:
        Orchestration.update_asynchronous_task_details(*async_update_list, f'Extract host list from ansible server... ')
        
        #Instantiate Customer object
        customer = Customer()
    
    	#Sync microservices
        timeout = 60
        order.command_synchronize(timeout)
    
        #Import objects from 'read_hosts_file' MS
        microservice_name = 'Read_hosts_file'
        response = order.command_objects_instances(microservice_name)
        if 'wo_status' in response:
            if response['wo_status'] == 'FAIL':
                ret = MSA_API.process_content(constants.FAILED, 'Failed to get object instances of the microservice with name "' + microservice_name + '".', context, True)
                print(ret)
                
        object_ids_array = response
    
        #Debug inject the response in the context.
        if object_ids_array:
            for object_id in object_ids_array:
                #Read object params by playbook - TODO
                object_id = object_ids_array[0] # This code is NOT support multi playbooks handling.
                response = order.command_objects_instances_by_id(microservice_name, object_id)
                if 'wo_status' in response:
                    if response['wo_status'] == 'FAIL':
                        ret = MSA_API.process_content(constants.FAILED, 'Failed to get hosts object instances where object_id = "' + object_id + '".', context, True)
                        print(ret)
                        sys.exit()

                object_details = response
                Orchestration.update_asynchronous_task_details(*async_update_list, f"Working with ansible hosts... Extract groups... ")
        
                if 'Read_hosts_file' in response:
                    object_details = response.get('Read_hosts_file').get(object_id)

                    for host_details_key in object_details['host_list']:
       
                        host_group_name = object_id
                        host_details = object_details['host_list'][host_details_key]
                        host_name = host_details['host']
                        host_username = host_details['ansible_user']
                        host_password = host_details['ansible_ssh_pass']
                        me_name = host_group_name + '[' + host_name + ']'
                        me_ext_reference = ''
                        
                        #Extract customer db id from customer db external reference
                        customer_db_id = customer_db_ext_ref[4:]
                        
                        #Create Ansible host corresponding ME.
                        device = Device(customer_id=customer_db_id, name=me_name, manufacturer_id=context['linux_manufacturer_id'], model_id=context['linux_model_id'], login=host_username, password=host_password, password_admin='', management_address=host_name, device_external=me_ext_reference, log_enabled=True, log_more_enabled=True, mail_alerting=True, reporting=True, snmp_community='public', device_id=None, management_port='22')
                        response = device.create()
                        if 'wo_status' in response:
                            if response['wo_status'] == constants.FAILED:
                                ret = MSA_API.process_content(constants.FAILED, 'Failed to create corresponding Ansible host ME with name= "'+me_name+'"', context, True)
                                print(ret)
                                sys.exit()
            
                        #Extract device id and put into context()
                        #Gather Device ID (numeric) from procvided ID
                        host_device_id = device.device_id
            
                        #Retrieve all configuration profiles of the customer and find out the one what has same name as required
                        #profile_list = customer.get_deployment_settings_by_customer_id(customer_db_id)
                        #profile_reference = 'NULL'
                        #for profile_details in profile_list:
                        #    if profile_details['name'] === context['linux_profile_name']:
                        #        profile_reference = context['profile_reference'] = profile_details['externalReference']
                    	
                    	#Attach configuration profile to managed device if reference has been found
                        '''
                        if profile_reference != 'NULL':
                            response = device.profile_attach(profile_reference)
                            status = response.get('status')
                            if status == constants.FAILED:
                                ret = MSA_API.process_content(constants.FAILED, 'Configration profile is has not been found.', context, True)
                                print(ret)
            
                            Orchestration.update_asynchronous_task_details(*async_update_list, f'Attaching configuration profile... OK')
                            sleep(3)
            
                        Orchestration.update_asynchronous_task_details(*async_update_list, f'Activating device... ')
                        '''
                		#Make initial provisioning
                        Orchestration.update_asynchronous_task_details(*async_update_list, f"Activating Managed Entity with id='" + str(host_device_id) + "' ...")
                        device.activate()


        Orchestration.update_asynchronous_task_details(*async_update_list, f"Extract host list from ansible server... OK")
            
        #Finish the task
        ret = MSA_API.process_content(constants.ENDED, 'Success. Ansible host are imported.', context, True)
        print(ret)
    else:
        ret = MSA_API.process_content(constants.ENDED, 'Success. Host import is not needed.', context, True)
        print(ret)
