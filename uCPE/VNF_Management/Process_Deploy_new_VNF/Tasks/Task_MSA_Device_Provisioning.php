<?php
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args() {
	
}


$PROCESSINSTANCEID = $context['PROCESSINSTANCEID'];
$EXECNUMBER = $context['EXECNUMBER'];
$TASKID = $context['TASKID'];
$process_params = array('PROCESSINSTANCEID' => $PROCESSINSTANCEID,
						'EXECNUMBER' => $EXECNUMBER,
						'TASKID' => $TASKID);

$device_id = substr($context['vnf_device_id'], 3);

$response = _device_do_initial_provisioning_by_id($device_id);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}

logToFile(debug_dump($response ,"***********INITIAL PROV**************\n"));
$response = wait_for_provisioning_completion($device_id, $process_params);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}
$wo_comment = $response['wo_comment'];
$response = prepare_json_response(ENDED, "MSA Device $device_id Provisioned successfully.\n$wo_comment", $context, true);
echo $response;

?>