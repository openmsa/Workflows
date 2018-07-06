<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/OPENSTACK/Library/OBMF/openstack_common_obmf.php';

function list_args()
{
	create_var_def('openstack_device_id', 'Device');
	create_var_def('networks.0.network', 'OBMFRef');
	create_var_def('networks.0.port', 'OBMFRef');
	create_var_def('networks.0.fixed_ip', 'IpAddress');
	create_var_def('server_name', 'String');
	create_var_def('availability_zone', 'OBMFRef');
	create_var_def('flavor', 'OBMFRef');
	create_var_def('image', 'OBMFRef');
	create_var_def('security_groups.0.security_group', 'OBMFRef');
}

check_mandatory_param('openstack_device_id');
check_mandatory_param('networks');
check_mandatory_param('flavor');
check_mandatory_param('image');
check_mandatory_param('server_name');
#check_mandatory_param('availability_zone');

$PROCESSINSTANCEID = $context['PROCESSINSTANCEID'];
$EXECNUMBER = $context['EXECNUMBER'];
$TASKID = $context['TASKID'];
$process_params = array('PROCESSINSTANCEID' => $PROCESSINSTANCEID,
						'EXECNUMBER' => $EXECNUMBER,
						'TASKID' => $TASKID);
	
// Openstack Server creation parameters
$server_name = $context['server_name'];
$availability_zone = $context['availability_zone'];
$flavor = $context['flavor'];
$image = $context['image'];
$networks = $context['networks'];
$security_groups = array();
if (!empty($context['security_groups'])) {
	$security_groups = $context['security_groups'];
}

$openstack_device_id = substr($context['openstack_device_id'], 3);

$response = _nova_server_create($openstack_device_id, $server_name, $networks,
									$availability_zone, $flavor, $image, $security_groups);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}

$response = get_server_id($openstack_device_id, $server_name);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}
$server_id = $response['wo_newparams']['server_id'];
	
$response = wait_for_server_status($openstack_device_id, $server_id, ACTIVE, $process_params);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}
	
$response = get_server_interface_details($openstack_device_id, $server_id, $networks);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}
	
$wo_comment = "Openstack Server created successfully.\nServer Id : $server_id\nServer Status : " . ACTIVE . "\n";
$wo_comment .= $response['wo_comment'];
$context['server_interface_details'] = $response['wo_newparams']['server_interface_details'];
$context['server_id'] = $server_id;
if (array_key_exists('floating_ip_address', $context)) {
	$context['device_ip_address'] = $context['floating_ip_address'];
}
$response = prepare_json_response(ENDED, $wo_comment, $context, true);
echo $response;

?>