<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/OPENSTACK/Library/REST/openstack_common_rest.php';

function list_args()
{
	create_var_def('networks.0.network', 'IpAddress');
	create_var_def('networks.0.port', 'Integer');
	create_var_def('networks.0.fixed_ip', 'IpAddress');
	create_var_def('server_name', 'String');
	create_var_def('availability_zone', 'String');
	create_var_def('flavor', 'String');
	create_var_def('image', 'String');
	create_var_def('security_groups.0.security_group', 'String');
}

check_mandatory_param('flavor');
check_mandatory_param('image');
check_mandatory_param('networks');
#check_mandatory_param('server_name');

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

$token_id = $context['token_id'];
$endpoints = $context['endpoints'];
$nova_endpoint = $endpoints[NOVA]['endpoints'][0][ADMIN_URL];
$neutron_endpoint = $endpoints[NEUTRON]['endpoints'][0][ADMIN_URL];

$response = _nova_server_create($nova_endpoint, $token_id, $server_name, $flavor, $image, $networks,
							$availability_zone, "", $security_groups);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}
$server_id = $response['wo_newparams']['server']['id'];
	
$response = wait_for_server_status($nova_endpoint, $token_id, $server_id, ACTIVE, $process_params);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}
$server_status_comment = $response['wo_comment'];
	
$response = get_server_interface_details($token_id, $nova_endpoint, $neutron_endpoint, $server_id, $networks);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}
	
$wo_comment = "Openstack Server created successfully.\nServer Id : $server_id\n$server_status_comment";
$wo_comment .= $response['wo_comment'];
$context['server_interface_details'] = $response['wo_newparams']['server_interface_details'];
$context['server_id'] = $server_id;

if (array_key_exists('floating_ip_address', $context)) {
	$context['device_ip_address'] = $context['floating_ip_address'];
}
$response = prepare_json_response(ENDED, $wo_comment, $context, true);
echo $response;

?>
