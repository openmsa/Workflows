<?php

/**
 * This file is necessary to include to use all the in-built libraries of /opt/fmc_repository/Reference/Common
 */
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Ansible_integration/ansible_integration_library.php';

//Import required variables
$playbook_files_array = $context['playbook_files_array'];
$device_id = $context['device_id'];
$microservice_file = $context['microservice_file'];
$microservice_name = $context['microservice_name'];
$variable_skeleton = $context['variable_skeleton'];
$microservice_files_array = array();

//Gather deployment settings ID what attached to Ansible ME
$response = json_decode(_device_asset_by_id($device_id), True);
$deployment_settings_id = $response['wo_newparams']['configProfileId'];

//Create 
foreach ($playbook_files_array as $playbook => $playbook_details) {
  $microservice_files_array[] = $playbook_details['microservice_path'];
}

$result = attach_file_to_deployment_settings($deployment_settings_id, $microservice_files_array);

task_success('Task OK');

?>