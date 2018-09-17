<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args()
{
	create_var_def('vm_name', 'String');
	create_var_def('rancher_host_labels', 'String');
}

check_mandatory_param('vm_name');
check_mandatory_param('rancher_host_labels');

# Execute WF via MSA API

foreach ($devices_list['wo_newparams'] as $device) {
	$device_id = $device['id'];

	$response = _device_read_by_id ($device_id);	
	$response = json_decode($response, true);	
	$response_status = $response['wo_status'];
	if ($response_status  == "FAIL") {
		task_exit(FAILED, "Read device is FAILED.");
		exit;
	}
	$device_name = $response['wo_newparams']['name']; 
	if ($device_name === $context['vm_name']) {
		$rancher_host_ip_address = $response['wo_newparams']['managementAddress'];
		break;
	}
}

$ubiqube_id = $context['UBIQUBEID'];
$service_name = "Process/VMWare/vCenter/SSH_login_and_command_execution/SSH_login_and_command_execution";
$process_name = "Process/VMWare/vCenter/SSH_login_and_command_execution/Process_Push_SSH_command";
$cmd = "sudo docker run -e CATTLE_AGENT_IP=" . $rancher_host_ip_address . " -e CATTLE_HOST_LABELS= " . $context['rancher_host_labels'] . " --rm --privileged -v /var/run/docker.sock:/var/run/docker.sock -v /var/lib/rancher:/var/lib/rancher rancher/agent:v1.2.10 http://" . $context['rancher_ip_address'] . ":" . $context['rancher_port'] ."/v1/scripts" . $context['registration_token'];

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

$response = wait_for_process_completion($process_id, $process_params);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}

task_exit(ENDED, "Rancher Host registered successfully.");

?>