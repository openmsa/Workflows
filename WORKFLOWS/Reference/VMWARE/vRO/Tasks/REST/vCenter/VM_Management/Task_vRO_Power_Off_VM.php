<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/VMWARE/vRO/Library/REST/vmware_vro_common_rest.php';

function list_args()
{
	create_var_def('vm', 'OBMFRef');
}

if (empty($context['vm'])) {

	$response = prepare_json_response(ENDED, "No VM to power-off.", $context, true);
	echo $response;
	exit;
}

$parameters = array();

$value = array("sdk-object" => array("type" => VC_VIRTUAL_MACHINE, "id" => $context['vm']));
vro_add_parameter_in_request($parameters, 'vm', VC_VIRTUAL_MACHINE, $value);

$parameters_array['parameters'] = $parameters;

vro_execute_workflow_and_wait_for_completion(VRO_POWER_OFF_VM_AND_WAIT_V20, $parameters_array);

$response = prepare_json_response(ENDED, "VM powered off successfully.", $context, true);
echo $response;

?>