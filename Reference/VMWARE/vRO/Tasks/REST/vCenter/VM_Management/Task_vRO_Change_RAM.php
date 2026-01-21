<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/VMWARE/vRO/Library/REST/vmware_vro_common_rest.php';

function list_args()
{
	create_var_def('vm', 'OBMFRef');
	create_var_def('memory', 'Integer');
}

check_mandatory_param('vm');
check_mandatory_param('memory');

$parameters = array();

$value = array("sdk-object" => array("type" => VC_VIRTUAL_MACHINE, "id" => $context['vm']));
vro_add_parameter_in_request($parameters, 'vm', VC_VIRTUAL_MACHINE, $value);

$value = array("number" => array("value" => $context['memory']));
vro_add_parameter_in_request($parameters, 'memory', 'number', $value);

$parameters_array['parameters'] = $parameters;

vro_execute_workflow_and_wait_for_completion(VRO_CHANGE_RAM_V20, $parameters_array);

$response = prepare_json_response(ENDED, "RAM changed successfully.", $context, true);
echo $response;

?>