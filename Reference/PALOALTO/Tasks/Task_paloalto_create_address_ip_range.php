<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/PALOALTO/Library/paloalto_generic_common.php';

function list_args() {
	create_var_def('device_id', 'Device');
	create_var_def('ip_range_name', 'String');
	create_var_def('start_address', 'IpAddress');
	create_var_def('end_address', 'IpAddress');
}

check_mandatory_param('device_id');
check_mandatory_param('ip_range_name');
check_mandatory_param('start_address');
check_mandatory_param('end_address');

$device_id = substr($context['device_id'], 3);
$ip_range_name = $context['ip_range_name'];
$start_address = $context['start_address'];
$end_address = $context['end_address'];

$response = _paloalto_generic_address_ip_range($device_id, CMD_CREATE, $ip_range_name, $start_address, $end_address);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}
	
$response = prepare_json_response(ENDED, "Address IP Range $ip_range_name created successfully on the PA Device $device_id", $context, true);
echo $response;

?>
