<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/Common/Library/msa_common.php';


//Retrive variables from $context() and define the new ones
$server_name = $context['server_name'] = $context['server_vendor']."[".$context['server_ip_address']."]";
$server_ip_address = $context['server_ip_address'];
$device_external_reference = $context['device_external_reference'] = hash('crc32', md5($context['server_vendor'].$context['server_ip_address'].$context['server_mac_address']));

//model and manufacture IDs should be changed properlly
$manufacture_id = $context['manufacture_id'] = '191200';
$model_id = $context['model_id'] = '191200';

$username = $context['username'];
$password = $password_admin = $context['password'];

//Extract numeric customer ID
if (preg_match('/.{3}\D*?(\d+?)/', $context['UBIQUBEID'], $matches) === 1) {
	$customer_db_id = $context['customer_db_id'] = $matches[1];
} else {
	$customer_db_id = $context['customer_db_id'] = -1;
}

//Create new managed entity
$response = json_decode(_device_create($customer_db_id,
						   			   $server_name,
						   			   $manufacture_id,
						   			   $model_id,
						   			   $username,
						   			   $password,
						   			   $password_admin,
						   			   $server_ip_address,
						   			   $device_external_reference
						   			  ), True);



if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}


//Extract device id and put into $context()
$device_id = $context['device_id'] = $response['wo_newparams']['entity']['id'];

if ($device_id) {
	$wo_comment = "Device ID : $device_id";
	$response = prepare_json_response(ENDED, "MSA Device created successfully.\n$wo_comment", $context, true);
	echo $response;
} else {
	task_error("Device has not been created successfully.");
}

?> 



 
