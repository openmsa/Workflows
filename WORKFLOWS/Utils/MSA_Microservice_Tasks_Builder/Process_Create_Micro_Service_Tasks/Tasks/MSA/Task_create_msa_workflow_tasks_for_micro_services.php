<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/MSA_Template_Management/Library/utility.php';

function list_args()
{
	create_var_def('msa_micro_service_path', 'String');
}

check_mandatory_param('msa_micro_service_path');

$msa_micro_service_path = $context['msa_micro_service_path'];
$msa_micro_service_path_exploded = explode("/", $msa_micro_service_path);
$msa_micro_service_name_with_xml = $msa_micro_service_path_exploded[count($msa_micro_service_path_exploded) - 1];
// addrerss.xml -> address
$msa_micro_service_name = substr($msa_micro_service_name_with_xml, 0, strlen($msa_micro_service_name_with_xml) - 4);
$msa_micro_service_dir = substr($msa_micro_service_path, 0, strlen($msa_micro_service_path) - strlen($msa_micro_service_name_with_xml));

logToFile("MICRO SERVICE PATH : $msa_micro_service_path");
logToFile("MICRO SERVICE DIR : $msa_micro_service_dir");
logToFile("MICRO SERVICE NAME : $msa_micro_service_name");

try {
	$msa_micro_service_task_variables = array();
	$msa_micro_service_task_variables[0]['name'] = "device_id";
	$msa_micro_service_task_variables[0]['type'] = "Device";
	$msa_micro_service_task_variables[0]['isMandatory'] = "true";
	
	$msa_micro_service_task_delete_variables = array();
	$msa_micro_service_task_delete_variables[0] = $msa_micro_service_task_variables[0];

	$additional_task_string = "\$device_id = substr(\$context['device_id'], 3);";
	$additional_task_string .= "\n\$object_id = \$context['object_id'];";
	$micro_service_vars_string = "\n\$micro_service_vars_array = array();";
	
	$msa_micro_service_variables = msa_micro_service_variables_to_workflow_variables($msa_micro_service_path);
	$msa_micro_service_task_variables_index = 1;
	$object_id_var_index = 1;
	foreach ($msa_micro_service_variables as $msa_micro_service_variable) {
		if (isset($msa_micro_service_variable['visible']) && $msa_micro_service_variable['visible'] === "false") {
			continue;
		}
		$msa_micro_service_task_variables[$msa_micro_service_task_variables_index] = $msa_micro_service_variable;
		$msa_micro_service_variable_name = substr($msa_micro_service_variable['name'], 7);
		$msa_micro_service_task_variables[$msa_micro_service_task_variables_index]['displayOrder'] = $msa_micro_service_task_variables_index;
		$msa_micro_service_task_variables[$msa_micro_service_task_variables_index]['name'] = $msa_micro_service_variable_name;
		if ($msa_micro_service_variable_name === "object_id") {
			$object_id_var_index = $msa_micro_service_task_variables_index;
		}
		if ($msa_micro_service_task_variables[$msa_micro_service_task_variables_index]['type'] === "ObjectRef") {
			$msa_micro_service_task_variables[$msa_micro_service_task_variables_index]['type'] = "OBMFRef";
		}
		$msa_micro_service_task_variables_index++;
			
		if (strpos($msa_micro_service_variable_name, ".0.") === false) {
			$micro_service_vars_string .= "\n\$micro_service_vars_array['{$msa_micro_service_variable_name}'] = \$context['{$msa_micro_service_variable_name}'];";
		}
		else {
			$name_array = explode(".0.", $msa_micro_service_variable_name);
			$array_variable_name = $name_array[0];
			if (strpos($micro_service_vars_string, "\n\$micro_service_vars_array['{$array_variable_name}'] = \$context['{$array_variable_name}'];") === false) {
				$micro_service_vars_string .= "\n\$micro_service_vars_array['{$array_variable_name}'] = \$context['{$array_variable_name}'];";
			}
		}
		if ($msa_micro_service_variable_name === "object_id") {
			$msa_micro_service_task_delete_variables[1] = $msa_micro_service_variable;
			$msa_micro_service_task_delete_variables[1]['name'] = $msa_micro_service_variable_name;
			$msa_micro_service_task_delete_variables[1]['type'] = "OBMFRef";
			/**
			 * TODO : Is it needed to change the displayOrder of that variable ??
			 */
		}
	}
	$micro_service_vars_string .= "\n\n\${$msa_micro_service_name} = array('{$msa_micro_service_name}' => array(\$object_id => \$micro_service_vars_array));";
	
	$micro_service_create_string = "\n\n\$response = execute_command_and_verify_response(\$device_id, CMD_CREATE, \${$msa_micro_service_name}, \"CREATE $msa_micro_service_name\");";
	$micro_service_create_string .= response_status_verifier_string();
	$success_message = "$msa_micro_service_name \$object_id created successfully on the Device \$device_id.";
	create_msa_workflow_task("{$msa_micro_service_dir}/{$msa_micro_service_name}/Tasks", "Task_Create", 
								array(), $msa_micro_service_task_variables, 
								"{$additional_task_string}{$micro_service_vars_string}{$micro_service_create_string}", false,
								$success_message);

	$micro_service_update_string = "\n\n\$response = execute_command_and_verify_response(\$device_id, CMD_UPDATE, \${$msa_micro_service_name}, \"UPDATE $msa_micro_service_name\");";
	$micro_service_update_string .= response_status_verifier_string();
	$success_message = "$msa_micro_service_name \$object_id updated successfully on the Device \$device_id.";
	$msa_micro_service_task_variables[$object_id_var_index]['type'] = "OBMFRef";
	create_msa_workflow_task("{$msa_micro_service_dir}/{$msa_micro_service_name}/Tasks", "Task_Update", 
								array(), $msa_micro_service_task_variables, 
								"{$additional_task_string}{$micro_service_vars_string}{$micro_service_update_string}", false,
								$success_message);

	$micro_service_vars_string = "\n\${$msa_micro_service_name} = array('{$msa_micro_service_name}' => \$object_id);";
	$micro_service_delete_string = "\n\n\$response = execute_command_and_verify_response(\$device_id, CMD_DELETE, \${$msa_micro_service_name}, \"DELETE $msa_micro_service_name\");";
	$micro_service_delete_string .= response_status_verifier_string();
	$success_message = "$msa_micro_service_name \$object_id deleted successfully on the Device \$device_id.";
	create_msa_workflow_task("{$msa_micro_service_dir}/{$msa_micro_service_name}/Tasks", "Task_Delete", 
								array(), $msa_micro_service_task_delete_variables, 
								"{$additional_task_string}{$micro_service_vars_string}{$micro_service_delete_string}", false,
								$success_message);
}
catch (Exception $e) {
	logToFile("Exception : $e");
}

$response = prepare_json_response(ENDED, "Workflow Tasks created succesfully for Micro Service $msa_micro_service_name", $context, true);
echo $response;

?>
