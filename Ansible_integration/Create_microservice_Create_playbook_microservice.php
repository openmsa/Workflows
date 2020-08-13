<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

//Gather vars from context
$microservice_variables_array = $context['microservice_variables'];
$playbook_variables_array = $context['playbook_variables'];
$playbook = $context['playbook'];
$variable_skeleton = $context['variable_skeleton'];


/*
Dynamically change playbook path. 
This is required to execute playbook on Ansible host
*/
$microservice_variables_array['var_playbook_path'] = sprintf($microservice_variables_array['var_playbook_path'], $playbook);

//Create a string that contains new variables to write to MS file
$microservice_create_vars = '';
foreach ($playbook_variables_array as $var => $var_attributes) {
  $current_variable = sprintf($variable_skeleton, $var_attributes['prompt'], $var, $var_attributes['default']);
  $microservice_variables_array[$var] = $current_variable;
  $microservice_create_vars .= $var.'={$params.'.$var.'} ';
}

//Create a string that is used as command for CREAT method
$microservice_create_line = '<operation>sudo ansible-playbook {$params.playbook_path} --extra-vars "'.$microservice_create_vars.'"</operation>';
$variable_line = '  <variables frozen="0">\n';
foreach ($microservice_variables_array as $var) {
  $variable_line .= $var.'\n';
}
$variable_line .= '  </variables>\n';

//Preserve the strings for next task
$context['variables_line'] = $variable_line;
$context['microservice_create_line'] = $microservice_create_line;

//Finish the task
task_success('Success. All parameters have been prepared to create microservice dynamically');
?>