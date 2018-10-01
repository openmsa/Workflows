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
  
}
sleep(40);

function pingAddress($ip) {

    $pingresult = exec("/bin/ping -c 3 $ip", $outcome, $status);
    if (0 == $status) {
        $status = "OK";
        task_exit(ENDED, "IP address, $ip, is  $status");
    } else {
        $status = "No reachable";
        task_exit(WARNING, "IP address, $ip, is  $status");
    }
   
}

$ip=$context['public_address_value'];
pingAddress($ip);

//task_exit(ENDED, $response);
//$ret = prepare_json_response(ENDED, $response, true);
?>