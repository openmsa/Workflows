<?php 

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args()
{
}

check_mandatory_param('device_id');
check_mandatory_param('device_ip_address');

$ip_address = $context['device_ip_address'];
$device_id = substr($context['device_id'], 3);
	
$response = _device_update_management_ip_address($device_id, $ip_address);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}
	
$response = prepare_json_response(ENDED, "Management IP $ip_address updated successfully on MSA Device $device_id.", $context, true);
echo $response;

?>