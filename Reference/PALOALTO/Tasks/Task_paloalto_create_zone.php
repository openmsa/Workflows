<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/PALOALTO/Library/paloalto_generic_common.php';

function list_args() {
	create_var_def('device_id', 'Device');
	create_var_def('zone_name', 'String');
	create_var_def('zone_type', 'String');
	create_var_def('zone_members.0.member', 'String');
}

check_mandatory_param('device_id');
check_mandatory_param('zone_name');
check_mandatory_param('zone_type');
check_mandatory_param('zone_members');

$device_id = substr($context['device_id'], 3);
$zone_name = $context['zone_name'];
$zone_type = $context['zone_type'];
$zone_members = $context['zone_members'];

$response = _paloalto_generic_zone($device_id, CMD_CREATE, $zone_name, $zone_type, $zone_members);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}
	
$response = prepare_json_response(ENDED, "Zone $zone_name created successfully on the PA Device $device_id", $context, true);
echo $response;

?>