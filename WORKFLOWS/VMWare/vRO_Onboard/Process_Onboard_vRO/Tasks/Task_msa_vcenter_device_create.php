<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args() {
	create_var_def('vro_ip_address', 'String');
	create_var_def('vro_port', 'Integer');
	create_var_def('vcenter_fqdn', 'String');
	create_var_def('vcenter_username', 'String');
	create_var_def('vcenter_password', 'Password');
}

check_mandatory_param('vro_ip_address');
check_mandatory_param('vro_port');
check_mandatory_param('vcenter_fqdn');
check_mandatory_param('vcenter_username');
check_mandatory_param('vcenter_password');

$customer_id = substr($context['UBIQUBEID'], 4);
$operator_prefix = substr($context['UBIQUBEID'], 0, 3);
$managed_device_name = $context['vcenter_username'];
$manufacturer_id = 24;
$model_id = 17010303;
$login = $managed_device_name;
$password = $context['vcenter_password'];
$password_admin = $password;
$device_ip_address = $context['vcenter_fqdn'];
$device_external_reference = "{$device_ip_address}-{$managed_device_name}";

$response = _device_create($customer_id, $managed_device_name, $manufacturer_id,
							$model_id, $login, $password, $password_admin, $device_ip_address, $device_external_reference);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}
$device_external_reference = $response['wo_newparams']['entity']['externalReference'];
$wo_comment = "vCenter Device External Reference : $device_external_reference";
$device_id = $response['wo_newparams']['entity']['id'];
$wo_comment .= "\nvCenter Device Id : $device_id";

$context['device_external_reference'] = $device_external_reference;
$context['device_id'] = "{$operator_prefix}{$device_id}";

$response = _orchestration_update_service_instance_reference($context['UBIQUBEID'], $context['SERVICEINSTANCEID'], $device_external_reference);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}
$wo_comment .= "\nUpdated Service Reference : $device_external_reference";

$response = prepare_json_response(ENDED, "vCenter Device created successfully.\n{$wo_comment}", $context, true);
echo $response;

?>