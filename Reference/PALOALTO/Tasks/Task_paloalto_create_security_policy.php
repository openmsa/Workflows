<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/PALOALTO/Library/paloalto_generic_common.php';

function list_args() {
	create_var_def('device_id', 'Device');
	create_var_def('name', 'String');
	create_var_def('zone_from', 'String');
	create_var_def('source_address', 'IpAddress');
	create_var_def('zone_to', 'String');
	create_var_def('destination_address', 'IpAddress');
	create_var_def('services.0.service', 'String');
	create_var_def('applications.0.application', 'String');
	create_var_def('users.0.users', 'String');
	create_var_def('categories.0.category', 'String');
	create_var_def('hip_prrofiles.0.hip_profile', 'String');
	create_var_def('profile_group', 'String');
	create_var_def('schedule', 'String');
	create_var_def('log_start', 'String');
	create_var_def('log_end', 'String');
	create_var_def('action', 'String');
}

check_mandatory_param('device_id');
check_mandatory_param('name');
check_mandatory_param('zone_from');
check_mandatory_param('zone_to');
check_mandatory_param('source_address');
check_mandatory_param('destination_address');
check_mandatory_param('services');
check_mandatory_param('action');

$device_id = substr($context['device_id'], 3);
$name = $context['name'];
$zone_from = $context['zone_from'];
$source_address = $context['source_address'];
$zone_to = $context['zone_to'];
$destination_address = $context['destination_address'];
$services = $context['services'];
$action = $context['action'];

$profile_group = "";
$schedule = "";
$log_start = "no";
$log_end = "yes";
$application = array();
$categories = array();
$users = array();
$hip_profiles = array();
if (array_key_exists('applications', $context)) {
	$application = $context['applications'];
}
if (array_key_exists('categories', $context)) {
	$categories = $context['categories'];
}
if (array_key_exists('users', $context)) {
	$users = $context['users'];
}
if (array_key_exists('hip_profiles', $context)) {
	$hip_profiles = $context['hip_profiles'];
}
if (array_key_exists('profile_group', $context)) {
	$profile_group = $context['profile_group'];
}

if (!empty($context['schedule'])) {
	$schedule = $context['schedule'];
}
if (!empty($context['log_start'])) {
	$log_start = $context['log_start'];
}
if (!empty($context['log_end'])) {
	$log_end = $context['log_end'];
}

$response = _paloalto_generic_security_policy($device_id, CMD_CREATE, $name,
							$zone_from, $source_address, $zone_to, $destination_address,
							$services, $action, $application, $users, $categories,
							$hip_profiles, $profile_group, $schedule, $log_start, $log_end);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}
	
$response = prepare_json_response(ENDED, "Security Policy $name created successfully on the PA Device $device_id", $context, true);
echo $response;

?>
