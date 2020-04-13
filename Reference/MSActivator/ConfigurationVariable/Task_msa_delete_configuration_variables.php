<?php 

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args()
{
	create_var_def('device_id', 'Device');
	create_var_def('variable.0.name', 'String'); 
}
check_mandatory_param('device_id');
check_mandatory_param('variable');

$device_id=$context['device_id'];
$device_id=getIdFromUbiId ($device_id);

foreach ($context['variable'] as $var) {
	logToFile("Delete variable ".$var['name']." to ".$context['device_id']);
	$response = _configuration_variable_delete($device_id, $var['name']);
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED || $response['wo_newparams'] !== "") {
		$response = json_encode($response);
		echo $response;
	}
}

$response = prepare_json_response(ENDED, "Variables deleted on $device_id", $context, true);
echo $response;

?>
