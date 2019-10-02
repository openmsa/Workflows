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
  /** 
   * You can use var_name convention for your variables
   * They will display automaticaly as "Var Name"
   * The allowed types are:
   *    'String', 'Boolean', 'Integer', 'Password', 'IpAddress',
   *    'IpMask', 'Ipv6Address', 'Composite', 'OBMFRef', 'Device'
   *
   * Add as many variables as needed
   */ 
   create_var_def('customer', 'String');
   create_var_def('manufacturer_id', 'String');
   create_var_def('model_id', 'String');
   create_var_def('device_id', 'String');
   create_var_def('status in msa', 'String');
}

//sleep(20);

check_mandatory_param('manufacturer_id');
check_mandatory_param('model_id');

// MSA device creation parameters
$customer_id = substr($context['customer'], 4);
$managed_device_name = $context['vm_name'];
$manufacturer_id = $context['manufacturer_id'];
$model_id = $context['model_id'];
$login = $context['admin_username'];
//$snmp_community = 'ubiqube';
$password = $context['admin_password'];
$password_admin = $context['admin_password'];
$device_ip_address = $context['public_address_value'];
$device_external_reference = "";

$device_external_reference = "";
if (array_key_exists('device_external_reference', $context)) {
	$device_external_reference = $context['device_external_reference'];
}

$response = _device_create($customer_id, $managed_device_name, $manufacturer_id,
							$model_id, $login, $password, "", $device_ip_address, $device_external_reference);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}
$context['status in msa']='Device Created';
$device_id = $response['wo_newparams']['entity']['externalReference'];
$context['device_id'] = $device_id;
$wo_comment = "Device External Reference : $device_id";
logToFile($wo_comment);
	

$response = prepare_json_response(ENDED, "MSA Devices created successfully.", $context, true);
echo $response;


?>
