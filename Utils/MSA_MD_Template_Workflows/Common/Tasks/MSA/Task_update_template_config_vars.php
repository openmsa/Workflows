<?php
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args()
{
}
foreach ($context['devices'] as $device){
	$device_id = substr($device['device_id'], 3);
	$input_vars_task_name = $context['input_vars_task_name'];
	$template_name = $context['template_name'];

	if (array_key_exists($input_vars_task_name, $context)) {
		foreach ($context[$input_vars_task_name] as $index => $template_vars) {
			if ($template_vars['type'] === "Array") {
				foreach ($template_vars['arrayVars'] as $template_var_index => $template_var) {
					
					/*
					 * TODO : Handle arrayOfArray type variables
					 */
					
					// Currently single Array variables are handled
					// monitorInterfaces.0.interfaceName
					// monitorInterfaces.1.interfaceName
					// {"context":{"monitorInterface":[{"interfaceName":"e1", "interfaceStatus":"up"}, 
					//									{"interfaceName":"e2", "interfaceStatus":"down"}]}}
					
					$template_var_keys = explode(".0.", $template_var['name']);
					if (array_key_exists($template_var_keys[0], $context)) {
						foreach ($context[$template_var_keys[0]] as $element_index => $element) {
							foreach ($element as $key => $value) {
								if ($key === $template_var_keys[count($template_var_keys) - 1]) {
									$response = _configuration_variable_create($device_id, $template_var_keys[0] . ".{$element_index}.{$key}", $value, $template_var['type']);
									$response = json_decode($response, true);
									if ($response['wo_status'] !== ENDED) {
										$response = json_encode($response);
										echo $response;
										exit;
									}
									break;
								}
							}
						}
					}
				}
			} else {
				$response = _configuration_variable_create($device_id, $template_vars['name'], $context[$template_vars['name']], $template_vars['type']);
				$response = json_decode($response, true);
				if ($response['wo_status'] !== ENDED) {
					$response = json_encode($response);
					echo $response;
					exit;
				}
			}
		}
	}
}

$response = prepare_json_response(ENDED, "Template $template_name config vars updated successfully.", $context, true);
echo $response;

?>