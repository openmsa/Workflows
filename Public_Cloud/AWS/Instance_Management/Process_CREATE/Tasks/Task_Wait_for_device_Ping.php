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

$a = ".";
for ($index = 0; $index < 5; $index++) {
    $a .= ".";
    update_asynchronous_task_details($context, "Wait for device Ping" . $a . "\nloop no : " . ($index+1));
    sleep(60);
}

task_exit(ENDED, "Task OK");

?>