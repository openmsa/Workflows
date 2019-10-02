<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args() {
	create_var_def('device_name', 'String');
	create_var_def('device_mngt_ip', 'String');
	create_var_def('device_login', 'String');
	create_var_def('device_password', 'String');

}

$operator_prefix = $context['operator_prefix'];
$customer_id = $context['customer_id'];
$customer_id_long = substr($customer_id, 4);
$device_name = $context['device_name'];
$manufacturer_id = $context['device_manufacturer'];
$model_id = $context['device_model'];
$device_login = $context['device_login'];
$device_password = $context['device_password'];
$device_mngt_ip = $context['device_mngt_ip'];
$device_external_reference = "";

$response = _device_create($customer_id_long, $device_name, $manufacturer_id, $model_id, $device_login, $device_password, $device_password, $device_mngt_ip, $device_external_reference);

$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}
/**
 * The REST API to create a device returns a unique external reference. An external reference is an identified for a device that can be optionally set at device creation. 
 * By default this external reference value is set to the device database identifier.
 */
$device_id = $response['wo_newparams']['entity']['externalReference'];
$wo_comment = "Device External Reference : $device_id";
logToFile($wo_comment);
	
$context['device_id'] = $device_id;
$response = prepare_json_response(ENDED, "Device created successfully.\n$wo_comment", $context, true);
echo $response;

?>
