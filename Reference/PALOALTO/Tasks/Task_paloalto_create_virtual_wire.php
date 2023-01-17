<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/PALOALTO/Library/paloalto_generic_common.php';

function list_args() {
	create_var_def('device_id', 'Device');
	create_var_def('vwire_name', 'String');
	create_var_def('vwire_interface1', 'String');
	create_var_def('vwire_interface2', 'String');
	create_var_def('vwire_tag_allowed', 'String');
	create_var_def('vwire_multicast_firewalling', 'String');
	create_var_def('vwire_link_state_pass_through', 'String');
}

check_mandatory_param('device_id');
check_mandatory_param('vwire_name');
check_mandatory_param('vwire_interface1');
check_mandatory_param('vwire_interface2');

$device_id = substr($context['device_id'], 3);
$vwire_name = $context['vwire_name'];
$vwire_interface1 = $context['vwire_interface1'];
$vwire_interface2 = $context['vwire_interface2'];
$vwire_tag_allowed = "";
$vwire_multicast_firewalling = "";
$vwire_link_state_pass_through = "";
if (!empty($context['vwire_tag_allowed'])) {
	$vwire_tag_allowed = $context['vwire_tag_allowed'];
}
if (!empty($context['vwire_multicast_firewalling'])) {
	$vwire_multicast_firewalling = $context['vwire_multicast_firewalling'];
}
if (!empty($context['vwire_link_state_pass_through'])) {
	$vwire_link_state_pass_through = $context['vwire_link_state_pass_through'];
}

$response = _paloalto_generic_virtual_wire($device_id, CMD_CREATE, $vwire_name, $vwire_interface1, $vwire_interface2,
							$vwire_tag_allowed, $vwire_multicast_firewalling, $vwire_link_state_pass_through);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}

$response = prepare_json_response(ENDED, "Virtual Wire $vwire_name created successfully on the PA Device $device_id", $context, true);
echo $response;

?>
