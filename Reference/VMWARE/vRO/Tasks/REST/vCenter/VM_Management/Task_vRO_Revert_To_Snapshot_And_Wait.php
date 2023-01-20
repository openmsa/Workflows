<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/VMWARE/vRO/Library/REST/vmware_vro_common_rest.php';

function list_args()
{
	create_var_def('snapshot', 'String');
	create_var_def('snapshot_revert_host', 'OBMFRef');
}

check_mandatory_param('snapshot');

$vcenter_fqdn = $context['vcenter_fqdn'];

$parameters = array();

$value = array("sdk-object" => array("type" => VC_VIRTUAL_MACHINE_SNAPSHOT, "id" => $context['snapshot']));
vro_add_parameter_in_request($parameters, 'snapshot', VC_VIRTUAL_MACHINE_SNAPSHOT, $value);

$value = array("sdk-object" => array("type" => VC_HOST_SYSTEM, "id" => "{$vcenter_fqdn}/" . $context['snapshot_revert_host']));
vro_add_parameter_in_request($parameters, 'vmhost', VC_HOST_SYSTEM, $value);

$parameters_array['parameters'] = $parameters;

vro_execute_workflow_and_wait_for_completion(VRO_REVERT_TO_SNAPSHOT_AND_WAIT_V20, $parameters_array);

$response = prepare_json_response(ENDED, "Snapshot reverted successfully to " . $context['snapshot'], $context, true);
echo $response;

?>