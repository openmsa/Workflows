<?php


require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

$ms_ipam_tenant = $context['microservices_array']['IPAM Tenants'];
$ms_ipam_site = $context['microservices_array']['IPAM Sites'];
$ms_ipam_device = $context['microservices_array']['IPAM Devices'];
$ipam_device_id = $context['ipam_device_id'];
$customer_name = $context['customer_name'];

$response = json_decode(synchronize_objects_and_verify_response($ipam_device_id), true);
if ($response['wo_status'] !== ENDED) {
  echo $response;
  exit;
}

$response = update_asynchronous_task_details($context, "Retrive information about customers... ");
$response = json_decode(import_objects($ipam_device_id, array($ms_ipam_tenant)), True);
$ms_objects_array = $response['wo_newparams'][$ms_ipam_tenant];

$does_tenant_exist = False;
foreach ($ms_objects_array as $tenant_name => $tenant_details) {
  if ($tenant_details['object_id'] === $customer_name) {
    $does_tenant_exist = True;
  }
}

if (!$does_tenant_exist) {
	task_error('Customer '.$customer_name.' does not exist in IPAM system');
} else {
  
  $sites_array = array();
  $response = json_decode(import_objects($ipam_device_id, array($ms_ipam_site)), True);
  $ms_objects_array = $response['wo_newparams'][$ms_ipam_site];
  foreach ($ms_objects_array as $site => $site_details) {
    if (array_key_exists('tenant', $site_details)) {
    	if ($site_details['tenant'] === $customer_name) {
    	  $sites_array[] = array('name' => $site_details['object_id'], 
    	                         'id'	=> $site_details['id']
    	                        );
  		}
    }
  }
    
  $devices_array = array();
  $response = json_decode(import_objects($ipam_device_id, array($ms_ipam_device)), True);
  $ms_objects_array = $response['wo_newparams'][$ms_ipam_device];
  foreach ($ms_objects_array as $device => $device_details) {
  	if (array_key_exists('tenant', $device_details)) {
      if ($device_details['tenant'] === $customer_name)  {
      	$devices_array[] = array('name' => $device_details['object_id'], 
                          	     'id'	=> $device_details['id']
                            		);
  	  }
    }
  }
}

$context['sites_array'] = $sites_array;
$context['devices_array'] = $devices_array;

task_success('Success. Customer '.$customer_name.' has '.count($sites_array).' sites and '.count($devices_array).' devices.');
?>