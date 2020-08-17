<?php

/**
 * This file is necessary to include to use all the in-built libraries of /opt/fmc_repository/Reference/Common
 */
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

$ms_path = $context['microservice_path'];
$device_id = $context['device_id'];

$response = json_decode(_device_asset_by_id($device_id), True);
$current_deplyment_settings_id = $response['wo_newparams']['configProfileId'];

//Prepare array to update deployment settings profile
$uris_array = array();
$uris_array[] = array("uri" => '/'.$ms_path);

//Update deployment settings profile
$response = json_decode(_profile_configuration_attach_files($current_deplyment_settings_id, $uris_array), true);
if ($response['wo_status'] !== ENDED) {
  echo $response;
  exit;
}

//Clean up $context
$context['variables_line'] = '';
$context['microservice_create_line'] = '';
$context['playbook_variables'] = array();
$context['microservice_name'] = '';

task_success('Success. Deployment settings profile has been updated successfully');

?>