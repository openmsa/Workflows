<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/VMWARE/vRO/Library/REST/vmware_vro_common_rest.php';

function list_args()
{
	create_var_def('folder', 'OBMFRef');
	create_var_def('path', 'String');
	create_var_def('name', 'String');
	create_var_def('asTemplate', 'Boolean');
	create_var_def('resourcePool', 'OBMFRef');
	create_var_def('host', 'OBMFRef');
}

check_mandatory_param('folder');
check_mandatory_param('path');
check_mandatory_param('asTemplate');
check_mandatory_param('resourcePool');

$vcenter_fqdn = $context['vcenter_fqdn'];

$parameters = array();

$value = array("sdk-object" => array("type" => VC_VM_FOLDER, "id" => "{$vcenter_fqdn}/" . $context['folder']));
vro_add_parameter_in_request($parameters, 'folder', VC_VM_FOLDER, $value);

$value = array("string" => array("value" => $context['path']));
vro_add_parameter_in_request($parameters, 'path', 'string', $value);

$value = array("string" => array("value" => $context['name']));
vro_add_parameter_in_request($parameters, 'name', 'string', $value);

$value = array("boolean" => array("value" => filter_var($context['asTemplate'], FILTER_VALIDATE_BOOLEAN)));
vro_add_parameter_in_request($parameters, 'asTemplate', 'boolean', $value);

$value = array("sdk-object" => array("type" => VC_RESOURCE_POOL, "id" => "{$vcenter_fqdn}/" . $context['resourcePool']));
vro_add_parameter_in_request($parameters, 'resourcePool', VC_RESOURCE_POOL, $value);

$value = array("sdk-object" => array("type" => VC_HOST_SYSTEM, "id" => "{$vcenter_fqdn}/" . $context['host']));
vro_add_parameter_in_request($parameters, 'host', VC_HOST_SYSTEM, $value);

$parameters_array['parameters'] = $parameters;

vro_execute_workflow_and_wait_for_completion(VRO_REGISTER_VM_V14, $parameters_array);

$id_full = $context['output_parameters'][0]['value']['sdk-object']['id'];
$context['registered_vm'] = str_replace(",id:", "/", $id_full);
$vm_id = substr($id_full, strpos($id_full, "id:") + 3);
$context['registered_vm_id'] = $vm_id;

$response = prepare_json_response(ENDED, "VM registered successfully.\nVM Id : $vm_id", $context, true);
echo $response;

?>