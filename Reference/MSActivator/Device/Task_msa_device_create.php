<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args() {
	create_var_def('customer_id', 'Integer');
	create_var_def('managed_device_name', 'String');
	create_var_def('device_external_reference', 'String');
	create_var_def('manufacturer_id', 'Integer');
	create_var_def('model_id', 'Integer');
	create_var_def('device_ip_address', 'IpAddress');
	create_var_def('login', 'String');
	create_var_def('password', 'Password');
	create_var_def('password_admin', 'Password');
}

check_mandatory_param('customer_id');
check_mandatory_param('managed_device_name');
check_mandatory_param('manufacturer_id');
check_mandatory_param('model_id');
check_mandatory_param('login');
check_mandatory_param('password');

// MSA device creation parameters
$customer_id = $context['customer_id'];
$managed_device_name = $context['managed_device_name'];
$manufacturer_id = $context['manufacturer_id'];
$model_id = $context['model_id'];
$login = $context['login'];
$password = $context['password'];
$password_admin = $context['password_admin'];
$device_ip_address = $context['device_ip_address'];
$device_external_reference = "";
if (array_key_exists('device_external_reference', $context)) {
	$device_external_reference = $context['device_external_reference'];
}

$response = _device_create($customer_id, $managed_device_name, $manufacturer_id,
							$model_id, $login, $password, $password_admin, $device_ip_address, $device_external_reference);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}
$device_id = $response['wo_newparams']['entity']['externalReference'];
$wo_comment = "Device External Reference : $device_id";
logToFile($wo_comment);
	
$context['device_id'] = $device_id;
$response = prepare_json_response(ENDED, "MSA Device created successfully.\n$wo_comment", $context, true);
echo $response;

?>
