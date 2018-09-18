<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/VMWARE/vRO/Library/REST/vmware_vro_common_rest.php';

function list_args()
{
	create_var_def('vm_name', 'String');
	create_var_def('cmd', 'String');
}

check_mandatory_param('vm_name');
check_mandatory_param('cmd');

$customer_reference = $context['UBIQUBEID'];

// Get Customer list of devices
$devices_list = _lookup_list_devices_by_customer_reference ($customer_reference);
$devices_list = json_decode($devices_list , true);

foreach ($devices_list['wo_newparams'] as &$device) {
	$device_id = $device['id'];

	$response = _device_read_by_id ($device_id);	
	$response = json_decode($response, true);	
	$response_status = $response['wo_status'];
	if ($response_status  == "FAIL") {
		task_exit(FAILED, "Read device is FAILED.");
		exit;
	}
	$device_name = $response['wo_newparams']['name']; 
	if ($device_name == $context['vm_name']) {
		$management_ip = $response['wo_newparams']['managementAddress'];
		$login = $response['wo_newparams']['login'];
		$password = $response['wo_newparams']['password'];
		break;
	}
}

$parameters = array();

$value = array("string" => array("value" => $management_ip));
vro_add_parameter_in_request($parameters, 'hostNameOrIP', 'string', $value);

$value = array("string" => array("value" => $login));
vro_add_parameter_in_request($parameters, 'username', 'string', $value);

$value = array("string" => array("value" => $password));
vro_add_parameter_in_request($parameters, 'password', 'SecureString', $value);

$value = array("string" => array("value" => $context['cmd']));
vro_add_parameter_in_request($parameters, 'cmd', 'string', $value);

$value = array("boolean" => array("value" => true));
vro_add_parameter_in_request($parameters, 'passwordAuthentication', 'boolean', $value);

$parameters_array['parameters'] = $parameters;

vro_execute_workflow_and_wait_for_completion(VRO_RUN_SSH_COMMAND_V9, $parameters_array);

$ssh_cmd_response = $context['output_parameters'][2]['value']['string']['value'];
$context['ssh_cmd_response'] = $ssh_cmd_response; 

task_exit(ENDED, "SSH command executed successfully.\nResponse :\n$ssh_cmd_response");

?>