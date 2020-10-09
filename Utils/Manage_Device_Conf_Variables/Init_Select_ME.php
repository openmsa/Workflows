<?php


require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/Common/Library/msa_common.php';
require_once 'Common.php';

/*
The process recieves server IP and MAC address as parameters
*/
function list_args()
{
  create_var_def('device_id', 'Device');
}

check_mandatory_param('device_id');

$ubi_id = $context['device_id'];

/*
Grab correct device_id
*/
logToFile('Device ID: '.$context['device_id']);
preg_match("/\S*?(?<device_id>\d+?)$/", $context['device_id'], $matches);
$context['device_id'] = $matches['device_id'];


$device_info = json_decode(_device_read_by_id ($context['device_id']));
$device_name = $device_info->wo_newparams->name;


$context["me_ref"] = $context['SERVICEINSTANCEID']." - [".$ubi_id."] - ".$device_name  ;


task_success('ME '.$context['device_id'].' selected');

?>