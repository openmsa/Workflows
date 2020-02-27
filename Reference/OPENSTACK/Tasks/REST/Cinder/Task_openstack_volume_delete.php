<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/OPENSTACK/Library/REST/openstack_common_rest.php';

function list_args()
{
	create_var_def('volume_id', 'String');
}

check_mandatory_param('volume_id');

$PROCESSINSTANCEID = $context['PROCESSINSTANCEID'];
$EXECNUMBER = $context['EXECNUMBER'];
$TASKID = $context['TASKID'];
$process_params = array('PROCESSINSTANCEID' => $PROCESSINSTANCEID,
						'EXECNUMBER' => $EXECNUMBER,
						'TASKID' => $TASKID);

$volume_id = $context['volume_id'];
$token_id = $context['token_id'];
$endpoints = $context['endpoints'];
$cinder_endpoint = $endpoints[CINDERV1]['endpoints'][0][ADMIN_URL];
	
$response = object_delete("volume", $token_id, "{$cinder_endpoint}/volumes/{$volume_id}");
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}
	
$response = wait_for_volume_status($cinder_endpoint, $token_id, $volume_id, CMD_DELETE, $process_params);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}

$response = prepare_json_response(ENDED, "Openstack Volume $volume_id Deleted successfully.", $context, true);
echo $response;
        
?>