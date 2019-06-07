<?php 

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args()
{
}

$PROCESSINSTANCEID = $context['PROCESSINSTANCEID'];
$EXECNUMBER = $context['EXECNUMBER'];
$TASKID = $context['TASKID'];
$process_params = array('PROCESSINSTANCEID' => $PROCESSINSTANCEID,
						'EXECNUMBER' => $EXECNUMBER,
						'TASKID' => $TASKID);
	
if (isset($context['NetworkInterfaces'])) {
$device_id = substr($context['device_id'], 3);
$netInterfaceCount =  count($context['NetworkInterfaces']);

// Generate configuration depending the count of interfaces
for ($i = 0; $i < $netInterfaceCount; $i++) 
{
	// TODO - set this variable as the workflow variable to get flexibility.
	$startPortIndex = 2;
	$portNumber = (int)$startPortIndex + $i;
	$interface = "port" . $portNumber;

	$command1 = "config system interface";
	$command2 = "edit " . $interface;
	$command3 = "set mode dhcp";
	$command4 = "end";
	$command5 = "next";
	
	$commands = "$command1\n$command2\n$command3\n$command4";
	
	if ($i == 0 )
	{
		$configuration = $commands;
	} else {
		//$configuration .= "\n$command5\n$commands";
		$configuration .= "\n$commands";
	}
}

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
	$response = json_encode($response);
	echo $response;
	exit;
}
$pushconfig_status_message = $response['wo_comment'];

$response = prepare_json_response(ENDED, "DHCP config is updated successfully on Interface $interface on the Fortigate Device $device_id.\n$pushconfig_status_message", $context, true);
echo $response;
} else {
$response = prepare_json_response(ENDED, "No interface found for this VNF", $context, true);
echo $response;
}

?>