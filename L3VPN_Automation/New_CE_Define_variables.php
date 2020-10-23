<?php

/**
 * This file is necessary to include to use all the in-built libraries of /opt/fmc_repository/Reference/Common
 */
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args()
{
  create_var_def('site', 'OBMFRef');
}

check_mandatory_param('site');

$site = $context['site'];
$device_models = $context['device_models_array'];
$ms_ipam_tenant = $context['microservices_array']['IPAM Tenants'];
$ms_ipam_site = $context['microservices_array']['IPAM Sites'];
$ms_ipam_device = $context['microservices_array']['IPAM Devices'];
$ipam_device_id = $context['ipam_device_id'];
$customer_name = $context['customer_name'];

$response = update_asynchronous_task_details($context, "Retrive information about device on the site...");
$response = json_decode(synchronize_objects_and_verify_response($ipam_device_id), true);
if ($response['wo_status'] !== ENDED) {
  echo $response;
  exit;
}

$response = json_decode(import_objects($ipam_device_id, array($ms_ipam_device)), True);
$ms_objects_array = $response['wo_newparams'][$ms_ipam_device];

$ce_device_name = null;
foreach($ms_objects_array as $device => $device_details) {
  if (array_key_exists('site', $device_details)) {
  	if ($device_details['site'] === $site) {
      $ce_device = $context['ce_device'] = $device_details;
    } 
  }
}

if (empty($ce_device)) {
  task_error('There are not any devices on site '.$site.' of customer '.$customer_name);
}

if ($ce_device['role'] !== 'CE') {
  task_error('Device '.$ce_device['object_id'].' is not CE device');
}

if ($ce_device['status'] !== 'staged') {
  task_error('Device '.$ce_device['object_id'].' is not in Staged status');
}

if (array_key_exists('local_context_data', $ce_device)) {
  logToFile(debug_dump($ce_device['local_context_data'], "DEBUG: LOCAL CONTEXT"));
  $local_context_data_object = simplexml_load_string($ce_device['local_context_data']);
  $ce_device['username'] = (string) $local_context_data_object->username;
  $ce_device['password'] = (string) $local_context_data_object->password;
  $ce_device['interface'] = (string) $local_context_data_object->interface;
  $ce_device['port'] = (string) $local_context_data_object->port;
}

$ce_device['manufacture_id'] = $device_models[$ce_device['vendor']]['manufacture_id'];
$ce_device['model_id'] = $device_models[$ce_device['vendor']]['model_id'][$ce_device['interface']];
$ce_device['depolyment_settings'] = $device_models[$ce_device['vendor']]['deployment_settings'][$ce_device['interface']];

$ip_addr_temp_array = explode('/', $ce_device['primary_ip']);
$ce_device['mgmt_ip_address'] = $ip_addr_temp_array[0];

$context['ce_device_details'] = $ce_device;

task_success('Task OK');
?>