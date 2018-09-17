<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/VMWARE/vRO/Library/REST/vmware_vro_common_rest.php';

function list_args()
{
}

if (empty($context['vm_id'])) {

	$response = prepare_json_response(ENDED, "No VM to delete", $context, true);
	echo $response;
	exit;
}

$parameters = array();

$value = array("sdk-object" => array("type" => VC_VIRTUAL_MACHINE, "id" => $context['vm_id']));
vro_add_parameter_in_request($parameters, 'vm', VC_VIRTUAL_MACHINE, $value);

$parameters_array['parameters'] = $parameters;

vro_execute_workflow_and_wait_for_completion(VRO_DELETE_VM_V20, $parameters_array);

$response = prepare_json_response(ENDED, "VM deleted successfully.", $context, true);
echo $response;

?>
