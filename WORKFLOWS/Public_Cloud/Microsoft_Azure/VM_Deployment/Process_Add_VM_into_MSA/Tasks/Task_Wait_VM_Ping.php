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
}
$context['operation']='Add '.$context['vm_name'].' into MSA';

sleep(6);
/**
function pingAddress($ip) {
    $pingresult = exec("/bin/ping -c 3 $ip", $outcome, $status);
    if (0 == $status) {
        $status = "alive"; 
        task_exit(ENDED, "IP address, $ip, is  $status");
    } else {
        $status = "dead";
        task_exit(WARNING," IP address, $ip, is  $status");
    }
    
   // return "IP address, $ip, is  $status";
}


$ip=$context['public_address_value'];

pingAddress($ip);
**/

task_exit(ENDED, "OK");

?>