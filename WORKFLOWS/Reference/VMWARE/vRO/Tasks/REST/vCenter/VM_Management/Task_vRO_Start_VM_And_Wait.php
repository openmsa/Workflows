<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/VMWARE/vRO/Library/REST/vmware_vro_common_rest.php';

function list_args()
{
	create_var_def('vm', 'OBMFRef');
	create_var_def('host', 'OBMFRef');
}

if (empty($context['vm'])) {

	$response = prepare_json_response(ENDED, "No VM to start.", $context, true);
	echo $response;
	exit;
}

$vcenter_fqdn = $context['vcenter_fqdn'];

$parameters = array();

$value = array("sdk-object" => array("type" => VC_VIRTUAL_MACHINE, "id" => $context['vm']));
vro_add_parameter_in_request($parameters, 'vm', VC_VIRTUAL_MACHINE, $value);

$value = array("sdk-object" => array("type" => VC_HOST_SYSTEM, "id" => "{$vcenter_fqdn}/" . $context['host']));
vro_add_parameter_in_request($parameters, 'host', VC_HOST_SYSTEM, $value);

$parameters_array['parameters'] = $parameters;

vro_execute_workflow_and_wait_for_completion(VRO_START_VM_AND_WAIT_V31, $parameters_array);

$response = prepare_json_response(ENDED, "VM started successfully.", $context, true);
echo $response;

?>
