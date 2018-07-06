<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/VMWARE/vRO/Library/REST/vmware_vro_common_rest.php';

function list_args()
{
	create_var_def('vm', 'String');
	create_var_def('setCPU', 'Boolean');
	create_var_def('setRAM', 'Boolean');
	create_var_def('setDisk', 'Boolean');
	create_var_def('cpuSharesLevel', 'Composite');
	create_var_def('cpuShares', 'Composite');
	create_var_def('cpuReservation', 'Composite');
	create_var_def('cpuLimit', 'Composite');
	create_var_def('ramSharesLevel', 'Composite');
	create_var_def('ramShares', 'Composite');
	create_var_def('ramReservation', 'Composite');
	create_var_def('ramLimit', 'Composite');
	create_var_def('diskSharesLevel', 'Composite');
	create_var_def('diskShares', 'Composite');
}

check_mandatory_param('vm');
check_mandatory_param('setCPU');
check_mandatory_param('setRAM');
check_mandatory_param('setDisk');

$parameters = array();

$value = array("sdk-object" => array("type" => VC_VIRTUAL_MACHINE, "id" => $context['vm']));
vro_add_parameter_in_request($parameters, 'vm', VC_VIRTUAL_MACHINE, $value);

$value = array("boolean" => array("value" => filter_var($context['setCPU'], FILTER_VALIDATE_BOOLEAN)));
vro_add_parameter_in_request($parameters, 'setCPU', 'boolean', $value);

$value = array("boolean" => array("value" => filter_var($context['setRAM'], FILTER_VALIDATE_BOOLEAN)));
vro_add_parameter_in_request($parameters, 'setRAM', 'boolean', $value);

$value = array("boolean" => array("value" => filter_var($context['setDisk'], FILTER_VALIDATE_BOOLEAN)));
vro_add_parameter_in_request($parameters, 'setDisk', 'boolean', $value);

$value = array("sdk-object" => array("type" => VC_SHARES_LEVEL, "id" => $context['cpuSharesLevel']));
vro_add_parameter_in_request($parameters, 'cpuSharesLevel', VC_SHARES_LEVEL, $value);

$value = array("number" => array("value" => $context['cpuShares']));
vro_add_parameter_in_request($parameters, 'cpuShares', 'number', $value);

$value = array("number" => array("value" => $context['cpuReservation']));
vro_add_parameter_in_request($parameters, 'cpuReservation', 'number', $value);

$value = array("number" => array("value" => $context['cpuLimit']));
vro_add_parameter_in_request($parameters, 'cpuLimit', 'number', $value);

$value = array("sdk-object" => array("type" => VC_SHARES_LEVEL, "id" => $context['ramSharesLevel']));
vro_add_parameter_in_request($parameters, 'ramSharesLevel', VC_SHARES_LEVEL, $value);

$value = array("number" => array("value" => $context['ramShares']));
vro_add_parameter_in_request($parameters, 'ramShares', 'number', $value);

$value = array("number" => array("value" => $context['ramReservation']));
vro_add_parameter_in_request($parameters, 'ramReservation', 'number', $value);

$value = array("number" => array("value" => $context['ramLimit']));
vro_add_parameter_in_request($parameters, 'ramLimit', 'number', $value);

$value = array("sdk-object" => array("type" => VC_SHARES_LEVEL, "id" => $context['diskSharesLevel']));
vro_add_parameter_in_request($parameters, 'diskSharesLevel', VC_SHARES_LEVEL, $value);

$value = array("number" => array("value" => $context['diskShares']));
vro_add_parameter_in_request($parameters, 'diskShares', 'number', $value);

$parameters_array['parameters'] = $parameters;

vro_execute_workflow_and_wait_for_completion(VRO_SET_VM_PERFORMANCE_V30, $parameters_array);

$response = prepare_json_response(ENDED, "VM Performance set successfully.", $context, true);
echo $response;

?>