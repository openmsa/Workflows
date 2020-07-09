<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/Common/Library/msa_common.php';


//Retrive variables from $context and define the new ones
$PROCESSINSTANCEID = $context['PROCESSINSTANCEID'];
$EXECNUMBER = $context['EXECNUMBER'];
$TASKID = $context['TASKID'];
$process_params = array('PROCESSINSTANCEID' => $PROCESSINSTANCEID,
                        'EXECNUMBER' => $EXECNUMBER,
                        'TASKID' => $TASKID);
$server_vendor = $context['server_vendor'];
$profile_name = $context['profile_name'] = strtolower('redfish_'.$server_vendor.'_profile');
$device_id = $context['device_id'];
$device_external_reference = $context['device_external_reference'];

//Define variables for device adaptor
_configuration_variable_create ($device_id, 'AUTH_HEADER', 'X-Auth-Token', $type ="String", $comment = "");
_configuration_variable_create ($device_id, 'AUTH_MODE', 'token', $type ="String", $comment = "");
_configuration_variable_create ($device_id, 'HTTP_HEADER', 'Content-Type: application/json', $type ="String", $comment = "");
_configuration_variable_create ($device_id, 'SIGNIN_REQ_PATH', '/redfish/v1/SessionService/Sessions/', $type ="String", $comment = "");
_configuration_variable_create ($device_id, 'TOKEN_XPATH', '//root/sessionToken', $type ="String", $comment = "");

//Additional variables what are used as shortcuts in microservices
_configuration_variable_create ($device_id, '_SYSTEM', "/redfish/v1/Systems", $type ="String", $comment = "");


//Make initial provisioning
$response = json_decode(_device_do_initial_provisioning_by_id($device_id), True);
if ($response['wo_status'] !== ENDED) {
  $response = json_encode($response);
  echo $response;
  exit;
}

//Wait when provisioning will be completed
$response = json_decode(wait_for_provisioning_completion($device_id, $process_params), True);
if ($response['wo_status'] !== ENDED) {
  $response = json_encode($response);
  echo $response;
  exit;
}

//Attach configuration profile to managed device
$response = json_decode(_profile_attach_to_device_by_reference ($profile_name, $device_external_reference), True);
if ($response['wo_status'] !== ENDED) {
  $response = json_encode($response);
  echo $response;
}


//Update managed entity config 
$response = json_decode(_device_do_update_config ($device_id), True);
  if ($response['wo_status'] !== ENDED) {
    $response = json_encode($response);
    echo $response;
}

//Mark managed entity as provisioned
$response = json_decode(_device_mark_as_provisioned($device_id), True);
if ($response['wo_status'] !== ENDED) {
  $response = json_encode($response);
  echo $response;
  exit;
}

//Waiting until the managed device will be finally avaliable
$response = json_decode(wait_for_device_reachability ($device_id, $process_params, $timeout = DEVICE_STATUS_CHANGE_TIMEOUT), True);
if ($response['wo_status'] !== ENDED) {
  $response = json_encode($response);
  echo $response;
  exit;
}
  
task_success("MSA Device $device_id is provisioned and reachable successfully.");

?>