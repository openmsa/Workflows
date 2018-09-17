<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args()
{
	create_var_def('ipAddress', 'String');
}

check_mandatory_param('ipAddress');

$customer_reference = $context['UBIQUBEID'];
$management_ip = $context['ipAddress'];
$return_message = "IP Duplication is not confirmed: FALSE";
$context['ip_address_exists'] = "false";

// Get Customer list of devices
$devices_list = _lookup_list_devices_by_customer_reference($customer_reference);
$devices_list = json_decode($devices_list , true);

foreach ($devices_list['wo_newparams'] as &$device) {
	$device_id = $device['id'];

	$response = _device_read_by_id ($device_id);
	$response = json_decode($response, true);
	if ($response['wo_status'] === FAILED) {
		task_exit(ENDED, "Read device is FAILED.");
		exit;
	}
	
	$device_mgmt_ip = $response['wo_newparams']['managementAddress'];
	
	if ($management_ip === $device_mgmt_ip) {
		$context['ip_address_exists'] = "true";
		$return_message = "IP Duplication is confirmed: TRUE";
		break;
	}
}

task_exit(ENDED, $return_message . "\n");

?>