<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args() {
	create_var_def('rancher_ip_address', 'String');
	create_var_def('rancher_port', 'Integer');
	create_var_def('rancher_username', 'String');
	create_var_def('rancher_password', 'Password');
	create_var_def('rancher_project_id', 'String');
}

check_mandatory_param('rancher_ip_address');
check_mandatory_param('rancher_port');
check_mandatory_param('rancher_username');
check_mandatory_param('rancher_password');
check_mandatory_param('rancher_project_id');

$response = _orchestration_update_service_instance_reference($context['UBIQUBEID'], $context['SERVICEINSTANCEID'], $context['rancher_ip_address'] . "-" . $context['rancher_project_id']);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}

task_exit(ENDED, "Rancher details entered successfully.");

?>