<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args() {
  //create_var_def('device_id', 'Device');
  //create_var_def('status in msa', 'String');
}

//$context['operation']='Delete '.$context['vm_name'].' from MSA';

if($context['vm_disk_name']=='') {
	$response = prepare_json_response(ENDED, "No device to delete", $context, true);
	echo $response;
	exit;
}

if($context['status in msa']=='Device Deleted') {

	$response = prepare_json_response(ENDED, "No device to delete", $context, true);
	echo $response;
	exit;
}

$device_id = substr($context['device_id'], 3);
$response = _device_delete($device_id);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response['wo_status'] = WARNING;
	$response = json_encode($response);
	echo $response;
	exit;
}

$context['status in msa']='Device Deleted';	

$response = prepare_json_response(ENDED, "MSA Device $device_id deleted successfully.", $context, true);
echo $response;

?>
