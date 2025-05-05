<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/VMWARE/vRO/Library/REST/vmware_vro_common_rest.php';

function list_args()
{
	create_var_def('hostNameOrIP', 'String');
	create_var_def('port', 'Integer');
	create_var_def('username', 'String');
	create_var_def('password', 'Composite');
	create_var_def('cmd', 'String');
	create_var_def('passwordAuthentication', 'Boolean');
	create_var_def('vco_key_path', 'Composite');
	create_var_def('passphrase', 'Composite');
	create_var_def('encoding', 'String');
}

check_mandatory_param('hostNameOrIP');
check_mandatory_param('username');
check_mandatory_param('cmd');
check_mandatory_param('passwordAuthentication');

$vcenter_fqdn = $context['vcenter_fqdn'];

$parameters = array();

$value = array("string" => array("value" => $context['hostNameOrIP']));
vro_add_parameter_in_request($parameters, 'hostNameOrIP', 'string', $value);

$value = array("number" => array("value" => $context['port']));
vro_add_parameter_in_request($parameters, 'port', 'number', $value);

$value = array("string" => array("value" => $context['username']));
vro_add_parameter_in_request($parameters, 'username', 'string', $value);

$value = array("SecureString" => array("value" => $context['password']));
vro_add_parameter_in_request($parameters, 'password', 'SecureString', $value);

$value = array("string" => array("value" => $context['cmd']));
vro_add_parameter_in_request($parameters, 'cmd', 'string', $value);

$value = array("boolean" => array("value" => filter_var($context['passwordAuthentication'], FILTER_VALIDATE_BOOLEAN)));
vro_add_parameter_in_request($parameters, 'passwordAuthentication', 'boolean', $value);

$value = array("Path" => array("value" => $context['vco_key_path']));
vro_add_parameter_in_request($parameters, 'path', 'Path', $value);

$value = array("SecureString" => array("value" => $context['passphrase']));
vro_add_parameter_in_request($parameters, 'passphrase', 'SecureString', $value);

$value = array("string" => array("value" => $context['encoding']));
vro_add_parameter_in_request($parameters, 'encoding', 'string', $value);

$parameters_array['parameters'] = $parameters;

vro_execute_workflow_and_wait_for_completion(VRO_RUN_SSH_COMMAND_V9, $parameters_array);

$result = $context['output_parameters']['result'];
$context['result'] = $result;
$output_text = $output_parameters['outputText'];
$context['output_text'] = $output_text;
$error_text = $output_parameters['errorText'];
$context['error_text'] = $error_text;

$wo_comment = "Result : $result\nOutput text : $output_text\nError text : $error_text";

$response = prepare_json_response(ENDED, "SSH command executed successfully.\n$wo_comment", $context, true);
echo $response;

?>