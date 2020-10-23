<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

$site = $context['site'];
$device_models = $context['device_models_array'];
$ms_ipam_tenant = $context['microservices_array']['IPAM Tenants'];
$ms_ipam_site = $context['microservices_array']['IPAM Sites'];
$ms_ipam_device = $context['microservices_array']['IPAM Devices'];
$ipam_device_id = $context['ipam_device_id'];
$customer_name = $context['customer_name'];
$ce_device_details = $context['ce_device_details'];

$response = update_asynchronous_task_details($context, "Creating managed entity ".$ce_device_details['object_id']."... ");

//Extract numeric customer ID
logToFile(debug_dump($context['UBIQUBEID'], "DEBUG: UBIQUBEID"));
if (preg_match('/^\D+?(\d+?)$/', $context['UBIQUBEID'], $matches) === 1) {
	$customer_db_id = $context['customer_db_id'] = $matches[1];
    logToFile(debug_dump($customer_db_id, "DEBUG: customer_db_id"));
} else {
	$customer_db_id = $context['customer_db_id'] = -1;
    logToFile(debug_dump($customer_db_id, "DEBUG: customer_db_id"));
}

//Create new managed entity
$response = json_decode(_device_create($customer_db_id,
	   			      			       $ce_device_details['object_id'],
	   			      			       $ce_device_details['manufacture_id'],
	   			      			       $ce_device_details['model_id'],
	   			      			       $ce_device_details['username'],
	   			      			       $ce_device_details['password'],
	   			      			       '',
	   			      			       $ce_device_details['mgmt_ip_address'],
	   			      			       $ce_device_details['object_id'],
                                   	   "true",
                                   	   "true",
                                   	   "true",
                                   	   "false",
                                   	   "public",
                                   	   "",
                                   	   $ce_device_details['port']
	 			  					                  ), 
                           True);


if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}

$ce_device_id = $context['ce_device_details']['ce_device_id'] = $response['wo_newparams']['entity']['id'];

if ($ce_device_id) {
	$wo_comment = "Device ID : $ce_device_id";
	$response = prepare_json_response(ENDED, "Creating managed entity ".$ce_device_details['object_id']."... \nMSA Device created successfully.\n".$wo_comment, $context, true);
	echo $response;
} else {
	task_error("CE Device has not been created successfully.");
}

?>