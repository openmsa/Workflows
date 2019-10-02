<?php 

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args()
{
	create_var_def('device_id', 'Device');
	create_var_def('variable.0.name', 'String'); 
	create_var_def('variable.0.value', 'String'); 
}
check_mandatory_param('device_id');
check_mandatory_param('variable');

$device_id = substr($context['device_id'], 3);

foreach ($context['variable'] as $var) {
	logToFile("Add variable ".$var['name']." value ".$var['value']." to ".$context['device_id']);
	$response = _configuration_variable_create($device_id, $var['name'], $var['value']);
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED || $response['wo_newparams'] !== "") {
		$response = json_encode($response);
		echo $response;
	}
}

$response = prepare_json_response(ENDED, "Variables configured on $device_id", $context, true);
echo $response;

?>
