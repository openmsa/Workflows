<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args()
{
	create_var_def('workflow_customers.0.ubiqube_id', 'Customer');
}

check_mandatory_param('workflow_customers');

$msa_templates_path = $context['msa_templates_path'];
$msa_templates_path_exploded = explode("/", $msa_templates_path);
$workflow_name = "";
for ($index = 0; $index < count($msa_templates_path_exploded); $index++) {
	$workflow_name .= $msa_templates_path_exploded[$index];
	if ($index !== count($msa_templates_path_exploded) - 1) {
		$workflow_name .= "_";
	}
}
$context['workflow_name'] = $workflow_name;

$msa_templates = $context['msa_templates'];
$workflow_customers = $context['workflow_customers'];

$wo_comment = "";

$workflow_variable_details = array();
$workflow_variable_details[0]['name'] = "device_id";
$workflow_variable_details[0]['displayOrder'] = 0;
$workflow_variable_details[0]['type'] = "Device";
$workflow_variable_details[0]['displayName'] = "Device Id";
$workflow_variable_details[0]['maxLength'] = 100;
$workflow_variable_details[0]['startIncrement'] = 0;
$workflow_variable_details[0]['isMandatory'] = "true";
$workflow_variable_details[0]['isUserLocked'] = "false";
$workflow_variable_details[0]['sdTypes'] = array(array('manId' => 1, 'modId' => 104), array('manId' => 1, 'modId' => 113));

$workflow_variable_details[1]['name'] = "position";
$workflow_variable_details[1]['displayOrder'] = 1;
$workflow_variable_details[1]['type'] = "String";
$workflow_variable_details[1]['displayName'] = "Position";
$workflow_variable_details[1]['maxLength'] = 100;
$workflow_variable_details[1]['startIncrement'] = 0;
$workflow_variable_details[1]['isMandatory'] = "true";
$workflow_variable_details[1]['isUserLocked'] = "false";
$workflow_variable_details[1]['default'] = "AUTO";
$workflow_variable_details[1]['editalbe'] = "false";
$workflow_variable_details[1]['validValues'] = array("AUTO", "PRE_CONFIG", "POST_CONFIG", "PRE_CUE_CONFIG", "POST_CUE_CONFIG");
$workflow_variable_index = 2;

$process_index = 0;
$process_details = array();
$process_details[$process_index]['name'] = "MSA_Template_Workflows/{$workflow_name}/Process_create";
$process_details[$process_index]['icon'] = "";
$process_details[$process_index]['visibility'] = 4;
$process_details[$process_index]['displayName'] = "Create";
$process_details[$process_index]['type'] = CMD_CREATE;
$process_details[$process_index]['tasks'][0]['name'] = WORKFLOWS_HOME_DIR . "MSA_Template_Workflows/{$workflow_name}/Process_create/Tasks/Task_create.php";
$process_details[$process_index]['tasks'][0]['processPath'] = "";
$process_details[$process_index++]['tasks'][0]['displayName'] = "Input device";

try {
	$params = array();
	$params[0]['name'] = "device_id";
	$params[0]['type'] = "Device";
	$params[0]['isMandatory'] = "true";
	$json_string = create_json_string_from_array($context['msa_templates']);
	$additional_task_string = "\$context['msa_templates'] = json_decode(\"{$json_string}\", true);";
	create_msa_workflow_task("MSA_Template_Workflows/{$workflow_name}/Process_create/Tasks", "Task_create", array(), $params, $additional_task_string);

	//$template_variable_details = array();
	foreach ($msa_templates as $index => $element) {
	
		$uri = $element['uri'];
		$variable_details = msa_template_variables_to_workflow_variables($uri);
		for ($template_var_index = 0; $template_var_index < count($variable_details); $template_var_index++) {
			if (recursive_array_search($variable_details[$template_var_index]['name'], $workflow_variable_details) === false) {
				$workflow_variable_details[$workflow_variable_index] = $variable_details[$template_var_index];
				$workflow_variable_details[$workflow_variable_index]['displayOrder'] = $workflow_variable_index;
				$workflow_variable_index++;
			}
		}
		//$template_variable_details[$index][] = $variable_details;

		$template_paths = explode("/", $uri);
		$template_paths_count = count($template_paths);
		$template_name = $template_paths[$template_paths_count - 1];
		$template_dir = "";
		//$process_dir_name = "";
		//$process_name = "";
		for ($template_paths_index = 0; $template_paths_index < $template_paths_count - 1; $template_paths_index++) {
			$template_dir .= $template_paths[$template_paths_index];
			//$process_dir_name .= $template_paths[$template_paths_index];
			//$process_name .= $template_paths[$template_paths_index];
			if ($template_paths_index !== $template_paths_count - 2) {
				$template_dir .= "/";
				//$process_dir_name .= "_";
				//$process_name .= "|";
			}
		}
		logToFile("TEMPLATE NAME : $template_name");
		logToFile("TEMPLATE DIR : $template_dir");
		
		$process_details[$process_index]['name'] = "MSA_Template_Workflows/{$workflow_name}/Process_{$template_name}";
		$process_details[$process_index]['icon'] = "";
		$process_details[$process_index]['visibility'] = 4;
		$process_details[$process_index]['displayName'] = $template_name;
		$process_details[$process_index]['type'] = CMD_UPDATE;		
		$process_details[$process_index]['tasks'][0]['name'] = WORKFLOWS_HOME_DIR . "MSA_Template_Workflows/Common/Tasks/MSA/Task_manage_templates_attachment.php";
		$process_details[$process_index]['tasks'][0]['processPath'] = "";
		$process_details[$process_index]['tasks'][0]['displayName'] = "Detach all Templates and Attach Template {$template_name}";
		$process_details[$process_index]['tasks'][1]['name'] = WORKFLOWS_HOME_DIR . "MSA_Template_Workflows/{$workflow_name}/Process_{$template_name}/Tasks/Task_{$template_name}_input_config_vars.php";
		$process_details[$process_index]['tasks'][1]['processPath'] = "";
		$process_details[$process_index]['tasks'][1]['displayName'] = "Input Template Config variables";
		$process_details[$process_index]['tasks'][2]['name'] = WORKFLOWS_HOME_DIR . "MSA_Template_Workflows/Common/Tasks/MSA/Task_update_template_config_vars.php";
		$process_details[$process_index]['tasks'][2]['processPath'] = "";
		$process_details[$process_index]['tasks'][2]['displayName'] = "Update Template Config vars";
		$process_details[$process_index]['tasks'][3]['name'] = WORKFLOWS_HOME_DIR . "MSA_Template_Workflows/Common/Tasks/MSA/Task_msa_device_update_config.php";
		$process_details[$process_index]['tasks'][3]['processPath'] = "";
		$process_details[$process_index]['tasks'][3]['displayName'] = "Update Device Config";
		$process_details[$process_index]['tasks'][4]['name'] = WORKFLOWS_HOME_DIR . "MSA_Template_Workflows/Common/Tasks/MSA/Task_manage_templates_reattachment.php";
		$process_details[$process_index]['tasks'][4]['processPath'] = "";
		$process_details[$process_index]['tasks'][4]['displayName'] = "Attach all detached Templates";
		$process_index++;
		
		$additional_task_string = "\$context['input_vars_task_name'] = \"Task_{$template_name}_input_config_vars\";";
		create_msa_workflow_task("MSA_Template_Workflows/{$workflow_name}/Process_{$template_name}/Tasks", "Task_{$template_name}_input_config_vars", array(), $variable_details, $additional_task_string);
	}
	
	$process_details[$process_index]['name'] = "MSA_Template_Workflows/{$workflow_name}/Process_Move_To_Trash";
	$process_details[$process_index]['icon'] = "";
	$process_details[$process_index]['visibility'] = 4;
	$process_details[$process_index]['displayName'] = "Move To Trash";
	$process_details[$process_index]['type'] = CMD_DELETE;
	$process_details[$process_index]['tasks'] = array();
	
	// Create MSA Workflow definition file
	create_msa_workflow_definition("MSA_Template_Workflows/{$workflow_name}", $workflow_name, $workflow_name, $workflow_variable_details, 
									$process_details, "MSA Template Workflows", "device_id");

	$wo_comment = "Workflow {$workflow_name}.xml created successfully.\n\n";
	
	foreach ($workflow_customers as $workflow_customer) {
		$customer_ubiqube_id = $workflow_customer['ubiqube_id'];
		$response = _orchestration_service_attach($customer_ubiqube_id, "Process/MSA_Template_Workflows/{$workflow_name}/{$workflow_name}.xml");
		$response = json_decode($response, true);
		if ($response['wo_status'] !== ENDED) {
			$wo_comment .= "Workflow attachment to the customer $customer_ubiqube_id : FAIL\n";
		}
		else {
			$wo_comment .= "Workflow attachment to the customer $customer_ubiqube_id : PASS\n";
		}
	}	
}
catch (Exception $e) {
	logToFile("Exception : $e");
	$response = prepare_json_response(FAILED, "Exception occured while creating MSA Workflows from Templates.\nPlease check logs for more details.", $context, true);
	echo $response;
	exit;
}

$response = prepare_json_response(ENDED, $wo_comment, $context, true);
echo $response;

?>