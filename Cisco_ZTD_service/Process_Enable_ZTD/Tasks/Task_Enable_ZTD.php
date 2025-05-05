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
  create_var_def('enable_ztd', 'Boolean');
  create_var_def('device_id', 'Boolean');
}

check_mandatory_param('enable_ztd');
$device_id = $context['device_id'];

$ztd_flag=$context['enable_ztd'];

if($ztd_flag === 'true'){
 $cmd_line="/opt/ubi-ztd/bin/set_ztd_enabled.sh $device_id 1";
 shell_exec($cmd_line);
 $msg="ZTD enabled";
}
else{
 $cmd_line="/opt/ubi-ztd/bin/set_ztd_enabled.sh $device_id 0";
 shell_exec($cmd_line);
 $msg="ZTD disabled";
}
task_exit(ENDED, $msg);

?>