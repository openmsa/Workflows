<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/PALOALTO/Library/paloalto_generic_common.php';

function list_args() {
	create_var_def('device_id', 'Device');
	create_var_def('url_filtering_user_profile_name', 'String');
	create_var_def('license_expired', 'String');
	create_var_def('enable_container_page', 'String');
	create_var_def('dynamic_url', 'String');
	create_var_def('log_container_page_only', 'String');
	create_var_def('allow_members.0.member', 'String');
	create_var_def('alert_members.0.member', 'String');
	create_var_def('block_members.0.member', 'String');
	create_var_def('continue_members.0.member', 'String');
	create_var_def('override_members.0.member', 'String');
	create_var_def('allow_list_urls.0.member', 'String');
	create_var_def('block_list_urls.0.member', 'String');
	create_var_def('action', 'String');
	create_var_def('description', 'String');
}

check_mandatory_param('device_id');
check_mandatory_param('url_filtering_user_profile_name');

$device_id = substr($context['device_id'], 3);
$url_filtering_user_profile_name = $context['url_filtering_user_profile_name'];
$license_expired = "";
$enable_container_page = "no";
$dynamic_url = "no";
$log_container_page_only = "yes";
$action = "block";
$description = "";
if (!empty($context['license_expired'])) {
	$license_expired = $context['license_expired'];
}
if (!empty($context['enable_container_page'])) {
	$enable_container_page = $context['enable_container_page'];
}
if (!empty($context['dynamic_url'])) {
	$dynamic_url = $context['dynamic_url'];
}
if (!empty($context['log_container_page_only'])) {
	$log_container_page_only = $context['log_container_page_only'];
}
if (!empty($context['action'])) {
	$action = $context['action'];
}
if (!empty($context['description'])) {
	$description = $context['description'];
}

if (array_key_exists('alert_members', $context)) {
	$alert = $context['alert_members'];
}
if (array_key_exists('allow_members', $context)) {
	$allow = $context['allow_members'];
}
if (array_key_exists('block_members', $context)) {
	$block = $context['block_members'];
}
if (array_key_exists('continue_members', $context)) {
	$continue = $context['continue_members'];
}
if (array_key_exists('override_members', $context)) {
	$override = $context['override_members'];
}
if (array_key_exists('allow_list_urls', $context)) {
	$allow_list = $context['allow_list_urls'];
}
if (array_key_exists('block_list_urls', $context)) {
	$block_list = $context['block_list_urls'];
}

$response = _paloalto_generic_url_filtering_user_profile($device_id, CMD_CREATE, $url_filtering_user_profile_name,
										$license_expired, $enable_container_page,
										$dynamic_url, $log_container_page_only,
										$alert, $allow, $block, $continue, $override,
										$allow_list, $block_list, $action, $description);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}

$response = prepare_json_response(ENDED, "URL Filtering User-profile $url_filtering_user_profile_name created successfully on the PA Device $device_id", $context, true);
echo $response;

?>
