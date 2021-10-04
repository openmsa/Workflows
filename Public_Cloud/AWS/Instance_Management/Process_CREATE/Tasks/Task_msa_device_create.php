<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args() {
	create_var_def('customer_id');
	//create_var_def('managed_device_name', 'String');
	//create_var_def('device_external_reference', 'String');
	create_var_def('manufacturer_id');
	create_var_def('model_id');
	create_var_def('device_ip_address');
	create_var_def('login');
	create_var_def('password');
	create_var_def('new_password');
	create_var_def('snmp_community');
}

//check_mandatory_param('managed_device_name');
check_mandatory_param('manufacturer_id');
check_mandatory_param('model_id');
check_mandatory_param('login');
check_mandatory_param('new_password');

if (!isset($context['customer_id'])) {
	$context['customer_id'] = $context['UBIQUBEID'];
}

// MSA device creation parameters
$customer_id = $context['customer_id'];
$customer_db_id = substr($customer_id,4);
$managed_device_name = $context["InstanceId"];
$context["service_id"]  = $context["service_id"] + " - " + $context["InstanceId"];
$manufacturer_id = $context['manufacturer_id'];
$model_id = $context['model_id'];
$login = $context['login'];
if (!isset($context["password"])) {
    $password = $context["InstanceId"];
} else {
    $password = $context["password"];
}
$password_admin = $context['new_password'];
$device_ip_address = $context['device_ip_address'];
$device_external_reference = "";
$snmp_community = $context['snmp_community'];
$device_hostname = str_replace(".", "-", $device_ip_address);
$context['hostname'] = "host-".$device_hostname;
$device_hostname = $context['hostname'];

$response = _device_create($customer_db_id, $managed_device_name, $manufacturer_id, $model_id, $login, $password, $password_admin, $device_ip_address, $device_external_reference, $log_enabled = "true", $log_more_enabled = "true",$mail_alerting = "true", $reporting = "true", $snmp_community, "", $device_hostname, 22);

$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}
$device_id = $response['wo_newparams']['entity']['externalReference'];
$wo_comment = "Device External Reference : $device_id";
logToFile($wo_comment);
	
$context['device_id'] = $device_id;

$device_id_long = substr($context['device_id'], 3);

_device_set_nature_by_id($device_id_long, "VPUB");


/**
* generate a hostname based on the public IP
* this is necessary for sysloct collection

$device_hostname = str_replace(".", "-", $device_ip_address);
$context['hostname'] = "host-".$device_hostname;
$device_hostname = $context['hostname'];
$response = _device_set_hostname_by_id ($device_id_long, $device_hostname);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}
*/
/**
* mark the device as provisioned so that it's getting monitored as soon as it's IP is accessible
*/ 
$response = _device_mark_as_provisioned($device_id_long);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}

if (isset($context["KeyName"])) {
	_configuration_variable_create ($device_id_long, "SSH_KEY", "/opt/devops/ssh/".$context["KeyName"].".pem");
}

$response = prepare_json_response(ENDED, "MSA Device created successfully.\n$wo_comment", $context, true);
echo $response;


?>
