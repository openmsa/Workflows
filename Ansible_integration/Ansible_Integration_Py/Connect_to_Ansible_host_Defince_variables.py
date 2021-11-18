from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk import constants
from msa_sdk.orchestration import Orchestration

dev_var = Variables()
dev_var.add('device_id', var_type='Device')
dev_var.add('playbook_path', var_type='String')
dev_var.add('microservice_skeleton', var_type='String')
dev_var.add('microservice_dir', var_type='String')
dev_var.add('do_import_hosts', var_type='Boolean')
context = Variables.task_call(dev_var)


Orchestration = Orchestration(context['UBIQUBEID'])
async_update_list = (context['PROCESSINSTANCEID'],
                     context['TASKID'], context['EXECNUMBER'])

if __name__ == "__main__":
    
    #Gather Device ID (numeric) from procvided ID
    device_id = context['device_id'][3:]
    context['device_id'] = device_id
    context['linux_model_id'] = '14020601'
    context['linux_manufacturer_id'] = '14020601'
    context['linux_profile_name'] = 'bash_profile'
    
    Orchestration.update_asynchronous_task_details(*async_update_list,
                                                   f'dentifying variables... ')

    #Define variables what will be written to created microservice file
    context['microservice_variables'] = dict(
    var_object_id='	<variable displayName="object_id" name="params.object_id" startIncrement="0" type="AutoIncrement" mandatoryArray="false" visible="false" description="" groupSeparator="" groupDisplayName="" displayOrder="0" increment="0" refServiceURI="" keepOnImport="false" editable="false" onlyDetailView="false" localVarNameMatch="" remoteVarNameMatch="" arrayCanAdd="true" arrayCanRemove="true" arrayCanMove="true" arrayCanEdit="true" isMandatory="false" isUserLocked="false" isGrouped="false" isSearchable="false" isUniqueGlobal="false"/>',
    var_playbook_path='	<variable displayName="Playbook path" name="params.playbook_path" startIncrement="0" type="String" mandatoryArray="false" visible="true" description="" groupSeparator="" groupDisplayName="" displayOrder="0" increment="0" refServiceURI="" keepOnImport="false" editable="true" onlyDetailView="true" localVarNameMatch="" remoteVarNameMatch="" arrayCanAdd="true" arrayCanRemove="true" arrayCanMove="true" arrayCanEdit="true" default="%s" isMandatory="false" isUserLocked="true" isGrouped="false" isSearchable="false" isUniqueGlobal="false"/>',
    var_ansible_hosts='	<variable displayName="Ansible hosts to execute" name="params.ansible_hosts" startIncrement="0" type="String" mandatoryArray="false" visible="true" description="" groupSeparator="" groupDisplayName="" displayOrder="0" increment="0" refServiceURI="" keepOnImport="false" editable="true" onlyDetailView="true" localVarNameMatch="" remoteVarNameMatch="" arrayCanAdd="true" arrayCanRemove="true" arrayCanMove="true" arrayCanEdit="true" default="%s" isMandatory="false" isUserLocked="true" isGrouped="false" isSearchable="false" isUniqueGlobal="false"/>'
    )
    
    #Define path to MS to read playbook content. THE MICROSERVICE SHOULD BE ATTACHED TO ANSIBLE ME DEPLOYMENT SETTINGS
    context['read_playbook_file'] = '/opt/fmc_repository/CommandDefinition/ANSIBLE/Read_playbook_file.xml'
    
    #Define path to MS to import list of playbook files. THE MICROSERVICE SHOULD BE ATTACHED TO ANSIBLE ME DEPLOYMENT SETTINGS
    context['retrieve_playbook_files'] = '/opt/fmc_repository/CommandDefinition/ANSIBLE/Retrieve_playbook_files_list.xml'
    
    #Name of a microservice to read playbook file content
    context['microservice_name'] = 'Read_playbook_file'
    context['variable_skeleton'] = '    <variable displayName="%s" name="params.%s" startIncrement="0" type="String" mandatoryArray="false" visible="true" description="" groupSeparator="" groupDisplayName="" displayOrder="0" increment="0" refServiceURI="" keepOnImport="false" editable="true" onlyDetailView="false" localVarNameMatch="" remoteVarNameMatch="" arrayCanAdd="true" arrayCanRemove="true" arrayCanMove="true" arrayCanEdit="true" displayNameHeader="" fullDisplayName="" default="%s" isMandatory="false" isUserLocked="false" isGrouped="false" isSearchable="false" isUniqueGlobal="false"/>'
    
    #Process name to create new MS
    Orchestration.update_asynchronous_task_details(*async_update_list, f'Identifying variables... OK')
    
    #Finish the task
    ret = MSA_API.process_content(constants.ENDED, 'Success. All variables have been defined', context, True)
    print(ret)
