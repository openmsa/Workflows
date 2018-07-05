<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/OPENSTACK/Library/REST/openstack_common_rest.php';

function list_args()
{
	create_var_def('volume_name', 'String');
	create_var_def('volume_size', 'Integer');
	create_var_def('availability_zone', 'String');
	create_var_def('volume_multiattach', 'Boolean');
	create_var_def('volume_bootable', 'Boolean');
	create_var_def('source_volume_id', 'String');
	create_var_def('volume_description', 'String');
	create_var_def('volume_snapshot_id', 'String');
	create_var_def('volume_image_reference', 'String');
	create_var_def('volume_type', 'String');
	create_var_def('volume_source_replica', 'String');
	create_var_def('volume_consistencygroup_id', 'String');
	#create_var_def('volume_metadata', 'String');
	#create_var_def('volume_scheduler_hints', 'String');
}

check_mandatory_param('volume_size');

$PROCESSINSTANCEID = $context['PROCESSINSTANCEID'];
$EXECNUMBER = $context['EXECNUMBER'];
$TASKID = $context['TASKID'];
$process_params = array('PROCESSINSTANCEID' => $PROCESSINSTANCEID,
						'EXECNUMBER' => $EXECNUMBER,
						'TASKID' => $TASKID);
	
// Openstack Volume creation parameters
$volume_name = $context['volume_name'];
$availability_zone = $context['availability_zone'];
$volume_size = intval($context['volume_size']);
$volume_multiattach = $context['volume_multiattach'];
$volume_bootable = $context['volume_bootable'];
$source_volume_id = $context['source_volume_id'];
$volume_description = $context['volume_description'];
$volume_snapshot_id = $context['volume_snapshot_id'];
$volume_image_reference = $context['volume_image_reference'];
$volume_type = $context['volume_type'];
$volume_source_replica = $context['volume_source_replica'];
$volume_consistencygroup_id = $context['volume_consistencygroup_id'];

/*
$volume_metadata = array();
if (!empty($context['volume_metadata'])) {
	$volume_metadata = $context['volume_metadata'];
}
$volume_scheduler_hints = array();
if (!empty($context['volume_scheduler_hints'])) {
	$volume_scheduler_hints = $context['volume_scheduler_hints'];
}
*/

$token_id = $context['token_id'];
$endpoints = $context['endpoints'];
$cinder_endpoint = $endpoints[CINDERV1]['endpoints'][0][ADMIN_URL];

$response = _cinder_volume_create($cinder_endpoint, $token_id, $volume_name, $volume_size,
									$availability_zone, $volume_multiattach, $volume_bootable, 
									$source_volume_id, $volume_description, 
									$volume_snapshot_id, $volume_image_reference,
									$volume_type, $volume_source_replica,
									$volume_consistencygroup_id);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}
$volume_id = $response['wo_newparams']['volume']['id'];

$response = wait_for_volume_status($cinder_endpoint, $token_id, $volume_id, VOLUME_AVAILABLE, $process_params);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}
$volume_status_comment = $response['wo_comment'];
	
$context['volume_id'] = $volume_id;
$wo_comment = "Openstack Volume created successfully.\nVolume Id : $volume_id \n$volume_status_comment";
$response = prepare_json_response(ENDED, $wo_comment, $context, true);
echo $response;

?>