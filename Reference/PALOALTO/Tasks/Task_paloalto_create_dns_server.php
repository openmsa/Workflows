<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/PALOALTO/Library/paloalto_generic_common.php';

function list_args() {
	create_var_def('device_id', 'Device');
	create_var_def('dns_primary_server', 'String');
	create_var_def('dns_secondary_server', 'String');
}

check_mandatory_param('device_id');
if(empty($context['dns_primary_server']) && empty($context['dns_secondary_server'])) {

	$response = prepare_json_response(FAILED,
                                       "DNS Servers detail is not present.",
                                       $context, true);
	echo $response;
	exit;
}

$device_id = substr($context['device_id'], 3);
$dns_primary_server = "";
$dns_secondary_server = "";
if (array_key_exists('dns_primary_server', $context)) {
	$dns_primary_server = $context['dns_primary_server'];
}
if (array_key_exists('dns_secondary_server', $context)) {
	$dns_secondary_server = $context['dns_secondary_server'];
}
	
$response = _paloalto_generic_dns_servers($device_id, CMD_CREATE, $dns_primary_server, $dns_secondary_server);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}

$response = prepare_json_response(ENDED, "DNS Servers configured successfully on the PA Device $device_id", $context, true);
echo $response;

?>
