<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/PALOALTO/Library/paloalto_generic_common.php';

function list_args() {
	create_var_def('device_id', 'Device');
	create_var_def('send_hostname', 'String');
	create_var_def('send_client_id', 'String');
	create_var_def('accept_dhcp_hostname', 'String');
	create_var_def('accept_dhcp_domain', 'String');
}

check_mandatory_param('device_id');
check_mandatory_param('send_hostname');
check_mandatory_param('send_client_id');
check_mandatory_param('accept_dhcp_hostname');
check_mandatory_param('accept_dhcp_domain');

$device_id = substr($context['device_id'], 3);
$send_hostname = $context['send_hostname'];
$send_client_id = $context['send_client_id'];
$accept_dhcp_hostname = $context['accept_dhcp_hostname'];
$accept_dhcp_domain = $context['accept_dhcp_domain'];
	
$response = _paloalto_generic_dhcp_client($device_id, CMD_CREATE, $send_hostname, $send_client_id, $accept_dhcp_hostname, $accept_dhcp_domain);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$dhcp_client_not_supported_message = "Could not find schema node for xpath \/config\/devices\/entry[@name='localhost.localdomain']\/deviceconfig\/system\/type\/dhcp-client";
	$wo_comment = $response['wo_comment'];
	if (strpos($wo_comment, $dhcp_client_not_supported_message) !== 0) {
		$wo_comment .= "DHCP Client configuration is not support on the PA device.";
		$wo_comment .= "\nHence, ignoring the Task Failure.";
		$response = prepare_json_response(ENDED, $wo_comment, $context, true);
	}
	else {
		$response = json_encode($response);
	}
	echo $response;
	exit;
}

$response = prepare_json_response(ENDED, "DHCP Client configured successfully on the PA Device $device_id", $context, true);
echo $response;

?>
