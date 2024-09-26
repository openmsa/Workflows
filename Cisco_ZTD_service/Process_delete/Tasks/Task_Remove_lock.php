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
$serialnum = $context['serialnum'];
shell_exec("rm -f /opt/ubi-ztd/var/lock/$serialnum.lock");

task_exit(ENDED, "Task OK");

?>