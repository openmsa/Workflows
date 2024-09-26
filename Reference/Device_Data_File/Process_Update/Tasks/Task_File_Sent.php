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

preg_match('/(?<digit>\d+)/',$context['device'],$device_id_number);
$context['device_id_number']=$device_id_number[1];
$context['cmd']="/opt/ubi-jentreprise/bin/api/device/readDeviceById.sh ".$context['device_id_number'];
$response_cmd= shell_exec($context['cmd']);
preg_match('#<ipAddress>\n<address>(.*)</address>\n<mask>#',$response_cmd, $out);
$context['device_ip']=$out[1];


// $cmd="scp ".$context['src_file']."  ".$context['user']."@".$context['device_ip'].":".$context['dst_file'];
$cmd="sshpass -p ".$context['password']." scp  -o StrictHostKeyChecking=no ".$context['src_file']."  ".$context['user']."@".$context['device_ip'].":".$context['dst_file']." 2> /dev/null";

shell_exec($cmd);



task_exit(ENDED, "OK, Check the first task in the Live Console");

?>