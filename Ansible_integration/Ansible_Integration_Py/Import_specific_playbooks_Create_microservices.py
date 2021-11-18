import os
import hashlib
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk import constants
from msa_sdk.order import Order
from msa_sdk.orchestration import Orchestration

dev_var = Variables()
dev_var.add('microservice_name_prefix', var_type='Device')
dev_var.add('playbook_list.0.playbook', var_type='String')
dev_var.add('do_monitor_changes', var_type='Boolean')
dev_var.add('monitoring_delay', var_type='String')
context = Variables.task_call(dev_var)

#Define variables
microservice_name_prefix = context['microservice_name_prefix']
microservice_file = context['read_playbook_file']
microservice_name = context['microservice_name']
variable_skeleton = context['variable_skeleton']
microservice_skeleton = context['microservice_skeleton']
microservice_dir = context['microservice_dir']

processName = context['processName']
service_id = context['service_id']
ubiqube_id = context['UBIQUBEID']

device_id = context['device_id'][3:]

#Instantiate Order object.
order = Order(device_id)

#Retrieve variables from context and define the new ones
Orchestration = Orchestration(ubiqube_id)
async_update_list = (context['PROCESSINSTANCEID'],
                     context['TASKID'], context['EXECNUMBER'])

#Syncing MS of Ansible host
Orchestration.update_asynchronous_task_details(*async_update_list, f'Syncing Ansible host... ')

#Sync microservices
timeout = 60
order.command_synchronize(timeout)

#Import Microservice objects
microservice_name = 'Retrieve_playbook_files_list'
response = order.command_objects_instances(microservice_name)
object_ids_json = json.dumps(response)
if 'wo_status' in response:
    if response['wo_status'] == 'FAIL':
        ret = MSA_API.process_content(constants.FAILED, 'Failed to get object instances of the microservice with name "' + microservice_name + '".', context, True)
        print(ret)

#Playbook object_id list            
object_ids_array = response

Orchestration.update_asynchronous_task_details(*async_update_list, f'Syncing Ansible host... OK')

Orchestration.update_asynchronous_task_details(*async_update_list, f'Working with playbook... "')

#Create playbook attribute array template
playbook_attributes_array = dict()

if 'playbook_list' in context:
    for details in context['playbook_list']:
        playbook_attributes_array.update(details['playbook'])

#Iterate each playbook file. Extract attributes (e.g. md5 sum, filename, etc..) and create microservice
if object_ids_array:
    for object_id in object_ids_array:
        #Read object params by playbook - TODO
        playbook_array = list()
        object_id = object_ids_array[0] # This code is NOT support multi playbooks handling.
        response = order.command_objects_instances_by_id(microservice_name, object_id)
        if 'wo_status' in response:
            if response['wo_status'] == 'FAIL':
                ret = MSA_API.process_content(constants.FAILED, 'Failed to playbook object instances where object_id = "' + object_id + '".', context, True)
                print(ret)
    
        Orchestration.update_asynchronous_task_details(*async_update_list, f"Working with playbook... "+object_details['object_id']+"... Extract attributes... ")
        
        if 'Retrieve_playbook_files_list' in response:
            object_details = response.get('Retrieve_playbook_files_list').get(object_id)
        
            playbook_path = object_details['object_id']
            playbook_md5sum = object_details['md5sum']
    
            if playbook_path in  playbook_attributes_array:
                hashed_key = hashlib.md5(playbook_path.encode())
                playbook_attributes_array[hashed_key] = dict(playbook_attributes=list(), microservice_attributes=list())
                playbook_attributes_array[hashed_key]['playbook_attributes']['path'] = playbook_path
                playbook_attributes_array[hashed_key]['playbook_attributes']['md5sum'] = playbook_md5sum

                #Create microservice name
                playbook_basename = os.path.basename(playbook_path)
                playbook_filename = os.path.splitext(playbook_basename)[0]
                playbook_microservice_name = microservice_name_prefix + ' (based on '+ playbook_filename + ')'
                playbook_attributes_array[hashed_key]['microservice_attributes']['name'] = playbook_microservice_name
                
                #Gather microservice skeleton path and name
                microservice_skeleton_name = os.path.basename(microservice_skeleton)
                microservice_skeleton_path = os.path.dirname(microservice_skeleton)
                
                #Sanitize file name
                playbook_microservice_file_name = playbook_microservice_name
                playbook_microservice_file_name = re.sub(r'/[| @()]/', r'_', playbook_microservice_file_name) + '.xml'
                playbook_attributes_array[hashed_key]['microservice_attributes']['file_name'] = playbook_microservice_file_name
                playbook_attributes_array[hashed_key]['microservice_attributes']['path'] = microservice_dir + playbook_microservice_file_name
                
                attributes_to_create_microservice = dict(playbook=playbook_attributes_array[hashed_key]['playbook_attributes']['path'], microservice_name= playbook_attributes_array[hashed_key]['microservice_attributes']['name'], microservice_skeleton=microservice_skeleton)
                Orchestration.update_asynchronous_task_details(*async_update_list, f"Working with playbook... "+object_details['object_id']+"... Create microsercvice... ")
                
                #Launch Create microservice task to create microservice
                Orchestration.execute_launch_process_instance(service_id, processName, json_encode(attributes_to_create_microservice))
                response = json.loads(Orchestration.content)
                status = response.get('status').get('status')
                if status == constants.ENDED:
                    announce = update_asynchronous_task_details(context, "Working with playbook... "+object_details['object_id']+'... Create microsercvice... DONE')
                else:
                    ret = MSA_API.process_content(constants.FAILED, 'Failed to create microservice.', context, True)
                    print(ret)
  
context['playbook_attributes_array'] = playbook_attributes_array
#Finish task
ret = MSA_API.process_content(constants.ENDED, 'Success. All microservices have been created', context, True)
print(ret)


#