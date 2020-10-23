<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/Common/Library/msa_common.php';

task_success('Task OK');

//Retrive variables from $context and define the new ones
$PROCESSINSTANCEID = $context['PROCESSINSTANCEID'];
$EXECNUMBER = $context['EXECNUMBER'];
$TASKID = $context['TASKID'];
$process_params = array('PROCESSINSTANCEID' => $PROCESSINSTANCEID,
                        'EXECNUMBER' => $EXECNUMBER,
                        'TASKID' => $TASKID);
$ce_device_detils = $context['ce_device_details']
$ce_device_id = $ce_device_detils['ce_device_id'];
$device_external_reference = $ce_device_detils['object_id'];
$device_models = $context['device_models_array'];
$deployment_settings = $ce_device_detils['deployment_settings'];


//Define variables for device adaptor
if ($ce_device_detils['interface'] === 'rest') {
  foreach ($ce_device_detils['local_context_data']['msa_specific']['rest_headers'] as $header => $value) {
    _configuration_variable_create ($ce_device_id, $header, $value, $type ="String", $comment = "");
  }
}

//Make initial provisioning
$response = json_decode(_device_do_initial_provisioning_by_id($ce_device_id), True);
if ($response['wo_status'] !== ENDED) {
  echo $response;
  exit;
}

//Wait when provisioning will be completed
$response = json_decode(wait_for_provisioning_completion($ce_device_id, $process_params), True);
if ($response['wo_status'] !== ENDED) {
  echo $response;
  exit;
}

$response = update_asynchronous_task_details($context, "Activating device... OK");
sleep(3);

$response = update_asynchronous_task_details($context, "Attaching configuration profile... ");

//Attach configuration profile to managed device
$response = json_decode(_profile_attach_to_device_by_reference ($deployment_settings, $device_external_reference), True);
if ($response['wo_status'] !== ENDED) {
  echo $response;
}

$response = update_asynchronous_task_details($context, "Attaching configuration profile... OK");
sleep(3);

//Waiting until the managed device will be finally avaliable
$response = json_decode(wait_for_device_reachability ($ce_device_id, $process_params, $timeout = DEVICE_STATUS_CHANGE_TIMEOUT), True);
if ($response['wo_status'] !== ENDED) {
  echo $response;
  exit;
}

$response = update_asynchronous_task_details($context, "Device syncing... ");

//Sync up the ME MSs
$response = json_decode(synchronize_objects_and_verify_response($ce_device_id), true);
if ($response['wo_status'] !== ENDED) {
  echo $response;
  exit;
}
  
task_success("MSA Device $ce_device_id is provisioned and reachable successfully.");

?>