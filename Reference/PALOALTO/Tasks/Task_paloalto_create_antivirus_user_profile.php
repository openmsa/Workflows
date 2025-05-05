<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/PALOALTO/Library/paloalto_generic_common.php';

function list_args() {
	create_var_def('device_id', 'Device');
	create_var_def('antivirus_user_profile_name', 'String');
	create_var_def('decoder.0.decoder_id', 'String');
	create_var_def('decoder.0.decoder_action', 'String');
	create_var_def('decoder.0.decoder_wildfire_action', 'String');
	create_var_def('packet_capture', 'String');
	create_var_def('description', 'String');
}

check_mandatory_param('device_id');
check_mandatory_param('antivirus_user_profile_name');
check_mandatory_param('decoder');

$device_id = substr($context['device_id'], 3);
$antivirus_user_profile_name = $context['antivirus_user_profile_name'];
$decoder = $context['decoder'];

$packet_capture = "no";
$description = "";
if (array_key_exists('packet_capture', $context)) {
	$packet_capture = $context['packet_capture'];
}
if (array_key_exists('description', $context)) {
	$description = $context['description'];
}
$response = _paloalto_generic_antivirus_user_profile($device_id, CMD_CREATE, $antivirus_user_profile_name,
									$decoder, $packet_capture, $description); 
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}
	
$response = prepare_json_response(ENDED, "Anti-virus User-profile $antivirus_user_profile_name created successfully on the PA Device $device_id", $context, true);
echo $response;

?>
