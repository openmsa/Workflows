<?php 

require_once COMMON_DIR . 'utility.php';
require_once COMMON_DIR . 'repository_common.php';

function create_msa_micro_service_information (&$object_definition, $name, $config_type, $display_field = "object_id", $group = "Default", 
												$description = "", $visibility = 5, $order = 10000, $import_rank = 1, $max_instances = 0, 
												$dynamic = "false", $default_display = "false", $reorder_instances = "false", 
												$import_mandatory_present = "false", $import_once = "false", $create_template_id = "", 
												$create_template_object = "", $icon = "/images/eclipseIcons/page_obj.gif",
												$related_objects = array(), $sort_ascending = "true", $sort_auto = "true", 
												$sort_numerical = "true", $sort_variable = "params._order") {

	$information = $object_definition->addChild('information');
	$information->addChild('configType', $config_type);
	$information->addChild('createTemplateId', $create_template_id);
	$information->addChild('createTemplateObject', $create_template_object);
	$information->addChild('defaultDisplay', $default_display);
	$information->addChild('description', $description);
	$information->addChild('displayField', $display_field);
	$information->addChild('dynamic', $dynamic);
	$information->addChild('group', $group);
	$information->addChild('icon', $icon);
	$information->addChild('importIfMandatoryPresent', $import_if_mandatory_present);
	$information->addChild('importonce', $import_once);
	$information->addChild('importrank', $import_rank);
	$information->addChild('maxInstances', $max_instances);
	$information->addChild('name', $name);
	$information->addChild('order', $order);
	$information->addChild('visibility', $visibility);
	$information->addChild('relatedObjects', $related_objects);
	$information->addChild('reorderinstances', $reorder_instances);
	$information->addChild('sortascending', $sort_ascending);
	$information->addChild('sortauto', $sort_auto);
	$information->addChild('sortnumerical', $sort_numerical);
	$information->addChild('sortvariable', $sort_variable);
}

/**
  <command name="IMPORT">
    <operation>abc</operation>
    <parser>
      <section>
        <regexp>@^\s \s*$@</regexp>
        <regexp>@^\s \s*$@</regexp>
      </section>
      <lines>
        <ignore>
          <regexp>@^\s \s*$@</regexp>
          <regexp>@^\s \s*$@</regexp>
        </ignore>
        <line>
          <array name="default_name">
            <lines>
              <ignore>
                <regexp>@^\s \s*$@</regexp>
              </ignore>
              <line>
                <array name="default_name">
                  <mregexp>@^\s \s*$@</mregexp>
                </array>
              </line>
            </lines>
          </array>
        </line>
        <line>
          <regexp>@^\s \s*$@</regexp>
        </line>
        <line>
          <regexp>@^\s \s*$@</regexp>
        </line>
        <line>
          <array name="default_name">
            <mregexp>@^\s \s*$@</mregexp>
            <mregexp>@^\s \s*$@</mregexp>
            <regexp>@^\s \s*$@</regexp>
          </array>
        </line>
      </lines>
    </parser>
    <post_template/>
  </command>
 */

/**
  <command name="IMPORT">
    <operation>asdasd</operation>
    <xpath>asdasd</xpath>
    <parser>
      <section>
        <xpath>//asdsadas</xpath>
      </section>
      <lines>
        <line>
          <xpath>//entry</xpath>
          <regexp>@(?&lt;variable_name&gt;.*)@</regexp>
        </line>
        <line>
          <array name="default_name">
            <xpath>//entry</xpath>
            <lines>
              <line>
                <xpath>//entry</xpath>
                <regexp>@(?&lt;variable_name&gt;.*)@</regexp>
              </line>
            </lines>
          </array>
        </line>
      </lines>
    </parser>
    <post_template/>
  </command>
 */

/**
 * Create CLI based Micro service Command section
 * 
 * @param unknown $object_definition
 * @param unknown $name
 * @param unknown $operation
 * @param unknown $parser
 * @param unknown $post_template
 */
function create_msa_micro_service_command_for_cli (&$object_definition, $name, $operation, $parser = array(), $post_template = "") {

	$micro_service_command = $object_definition->addChild('command');
	$micro_service_command->addAttribute('name', $name);
	$micro_service_command->addChild('operation', htmlspecialchars($operation, ENT_XML1, 'UTF-8'));
	if ($name === CMD_IMPORT) {
		$micro_service_command->addChild('parser', $parser);
		$section = $micro_service_command->addChild('section');
		foreach ($micro_service_identifier_extractors as $micro_service_identifier_extractor) {
			$section->addChild('regexp', $micro_service_identifier_extractor);
		}
		/**
		 * TODO : Complete the IMPORT parser definition
		 */
		$micro_service_command->addChild('post_template', htmlspecialchars($post_template, ENT_XML1, 'UTF-8'));
	}
}

/**
 * Create API based Micro service Command section
 *
 * @param unknown $object_definition
 * @param unknown $name
 * @param unknown $operation
 * @param unknown $parser
 * @param unknown $post_template
 */
function create_msa_micro_service_command_for_api (&$object_definition, $name, $xpath, $operation, $rest = "", 
													$parser =  array(), $post_template = "") {

	$micro_service_command = $object_definition->addChild('command');
	$micro_service_command->addAttribute('name', $name);
	$micro_service_command->addChild('operation', htmlspecialchars($operation, ENT_XML1, 'UTF-8'));
	$micro_service_command->addChild('xpath', $xpath);
	if ($name === CMD_IMPORT) {
		$micro_service_command->addChild('parser', $parser);
		$section = $micro_service_command->addChild('section');
		foreach ($micro_service_identifier_extractors as $micro_service_identifier_extractor) {
			$section->addChild('regexp', $micro_service_identifier_extractor);
		}
		/**
		 * TODO : Complete the IMPORT parser definition
		 */
		$micro_service_command->addChild('post_template', htmlspecialchars($post_template, ENT_XML1, 'UTF-8'));
	}
	else {
		$micro_service_command->addChild('rest', $rest);
	}
}

/**
 * Create MSA micro_service from MSA Templates
 * 
 * @param unknown $micro_service_dir
 * @param unknown $micro_service_name
 * @param unknown $micro_service_display_name
 * @param unknown $config_type
 * @param unknown $variable_details
 * @param unknown $command_details
 * @param string $example_content
 * @param string $display_field
 * @param string $group
 * @param string $description
 * @param number $visibility
 * @param number $order
 * @param number $import_rank
 * @param number $max_instances
 * @param string $dynamic
 * @param string $default_display
 * @param string $reorder_instances
 * @param string $import_mandatory_present
 * @param string $import_once
 * @param string $create_template_id
 * @param string $create_template_object
 * @param string $icon
 * @param unknown $related_objects
 * @param string $sort_ascending
 * @param string $sort_auto
 * @param string $sort_numerical
 * @param string $sort_variable
 */
function create_msa_micro_service_definition ($micro_service_dir, $micro_service_name, $micro_service_display_name, $config_type,
												$variable_details, $command_details, $example_content = "",
												$display_field = "object_id", $group = "Default", 
												$description = "", $visibility = 5, $order = 10000, 
												$import_rank = 1, $max_instances = 0, $dynamic = "false", 
												$default_display = "false", $reorder_instances = "false", 
												$import_mandatory_present = "false", $import_once = "false", $create_template_id = "", 
												$create_template_object = "", $icon = "/images/eclipseIcons/page_obj.gif",
												$related_objects = array(), $sort_ascending = "true", $sort_auto = "true", 
												$sort_numerical = "true", $sort_variable = "params._order") {

	$xmlstr = <<<XML
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<ObjectDefinition/>
XML;
	$object_definition = new SimpleXMLElement($xmlstr);

	create_msa_micro_service_information($object_definition, $micro_service_display_name, $config_type, $display_field, $group, 
											$description, $visibility, $order, $import_rank, $max_instances, $dynamic, $default_display, 
											$reorder_instances, $import_mandatory_present, $import_once, $create_template_id, 
											$create_template_object, $icon, $related_objects, $sort_ascending, $sort_auto, 
											$sort_numerical, $sort_variable);

	convert_variables_array_to_xml_definition($object_definition, $variable_details);
	
	$example = $object_definition->addChild('example');
	$example->addChild('content', htmlspecialchars($example_content, ENT_XML1, 'UTF-8'));

	for ($index = 0; $index < count($command_details); $index++) {
		
		$name = $command_details[$index]['name'];
		$operation = $command_details[$index]['operation'];
		$parser = array();
		$post_template = "";
		if ($name === CMD_IMPORT) {
			$parser = $command_details[$index]['parser'];
			$post_template = $command_details[$index]['post_template'];
		}
		
		if ($config_type === "cli") {
			create_msa_micro_service_command_for_cli($object_definition, $name, $operation, $parser, $post_template);
		}
		else {
			$xpath = "";
			if (isset($command_details[$index]['xpath'])) {
				$xpath = $command_details[$index]['xpath'];
			}
			$rest = "";
			if ($name !== CMD_IMPORT) {
				$rest = $command_details[$index]['rest'];
			}
			create_msa_micro_service_command_for_api($object_definition, $name, $xpath, $operation, $rest, $parser, $post_template);
		}
	}

	if (!is_dir(micro_serviceS_HOME_DIR . $micro_service_dir)) {
		mkdir(micro_serviceS_HOME_DIR . $micro_service_dir, 0750, true);
	}

	$micro_service_file = MICRO_SERVICES_HOME_DIR . "{$micro_service_dir}/{$micro_service_name}.xml";
	$object_definition->asXML($micro_service_file);

	shell_exec("chmod 750 {$micro_service_file}");

	// Create MSA Micro Service Meta file
	create_msa_repository_meta_file(MICRO_SERVICES_HOME_DIR . "{$micro_service_dir}/.meta_{$micro_service_name}.xml",
									"CommandDefinition", "UPLOAD", $micro_service_name);
}

?>