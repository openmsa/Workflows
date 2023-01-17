<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/VMWARE/vRO/Library/REST/vmware_vro_common_rest.php';

function list_args()
{
	create_var_def('vm', 'String');
	create_var_def('datastore', 'OBMFRef');
	create_var_def('diskIndex', 'Integer');
	create_var_def('diskSize', 'Integer');
	create_var_def('diskMode', 'String');
	create_var_def('scsiBusNumber', 'Integer');
	create_var_def('thinProvisioned', 'Boolean');
}

check_mandatory_param('vm');
check_mandatory_param('datastore');
check_mandatory_param('diskIndex');
check_mandatory_param('diskSize');
check_mandatory_param('diskMode');
check_mandatory_param('thinProvisioned');

$vcenter_fqdn = $context['vcenter_fqdn'];

$parameters = array();

$value = array("sdk-object" => array("type" => VC_VIRTUAL_MACHINE, "id" => $context['vm']));
vro_add_parameter_in_request($parameters, 'vm', VC_VIRTUAL_MACHINE, $value);

$value = array("sdk-object" => array("type" => VC_DATASTORE, "id" => "{$vcenter_fqdn}/" . $context['datastore']));
vro_add_parameter_in_request($parameters, 'datastore', VC_DATASTORE, $value);

$value = array("number" => array("value" => $context['diskIndex']));
vro_add_parameter_in_request($parameters, 'diskIndex', 'number', $value);

$value = array("number" => array("value" => $context['diskSize']));
vro_add_parameter_in_request($parameters, 'diskSize', 'number', $value);

$value = array("sdk-object" => array("type" => VC_DISK_MODE, "id" => $context['diskMode']));
vro_add_parameter_in_request($parameters, 'diskMode', VC_DISK_MODE, $value);

$value = array("number" => array("value" => $context['scsiBusNumber']));
vro_add_parameter_in_request($parameters, 'scsiBusNumber', 'number', $value);

$value = array("boolean" => array("value" => filter_var($context['thinProvisioned'], FILTER_VALIDATE_BOOLEAN)));
vro_add_parameter_in_request($parameters, 'thinProvisioned', 'boolean', $value);

$parameters_array['parameters'] = $parameters;

vro_execute_workflow_and_wait_for_completion(VRO_ADD_DISK_V20, $parameters_array);

$response = prepare_json_response(ENDED, "Disk added successfully.", $context, true);
echo $response;

?>
