<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/OPENSTACK/Library/OBMF/openstack_common_obmf.php';

function list_args()
{
	create_var_def('openstack_device_id', 'Device');
}

check_mandatory_param('openstack_device_id');
$PROCESSINSTANCEID = $context['PROCESSINSTANCEID'];
$EXECNUMBER = $context['EXECNUMBER'];
$TASKID = $context['TASKID'];
$process_params = array('PROCESSINSTANCEID' => $PROCESSINSTANCEID,
						'EXECNUMBER' => $EXECNUMBER,
						'TASKID' => $TASKID);

$openstack_device_id = $context['openstack_device_id'];
$openstack_device_id = getIdFromUbiId ($openstack_device_id);
$server_interface_details = $context['server_interface_details'];
$external_network_port_id = $server_interface_details[1]['port_id'];
$private_network_port_id = $server_interface_details[2]['port_id'];
	
$response = _neutron_disable_port_security($openstack_device_id, $external_network_port_id);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}
$response = _neutron_disable_port_security($openstack_device_id, $private_network_port_id);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}
	
$message="Port Security disabled successfully on Traffic Interfaces.";
update_asynchronous_task_details($process_params, $message);
$response = prepare_json_response(ENDED, "Port Security disabled successfully on Traffic Interfaces.", $context, true);
echo $response;

?>