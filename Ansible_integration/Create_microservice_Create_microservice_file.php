<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

//Gather variables from context
$variables_line = $context['variables_line'];
$microservice_create_line = $context['microservice_create_line'];
$microservice_name = $context['microservice_name'];
$microservice_skeleton = $context['microservice_skeleton'];
$microservice_dir = $context['microservice_dir'];

//Gather MS skeleton file path and MS skeleton file name from variable
$result = preg_match('|^(\S+?)([^/]+?\.xml)|', $microservice_skeleton, $matches);
$microservice_skeleton_path = $matches[1];
$microservice_skeleton_name = $matches[2];

//Sanitize file name
$microservice_file_name = preg_replace('/[| @()]/', '_', $microservice_name).'.xml';

//Copy MS skeleton to new file
$cp_command = '/bin/cp '.$microservice_skeleton.' '.$microservice_dir.$microservice_file_name;
$cp_command .= '; /bin/cp '.$microservice_skeleton_path.'.meta_'.$microservice_skeleton_name.' '.$microservice_dir.'.meta_'.$microservice_file_name;
$result = shell_exec($cp_command);

//Write MS name to MS file
$sed_command = '/bin/sed -i \'s@ansible_playbook_skeleton@'.$microservice_name.'@\' '.$microservice_dir.$microservice_file_name;
$result = shell_exec($sed_command);

//Write variables to MS file
$sed_command = '/bin/sed -i \'s@<variables frozen="0"></variables>@'.$variables_line.'@\' '.$microservice_dir.$microservice_file_name;
$result = shell_exec($sed_command);

//Write command to execute on CREAT step to MS file
$sed_command = '/bin/sed -i \'s@<operation></operation>@'.$microservice_create_line.'@\' '.$microservice_dir.$microservice_file_name;
$result = shell_exec($sed_command);

$context['microservice_path'] = $microservice_dir.$microservice_file_name;
  
//Looks like we have finished. COngrats!
task_success('Success. Microservice '.$microservice_file_name.'has been created successfully.');

?>