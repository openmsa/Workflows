<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/PALOALTO/Library/paloalto_generic_common.php';

function list_args() {
	create_var_def('device_id', 'Device');
	create_var_def('auth_code', 'String');
}

check_mandatory_param('device_id');
check_mandatory_param('auth_code');

$device_id = substr($context['device_id'], 3);
$auth_code = $context['auth_code'];
$response = _paloalto_generic_license($device_id, CMD_CREATE, $auth_code);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}

// Sleep for 2 seconds to ensure the device Reboot initiated before checking auto-com job status in next task
sleep(2);

$response = prepare_json_response(ENDED, "Auto-Licensing with auth-code $auth_code completed successfully on the PA Device $device_id", $context, true);
echo $response;

?>
