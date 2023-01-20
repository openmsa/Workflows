<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/VMWARE/vRO/Library/REST/vmware_vro_common_rest.php';

function list_args()
{
	create_var_def('vm', 'String');
	create_var_def('connectAtPowerOn', 'Boolean');
	create_var_def('deviceType', 'String');
	create_var_def('filePath', 'String');
}

check_mandatory_param('vm');
check_mandatory_param('deviceType');

$parameters = array();

$value = array("sdk-object" => array("type" => VC_VIRTUAL_MACHINE, "id" => $context['vm']));
vro_add_parameter_in_request($parameters, 'vm', VC_VIRTUAL_MACHINE, $value);

$value = array("boolean" => array("value" => filter_var($context['connectAtPowerOn'], FILTER_VALIDATE_BOOLEAN)));
vro_add_parameter_in_request($parameters, 'connectAtPowerOn', 'boolean', $value);

$value = array("string" => array("value" => $context['deviceType']));
vro_add_parameter_in_request($parameters, 'deviceType', 'string', $value);

$value = array("string" => array("value" => $context['filePath']));
vro_add_parameter_in_request($parameters, 'filePath', 'string', $value);

$parameters_array['parameters'] = $parameters;

vro_execute_workflow_and_wait_for_completion(VRO_ADD_CD_ROM_V20, $parameters_array);

$response = prepare_json_response(ENDED, "CD-ROM added succesfully.", $context, true);
echo $response;

?>
