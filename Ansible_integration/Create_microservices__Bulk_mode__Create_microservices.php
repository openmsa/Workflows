<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

//Define variables
function list_args()
{
  create_var_def('microservice_name_prefix', 'String');
  create_var_def('do_monitor_changes', 'Boolean');
  create_var_def('monitoring_delay', 'String');
}

check_mandatory_param('microservice_name_prefix');
check_mandatory_param('do_monitor_changes');
check_mandatory_param('monitoring_delay');

$microservice_name_prefix = $context['microservice_name_prefix'];
$microservice_file = $context['read_playbook_file'];
$microservice_name = $context['microservice_name'];
$variable_skeleton = $context['variable_skeleton'];
$microservice_skeleton = $context['microservice_skeleton'];
$microservice_dir = $context['microservice_dir'];
$device_id = $context['device_id'];
$processName = $context['processName'];
$service_id = $context['service_id'];
$ubiqube_id = $context['UBIQUBEID'];

//Syncing MS of Ansible host
$announce = update_asynchronous_task_details($context, "Syncing Ansible host... ");
$response = json_decode(synchronize_objects_and_verify_response($device_id), true);
if ($response['wo_status'] !== ENDED) {
  echo $response;
  exit;
}

$response = json_decode(import_objects($device_id, array('Retrieve_playbook_files_list')), True);
$object_ids_array = $response['wo_newparams']['Retrieve_playbook_files_list'];
$announce = update_asynchronous_task_details($context, "Syncing Ansible host... OK");

$announce = update_asynchronous_task_details($context, "Working with playbook... ");
$playbook_attributes_array = array();

//Iterate each playbook file. Extract attributes (e.g. md5 sum, filename, etc..) and create microservice
foreach ($object_ids_array as $object_id => $object_details) {
  $announce = update_asynchronous_task_details($context, "Working with playbook... ".$object_details['object_id'].'... Extract attributes... ');
  $playbook_attributes_array[md5($object_details['object_id'])] = array('playbook_attributes' => array(),
                                                                        'microservice_attributes' => array()
                                                                        );
  $playbook_attributes_array[md5($object_details['object_id'])]['playbook_attributes']['path'] = $object_details['object_id'];
  $playbook_attributes_array[md5($object_details['object_id'])]['playbook_attributes']['md5sum'] = $object_details['md5sum'];


  //Create microservice name
  $result = preg_match('|^(\S+?)([^/]+?\.yml)|', $object_details['object_id'], $matches);
  $playbook_microservice_name = $microservice_name_prefix.' (based on '.str_replace('.yml', '', $matches[2]).')';
  $playbook_attributes_array[md5($object_details['object_id'])]['microservice_attributes']['name'] = $playbook_microservice_name;

  //Gather microservice skeleton path and name
  $result = preg_match('|^(\S+?)([^/]+?\.xml)|', $microservice_skeleton, $matches);
  $microservice_skeleton_path = $matches[1];
  $microservice_skeleton_name = $matches[2];
  
  //Sanitize file name
  $playbook_microservice_file_name = $playbook_microservice_name;
  $playbook_microservice_file_name = preg_replace('/[| @()]/', '_', $playbook_microservice_file_name).'.xml';
  $playbook_attributes_array[md5($object_details['object_id'])]['microservice_attributes']['file_name'] = $playbook_microservice_file_name;
  $playbook_attributes_array[md5($object_details['object_id'])]['microservice_attributes']['path'] = $microservice_dir.$playbook_microservice_file_name;

  $attributes_to_create_microservice = array('playbook'                => $playbook_attributes_array[md5($object_details['object_id'])]['playbook_attributes']['path'],
                                             'microservice_name'       => $playbook_attributes_array[md5($object_details['object_id'])]['microservice_attributes']['name'],
                                              'microservice_skeleton' => $microservice_skeleton
  );
  $announce = update_asynchronous_task_details($context, "Working with playbook... ".$object_details['object_id'].'... Create microsercvice...');
  
  //Launch Create microservice task to create microservice
  $result = _orchestration_launch_process_instance($ubiqube_id, $service_id, $processName, json_encode($attributes_to_create_microservice));
  sleep(15);
  $announce = update_asynchronous_task_details($context, "Working with playbook... ".$object_details['object_id'].'... Create microsercvice... DONE');
}

$context['playbook_attributes_array'] = $playbook_attributes_array;
//Finish task
task_success('Success. All microservices have been created');
?>