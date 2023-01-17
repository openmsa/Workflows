<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/VMWARE/vRO/Library/REST/vmware_vro_common_rest.php';

function list_args()
{
  create_var_def('criteria', 'String');
}

$parameters = array();

$value = array("string" => array("value" => $context['criteria']));
vro_add_parameter_in_request($parameters, 'criteria', 'string', $value);

$parameters_array['parameters'] = $parameters;

vro_execute_workflow_and_wait_for_completion(VRO_GET_VMS_BY_NAME_V102, $parameters_array);

$context['vm'] = array();
$index = 0;
foreach ($context['output_parameters'][0]['value']['array']['elements'] as $element) {
	$id_full = $element['sdk-object']['id'];
	$vm_id = substr($id_full, strpos($id_full, "id:") + 3);
	$context['vm'][$index]['id'] = $vm_id;
	/**
	 * TODO : Need more info like VM name etc..?
	 */
	$index++;
}

$context['vm_count'] = $index;

task_exit(ENDED, "VM details fetched successfully.");

?>