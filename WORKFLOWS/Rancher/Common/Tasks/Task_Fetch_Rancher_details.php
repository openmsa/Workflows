<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args()
{
	create_var_def('rancher_reference', 'String');
}

check_mandatory_param('rancher_reference');

$rancher_reference = $context['rancher_reference'];

$response = _orchestration_read_service_instance_by_reference($context['UBIQUBEID'], $rancher_reference);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}
$service_id = $response['wo_newparams']['id'];

$response = _orchestration_get_service_variable_by_service_id_variable_name($service_id, "rancher_ip_address");
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}
$context['rancher_ip_address'] = $response['wo_newparams']['rancher_ip_address'];

$response = _orchestration_get_service_variable_by_service_id_variable_name($service_id, "rancher_port");
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}
$context['rancher_port'] = $response['wo_newparams']['rancher_port'];

$response = _orchestration_get_service_variable_by_service_id_variable_name($service_id, "rancher_username");
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}
$context['rancher_username'] = $response['wo_newparams']['rancher_username'];

$response = _orchestration_get_service_variable_by_service_id_variable_name($service_id, "rancher_password");
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}
$context['rancher_password'] = $response['wo_newparams']['rancher_password'];

$response = _orchestration_get_service_variable_by_service_id_variable_name($service_id, "rancher_project_id");
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}
$context['rancher_project_id'] = $response['wo_newparams']['rancher_project_id'];

$response = prepare_json_response(ENDED, "Rancher detailed fetched successfully.", $context, true);
echo $response;

?>