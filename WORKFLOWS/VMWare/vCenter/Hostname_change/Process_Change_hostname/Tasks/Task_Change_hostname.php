<?php

/**
 * This file is necessary to include to use all the in-built libraries of /opt/fmc_repository/Reference/Common
 */
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args()
{
	create_var_def('vm_name', 'String');
	create_var_def('newHostname', 'String');
}

check_mandatory_param('vm_name');
check_mandatory_param('newHostname');

# Execute WF via MSA API

$ubiqube_id = $context['UBIQUBEID'];
$service_name = "Process/VMWare/vCenter/SSH_login_and_command_execution/SSH_login_and_command_execution";
$process_name = "Process/VMWare/vCenter/SSH_login_and_command_execution/Process_Push_SSH_command";
$cmd = "hostname " . $context['newHostname'];

$json_body = array("vcenter_device_id" => $context['vcenter_device_id'],"vm_name" => $context['vm_name'],"cmd" => $cmd);
$json_body = json_encode($json_body);

$response = _orchestration_execute_service ($ubiqube_id, $service_name, $process_name, $json_body);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}

$process_id = $response['wo_newparams']['processId']['id'];

$response = wait_for_process_completion($process_id, $context);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}

task_exit(ENDED, "VM hostname changed successfully.");

?>