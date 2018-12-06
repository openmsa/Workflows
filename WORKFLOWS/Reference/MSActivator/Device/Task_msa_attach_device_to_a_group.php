<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args() {
	create_var_def('device_id', 'Device');
	create_var_def('device_group_id', 'Integer');
}

if(empty($context['device_id'])) {
	$response = prepare_json_response(ENDED, "No device", $context, true);
	echo $response;
	exit;
}

$device_id = substr($context['device_id'], 3);
if(empty($context['device_id'])) {
	$response = prepare_json_response(ENDED, "No group specified.", $context, true);
}else{
	shell_exec('/opt/ubi-jentreprise/bin/api/devicegroup/attachDeviceToDeviceGroup.sh '.$device_id.' '.$context['device_group_id'].'');
	$response = prepare_json_response(ENDED, "Device $device_id attached to a specific group .", $context, true);
}

echo $response;

?>
