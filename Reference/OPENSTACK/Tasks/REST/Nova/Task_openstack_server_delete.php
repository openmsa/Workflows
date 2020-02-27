<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/OPENSTACK/Library/REST/openstack_common_rest.php';

function list_args()
{
	create_var_def('server_id', 'String');
}

check_mandatory_param('server_id');

$PROCESSINSTANCEID = $context['PROCESSINSTANCEID'];
$EXECNUMBER = $context['EXECNUMBER'];
$TASKID = $context['TASKID'];
$process_params = array('PROCESSINSTANCEID' => $PROCESSINSTANCEID,
						'EXECNUMBER' => $EXECNUMBER,
						'TASKID' => $TASKID);

$server_id = $context['server_id'];
$token_id = $context['token_id'];
$endpoints = $context['endpoints'];
$nova_endpoint = $endpoints[NOVA]['endpoints'][0][ADMIN_URL];
	
$response = wait_for_server_status($nova_endpoint, $token_id, $server_id, SHUTOFF, $process_params);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}

$response = _nova_server_delete($nova_endpoint, $token_id, $server_id);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}
	
$response = prepare_json_response(ENDED, "Openstack Server $server_id Deleted successfully.", $context, true);
echo $response;
        
?>