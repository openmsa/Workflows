<?php 

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args()
{
	create_var_def('device_id', 'Device');
	create_var_def('variable_name', 'String'); 
}

check_mandatory_param('device_id');
check_mandatory_param('variable_name');

logToFile("Delete variable ".$context['variable_name']." to ".$context['device_id']);

$device_id=$context['device_id'];
$device_id = preg_replace('/[A-Z]+/', '', $device_id);
$response = _configuration_variable_delete($device_id, $context['variable_name']);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED || $response['wo_newparams'] !== "") {
	$response = json_encode($response);
	echo $response;
	exit;
}

$response = prepare_json_response(ENDED, "Variable ".$context['variable_name']." removed on $device_id", $context, true);
echo $response;

?>