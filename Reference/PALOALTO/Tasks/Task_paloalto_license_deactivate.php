<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/PALOALTO/Library/paloalto_generic_common.php';

function list_args() {
	create_var_def('device_id', 'Device');
}

check_mandatory_param('device_id');

$device_id = substr($context['device_id'], 3);

$response = _paloalto_generic_license($device_id, CMD_DELETE);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}
	
$response = prepare_json_response(ENDED, "License Deactivation completed successfully on the PA Device $device_id", $context, true);
echo $response;

?>
