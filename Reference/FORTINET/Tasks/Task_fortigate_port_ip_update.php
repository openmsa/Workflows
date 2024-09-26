<?php 

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args()
{
}

check_mandatory_param('interface');
check_mandatory_param('ip_address');
check_mandatory_param('netmask');

$PROCESSINSTANCEID = $context['PROCESSINSTANCEID'];
$EXECNUMBER = $context['EXECNUMBER'];
$TASKID = $context['TASKID'];
$process_params = array('PROCESSINSTANCEID' => $PROCESSINSTANCEID,
						'EXECNUMBER' => $EXECNUMBER,
						'TASKID' => $TASKID);
	
$operator_prefix = $context['operator_prefix'];
$device_id = substr($context['device_id'], 3);
$ip_address = $context['ip_address'];
$netmask = $context['netmask'];
$interface = $context['interface'];

$command1 = "config system interface";
$command2 = "edit $interface";
$command3 = "set ip $ip_address $netmask";
$command4 = "end";
$configuration = "$command1\n$command2\n$command3\n$command4";
$response = _device_do_push_configuration_by_id($device_id, $configuration);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}
	
$timeout_prompt = $operator_prefix . $device_id . " # ";
if ($interface == 'port1'){
  //for port1, we lost the connection when we change the IP, we get 'timeout, buffer received'
  $timeout_ignone_messasges = array("timeout, buffer received", "timeout, $timeout_prompt not found", "timeout,  #  not found");
}else{
  $timeout_ignone_messasges = array("timeout, $timeout_prompt not found", "timeout,  #  not found");
}
$response = wait_for_pushconfig_completion($device_id, $process_params, $timeout_ignone_messasges);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}
$pushconfig_status_message = $response['wo_comment'];

$response = prepare_json_response(ENDED, "IP Address $ip_address-$netmask updated successfully on Interface $interface on the Fortigate Device $device_id.\n$pushconfig_status_message", 
										$context, true);
echo $response;

?>