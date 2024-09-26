<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/PALOALTO/Library/paloalto_generic_common.php';

function list_args() {
	create_var_def('device_id', 'Device');
	create_var_def('profile_group_name', 'String');
	create_var_def('anti_spyware', 'String');
	create_var_def('anti_virus', 'String');
	create_var_def('vulnerability', 'String');
	create_var_def('wildfire_analysis', 'String');
	create_var_def('url_filtering', 'String');
	create_var_def('file_blocking', 'String');
	create_var_def('data_filtering', 'String');
}

check_mandatory_param('device_id');
if(empty($context['profile_group_name']) || (empty($context['anti_virus']) && empty($context['anti_spyware']) &&
		empty($context['vulnerability']) && empty($context['wildfire_analysis']) && empty($context['url_filtering']) &&
		empty($context['file_blocking']) && empty($context['data_filtering']))) {

	$response = prepare_json_response(FAILED,
                                       "All mandatory parameters are not present to create profile group.",
                                       $context, true);
	echo $response;
	exit;
}

$device_id = substr($context['device_id'], 3);
$profile_group_name = $context['profile_group_name'];
$anti_virus = "";
$anti_spyware = "";
$vulnerability = "";
$wildfire_analysis = "";
$url_filtering = "";
$file_blocking = "";
$data_filtering = "";
if (!empty($context['anti_virus'])) {
	$anti_virus = $context['anti_virus'];
}
if (!empty($context['anti_spyware'])) {
	$anti_spyware = $context['anti_spyware'];
}
if (!empty($context['vulnerability'])) {
	$vulnerability = $context['vulnerability'];
}
if (!empty($context['wildfire_analysis'])) {
	$wildfire_analysis = $context['wildfire_analysis'];
}
if (!empty($context['url_filtering'])) {
	$url_filtering = $context['url_filtering'];
}
if (!empty($context['file_blocking'])) {
	$file_blocking = $context['file_blocking'];
}
if (!empty($context['data_filtering'])) {
	$data_filtering = $context['data_filtering'];
}

$response = _paloalto_generic_profile_group($device_id, CMD_CREATE, $profile_group_name, $anti_virus,
							$anti_spyware, $vulnerability, $wildfire_analysis,
							$url_filtering, $file_blocking, $data_filtering);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}
	
$response = prepare_json_response(ENDED, "Profile Group $profile_group_name created successfully on the PA Device $device_id", $context, true);
echo $response;

?>
