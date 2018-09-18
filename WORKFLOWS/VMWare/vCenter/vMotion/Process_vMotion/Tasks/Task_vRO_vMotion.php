<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/VMWARE/vRO/Library/REST/vmware_vro_common_rest.php';

function list_args()
{
	create_var_def('host', 'OBMFRef');
	create_var_def('pool', 'OBMFRef');
	#create_var_def('priority', 'String');
	#create_var_def('state', 'String');
}

check_mandatory_param('host');
check_mandatory_param('pool');

if (empty($context['vm_id'])) {

	$response = prepare_json_response(ENDED, "No VM to migrate.", $context, true);
	echo $response;
	exit;
}

$vcenter_fqdn = $context['vcenter_fqdn'];

$parameters = array();

$value = array("sdk-object" => array("type" => VC_VIRTUAL_MACHINE, "id" => $context['vm_id']));
vro_add_parameter_in_request($parameters, 'vm', VC_VIRTUAL_MACHINE, $value);

$value = array("sdk-object" => array("type" => VC_HOST_SYSTEM, "id" => "{$vcenter_fqdn}/" . $context['host']));
vro_add_parameter_in_request($parameters, 'host', VC_HOST_SYSTEM, $value);

$value = array("sdk-object" => array("type" => VC_VIRTUAL_MACHINE_MOVE_PRIORITY, "id" => "highPriority"));
vro_add_parameter_in_request($parameters, 'priority', VC_VIRTUAL_MACHINE_MOVE_PRIORITY, $value);

$value = array("sdk-object" => array("type" => VC_RESOURCE_POOL, "id" => "{$vcenter_fqdn}/" . $context['pool']));
vro_add_parameter_in_request($parameters, 'pool', VC_RESOURCE_POOL, $value);

/**
$value = array("sdk-object" => array("type" => VC_VIRTUAL_MACHINE_MOVE_PRIORITY, "id" => $context['priority']));
vro_add_parameter_in_request($parameters, 'priority', VC_VIRTUAL_MACHINE_MOVE_PRIORITY, $value);

$value = array("sdk-object" => array("type" => VC_VIRTUAL_MACHINE_POWER_STATE, "id" => $context['state']));
vro_add_parameter_in_request($parameters, 'state', VC_VIRTUAL_MACHINE_POWER_STATE, $value);
*/

$parameters_array['parameters'] = $parameters;

vro_execute_workflow_and_wait_for_completion(VRO_MIGRATE_VIRTUAL_MACHINE_WITH_VMOTION_V20, $parameters_array);

$response = prepare_json_response(ENDED, "VM migrated with vMotion successfully.", $context, true);
echo $response;

?>