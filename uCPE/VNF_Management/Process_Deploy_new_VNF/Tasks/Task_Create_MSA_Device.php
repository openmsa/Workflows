<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args() {
	//create_var_def('customer_id', 'Integer');
	//create_var_def('device_external_reference', 'String');
	create_var_def('manufacturer_id', 'Integer');
	create_var_def('model_id', 'Integer');
	create_var_def('device_ip_address', 'IP Address');
	create_var_def('login', 'String');
	create_var_def('password', 'Password');
	create_var_def('new_password', 'Password');
	//create_var_def('snmp_community', 'String');
}

//check_mandatory_param('customer_id');
check_mandatory_param('manufacturer_id');
check_mandatory_param('model_id');
check_mandatory_param('login');
check_mandatory_param('new_password');


$PROCESSINSTANCEID = $context['PROCESSINSTANCEID'];
$EXECNUMBER = $context['EXECNUMBER'];
$TASKID = $context['TASKID'];
$process_params = array('PROCESSINSTANCEID' => $PROCESSINSTANCEID,
						'EXECNUMBER' => $EXECNUMBER,
						'TASKID' => $TASKID);

$context['customer_id'] = $context['UBIQUBEID'];
$context['snmp_community'] = "my_community";

// MSA device creation parameters
$customer_id = $context['customer_id'];
$customer_db_id = substr($customer_id,4);
$managed_device_name = $context["vnf_name"];
$manufacturer_id = $context['manufacturer_id'];
$model_id = $context['model_id'];
$login = $context['login'];
$password = $context["password"];
$password_admin = $context['new_password'];
$device_ip_address = $context['device_ip_address'];
$device_external_reference = "";

if (array_key_exists('device_external_reference', $context)) {
	$device_external_reference = $context['device_external_reference'];
}

$response = _device_create($customer_db_id, $managed_device_name, $manufacturer_id,
							$model_id, $login, $password, $password_admin, $device_ip_address, $device_external_reference);

$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}
$device_id = $response['wo_newparams']['entity']['externalReference'];
$wo_comment = "Device External Reference : $device_id";
logToFile($wo_comment);
	
$context['vnf_device_id'] = $device_id;

$device_id_long = substr($context['vnf_device_id'], 3);

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

$response = prepare_json_response(ENDED, "MSA Device created successfully.\n$wo_comment", $context, true);
echo $response;


?>
