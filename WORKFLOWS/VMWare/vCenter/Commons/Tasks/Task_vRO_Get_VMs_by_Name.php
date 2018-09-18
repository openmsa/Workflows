<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/VMWARE/vRO/Library/REST/vmware_vro_common_rest.php';

function list_args()
{
  create_var_def('vm_name', 'String');
}

if (empty($context['vm_name'])) {
	task_exit(FAILED, "Empty vm_name not allowed, since it lists all the VMs.");
}

$parameters = array();

$value = array("string" => array("value" => "^" . $context['vm_name'] . "$"));
vro_add_parameter_in_request($parameters, 'criteria', 'string', $value);

$parameters_array['parameters'] = $parameters;

vro_execute_workflow_and_wait_for_completion(VRO_GET_VMS_BY_NAME_V102, $parameters_array);

$vm_id = $context['output_parameters'][0]['value']['array']['elements'][0]['sdk-object']['id'];
$context['vm_id'] = $vm_id; 

task_exit(ENDED, "VM details fetched successfully.\nVM Id : $vm_id");

?>
