<?php 

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args()
{
	create_var_def('device_id', 'Device');
	create_var_def('variable_name', 'String'); 
	create_var_def('variable_value', 'String'); 
}

check_mandatory_param('device_id');
check_mandatory_param('variable_name');
check_mandatory_param('variable_value');

logToFile("Add variable ".$context['variable_name']." value ".$context['variable_value']." to ".$context['device_id']);

$device_id=$context['device_id'];
$device_id=getIdFromUbiId ($device_id);
$response = _configuration_variable_create($device_id, $context['variable_name'], $context['variable_value']);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED || $response['wo_newparams'] !== "") {
	$response = json_encode($response);
	echo $response;
	exit;
}

$response = prepare_json_response(ENDED, "Variable ".$context['variable_name']." configured on $device_id", $context, true);
echo $response;

?>