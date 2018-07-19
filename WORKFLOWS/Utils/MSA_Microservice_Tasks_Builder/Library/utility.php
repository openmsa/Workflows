<?php 

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/MSA/MSA_Template_Management/Library/constants.php';

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

function create_msa_workflow_information (&$object_definition, $name, $display_field, $execute_details_visibility = 5, 
											$read_variable_visbility = 5, $show_detailed_workflow_instances = "false", 
											$show_process_exec_console = "false", $show_variables = "false", $visibility = 5, 
											$order = 10000, $group = "", $icon = "", $description = "") {
	
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

function create_msa_workflow_variable (&$variables, $name, $display_order, $type = "String",  $display_name = "", $default = "", 
										$section = "", $description = "", $max_length = 100, $start_increment = 0, $is_mandatory = "true",
										$is_userlocked = "false", $visible = "true", $editable = "false", $valid_values = array(),
										$sd_types = array(), $reference_device_id_var = "", $classes = array(), $keep_on_import = "",
										$is_grouped = "", $group_display_name = "") {
	
	$variable = $variables->addChild('variable');
	if ($default !== "") {
		$variable->addAttribute('default', $default);
	}
	if (isset($display_name)) {
		$variable->addAttribute('displayName', $display_name);
	}
	else {
		$variable->addAttribute('displayName', ucwords(str_replace('_', ' ', $name)));
	}
	$variable->addAttribute('name', "params.{$name}");
	if ($section !== "") {
		$sections = $variable->addChild('sections');
		$sections->addChild('section', $section);
	}
	$variable->addChild('description', $description);
	$variable->addAttribute('displayOrder', $display_order);
	$variable->addAttribute('maxLength', $max_length);
	$variable->addAttribute('startIncrement', $start_increment);
	$variable->addAttribute('type', $type);
	if (!empty($sd_types)) {
		$device_types = $variable->addChild('sdTypes');
		foreach ($sd_types as $sd_type) {
			$device_type = $device_types->addChild('sdType');
			$device_type->addAttribute('manId', $sd_type['man_id']);
			$device_type->addAttribute('modId', $sd_type['mon_id']);
		}
	}
	if (!empty($keep_on_import)) {
		$variable->addAttribute('keepOnImport', $keep_on_import);
	}
	if (!empty($reference_device_id_var)) {
		$variable->addAttribute('refDeviceIdVar', "params.{$reference_device_id_var}");
	}
	if (!empty($classes)) {
		$objects = $variable->addChild('classes');
		foreach ($classes as $class) {
			$object = $objects->addChild('class', $class);
		}
	}
	$variable->addAttribute('isMandatory', $is_mandatory);
	$variable->addAttribute('isUserLocked', $is_userlocked);
	$variable->addAttribute('visible', $visible);
	$variable->addAttribute('editable', $editable);
	if (!empty($valid_values)) {
		$values = $variable->addChild('values');
		foreach ($valid_values as $valid_value) {
			if (is_array($valid_value)){ // && array_key_exists('display_value', $valid_value)) {
				$value = $values->addChild('value', $valid_value['value']);
				$value->addAttribute('displayValue', $valid_value['display_value']);
			}
			else {
				$values->addChild('value', $valid_value);
			}
		}
	}
	if (!empty($is_grouped)) {
		$variable->addAttribute('isGrouped', $is_grouped);
		if ($is_grouped) {
			$variable->addAttribute('groupDisplayName', $group_display_name);
		}
	}
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
		$task->addChild('processPath', $task_params['process_path']);
		$task->addChild('displayName', $task_params['display_name']);
	}
}

function msa_template_variables_to_workflow_variables ($variables_string) {
	
	$p = xml_parser_create();
	xml_parse_into_struct($p, $variables_string, $vals);
	xml_parser_free($p);

	$variable_index = 0;
	$variable_details = array();
	for ($index = 0; $index < count($vals); $index++) {
	
		if (array_key_exists('attributes', $vals[$index])) {
	
			$attributes = $vals[$index]['attributes'];
			$name = $attributes['NAME'];
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
			$variable_details[$variable_index]['display_order'] = $variable_index;
			$variable_details[$variable_index]['type'] = $type;
			$variable_details[$variable_index]['display_name'] = $name;
			$variable_details[$variable_index]['default'] = $default;
			$variable_details[$variable_index]['max_length'] = $max_length;
			$variable_details[$variable_index]['is_mandatory'] = $is_mandatory;
			$variable_details[$variable_index]['is_userlocked'] = $is_userlocked;
			$variable_details[$variable_index]['valid_values'] = $valid_values;
			$variable_index++;
		}
	}
	return $variable_details;
}


/**
 * Create MSA Workflow from MSA Templates
 * 
 * @param unknown $template_details
 */
function create_msa_workflow_defition ($workflow_dir, $workflow_name, $workflow_display_name, $variable_details, $process_details, $group = "", 
										$display_field = "SERVICEINSTANCEREFERENCE", $visibility = 5, $execute_details_visibility = 5,
										$read_variable_visbility = 5, $show_detailed_workflow_instances = "false",
										$show_process_exec_console = "false", $show_variables = "false", $order = 10000, 
										$icon = "/images/repository/CommandDefinition/icons/web cluster.jpg", $description = "") {
	
	$xmlstr = <<<XML
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<objectDefinition/>
XML;
	$object_definition = new SimpleXMLElement($xmlstr);

	create_msa_workflow_information($object_definition, $workflow_name, $display_field, $execute_details_visibility, 
									$read_variable_visbility, $show_detailed_workflow_instances, $show_process_exec_console,
									$show_variables, $visibility, $order, $group, $icon, $description);
	
	$variables = $object_definition->addChild('variables');
	$variables->addAttribute('frozen', '0');
	
	for ($index = 0; $index < count($variable_details); $index++) {

		$name = $variable_details[$index]['name'];
		$display_order = $variable_details[$index]['display_order'];
		$type = "String";
		if (isset($variable_details[$index]['type'])) {
			$type = $variable_details[$index]['type'];	
		}
		$display_name = $name;
		if (isset($variable_details[$index]['display_name'])) {
			$display_name = $variable_details[$index]['display_name'];
		}
		$default = "";
		if (isset($variable_details[$index]['default'])) {
			$default = $variable_details[$index]['default'];
		}
		$section = "";
		if (isset($variable_details[$index]['section'])) {
			$section = $variable_details[$index]['section'];
		}
		$desctiption = "";
		if (isset($variable_details[$index]['description'])) {
			$desctiption = $variable_details[$index]['description'];
		}
		$max_length = 100;
		if (isset($variable_details[$index]['max_length'])) {
			$max_length = $variable_details[$index]['max_length'];
		}
		$start_increment = 0;
		if (isset($variable_details[$index]['start_increment'])) {
			$start_increment = $variable_details[$index]['start_increment'];
		}
		$is_mandatory = "true";
		if (isset($variable_details[$index]['is_mandatory'])) {
			$is_mandatory = $variable_details[$index]['is_mandatory'];
		}
		$is_userlocked = "false";
		if (isset($variable_details[$index]['is_userlocked'])) {
			$is_userlocked = $variable_details[$index]['is_userlocked'];
		}
		$visible = "true";
		if (isset($variable_details[$index]['visible'])) {
			$visible = $variable_details[$index]['visible'];
		}
		$editable = "false";
		if (isset($variable_details[$index]['editable'])) {
			$editable = $variable_details[$index]['editable'];
		}
		$valid_values = array();
		if (isset($variable_details[$index]['valid_values'])) {
			$valid_values = $variable_details[$index]['valid_values'];
		}
		$sd_types = array();
		if (isset($variable_details[$index]['sd_types'])) {
			$sd_types = $variable_details[$index]['sd_types'];
		}
		$reference_device_id_var = "";
		if (isset($variable_details[$index]['reference_device_id_var'])) {
			$reference_device_id_var = $variable_details[$index]['reference_device_id_var'];
		}
		$classes = array();
		if (isset($variable_details[$index]['classes'])) {
			$classes = $variable_details[$index]['classes'];
		}
		$keep_on_import = "";
		if (isset($variable_details[$index]['keep_on_import'])) {
			$keep_on_import = $variable_details[$index]['keep_on_import'];
		}
		$is_grouped = "";
		if (isset($variable_details[$index]['is_grouped'])) {
			$is_grouped = $variable_details[$index]['is_grouped'];
		}
		$group_display_name = "";
		if (isset($variable_details[$index]['group_display_name'])) {
			$group_display_name = $variable_details[$index]['group_display_name'];
		}
				
		create_msa_workflow_variable($variables, $name, $display_order, $type, $display_name, $default, $section, $desctiption, $max_length, 
									$start_increment, $is_mandatory, $is_userlocked, $visible, $editable, $valid_values, $sd_types, 
									$reference_device_id_var, $classes, $keep_on_import, $is_grouped, $group_display_name);
	}
	
	$example = $object_definition->addChild('example');
	$example->addChild('content');

	for ($index = 0; $index < count($process_details); $index++) {
		
		create_msa_workflow_process($object_definition, $process_details[$index]['name'], $process_details[$index]['icon'], 
									$process_details[$index]['visibility'], $process_details[$index]['display_name'], 
									$process_details[$index]['type'], $process_details[$index]['tasks']);
		if (!is_dir(WORKFLOWS_HOME_DIR . $process_details[$index]['name'] . "/Tasks")) {
			mkdir(WORKFLOWS_HOME_DIR . $process_details[$index]['name'] . "/Tasks", 0755, true);
		}
	}

	$workflow_file = WORKFLOWS_HOME_DIR . "{$workflow_dir}/{$workflow_name}.xml";
	$object_definition->asXML($workflow_file);
	
	shell_exec("chmod 755 {$workflow_file}");
	
	// Create MSA Workflow Meta file
	create_msa_workflow_meta_file($workflow_dir, $workflow_name);
}

/**
 * Create MSA Workflow Meta file
 * 
 * @param unknown $template_details
 */
function create_msa_workflow_meta_file ($workflow_dir, $workflow_name) {
		
	$xmlstr = <<<XML
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<metadata/>
XML;
	$metadata = new SimpleXMLElement($xmlstr);
	
	$map = $metadata->addChild('map');
	$entry = $map->addChild('entry');
	$entry->addChild('key', 'FILE_TYPE');
	$entry->addChild('value', 'text');
	$entry = $map->addChild('entry');
	$entry->addChild('key', 'DATE_MODIFICATION');
	$entry->addChild('value');
	$entry = $map->addChild('entry');
	$entry->addChild('key', 'COMMENT');
	$entry->addChild('value');
	$entry = $map->addChild('entry');
	$entry->addChild('key', 'REPOSITORY');
	$entry->addChild('value', 'CommandDefinition');
	$entry = $map->addChild('entry');
	$entry->addChild('key', 'DATE_CREATION');
	$entry->addChild('value', strtotime("now"));
	$entry = $map->addChild('entry');
	$entry->addChild('key', 'CONFIGURATION_FILTER');
	$entry->addChild('value');
	$entry = $map->addChild('entry');
	$entry->addChild('key', 'TAG');
	$entry->addChild('value', $workflow_name);
	$entry = $map->addChild('entry');
	$entry->addChild('key', 'TYPE');
	$entry->addChild('value', 'UPLOAD');
	
	$workflow_meta_file = WORKFLOWS_HOME_DIR . "{$workflow_dir}/.meta_{$workflow_name}.xml";
	$metadata->asXML($workflow_meta_file);
	
	shell_exec("chmod 755 {$workflow_meta_file}");
}

function create_json_string_from_array ($array) {
	return str_replace("\"", "\\\"", json_encode($array));
}

/**
 * Create MSA Task
 * 
 * @param unknown $template_details
 */
function create_msa_workflow_task ($task_dir, $task_name, $additional_import_files_array = array(), $parameters = array(), $additional_task_string = "", $task_success_message = "Task completed successfully.") {
	
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

		logtoFile(debug_dump($parameters, "MSA Workflow User-input Parameters for the Task $task_name\n"));
		$parameters_index = 0;
		for ($index = 0; $index < count($parameters); $index++) {

			$name = $parameters[$index]['name'];
			$type = "String";
			if (isset($parameters[$index]['type'])) {
				$type = $parameters[$index]['type'];
			}
			$mandatory = "false";
			if (isset($parameters[$index]['is_mandatory'])) {
				$mandatory = $parameters[$index]['is_mandatory'];
			}

			$task .= "\ncreate_var_def('$name', '$type');";
			if (strpos($name, ".0.") !== false) {
				$name_array = explode(".0.", $name);
				$params_name = $name_array[0];
				if ($mandatory === "true") {
					if (strpos($check_mandatory_params, "\ncheck_mandatory_param('$params_name');") === false) {
						$check_mandatory_params .= "\ncheck_mandatory_param('$params_name');";						
					}
				}
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
			else {
				if ($mandatory === "true") {
					$check_mandatory_params .= "\ncheck_mandatory_param('$name');";
				}
				$user_inputs .= "\$context['$task_name'][$parameters_index]['name'] = '$name';\n";
				$user_inputs .= "\$context['$task_name'][$parameters_index]['type'] = '$type';\n";
				$parameters_index++;
			}
		}
	}
	
	$task .= "\n}";
	if ($check_mandatory_params !== "") {
		$task .= "\n\n{$check_mandatory_params}";
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
	
	shell_exec("chmod 755 $task_file");	
}

?>