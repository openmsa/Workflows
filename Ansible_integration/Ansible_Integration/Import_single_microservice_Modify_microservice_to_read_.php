<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

//Define variables
function list_args()
{
  create_var_def('playbook', 'OBMFRef');
  create_var_def('microservice_name', 'String');
}

check_mandatory_param('playbook');
check_mandatory_param('microservice_name');

$microservice_skeleton = $context['microservice_skeleton'];
$device_id = $context['device_id'];
$playbook = $context['playbook'];

/*$microservice_file is path to microservice that will be modified dynamically
to read a playbook file content 
*/
$microservice_file = $context['read_playbook_file'];
//The string that contain chosen playbook path
$rewrite_string = '<operation>cat '.$playbook.' ';

//Modify microservice file
$sed_command = 'sed -i \'s@<operation>cat [^ ]* @'.$rewrite_string.'@\' '.$microservice_file;
$result = shell_exec($sed_command);

//Finish task
task_success('Success. The microservice to read playbook file content has been modified.');
?>