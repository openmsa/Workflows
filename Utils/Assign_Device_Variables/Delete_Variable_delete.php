<?php


require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/Common/Library/msa_common.php';


/*
The process recieves server IP and MAC address as parameters
*/
function list_args()
{
}



$device_id = $context['device_id'];
$variable_name = $context['variable_name'];
$variable_type = $context['variable_type'];
$variable_value = $context['variable_value'];

_configuration_variable_delete ($device_id, $variable_name);

task_success('The variable '.$variable_name.'(type is '.$variable_type.') with value '.$variable_value.' has been deleted from device '.$device_id.' successfully');

?>