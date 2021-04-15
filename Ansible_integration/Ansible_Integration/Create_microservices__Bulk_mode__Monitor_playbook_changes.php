<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Ansible_integration/Ansible_Integration/ansible_integration_library.php';
/*
$delay = 30;
$do_monitor_changes = $context['do_monitor_changes'];
$device_id = $context['device_id'];
$microservice_variables_array = $context['microservice_variables'];
$playbook_files_array = $context['playbook_files_array'];
$microservice_name_prefix = $context['microservice_name_prefix'];
$microservice_skeleton = $context['microservice_skeleton'];
$microservice_file = $context['microservice_file'];
$microservice_name = $context['microservice_name'];
$variable_skeleton = $context['variable_skeleton'];


$test = 1;
if ($do_monitor_changes) {
  while ($test < 5) {
    sleep($delay);
    
  $response = json_decode(synchronize_objects_and_verify_response($device_id), true);
  if ($response['wo_status'] !== ENDED) {
    echo $response;
    exit;
  }
  
  $response = json_decode(import_objects($device_id, array('Retrieve_playbook_files_list')), True);
  $object_ids_array = $response['wo_newparams']['Retrieve_playbook_files_list'];
    
  foreach ($object_ids_array as $object_id => $object_details) {
      if (array_key_exists(md5($object_details['object_id']), $playbook_files_array)) {
          if ($object_details['md5sum'] !== $playbook_files_array[md5($object_details['object_id'])]['md5sum']) {
            $playbook_microservice_file_path = $playbook_files_array[md5($object_details['object_id'])]['microservice_path'];
            unset($playbook_files_array[md5($object_details['object_id'])]);
            $playbook_files_array[md5($object_details['object_id'])] = re_create_microservice($device_id, $playbook_microservice_file_path, $object_details['object_id'], $microservice_variables_array, $variable_skeleton, $microservice_skeleton, $microservice_file);
          }
        } else {
         $playbook_files_array[md5($object_details['object_id'])] = create_microservice($device_id, $playbook_file_path, $microservice_variables_array, $variable_skeleton);
        }
  }
    $test += 1;
  }
}
*/
task_success('Ok. Bye');

?>