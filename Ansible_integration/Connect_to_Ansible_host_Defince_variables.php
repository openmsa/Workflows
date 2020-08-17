<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';


//Define variables
function list_args()
{
  create_var_def('device_id', 'Device');
  create_var_def('playbook_path', 'String');
  create_var_def('microservice_skeleton', 'String');
  create_var_def('microservice_dir', 'String');
}
check_mandatory_param('device_id');
check_mandatory_param('playbook_path');
check_mandatory_param('microservice_skeleton');
check_mandatory_param('microservice_dir');

//Gather Device ID (numeric) from procvided ID
preg_match("/\S*?(?<device_id>\d+?)$/", $context['device_id'], $matches);
$context['device_id'] = $matches['device_id'];

$announce = update_asynchronous_task_details($context, "Identifying variables... ");

//Define variables what will be written to created microservice file
$context['microservice_variables'] = array(
'var_object_id' => '	<variable displayName="object_id" name="params.object_id" startIncrement="0" type="AutoIncrement" mandatoryArray="false" visible="false" description="" groupSeparator="" groupDisplayName="" displayOrder="0" increment="0" refServiceURI="" keepOnImport="false" editable="false" onlyDetailView="false" localVarNameMatch="" remoteVarNameMatch="" arrayCanAdd="true" arrayCanRemove="true" arrayCanMove="true" arrayCanEdit="true" isMandatory="false" isUserLocked="false" isGrouped="false" isSearchable="false" isUniqueGlobal="false"/>',
'var_playbook_path' => '	<variable displayName="Playbook path" name="params.playbook_path" startIncrement="0" type="String" mandatoryArray="false" visible="true" description="" groupSeparator="" groupDisplayName="" displayOrder="0" increment="0" refServiceURI="" keepOnImport="false" editable="true" onlyDetailView="false" localVarNameMatch="" remoteVarNameMatch="" arrayCanAdd="true" arrayCanRemove="true" arrayCanMove="true" arrayCanEdit="true" default="%s" isMandatory="false" isUserLocked="false" isGrouped="false" isSearchable="false" isUniqueGlobal="false"/>'
);

//Define path to MS to read playbook content. THE MICROSERVICE SHOULD BE ATTACHED TO ANSIBLE ME DEPLOYMENT SETTINGS
$context['read_playbook_file'] = '/opt/fmc_repository/CommandDefinition/OpenMSA/ANSIBLE/Read_playbook_file.xml';

//Define path to MS to import list of playbook files. THE MICROSERVICE SHOULD BE ATTACHED TO ANSIBLE ME DEPLOYMENT SETTINGS
$context['retrieve_playbook_files'] = '/opt/fmc_repository/CommandDefinition/OpenMSA/ANSIBLE/Retrieve_playbook_files_list.xml';

//Name of a microservice to read playbook file content
$context['microservice_name'] = 'Read_playbook_file';
$context['variable_skeleton'] = '    <variable displayName="%s" name="params.%s" startIncrement="0" type="String" mandatoryArray="false" visible="true" description="" groupSeparator="" groupDisplayName="" displayOrder="0" increment="0" refServiceURI="" keepOnImport="false" editable="true" onlyDetailView="false" localVarNameMatch="" remoteVarNameMatch="" arrayCanAdd="true" arrayCanRemove="true" arrayCanMove="true" arrayCanEdit="true" displayNameHeader="" fullDisplayName="" default="%s" isMandatory="false" isUserLocked="false" isGrouped="false" isSearchable="false" isUniqueGlobal="false"/>';

//Process name to create new MS
$context['processName'] = 'Process/_TEST_Ansible_integration/Create_microservice';

$announce = update_asynchronous_task_details($context, "Identifying variables... OK");

//Finish the task
task_success('Success. All variables have been defined');
?>