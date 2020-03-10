<?php 

require_once COMMON_DIR . 'utility.php';
require_once COMMON_DIR . 'repository_common.php';

function create_msa_workflow_information (&$object_definition, $name, $display_field = "service_id", $execute_details_visibility = 5, 
											$read_variable_visbility = 5, $show_detailed_workflow_instances = "false", 
											$show_process_exec_console = "false", $show_variables = "false", $visibility = 5, 
											$order = 10000, $group = "", $icon = "/images/eclipseIcons/page_obj.gif", $description = "") {

	$information = $object_definition->addChild('information');
	$information->addChild('description', $description);
	$information->addChild('displayField', $display_field);
	$information->addChild('executionDetailsVisibility', $execute_details_visibility);
	$information->addChild('group', $group);
	$information->addChild('icon', $icon);
	$information->addChild('name', $name);
	$information->addChild('order', $order);
	$information->addChild('readVariableVisibility', $read_variable_visbility);
	$information->addChild('showDetailedServiceInstances', $show_detailed_workflow_instances);
	$information->addChild('showProcessExecConsole', $show_process_exec_console);
	$information->addChild('showVariables', $show_variables);
	$information->addChild('visibility', $visibility);
}

function create_msa_workflow_process (&$object_definition, $name, $icon, $visibility, $display_name, $type, $tasks = array()) {
	
	$process = $object_definition->addChild('process');
	$process->addAttribute('name', $name);
	$process->addChild('icon', $icon);
	$process->addChild('visibility', $visibility);
	$process->addChild('displayName', $display_name);
	$process->addChild('type', $type);
	foreach ($tasks as $task_params) {
		$task = $process->addChild('task');
		$task->addAttribute('name', $task_params['name']);
		$task->addChild('processPath', $task_params['processPath']);
		$task->addChild('displayName', $task_params['displayName']);
	}
}

/**
 * Create MSA Micro service variables to workflow variables
 * 
 * @param unknown $micro_service_uri
 * @return Ambigous <multitype:, unknown>
 */
function msa_micro_service_variables_to_workflow_variables ($micro_service_uri) {

	/*
	$output_array = array();
	exec("cat " . TEMPLATES_HOME_DIR . $micro_service_uri, $output_array);
	$micro_service_definition_string = "";
	for ($output_array_index = 0; $output_array_index < count($output_array); $output_array_index++) {
		$micro_service_definition_string .= $output_array[$output_array_index] . "\n";
	}
	$object_definition = new SimpleXMLElement($micro_service_definition_string);
	$micro_service_variables = $object_definition->ObjectDefinition->variables;
	*/
	
	$xml = simplexml_load_file(MICRO_SERVICES_HOME_DIR . $micro_service_uri);
	$micro_service_defition = json_decode(json_encode($xml), true);
	$variables = $micro_service_defition['variables']['variable'];
	
	$micro_service_variables = array();
	$index = 0;
	foreach ($variables as $variable) {
		foreach ($variable as $key => $value) {
			if ($key === "@attributes") {
				foreach ($value as $attribute_key => $attribute_value) {
					$micro_service_variables[$index][$attribute_key] = $attribute_value;
				}
			}
			else {
				$micro_service_variables[$index][$key] = $value;
			}
		}
		$index++;
	}
	logToFile(debug_dump($micro_service_variables, "MICRO SERVICE VARIABLES :\n"));
	return $micro_service_variables;
}

function get_variables_string_from_template ($template_uri) {

	$output_array = array();
	exec("cat " . TEMPLATES_HOME_DIR . $template_uri, $output_array);
	$variables_string = "";
	if ($output_array[0] === "{*") {
		for ($output_array_index = 1; $output_array[$output_array_index] !== "*}"; $output_array_index++) {
			$variables_string .= $output_array[$output_array_index] . "\n";
		}
	}
	return $variables_string;
}

/**
 * Create MSA Template variables to Workflow variables
 * 
 * @param unknown $template_uri
 * @return Ambigous <multitype:, multitype:NULL >
 */
function msa_template_variables_to_workflow_variables ($template_uri) {
	
	$variables_string = get_variables_string_from_template($template_uri);
	logToFile("VARIABLES STRING FROM TEMPLATE :\n$variables_string");
	
	$p = xml_parser_create();
	xml_parse_into_struct($p, $variables_string, $vals);
	xml_parser_free($p);

	$variable_index = 0;
	$variable_details = array();
	for ($index = 0; $index < count($vals); $index++) {
	
		if (array_key_exists('attributes', $vals[$index])) {
	
			$attributes = $vals[$index]['attributes'];
			$name = $attributes['NAME'];
			$display_name = "";
			$section = "";
			if (strpos($name, ".0.") !== false) {
				$name_array = explode(".0.", $name);
				$name_array_count = count($name_array);
				$display_name = $name_array[$name_array_count - 1];
				for ($name_array_index = 0; $name_array_index < ($name_array_count - 1); $name_array_index++) {
					$section .= $name_array[$name_array_index];
					if ($name_array_index !== ($name_array_count - 2)) {
						$section .= "|";
					}
				}
			}
			else {
				$display_name = $name;
			}
			$type = $attributes['TYPE'];
			$max_length = $attributes['MAXLENGTH'];
			$is_userlocked = "false";
			$is_mandatory = "true";
			if (array_key_exists('ISUSERLOCKED', $attributes)) {
				$is_userlocked = $attributes['ISUSERLOCKED'];
				$is_mandatory = "false";
			}
			$default = "";
			if (array_key_exists('DEFAULT', $attributes)) {
				$default = $attributes['DEFAULT'];
			}
			$valid_values = array();
			if ($vals[$index+1]['tag'] === "VALUES" && $vals[$index+1]['type'] === "open") {
				$index += 2;
				while($vals[$index]['tag'] !== "VALUES" || $vals[$index]['type'] !== "close") {
					if ($vals[$index]['tag'] === "VALUE" && $vals[$index]['type'] === "complete") {
						$valid_values[] = $vals[$index]['value'];
					}
					$index += 2;
				}
			}
			$variable_details[$variable_index]['name'] = $name;
			$variable_details[$variable_index]['displayOrder'] = $variable_index;
			$variable_details[$variable_index]['type'] = $type;
			$variable_details[$variable_index]['displayName'] = $display_name;
			$variable_details[$variable_index]['section'] = $section;
			$variable_details[$variable_index]['default'] = $default;
			$variable_details[$variable_index]['maxLength'] = $max_length;
			$variable_details[$variable_index]['isMandatory'] = $is_mandatory;
			$variable_details[$variable_index]['isUserLocked'] = $is_userlocked;
			$variable_details[$variable_index]['validValues'] = $valid_values;
			$variable_index++;
		}
	}
	return $variable_details;
}


/**
 * Create MSA Workflow from MSA Templates
 * 
 * @param unknown $workflow_dir
 * @param unknown $workflow_name
 * @param unknown $workflow_display_name
 * @param unknown $variable_details
 * @param unknown $process_details
 * @param string $group
 * @param string $display_field
 * @param number $visibility
 * @param number $execute_details_visibility
 * @param number $read_variable_visbility
 * @param string $show_detailed_workflow_instances
 * @param string $show_process_exec_console
 * @param string $show_variables
 * @param number $order
 * @param string $icon
 * @param string $description
 */
function create_msa_workflow_definition ($workflow_dir, $workflow_name, $workflow_display_name, $variable_details, $process_details, 
										$group = "", $display_field = "SERVICEINSTANCEREFERENCE", $visibility = 5, 
										$execute_details_visibility = 5, $read_variable_visbility = 5, 
										$show_detailed_workflow_instances = "false", $show_process_exec_console = "false", 
										$show_variables = "false", $order = 10000, 
										$icon = "/images/repository/CommandDefinition/icons/web cluster.jpg", $description = "") {
	
	$xmlstr = <<<XML
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<ObjectDefinition/>
XML;
	$object_definition = new SimpleXMLElement($xmlstr);

	create_msa_workflow_information($object_definition, $workflow_name, $display_field, $execute_details_visibility, 
									$read_variable_visbility, $show_detailed_workflow_instances, $show_process_exec_console,
									$show_variables, $visibility, $order, $group, $icon, $description);
	
	convert_variables_array_to_xml_definition($object_definition, $variable_details);
	
	$example = $object_definition->addChild('example');
	$example->addChild('content');

	for ($index = 0; $index < count($process_details); $index++) {
		
		create_msa_workflow_process($object_definition, $process_details[$index]['name'], $process_details[$index]['icon'], 
									$process_details[$index]['visibility'], $process_details[$index]['displayName'], 
									$process_details[$index]['type'], $process_details[$index]['tasks']);
		if (!is_dir(WORKFLOWS_HOME_DIR . $process_details[$index]['name'] . "/Tasks")) {
			mkdir(WORKFLOWS_HOME_DIR . $process_details[$index]['name'] . "/Tasks", 0755, true);
		}
	}

	$workflow_file = WORKFLOWS_HOME_DIR . "{$workflow_dir}/{$workflow_name}.xml";
	$object_definition->asXML($workflow_file);
	
	shell_exec("chmod 750 {$workflow_file}");
	
	// Create MSA Workflow Meta file
	create_msa_repository_meta_file(WORKFLOWS_HOME_DIR . "{$workflow_dir}/.meta_{$workflow_name}.xml", 
									"Process", "UPLOAD", $workflow_name);
}

function response_status_verifier_string () {
	
	$string = "\n\$response = json_decode(\$response, true);";
	$string .= "\nif (\$response['wo_status'] !== ENDED) {";
	$string .= "\n\t\$response = prepare_json_response(\$response['wo_status'], \$response['wo_comment'], \$context, true);";
	$string .= "\n\techo \$response;";
	$string .= "\n\texit;";
	$string .= "\n}";
	return $string;
}

/**
 * Create MSA Task
 * 
 * @param unknown $task_dir
 * @param unknown $task_name
 * @param unknown $additional_import_files_array
 * @param unknown $parameters
 * @param string $additional_task_string
 * @param string $store_params_into_task_name_context_array
 * @param string $task_success_message
 */
function create_msa_workflow_task ($task_dir, $task_name, $additional_import_files_array = array(), $parameters = array(), 
									$additional_task_string = "", $store_params_into_task_name_context_array = true, 
									$task_success_message = "Task completed successfully.") {
	
	$task = "<?php";
	$task .= "\nrequire_once '/opt/fmc_repository/Process/Reference/Common/common.php';";
	if (!empty($additional_import_files_array)) {
		foreach ($additional_import_files_array as $import_file) {
			$task .= "\nrequire_once '$import_file';";
		}
	}
	
	$task .= "\n\nfunction list_args()";
	$task .= "\n{";
	
	$check_mandatory_params = "";
	$user_inputs = "";
	if (!empty($parameters)) {

		logtoFile(debug_dump($parameters, "MSA Workflow User-input Parameters for the Task {$task_dir}/{$task_name}\n"));
		$parameters_index = 0;
		for ($index = 0; $index < count($parameters); $index++) {

			/** 
			 * Add below condition if needed
			 * 
			if (isset($parameters['visible']) && $parameters['visible'] === "false") {
				continue;
			}
			*/
			$name = $parameters[$index]['name'];
			/**
			 * Add below condition if needed
			 * 
				if (strpos($name, "params.") === 0) {
					$name = substr($name, 7);
				}
			*/
			$type = "String";
			if (isset($parameters[$index]['type'])) {
				$type = $parameters[$index]['type'];
			}
			$mandatory = "false";
			if (isset($parameters[$index]['isMandatory'])) {
				$mandatory = $parameters[$index]['isMandatory'];
			}

			$task .= "\n\tcreate_var_def('$name', '$type');";
			if (strpos($name, ".0.") !== false) {
				$name_array = explode(".0.", $name);
				$params_name = $name_array[0];
				if ($mandatory === "true") {
					if (strpos($check_mandatory_params, "\ncheck_mandatory_param('$params_name');") === false) {
						$check_mandatory_params .= "\ncheck_mandatory_param('$params_name');";						
					}
				}
				if ($store_params_into_task_name_context_array) {
					if (strpos($user_inputs, "\$context['$task_name'][$parameters_index]['name'] = '$params_name';\n") === false) {
						$user_inputs .= "\$context['$task_name'][$parameters_index]['name'] = '$params_name';\n";
						$user_inputs .= "\$context['$task_name'][$parameters_index]['type'] = 'Array';\n";
						$array_var_index = 0;
					}
					else {
						$parameters_index--;
					}
					$user_inputs .= "\$context['$task_name'][$parameters_index]['arrayVars'][$array_var_index]['name'] = '$name';\n";
					$user_inputs .= "\$context['$task_name'][$parameters_index]['arrayVars'][$array_var_index]['type'] = '$type';\n";
					$parameters_index++;
					$array_var_index++;
				}
			}
			else {
				if ($mandatory === "true") {
					$check_mandatory_params .= "\ncheck_mandatory_param('$name');";
				}
				if ($store_params_into_task_name_context_array) {
					$user_inputs .= "\$context['$task_name'][$parameters_index]['name'] = '$name';\n";
					$user_inputs .= "\$context['$task_name'][$parameters_index]['type'] = '$type';\n";
					$parameters_index++;
				}
			}
		}
	}
	
	$task .= "\n}";
	if ($check_mandatory_params !== "") {
		$task .= "\n{$check_mandatory_params}";
	}
	if ($user_inputs) {
		$task .= "\n\n{$user_inputs}";
	}
	if ($additional_task_string !== "") {
		$task .= "\n\n{$additional_task_string}";
	}
	
	$task .= "\n\n\$response = prepare_json_response(ENDED, \"$task_success_message\", \$context, true);";
	$task .= "\necho \$response;";
	$task .= "\n?>\n";

	if (!is_dir(WORKFLOWS_HOME_DIR . "{$task_dir}")) {
		mkdir(WORKFLOWS_HOME_DIR . "{$task_dir}", 0755, true);
	}
	$task_file = WORKFLOWS_HOME_DIR . "{$task_dir}/{$task_name}.php";
	if (file_exists($task_file)) {
		shell_exec("rm -f $task_file");
	}
	$fp = fopen($task_file, 'c+');
	fwrite($fp, $task);
	fclose($fp);
	
	shell_exec("chmod 750 $task_file");	
}

?>