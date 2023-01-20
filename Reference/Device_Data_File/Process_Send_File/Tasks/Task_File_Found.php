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
  create_var_def('src_file', 'String');
  create_var_def('dst_file', 'String');
  create_var_def('device', 'Device');
  create_var_def('user', 'String');
  create_var_def('password', 'Password');
  create_var_def('device_ip', 'IpAddress');
  
}

$cmd="ls ".$context['src_file'];

$response_cmd= shell_exec($cmd);

preg_match('#(.*)#',$response_cmd, $out);
$file1=$out[1];


if ($file1==$context['src_file'])
{
task_exit(ENDED, "File Found");
}

if (!empty($file1)) {
if (strpos('ls: cannot access',$file1) !== false) {
  task_exit(WARNING, "File does not exist");
}
}

else
{
task_exit(WARNING, "Error");
}

?>