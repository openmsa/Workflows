<?php


require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/Common/Library/msa_common.php';


/*
The process recieves server IP and MAC address as parameters
*/
function list_args()
{
  create_var_def('device_id', 'Device');
}

check_mandatory_param('device_id');

$context["me_ref"] = $context['PROCESSINSTANCEID']."-".$context['device_id'];


/*
Grab correct device_id
*/
logToFile(debug_dump($context['device_id'], 'DEBUG: DEVICE ID'));
preg_match("/\S*?(?<device_id>\d+?)$/", $context['device_id'], $matches);
$context['device_id'] = $matches['device_id'];

task_success('ME '.$context['device_id'].' selected');


?>