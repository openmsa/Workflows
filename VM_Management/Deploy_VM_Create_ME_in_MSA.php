<?php

/**
 * This file is necessary to include to use all the in-built libraries of /opt/fmc_repository/Reference/Common
 */
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

/**
 * List all the parameters required by the task
 */
function list_args()
{

}
// MSA device creation parameters
$customer_id = "20";
$managed_device_name = $context['name'];
$manufacturer_id = "14020601";
$model_id = "14020601";
$login = "root";
$password = '123456';
$password_admin = '123456';
$device_ip_address = "10.31.1.198";
$device_external_reference =  $context['name'];

$response = _device_create($customer_id, $managed_device_name, $manufacturer_id,
							$model_id, $login, $password, $password_admin, $device_ip_address, $device_external_reference);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}
//Original lines are commented
//$device_id = $response['wo_newparams']['entity']['externalReference'];
//$wo_comment = "Device External Reference : $device_id";

$device_id = $response['wo_newparams']['entity']['id'];
$wo_comment = "Device ID : $device_id";
logToFile($wo_comment);
	
$context['device_id'] = $device_id;
$response = prepare_json_response(ENDED, "MSA Device created successfully.\n$wo_comment", $context, true);
echo $response;


?>