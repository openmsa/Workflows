<?php 

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args()
{
	create_var_def('uris.0.uri', 'String');
}

check_mandatory_param('device_id');
check_mandatory_param('uris');

$device_id=$context['device_id'];
$device_id = preg_replace('/[A-Z]+/', '', $device_id);
$uris = $context['uris'];
$uris_array = array();
$index = 0;
foreach ($uris as $uri) {
	$uris_array[$index++] = $uri;
}
$response = _device_configuration_detach_files_from_device($device_id, $uris_array);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED || $response['wo_newparams'] !== "") {
	$response = json_encode($response);
	echo $response;
	exit;
}

$response = prepare_json_response(ENDED, "Files Detached successfully from the Device : $device_id", $context, true);
echo $response;

?>