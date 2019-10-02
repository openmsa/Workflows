<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args()
{
	create_var_def('device_ip_address', 'IpAddress');
	create_var_def('ssh_port_no', 'Integer');
}

check_mandatory_param('device_ip_address');

$PROCESSINSTANCEID = $context['PROCESSINSTANCEID'];
$EXECNUMBER = $context['EXECNUMBER'];
$TASKID = $context['TASKID'];
$process_params = array('PROCESSINSTANCEID' => $PROCESSINSTANCEID,
						'EXECNUMBER' => $EXECNUMBER,
						'TASKID' => $TASKID);

$device_ip_address = $context['device_ip_address'];
$port_no = SSH_DEFAULT_PORT_NO;
if (!empty($context['ssh_port_no'])) {
	$port_no = $context['ssh_port_no'];
}
$response = wait_for_ssh_status($device_ip_address, $port_no, $process_params);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}
$ssh_status_message = $response['wo_comment'];
	
$response = prepare_json_response(ENDED, "IP Address $device_ip_address is now reachable from MSA.\n$ssh_status_message", $context, true);
echo $response;

?>