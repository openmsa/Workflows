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

$response = _configuration_variable_list ($device_id);
logToFile(debug_dump($response, "VAR LIST\n"));

task_success('The variable listed in process log file');

?>