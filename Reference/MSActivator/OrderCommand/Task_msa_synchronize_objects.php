<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args()
{
  create_var_def('device_id', 'Device');
}

check_mandatory_param('device_id');

$id = substr($context['device_id'], 3);
$response = synchronize_objects_and_verify_response($id);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}

$response = prepare_json_response(ENDED, "Objects Synchronization successful for the device " . $context['device_id'], $context, true);
echo $response;

?>