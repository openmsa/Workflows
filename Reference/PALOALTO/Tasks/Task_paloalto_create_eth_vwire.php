<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/PALOALTO/Library/paloalto_generic_common.php';

function list_args() {
	create_var_def('device_id', 'Device');
	create_var_def('name', 'String');
	create_var_def('subinterfaces.0.subinterface_id', 'String');
	create_var_def('subinterfaces.0.tag', 'String');
}

check_mandatory_param('device_id');
check_mandatory_param('name');
check_mandatory_param('subinterfaces');

$device_id = substr($context['device_id'], 3);
$name = $context['name'];
$subinterfaces = $context['subinterfaces'];
$interface_type = "virtual-wire";
	
$response = _paloalto_generic_ethernet($device_id, CMD_CREATE, $name, $interface_type);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}

$response = _paloalto_generic_eth_tag($device_id, CMD_CREATE, $name, $subinterfaces);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}
	
$response = prepare_json_response(ENDED, "Ethernet V-wire $name created successfully on the PA Device $device_id", $context, true);
echo $response;

?>
