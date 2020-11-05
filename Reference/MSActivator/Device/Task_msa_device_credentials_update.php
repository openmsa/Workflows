<?php 

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args()
{
}

check_mandatory_param('device_id');
check_mandatory_param('device_login');
check_mandatory_param('device_password');

$device_id=$context['device_id'];
$device_id=getIdFromUbiId ($device_id);
$login = $context['device_login'];
$password = $context['device_password'];

$response = _device_update_credentials($device_id, $login, $password);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}
	
$response = prepare_json_response(ENDED, "Device credentials updated successfully for MSA Device $device_id.", $context, true);
echo $response;

?>