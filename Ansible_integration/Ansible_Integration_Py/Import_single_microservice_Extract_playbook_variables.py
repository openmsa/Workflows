import json
import re
import sys
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk import constants
from msa_sdk.order import Order
from msa_sdk.orchestration import Orchestration
from asyncio.tasks import wait

dev_var = Variables()
context = Variables.task_call(dev_var)

#Define variables
device_id = context['device_id']
playbook = context['playbook']

#Instantiate Order object.
order = Order(device_id)

#Retrieve variables from context and define the new ones
Orchestration = Orchestration(context['UBIQUBEID'])
async_update_list = (context['PROCESSINSTANCEID'],
                     context['TASKID'], context['EXECNUMBER'])

if __name__ == "__main__":

    #Sync out Ansible host to read playbook file content
    timeout = 60
    order.command_synchronize(timeout)

    #Read playbook file content
    microservice_name = 'Read_playbook_file'
    response = order.command_objects_instances(microservice_name)
    object_ids_json = json.dumps(response)
    if 'wo_status' in response:
        if response['wo_status'] == 'FAIL':
            ret = MSA_API.process_content(constants.FAILED, 'Failed to get object instances of the microservice with name "' + microservice_name + '".', context, True)
            print(ret)

    object_ids_array = response
    
    #Read object params by playbook - TODO
    playbook_array = dict()
    object_id = object_ids_array[0] # This code is NOT support multi playbooks handling.
    response = order.command_objects_instances_by_id(microservice_name, object_id)
    playbook_json = json.dumps(response)
    if 'wo_status' in response:
        if response['wo_status'] == 'FAIL':
            ret = MSA_API.process_content(constants.FAILED, 'Failed to playbook object instances where object_id = "' + object_id + '".', context, True)
            print(ret)

    if 'Read_playbook_file' in response:
        read_playbook_file = response.get('Read_playbook_file').get(object_id).get('text')
        playbook_array = read_playbook_file.split('|')

    #vars_array is an array that contains strings with extra-args variables
    vars_array = list()

    '''playbook_variables contains extracted variables like 
    array("var_name1" => array("var_name2")
    '''
    playbook_variables = dict()

    #Just bool flag for parser
    is_section = False

    #Extract lines with extra args
    for line in playbook_array:
        section_end_pattern = ''
        matches = re.findall(section_end_pattern, line)
        if is_section and matches:
            is_section = False

        if is_section:
            vars_array.append(strip(line).copy())

        matches = re.findall(r'vars_prompt', line)
        #Orchestration.update_asynchronous_task_details(*async_update_list, f'Matched: '+json.dumps(matches))
        #wait(5)

        if matches:
            is_section = True
            intention = matches[0]
            section_end_pattern = '^'+intention+'\S' ### WARNING: TODO - To be clearly re-defined.

        matches = re.match(r"\s*?-\s*?hosts:(?P<match>.*)", line)
        if matches:
            context['ansible_hosts'] = matches['match']

        #Extract variables from var lines
        var_name = ''
        for line in vars_array:
            matches = re.findall('- name', line)
            if matches:
                temp_array = line.split(':')
                var_name = strip(temp_array[1])
                playbook_variables[var_name] = dict()
            else:
                temp_array = line.split(':')
                playbook_variables[var_name][strip(temp_array[0])] = strip(strip(temp_array[1]))

    context['playbook_variables'] = playbook_variables
    
    
    #Finish the task
    ret = MSA_API.process_content(constants.ENDED, 'Success. All variables have been defined. '+json.dumps(playbook_variables), context, True)
    print(ret)