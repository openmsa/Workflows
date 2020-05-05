<?php

/**
 * This file is necessary to include to use all the in-built libraries of /opt/fmc_repository/Reference/Common
 */
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

/**
 * List all the parameters required by the task
 */
function list_args() {
	create_var_def ( 'devices.0.id', 'String' );
}

/**
 * End of the task do not modify after this point
 */
task_exit ( ENDED, "Task OK" );

?>