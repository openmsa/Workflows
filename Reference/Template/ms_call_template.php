<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args()
{
  create_var_def('device_id', 'Device');
  VAR_DEFINITIONS
}

check_mandatory_param('device_id');

$device_id = $context['device_id'];
$device_id = getIdFromUbiId ($device_id);

OBJECT_PARAMETERS

$response = execute_command_and_verify_response($device_id, "CMD_NAME", $object_parameters, "CMD_NAME MICROSERVICENAME");
  $response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = prepare_json_response($response['wo_status'], $response['wo_comment'], $context, true);
	echo $response;
	exit;
}

$response = prepare_json_response(ENDED, "order command execute successfull", $response['wo_newparams'], true);
echo $response;
?>
