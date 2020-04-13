<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args() {
	create_var_def('device_id', 'Device');
}

check_mandatory_param('device_id');

$PROCESSINSTANCEID = $context['PROCESSINSTANCEID'];
$EXECNUMBER = $context['EXECNUMBER'];
$TASKID = $context['TASKID'];
$process_params = array('PROCESSINSTANCEID' => $PROCESSINSTANCEID,
						'EXECNUMBER' => $EXECNUMBER,
						'TASKID' => $TASKID);
$device_id=$context['device_id'];
$device_id=getIdFromUbiId ($device_id);

$server_interface_details = $context['server_interface_details'];
$onm_ip = $server_interface_details[0]['ip_address'];
$priv_ip= $server_interface_details[1]['ip_address'];
$ext_ip=$server_interface_details[2]['ip_address'];
$password = $context['password'];

//Provide configuration variables
_configuration_variable_create ($device_id, 'ADMIN_PASSWD', $password, $type ="String", $comment = "");
_configuration_variable_create ($device_id, 'EXT_DEMO_IP', $ext_ip, $type ="String", $comment = "");
_configuration_variable_create ($device_id, 'EXT_DEMO_MASK', '255.255.255.0', $type ="String", $comment = "");
_configuration_variable_create ($device_id, 'ONM_DEMO_IP', $onm_ip, $type ="String", $comment = "");
_configuration_variable_create ($device_id, 'ONM_DEMO_MASK', '255.255.255.0', $type ="String", $comment = "");
_configuration_variable_create ($device_id, 'PRIV_DEMO_IP', $priv_ip, $type ="String", $comment = "");
_configuration_variable_create ($device_id, 'PRIV_DEMO_MASK', '255.255.255.0', $type ="String", $comment = "");


$response = _device_do_initial_provisioning_by_id($device_id);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}
	
$response = wait_for_provisioning_completion($device_id, $process_params);
$response = json_decode($response, true);
/*if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}*/
$wo_comment = $response['wo_comment'];
$response = prepare_json_response(ENDED, "MSA Device $device_id Provisioned successfully.\n$wo_comment", $context, true);
echo $response;

?>