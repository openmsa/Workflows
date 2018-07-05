<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/OPENSTACK/Library/REST/openstack_common_rest.php';

function list_args()
{
	create_var_def('server_id', 'String');
	create_var_def('volume_id', 'String');
	create_var_def('volume_device', 'String');
}

check_mandatory_param('server_id');
check_mandatory_param('volume_id');

$PROCESSINSTANCEID = $context['PROCESSINSTANCEID'];
$EXECNUMBER = $context['EXECNUMBER'];
$TASKID = $context['TASKID'];
$process_params = array('PROCESSINSTANCEID' => $PROCESSINSTANCEID,
						'EXECNUMBER' => $EXECNUMBER,
						'TASKID' => $TASKID);

$server_id = $context['server_id'];
$volume_id = $context['volume_id'];
$device = $context['volume_device'];
$token_id = $context['token_id'];
$endpoints = $context['endpoints'];
$nova_endpoint = $endpoints[NOVA]['endpoints'][0][ADMIN_URL];
$cinder_endpoint = $endpoints[CINDERV1]['endpoints'][0][ADMIN_URL];

$response = _nova_volume_attach($nova_endpoint, $token_id, $server_id, $volume_id, $device);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}

$response = wait_for_volume_status($cinder_endpoint, $token_id, $volume_id, VOLUME_IN_USE, $process_params);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}
$volume_status_comment = $response['wo_comment'];
	
$response = prepare_json_response(ENDED, "Volume $volume_id attached successfully to the server $server_id.\n$volume_status_comment", $context, true);
echo $response;
?>