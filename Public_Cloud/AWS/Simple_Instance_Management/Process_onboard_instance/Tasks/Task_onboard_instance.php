<?php

/**
 * This file is necessary to include to use all the in-built libraries of /opt/fmc_repository/Reference/Common
 */
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

/**
 * List all the parameters required by the task
 */
function list_args()
{
  create_var_def('aws_device_id', 'Device');
  create_var_def('instance_id', 'String');
}

check_mandatory_param('aws_device_id');

$PROCESSINSTANCEID = $context['PROCESSINSTANCEID'];
$EXECNUMBER = $context['EXECNUMBER'];
$TASKID = $context['TASKID'];
$process_params = array('PROCESSINSTANCEID' => $PROCESSINSTANCEID,
						'EXECNUMBER' => $EXECNUMBER,
						'TASKID' => $TASKID);
$context['id_for_display'] = $context['SERVICEINSTANCEID']." - ".$context['instance_id'];

$device_id = substr($context['aws_device_id'], 3);

$response = synchronize_objects_and_verify_response($device_id);

$response = _device_read_by_id($device_id);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}
$key = $response['wo_newparams']['login'];
$context["key"] = $key;
$secret = $response['wo_newparams']['password'];
$context["secret"] = $secret;


$response = _device_get_hostname_by_id($device_id);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}

$region = $response['wo_newparams']['hostname'];
$context["region"] = $region;

$instance_id = $context['instance_id'];
task_success("$instance_id onboarded");
?>