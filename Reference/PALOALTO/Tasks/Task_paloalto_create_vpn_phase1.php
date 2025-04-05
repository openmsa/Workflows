<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/PALOALTO/Library/paloalto_generic_common.php';

function list_args() {
	create_var_def('device_id', 'Device');
	create_var_def('vpn_phase1_name', 'String');
	create_var_def('lifetime', 'String');
	create_var_def('encryption.0.member', 'String');
	create_var_def('hash.0.member', 'String');
	create_var_def('dhgroup.0.member', 'String');
}

check_mandatory_param('device_id');
check_mandatory_param('vpn_phase1_name');
check_mandatory_param('lifetime');
check_mandatory_param('encryption');
check_mandatory_param('hash');
check_mandatory_param('dhgroup');

$device_id = substr($context['device_id'], 3);
$vpn_phase1_name = $context['vpn_phase1_name'];
$lifetime = $context['lifetime'];
$encryption = $context['encryption'];
$hash = $context['hash'];
$dhgroup = $context['dhgroup'];

$response = _paloalto_generic_vpn_phase1($device_id, CMD_CREATE, $vpn_phase1_name, $lifetime,
											$encryption, $hash, $dhgroup);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}
	
$response = prepare_json_response(ENDED, "VPN Phase-1 $vpn_phase1_name created successfully on the PA Device $device_id", $context, true);
echo $response;

?>
