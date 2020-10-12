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

if (!isset($context['server_device'])) {
	$server_vendor = $context['server_vendor'];
	$profile_name = $context['profile_name'] = strtolower('redfish_'.$server_vendor.'_profile');
	$device_id = $context['device_id'];
	$device_external_reference = $context['device_external_reference'];
	
	$response = update_asynchronous_task_details($context, "Attaching configuration profile... ");
	
	//Attach configuration profile to managed device
	$response = json_decode(_profile_attach_to_device_by_reference ($profile_name, $device_external_reference), True);
	if ($response['wo_status'] !== ENDED) {
	  echo $response;
	}

	$response = update_asynchronous_task_details($context, "Attaching configuration profile... OK");
	sleep(3);
	
	$response = update_asynchronous_task_details($context, "Activating device... ");
	
	//Make initial provisioning
	$response = json_decode(_device_do_initial_provisioning_by_id($device_id), True);
	if ($response['wo_status'] !== ENDED) {
	  echo $response;
	  exit;
	}
	
	//Wait when provisioning will be completed
	$response = json_decode(wait_for_provisioning_completion($device_id, $process_params), True);
	if ($response['wo_status'] !== ENDED) {
	  echo json_encode($response);
	  exit;
	}
	
	$response = update_asynchronous_task_details($context, "Activating device... OK");
	sleep(3);
	
	//Waiting until the managed device will be finally avaliable
	$response = json_decode(wait_for_device_reachability ($device_id, $process_params, $timeout = DEVICE_STATUS_CHANGE_TIMEOUT), True);
	if ($response['wo_status'] !== ENDED) {
	  echo $response;
	  exit;
	}
	
	sleep (30);
	
	$response = update_asynchronous_task_details($context, "Device syncing... ");
	
	//Sync up the ME MSs
	$response = json_decode(synchronize_objects_and_verify_response($device_id), true);
	if ($response['wo_status'] !== ENDED) {
	  echo $response;
	  exit;
	}
	
	//Sync up the referenced MSs
	$response = json_decode(synchronize_objects_and_verify_response($device_id), true);
	if ($response['wo_status'] !== ENDED) {
	  echo $response;
	  exit;
	}
	
	$response = update_asynchronous_task_details($context, "Device syncing... OK");
	sleep(3);
	  
	task_success("MSA Device $device_id is provisioned and reachable successfully.");
} else {
  task_success("Device is already provisioned successfully.");
}
	
?>