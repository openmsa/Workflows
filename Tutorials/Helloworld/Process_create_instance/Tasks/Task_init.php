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
  create_var_def('name', 'String');
}

check_mandatory_param('name');

/**
 * get the value of name from the context and create a variable out of it
 */
$name=$context['name'];
/**
 * print the value in the log file /opt/jboss/latest/log/process.log 
 */
logToFile($name);

/**
 * End of the task do not modify after this point
 */
task_exit(ENDED, "Hello " . $name);

?>
