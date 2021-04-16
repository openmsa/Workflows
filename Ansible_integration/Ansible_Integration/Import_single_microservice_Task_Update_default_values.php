<?php

/**
 * This file is necessary to include to use all the in-built libraries of /opt/fmc_repository/Reference/Common
 */
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/Common/Library/asset_rest.php';

$workflow_name = $context['execute_workflow'];
$response = _repository_get_workflow_definition($workflow_name);

$workflow_details = json_decode($response, True)['wo_newparams'];

logToFile(debug_dump($response, 'DEBUG: GET WORKFLOW DEFINITION'));
$value_name = explode(".", $context['microservice_file_name'])[0];
  
$result = preg_match('|^(\S+?)([^/]+?\.yml)|', $context['playbook'], $matches);
$value_display = $matches[2];
  
$new_value_array = array("displayValue"    => $value_display,
                         "displayValue_de" => "",
                         "displayValue_en" => "",
                         "displayValue_es" => "",
                         "displayValue_fr" => "",
                         "displayValue_ja" => "",
                         "actualValue"     => $value_name
                        );

foreach ($workflow_details['variables']['variable'] as $var => &$var_details) {
  if ($var_details['name'] == 'params.ansible_microservice') {
    if (!$var_details['values']) {
      $var_details['values'] = array();
    }
    array_push($var_details['values'], $new_value_array);
  }
}

$response = _repository_change_workflow_definition($workflow_name, json_encode($workflow_details));


//Clean up $context
$context['variables_line'] = '';
$context['microservice_create_line'] = '';
$context['playbook_variables'] = array();
$context['microservice_name'] = '';
task_success('Success. Deployment settings profile has been updated successfully');

?>