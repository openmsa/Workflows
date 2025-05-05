<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/VMWARE/vRO/Library/REST/vmware_vro_common_rest.php';

function list_args()
{
	create_var_def('vmName', 'String');
	create_var_def('vmGuestOs', 'String');
	create_var_def('vmFolder', 'OBMFRef');
	create_var_def('vmResourcePool', 'OBMFRef');
	create_var_def('vmHost', 'OBMFRef');
	create_var_def('vmDiskSize', 'Integer');
	create_var_def('vmMemorySize', 'Integer');
	create_var_def('vmNbOfCpus', 'Integer');
	create_var_def('vmNetwork', 'OBMFRef');
	create_var_def('vmDatastore', 'OBMFRef');
	create_var_def('diskThinProvisioned', 'Boolean');
}

check_mandatory_param('vmName');
check_mandatory_param('vmGuestOs');
check_mandatory_param('vmFolder');
check_mandatory_param('vmResourcePool');
check_mandatory_param('vmHost');
check_mandatory_param('vmDiskSize');
check_mandatory_param('vmMemorySize');
check_mandatory_param('vmNbOfCpus');
check_mandatory_param('vmNetwork');
check_mandatory_param('vmDatastore');
check_mandatory_param('diskThinProvisioned');

$vcenter_fqdn = $context['vcenter_fqdn'];

$parameters = array();

$value = array("string" => array("value" => $context['vmName']));
vro_add_parameter_in_request($parameters, 'vmName', 'string', $value);

$value = array("sdk-object" => array("type" => VC_VM_GUEST_OS, "id" => $context['vmGuestOs']));
vro_add_parameter_in_request($parameters, 'vmGuestOs', VC_VM_GUEST_OS, $value);

$value = array("sdk-object" => array("type" => VC_VM_FOLDER, "id" => "{$vcenter_fqdn}/" . $context['vmFolder']));
vro_add_parameter_in_request($parameters, 'vmFolder', VC_VM_FOLDER, $value);

$value = array("sdk-object" => array("type" => VC_RESOURCE_POOL, "id" => "{$vcenter_fqdn}/" . $context['vmResourcePool']));
vro_add_parameter_in_request($parameters, 'vmResourcePool', VC_RESOURCE_POOL, $value);

$value = array("sdk-object" => array("type" => VC_HOST_SYSTEM, "id" => "{$vcenter_fqdn}/" . $context['vmHost']));
vro_add_parameter_in_request($parameters, 'vmHost', VC_HOST_SYSTEM, $value);

$value = array("number" => array("value" => intval($context['vmDiskSize'])));
vro_add_parameter_in_request($parameters, 'vmDiskSize', 'number', $value);

$value = array("number" => array("value" => intval($context['vmMemorySize'])));
vro_add_parameter_in_request($parameters, 'vmMemorySize', 'number', $value);

$value = array("number" => array("value" => intval($context['vmNbOfCpus'])));
vro_add_parameter_in_request($parameters, 'vmNbOfCpus', 'number', $value);

$value = array("sdk-object" => array("type" => VC_NETWORK, "id" => "{$vcenter_fqdn}/" . $context['vmNetwork']));
vro_add_parameter_in_request($parameters, 'vmNetwork', VC_NETWORK, $value);

$value = array("sdk-object" => array("type" => VC_DATASTORE, "id" => "{$vcenter_fqdn}/" . $context['vmDatastore']));
vro_add_parameter_in_request($parameters, 'vmDatastore', VC_DATASTORE, $value);

$value = array("boolean" => array("value" => filter_var($context['diskThinProvisioned'], FILTER_VALIDATE_BOOLEAN)));
vro_add_parameter_in_request($parameters, 'diskThinProvisioned', 'boolean', $value);

$parameters_array['parameters'] = $parameters;

vro_execute_workflow_and_wait_for_completion(VRO_CREATE_SIMPLE_VM_V20, $parameters_array);

$id_full = $context['output_parameters'][0]['value']['sdk-object']['id'];
$context['vm'] = str_replace(",id:", "/", $id_full);
$vm_id = substr($id_full, strpos($id_full, "id:") + 3);
$context['vm_id'] = $vm_id;

$response = prepare_json_response(ENDED, "VM created successfully.\nVM Id : $vm_id", $context, true);
echo $response;

?>