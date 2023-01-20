<?php 

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args()
{
	create_var_def('device_id', 'Device');
	create_var_def('ip_address', 'IpAddress');
}

check_mandatory_param('device_id');
check_mandatory_param('ip_address');

$PROCESSINSTANCEID = $context['PROCESSINSTANCEID'];
$EXECNUMBER = $context['EXECNUMBER'];
$TASKID = $context['TASKID'];
$process_params = array('PROCESSINSTANCEID' => $PROCESSINSTANCEID,
						'EXECNUMBER' => $EXECNUMBER,
						'TASKID' => $TASKID);
	
$device_id = substr($context['device_id'], 3);
$ip_address = $context['ip_address'];

$configuration = "execute ping $ip_address";
$response = _device_do_push_configuration_by_id($device_id, $configuration);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}

$response = wait_for_pushconfig_completion($device_id, $process_params);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$context['ping_response'] = "Not Available";
	$context['ping_status'] = "Not Available";
	$response = prepare_json_response(FAILED, $response['wo_comment'] . "\nPING Status : Not Available", $context, true);
	echo $response;
	exit;
}
$pushconfig_status_message = $response['wo_comment'];
$context['ping_response'] = substr($pushconfig_status_message, strpos($pushconfig_status_message, "Push Config Message : ") 
																	+ strlen("Push Config Message : "));

if (strpos($pushconfig_status_message, "100% packet loss") !== false) {
	$pushconfig_status_message .= "PING Status : " . FAILED;
	$context['ping_status'] = FAILED;
}
else {
	$pushconfig_status_message .= "PING Status : " . STATUS_OK;
	$context['ping_status'] = STATUS_OK;
}
$response = prepare_json_response(ENDED, $pushconfig_status_message, $context, true);
echo $response;
?>