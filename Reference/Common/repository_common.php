<?php 

/**
 * Create MSA Workflow/Micro-service VARIABLES section definition
 * 
 * @param unknown $variables
 * @param unknown $name
 * @param unknown $display_order
 * @param string $type
 * @param string $display_name
 * @param string $default
 * @param string $section
 * @param string $description
 * @param string $is_mandatory
 * @param string $is_mandatory_array
 * @param string $is_userlocked
 * @param string $visible
 * @param string $editable
 * @param unknown $valid_values
 * @param unknown $sd_types
 * @param unknown $classes
 * @param string $reference_device_id_var
 * @param string $local_var_name_match
 * @param string $remote_var_name_match
 * @param string $only_detail_view
 * @param number $start_increment
 * @param number $increment
 * @param string $selector
 * @param unknown $behaviors
 * @param number $max_length
 * @param number $cols
 * @param number $rows
 * @param string $display_type
 * @param number $display_cols
 * @param string $keep_on_import
 * @param string $array_can_add
 * @param string $array_can_edit
 * @param string $array_can_remove
 * @param string $array_can_move
 * @param string $is_searchable
 * @param string $is_unique_global
 * @param string $is_grouped
 * @param string $group_separator
 * @param string $group_display_name
 */
function create_variable_definition (&$variables, $name, $display_order, $type = "String", $display_name = "", $default = "",
									$section = "", $description = "", $is_mandatory = "true", $is_mandatory_array = "false",
									$is_userlocked = "false", $visible = "true", $editable = "false", $valid_values = array(),
									$sd_types = array(), $classes = array(), $reference_device_id_var = "", $local_var_name_match = "",
									$remote_var_name_match = "", $only_detail_view = "", $start_increment = 0, $increment = 1,
									$selector = "", $behaviors = array(), $max_length = 100, $cols = 0, $rows = 0,
									$display_type = "", $display_cols = 1, $keep_on_import = "",
									$array_can_add = "", $array_can_edit = "", $array_can_remove = "",
									$array_can_move = "", $is_searchable = "", $is_unique_global = "",
									$is_grouped = "", $group_separator = "", $group_display_name = "") {

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
	$params_name = $name;
	if (strpos($name, "params.") !== 0) {
		$params_name = "params.{$name}";
	}
	$variable->addAttribute('name', $params_name);
	/**
	 * TODO : Check if <sections> recursion is allowed. If yes, implement and test.
	*/
	if ($section !== "") {
		$sections = $variable->addChild('sections');
		$sections->addChild('section', $section);
	}
	$variable->addChild('description', $description);
	$variable->addAttribute('type', $type);
	$variable->addAttribute('displayOrder', $display_order);
	$variable->addAttribute('maxLength', $max_length);
	$variable->addAttribute('startIncrement', $start_increment);
	$variable->addAttribute('isMandatory', $is_mandatory);
	$variable->addAttribute('isMandatoryArray', $is_mandatory_array);
	$variable->addAttribute('isUserLocked', $is_userlocked);
	$variable->addAttribute('visible', $visible);
	$variable->addAttribute('editable', $editable);
	if (!empty($valid_values)) {
		$values = $variable->addChild('values');
		foreach ($valid_values as $valid_value) {
			if (is_array($valid_value)){ // && array_key_exists('displayValue', $valid_value)) {
				$value = $values->addChild('value', $valid_value['value']);
				$value->addAttribute('displayValue', $valid_value['displayValue']);
			}
			else {
				$values->addChild('value', $valid_value);
			}
		}
	}

	if (!empty($only_detail_view)) {
		$variable->addttribute('onlyDetailView', $only_detail_view);
	}
	if (!empty($keep_on_import)) {
		$variable->addAttribute('keepOnImport', $keep_on_import);
	}
	if ($cols !== 0) {
		$variable->addAttribute('cols', $cols);
	}
	if ($rows !== 0) {
		$variable->addAttribute('rows', $rows);
	}
	if (!empty($display_type)) {
		$variable->addAttribute('displayType', $display_type);
		if ($display_type === "alt") {
			$variable->addAttribute('displayCols', $display_cols);
		}
	}
	if (!empty($array_can_add)) {
		$variable->addAttribute('arrayCanAdd', $array_can_add);
	}
	if (!empty($array_can_edit)) {
		$variable->addAttribute('arrayCanEdit', $array_can_edit);
	}
	if (!empty($array_can_remove)) {
		$variable->addAttribute('arrayCanRemove', $array_can_remove);
	}
	if (!empty($array_can_move)) {
		$variable->addAttribute('arrayCanMove', $array_can_move);
	}
	if (!empty($is_searchable)) {
		$variable->addAttribute('isSearchable', $is_searchable);
	}

	switch ($type) {
		case "AutoIncrement":
			$variable->addAttribute('increment', $increment);
			if ($is_unique_global === "") {
				$is_unique_global = "true";
			}
			$variable->addAttribute('isUniqueGlobal', $is_unique_global);
			if (!empty($classes)) {
				$objects = $variable->addChild('classes');
				foreach ($classes as $class) {
					$object = $objects->addChild('class', $class);
				}
			}
			break;
		case "Composite":
			if (!empty($selector)) {
				if (strpos($selector, "params.") !== 0) {
					$selector = "params.{$selector}";
				}
				$variable->addAttribute('selector', $selector);
			}
				
			/**
			 * TODO :
			 * 1] Test one-level "Composite" variables.
			 * 2] Implement behaviors recursion and test.
			 */
			if (!empty($behaviors)) {
				$composite_behaviors = $variable->addChild('behaviors');
				foreach ($behaviors as $behavior) {
					$composite_behavior = $composite_behaviors->addChild('behavior', $behavior);
					foreach ($behavior as $behavior_attribute) {
						$composite_behavior->addAttribute("$behavior_attribute", $behavior[$behavior_attribute]);
					}
				}
			}
			break;
		case "OBMFRef":
		case "ObjectRef":
			if (!empty($reference_device_id_var)) {
				if (strpos($reference_device_id_var, "params.") !== 0) {
					$reference_device_id_var = "params.{$reference_device_id_var}";
				}
				$variable->addAttribute('refDeviceIdVar', $reference_device_id_var);
			}
			if (!empty($local_var_name_match)) {
				$variable->addAttribute('localVarNameMatch', $local_var_name_match);
			}
			if (!empty($remote_var_name_match)) {
				$variable->addAttribute('remoteVarNameMatch', $remote_var_name_match);
			}
			if (!empty($classes)) {
				$objects = $variable->addChild('classes');
				foreach ($classes as $class) {
					$object = $objects->addChild('class', $class);
				}
			}
			break;
		case "Device":
			if (!empty($sd_types)) {
				$device_types = $variable->addChild('sdTypes');
				foreach ($sd_types as $sd_type) {
					$device_type = $device_types->addChild('sdType');
					$device_type->addAttribute('manId', $sd_type['manId']);
					$device_type->addAttribute('modId', $sd_type['modId']);
				}
			}
			break;
	}

	if (!empty($is_grouped)) {
		$variable->addAttribute('isGrouped', $is_grouped);
		if ($is_grouped) {
			$variable->addAttribute('groupSeparator', $group_separator);
			$variable->addAttribute('groupDisplayName', $group_display_name);
		}
	}
}

function convert_variables_array_to_xml_definition (&$object_definition, $variable_details) {

	$variables = $object_definition->addChild('variables');
	$variables->addAttribute('frozen', '0');
	
	for ($index = 0; $index < count($variable_details); $index++) {
	
		$name = $variable_details[$index]['name'];
		$display_order = $variable_details[$index]['displayOrder'];
		$type = "String";
		if (isset($variable_details[$index]['type'])) {
			$type = $variable_details[$index]['type'];
		}
		$display_name = $name;
		if (isset($variable_details[$index]['displayName'])) {
			$display_name = $variable_details[$index]['displayName'];
		}
		$default = "";
		if (isset($variable_details[$index]['default'])) {
			$default = $variable_details[$index]['default'];
		}
		$section = "";
		if (isset($variable_details[$index]['section'])) {
			$section = $variable_details[$index]['section'];
		}
		$description = "";
		if (isset($variable_details[$index]['description'])) {
			$description = $variable_details[$index]['description'];
		}
		$is_mandatory = "true";
		if (isset($variable_details[$index]['isMandatory'])) {
			$is_mandatory = $variable_details[$index]['isMandatory'];
		}
		$is_mandatory_array = "false";
		if (isset($variable_details[$index]['isMandatoryArray'])) {
			$is_mandatory_array = $variable_details[$index]['isMandatoryArray'];
		}
		$is_userlocked = "false";
		if (isset($variable_details[$index]['isUserLocked'])) {
			$is_userlocked = $variable_details[$index]['isUserLocked'];
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
		if (isset($variable_details[$index]['validValues'])) {
			$valid_values = $variable_details[$index]['validValues'];
		}
		$sd_types = array();
		if (isset($variable_details[$index]['sdTypes'])) {
			$sd_types = $variable_details[$index]['sdTypes'];
		}
		$classes = array();
		if (isset($variable_details[$index]['classes'])) {
			$classes = $variable_details[$index]['classes'];
		}
		$reference_device_id_var = "";
		if (isset($variable_details[$index]['refDeviceIdVar'])) {
			$reference_device_id_var = $variable_details[$index]['refDeviceIdVar'];
		}
		$local_var_name_match = "";
		if (isset($variable_details[$index]['refDeviceIdVar'])) {
			$local_var_name_match = $variable_details[$index]['refDeviceIdVar'];
		}
		$remote_var_name_match = "";
		if (isset($variable_details[$index]['refDeviceIdVar'])) {
			$remote_var_name_match = $variable_details[$index]['refDeviceIdVar'];
		}
		$only_detail_view = "";
		if (isset($variable_details[$index]['editable'])) {
			$only_detail_view = $variable_details[$index]['editable'];
		}
		$start_increment = 0;
		if (isset($variable_details[$index]['startIncrement'])) {
			$start_increment = $variable_details[$index]['startIncrement'];
		}
		$increment = 1;
		if (isset($variable_details[$index]['increment'])) {
			$increment = $variable_details[$index]['increment'];
		}
		$selector = "";
		if (isset($variable_details[$index]['selector'])) {
			$selector = $variable_details[$index]['selector'];
		}
		$behaviors = array();
		if (isset($variable_details[$index]['classes'])) {
			$behaviors = $variable_details[$index]['classes'];
		}
		$max_length = 100;
		if (isset($variable_details[$index]['maxLength'])) {
			$max_length = $variable_details[$index]['maxLength'];
		}
		$cols = 0;
		if (isset($variable_details[$index]['cols'])) {
			$cols = $variable_details[$index]['cols'];
		}
		$rows = 0;
		if (isset($variable_details[$index]['rows'])) {
			$rows = $variable_details[$index]['rows'];
		}
		$display_type = "";
		if (isset($variable_details[$index]['displayType'])) {
			$display_type = $variable_details[$index]['displayType'];
		}
		$display_cols = 1;
		if (isset($variable_details[$index]['displayCols'])) {
			$display_cols = $variable_details[$index]['displayCols'];
		}
		$keep_on_import = "";
		if (isset($variable_details[$index]['keepOnImport'])) {
			$keep_on_import = $variable_details[$index]['keepOnImport'];
		}
		$array_can_add = "";
		if (isset($variable_details[$index]['arrayCanAdd'])) {
			$array_can_add = $variable_details[$index]['arrayCanAdd'];
		}
		$array_can_edit = "";
		if (isset($variable_details[$index]['arrayCanEdit'])) {
			$array_can_edit = $variable_details[$index]['arrayCanEdit'];
		}
		$array_can_remove = "";
		if (isset($variable_details[$index]['arrayCanRemove'])) {
			$array_can_remove = $variable_details[$index]['arrayCanRemove'];
		}
		$array_can_move = "";
		if (isset($variable_details[$index]['arrayCanMove'])) {
			$array_can_move = $variable_details[$index]['arrayCanMove'];
		}
		$is_searchable = "";
		if (isset($variable_details[$index]['isSearchable'])) {
			$is_searchable = $variable_details[$index]['isSearchable'];
		}
		$is_unique_global = "";
		if (isset($variable_details[$index]['isUniqueGlobal'])) {
			$is_unique_global = $variable_details[$index]['isUniqueGlobal'];
		}
		$is_grouped = "";
		if (isset($variable_details[$index]['isGrouped'])) {
			$is_grouped = $variable_details[$index]['isGrouped'];
		}
		$group_separator = "";
		if (isset($variable_details[$index]['groupSeparator'])) {
			$group_separator = $variable_details[$index]['groupSeparator'];
		}
		$group_display_name = "";
		if (isset($variable_details[$index]['groupDisplayName'])) {
			$group_display_name = $variable_details[$index]['groupDisplayName'];
		}
	
		create_variable_definition($variables, $name, $display_order, $type, $display_name, $default, $section, $description,
									$is_mandatory, $is_mandatory_array, $is_userlocked, $visible, $editable, $valid_values,
									$sd_types, $classes, $reference_device_id_var, $local_var_name_match,
									$remote_var_name_match, $only_detail_view, $start_increment, $increment,
									$selector, $behaviors, $max_length, $cols, $rows, $display_type, $display_cols,
									$keep_on_import, $array_can_add, $array_can_edit, $array_can_remove,
									$array_can_move, $is_searchable, $is_unique_global,
									$is_grouped, $group_separator, $group_display_name);
	}
}

/**
 * Create MSA repository Meta file
 *
 * @param unknown $dir
 * @param unknown $name
 * @param unknown $repository
 * @param string $type
 * @param string $file_type
 * @param string $tag
 * @param string $comment
 * @param string $model
 * @param string $manufacturer
 * @param string $configuration_filter
 */
function create_msa_repository_meta_file ($meta_file, $repository, $type = "UPLOAD", $tag = "", $comment = "", 
											$model = "", $manufacturer = "", $file_type = "text", $configuration_filter = "") {

	$xmlstr = <<<XML
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<metadata/>
XML;
	$metadata = new SimpleXMLElement($xmlstr);

	$map = $metadata->addChild('map');
	if (isset($model)) {
		$entry = $map->addChild('entry');
		$entry->addChild('key', 'MODEL');
		$entry->addChild('value', $model);
	}
	if (isset($manufacturer)) {
		$entry = $map->addChild('entry');
		$entry->addChild('key', 'MANUFACTURER');
		$entry->addChild('value', $manufacturer);
	}
	$entry->addChild('key', 'FILE_TYPE');
	$entry->addChild('value', $file_type);
	$entry = $map->addChild('entry');
	$entry->addChild('key', 'DATE_MODIFICATION');
	$entry->addChild('value');
	$entry = $map->addChild('entry');
	$entry->addChild('key', 'COMMENT');
	$entry->addChild('value', $comment);
	$entry = $map->addChild('entry');
	$entry->addChild('key', 'REPOSITORY');
	$entry->addChild('value', $repository);
	$entry = $map->addChild('entry');
	$entry->addChild('key', 'DATE_CREATION');
	$entry->addChild('value', strtotime("now"));
	$entry = $map->addChild('entry');
	$entry->addChild('key', 'CONFIGURATION_FILTER');
	$entry->addChild('value', $configuration_filter);
	$entry = $map->addChild('entry');
	$entry->addChild('key', 'TAG');
	$entry->addChild('value', $tag);
	$entry = $map->addChild('entry');
	$entry->addChild('key', 'TYPE');
	$entry->addChild('value', $type);

	$metadata->asXML($meta_file);

	shell_exec("chmod 750 {$meta_file}");
}

?>
