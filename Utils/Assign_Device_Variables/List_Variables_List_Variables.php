<?php


require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/Common/Library/msa_common.php';
require_once 'Common.php';


/*
The process recieves server IP and MAC address as parameters
*/
function list_args()
{
}

unset($context['variables']);

$device_id = $context['device_id'];

update_var_array($device_id);

task_success('The variable listed in process log file');

?>