<?php 

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once __DIR__.'/constants.php';


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

?>