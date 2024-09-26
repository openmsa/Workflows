<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/PALOALTO/Library/paloalto_generic_common.php';

function list_args() {
	create_var_def('device_id', 'Device');
	create_var_def('ip_netmask_name', 'String');
	create_var_def('address', 'IpAddress');
	create_var_def('masklen', 'Integer');
}

check_mandatory_param('device_id');
check_mandatory_param('ip_netmask_name');
check_mandatory_param('address');
check_mandatory_param('masklen');

$device_id = substr($context['device_id'], 3);
$ip_netmask_name = $context['ip_netmask_name'];
$address = $context['address'];
$masklen = $context['masklen'];

$response = _paloalto_generic_address_ip_netmask($device_id, CMD_CREATE, $ip_netmask_name, $address, $masklen);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}
	
$response = prepare_json_response(ENDED, "Address IP Netmask $ip_netmask_name created successfully on the PA Device $device_id", $context, true);
echo $response;

?>
