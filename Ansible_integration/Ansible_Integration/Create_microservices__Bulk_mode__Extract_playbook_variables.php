<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Ansible_integration/Ansible_Integration/ansible_integration_library.php';

//Define variables
function list_args()
{
  create_var_def('microservice_name_prefix', 'String');
  create_var_def('microservice_skeleton', 'String');
  create_var_def('do_monitor_changes', 'Boolean');
}

check_mandatory_param('microservice_name_prefix');
check_mandatory_param('microservice_skeleton');
check_mandatory_param('do_monitor_changes');


$microservice_file = $context['microservice_file'];
$microservice_name = $context['microservice_name'];
$variable_skeleton = $context['variable_skeleton'];
$device_id = $context['device_id'];

$response = json_decode(synchronize_objects_and_verify_response($device_id), true);
if ($response['wo_status'] !== ENDED) {
  echo $response;
  exit;
}

$response = json_decode(import_objects($device_id, array('Retrieve_playbook_files_list')), True);
$object_ids_array = $response['wo_newparams']['Retrieve_playbook_files_list'];


$playbook_files_array = array();
foreach ($object_ids_array as $object_id => $object_details) {
  $playbook_file_path = $object_details['object_id'];
  $playbook_files_array[md5($playbook_file_path)] = playbook_attributes($object_details);
  $result = modify_microservice_to_read_playbook($playbook_file_path, $microservice_file);
  
  //Sync out Ansible host to read playbook file list
  $response = json_decode(synchronize_objects_and_verify_response($device_id), true);
  if ($response['wo_status'] !== ENDED) {
    echo $response;
    exit;
  }
  $playbook_files_array[md5($playbook_file_path)]['variables'] = extract_variables ($device_id, $microservice_name);
}

$context['playbook_files_array'] = $playbook_files_array;

//Finish task
task_success('Success. All playbook files were parsed and variables have been extracted');
?>