<?php

/**
 * This file is necessary to include to use all the in-built libraries of /opt/fmc_repository/Reference/Common
 */
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args()
{
  create_var_def('vendor', 'String');
  create_var_def('manufacture_id', 'String');
  create_var_def('model_id', 'String');
}


check_mandatory_param('vendor');
check_mandatory_param('manufacture_id');
check_mandatory_param('model_id');

$vendor = $context['vendor'];
$context['microservice_path'] = $microservice_path = 'CommandDefinition/REDFISHAPI/Generic/';
$context['microservice_file_array'] = $microservice_file_array = array(
  										'redfish_bios_settings.xml',
										'redfish_inventory_fw_links.xml',
										'redfish_inventory_fw.xml',
										'redfish_inventory_sw_links.xml',
										'redfish_inventory_sw.xml',
										'redfish_server_account_links.xml',
										'redfish_server_accounts.xml',
										'redfish_server_actions.xml',
										'redfish_server_general.xml'
										);
//Identify Customer ID
if (preg_match('/.{3}\D*?(\d+?)/', $context['UBIQUBEID'], $matches) === 1) {
	$customer_db_id = $context['customer_db_id'] = $matches[1];
} else {
	$customer_db_id = $context['customer_db_id'] = -1;
}

$profile_name = $context['profile_name'] = $profile_reference = $context['profile_reference'] = 'redfish_'.strtolower($context['vendor']).'_profile';

$profile_comment = $context['profile_comment'] = 'The profile contains microservices to work with '.$vendor.' servers via Redfish API';

//Create configuration profile
$response = json_decode(_profile_configuration_create ($customer_db_id, $profile_name, $profile_reference, $profile_comment, $context['manufacture_id'], $context['model_id']), True);

if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	exit;
}

$context['profile_id'] = $response['wo_newparams']['id'];

task_success('Profile '.$profile_name.' with ID '.$context['profile_id'].' has been created sucessfully');
?>