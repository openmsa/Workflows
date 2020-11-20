<?php

/**
 * This file is necessary to include to use all the in-built libraries of /opt/fmc_repository/Reference/Common
 */
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args()
{
  
}

/*//Deleting the VM using following curl cli

$curl_str='curl -k -H "content-type: application/json" -H 'vmware-api-session-zd:f0652cf2803809287ec8fcbc466b86c8' -X DELETE 'https://10.31.1.7/rest/vcenter/vm/$contex['vm_id']';

exec_loca($curl_str);
task_success('VM Deleted');
*/
task_success('VM Deleted');
?>