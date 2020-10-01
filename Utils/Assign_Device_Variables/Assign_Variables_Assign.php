<?php


require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/Common/Library/msa_common.php';


/*
The process recieves server IP and MAC address as parameters
*/
function list_args()
{
  create_var_def('device_id', 'Device');
  create_var_def('variable_name', 'String');
  create_var_def('variable_type', 'String');
  create_var_def('variable_value', 'String');
}


check_mandatory_param('device_id');
check_mandatory_param('variable_name');
check_mandatory_param('variable_type');
check_mandatory_param('variable_value');

/*
Grab correct device_id
*/
logToFile(debug_dump($context['device_id'], 'DEBUG: DEVICE ID'));
preg_match("/\S*?(?<device_id>\d+?)$/", $context['device_id'], $matches);
$context['device_id'] = $matches['device_id'];

$device_id = $context['device_id'];
$variable_name = $context['variable_name'];
$variable_type = $context['variable_type'];
$variable_value = $context['variable_value'];

_configuration_variable_create ($device_id, $variable_name, $variable_value, $type =$variable_type, $comment = "");

task_success('The variable '.$variable_name.'(type is '.$variable_type.') with value '.$variable_value.' has been added to device '.$device_id.' successfully');

?>