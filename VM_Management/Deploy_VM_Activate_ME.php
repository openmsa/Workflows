<?php

/**
 * This file is necessary to include to use all the in-built libraries of /opt/fmc_repository/Reference/Common
 */
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

/**
 * List all the parameters required by the task
 */
function list_args()
{
  
}
$device_id=$context['device_id'];
$device_id=getIdFromUbiId ($device_id);
$response = _device_mark_as_provisioned($device_id);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}
	
$response = prepare_json_response(ENDED, "MSA Device $device_id marked as provisioned successfully.", $context, true);
echo $response;

?>