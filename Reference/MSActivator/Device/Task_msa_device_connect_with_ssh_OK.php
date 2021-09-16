<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args()
{
}

// Wait the given IP $context['device_ip_address'] response to ssh 

check_mandatory_param('device_ip_address');

$PROCESSINSTANCEID = $context['PROCESSINSTANCEID'];
$EXECNUMBER = $context['EXECNUMBER'];
$TASKID = $context['TASKID'];
$process_params = array('PROCESSINSTANCEID' => $PROCESSINSTANCEID,
						'EXECNUMBER' => $EXECNUMBER,
						'TASKID' => $TASKID);
	
$device_ip_address = $context['device_ip_address'];
$port_no = SSH_DEFAULT_PORT_NO;
$response = wait_for_ssh_status($device_ip_address, $port_no, $process_params);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}

$ssh_status_message = $response['wo_comment'];
	
$response = prepare_json_response(ENDED, "IP Address $device_ip_address is now reachable (SSH) from MSA.\n$ssh_status_message", $context, true);
echo $response;

?>