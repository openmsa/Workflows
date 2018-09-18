<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/VMWARE/vRO/Library/REST/vmware_vro_common_rest.php';

function list_args()
{
	create_var_def('snapshot_name', 'String');
	#create_var_def('description', 'String');
	#create_var_def('snapshot_memory', 'Boolean');
	#create_var_def('quiesce', 'Boolean');
}

check_mandatory_param('snapshot_name');
#check_mandatory_param('snapshot_memory');
#check_mandatory_param('quiesce');

if (empty($context['vm_id'])) {

	$response = prepare_json_response(ENDED, "No VM to power-off.", $context, true);
	echo $response;
	exit;
}

#$vcenter_fqdn = $context['vcenter_fqdn'];

$parameters = array();

$value = array("sdk-object" => array("type" => VC_VIRTUAL_MACHINE, "id" => $context['vm_id']));
vro_add_parameter_in_request($parameters, 'vm', VC_VIRTUAL_MACHINE, $value);

$value = array("string" => array("value" => $context['snapshot_name']));
vro_add_parameter_in_request($parameters, 'name', 'string', $value);

/**
$value = array("string" => array("value" => $context['description']));
vro_add_parameter_in_request($parameters, 'description', 'string', $value);

$value = array("boolean" => array("value" => filter_var($context['snapshot_memory'], FILTER_VALIDATE_BOOLEAN)));
vro_add_parameter_in_request($parameters, 'memory', 'boolean', $value);

$value = array("boolean" => array("value" => filter_var($context['quiesce'], FILTER_VALIDATE_BOOLEAN)));
vro_add_parameter_in_request($parameters, 'quiesce', 'boolean', $value);
*/

$parameters_array['parameters'] = $parameters;

vro_execute_workflow_and_wait_for_completion(VRO_CREATE_SNAPSHOT_V20, $parameters_array);

$snapshot_id = $context['output_parameters'][0]['value']['sdk-object']['id'];
$context['snapshot_id'] = str_replace(",id:", "/", $snapshot_id);

$response = prepare_json_response(ENDED, "Snapshot created successfully.\nSnapshot id : $snapshot_id", $context, true);
echo $response;

?>