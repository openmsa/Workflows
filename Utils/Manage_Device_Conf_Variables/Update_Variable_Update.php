<?php


require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/Common/Library/msa_common.php';
require_once 'Common.php';


function list_args()
{
  create_var_def('variable_name', 'String');
  create_var_def('variable_value', 'String');
}

$device_id = $context['device_id'];
$variable_name = $context['variable_name'];
$variable_value = $context['variable_value'];

_configuration_variable_delete ($device_id, $variable_name);

_configuration_variable_create ($device_id, $variable_name, $variable_value, $type = "String", $comment = "");

update_var_array($device_id);

task_success('The variable '.$variable_name.' with value '.$variable_value.' has been successfully updated and added to device '.$device_id);

?>