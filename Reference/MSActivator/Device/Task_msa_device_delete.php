<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args() {
	create_var_def('device_id', 'Device');
}

if(empty($context['device_id'])) {

	$response = prepare_json_response(ENDED, "No device to delete", $context, true);
	echo $response;
	exit;
}

$device_id=$context['device_id'];
$device_id=getIdFromUbiId ($device_id);
$response = _device_delete($device_id);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
  if (isset($response['wo_comment']) && preg_match("/not found in database/i",$response['wo_comment'],$match)){
    //Device not found in the MSA Database
    $response = prepare_json_response(ENDED, "OK, MSA Device $device_id not found in DB", $context, true);
    echo $response;
  }else{
    $response['wo_status'] = WARNING;
    $response = json_encode($response);
    echo $response;
    exit;
  }
}
	
$response = prepare_json_response(ENDED, "MSA Device $device_id deleted successfully.", $context, true);
echo $response;

?>
