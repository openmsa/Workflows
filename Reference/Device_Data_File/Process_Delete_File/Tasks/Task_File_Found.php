<?php

/**
 * This file is necessary to include to use all the in-built libraries of /opt/fmc_repository/Reference/Common
 */
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

/**
 * List all the parameters required by the task
 */
function list_args()
{
  /**
   * You can use var_name convention for your variables
   * They will display automaticaly as "Var Name"
   * The allowed types are:
   *    'String', 'Boolean', 'Integer', 'Password', 'IpAddress',
   *    'IpMask', 'Ipv6Address', 'Composite', 'OBMFRef', 'Device'
   *
   * Add as many variables as needed
   */
  create_var_def('user', 'String');
  create_var_def('password', 'Password');
  create_var_def('file_to_delete', 'String');
 
}


$cmd="sshpass -p ".$context['password']." ssh -o StrictHostKeyChecking=no ".$context['user']."@".$context['device_ip']." shell ls ".$context['file_to_delete']." 2> /dev/null";



$response_cmd= shell_exec($cmd);

preg_match('#Done\s+(.*)\s+Done#',$response_cmd, $out);


if ( ! isset($out[1])) {
   $out[1] ='null';
}

$file1=$out[1];


if ($file1==$context['file_to_delete'])
{
task_exit(ENDED, "File Found");
}

else
{
task_exit(WARNING, "Error");
}


?>