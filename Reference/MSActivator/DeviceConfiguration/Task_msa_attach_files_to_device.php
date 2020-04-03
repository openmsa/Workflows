<?php 

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args()
{
	create_var_def('uris.0.uri', 'String'); // Configuration/MSA/...
	create_var_def('position', 'String'); // PRE_CONFIG, POST_CONFIG, AUTO
}

check_mandatory_param('device_id');
check_mandatory_param('uris');
check_mandatory_param('position');

$device_id=$context['device_id'];
$device_id = preg_replace('/[A-Z]+/', '', $device_id);
$uris = $context['uris'];
$uris_array = array();
$index = 0;
foreach ($uris as $uri) {
	$uris_array[$index++] = $uri;
}
$position = $context['position'];
$response = _device_configuration_attach_files_to_device($device_id, $uris_array, $position);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED || $response['wo_newparams'] !== "") {
	$response = json_encode($response);
	echo $response;
	exit;
}

$response = prepare_json_response(ENDED, "Files Attached successfully to the Device : $device_id", $context, true);
echo $response;

?>