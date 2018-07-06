<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args()
{
	create_var_def('vcenter_device_id', 'Device');
}

check_mandatory_param('vcenter_device_id');

$response = _device_read_by_id(substr($context['vcenter_device_id'], 3));
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}
$vcenter_device_external_reference = $response['wo_newparams']['externalReference'];

$response = _orchestration_read_service_instance_by_reference($context['UBIQUBEID'], $vcenter_device_external_reference);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}
$service_id = $response['wo_newparams']['id'];

$response = _orchestration_get_service_variable_by_service_id_variable_name($service_id, "vro_ip_address");
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}
$context['vro_ip_address'] = $response['wo_newparams']['vro_ip_address'];

$response = _orchestration_get_service_variable_by_service_id_variable_name($service_id, "vro_port");
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}
$context['vro_port'] = $response['wo_newparams']['vro_port'];

$response = _orchestration_get_service_variable_by_service_id_variable_name($service_id, "vcenter_fqdn");
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}
$context['vcenter_fqdn'] = $response['wo_newparams']['vcenter_fqdn'];

$response = _orchestration_get_service_variable_by_service_id_variable_name($service_id, "vcenter_username");
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}
$context['vcenter_username'] = $response['wo_newparams']['vcenter_username'];

$response = _orchestration_get_service_variable_by_service_id_variable_name($service_id, "vcenter_password");
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}
$context['vcenter_password'] = $response['wo_newparams']['vcenter_password'];

$wo_comment = "vRO detailed fetched successfully.";
$response = prepare_json_response(ENDED, $wo_comment, $context, true);
echo $response;

?>