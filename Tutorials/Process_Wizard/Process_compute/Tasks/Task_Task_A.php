<?php
/**
 * This file is necessary to include to use all the in-built libraries of /opt/fmc_repository/Reference/Common
 */
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
/**
 * List all the parameters required by the task
 */
function list_args() {
  create_var_def('a', 'Integer');
}

/**
 * Use the keyword PAUSE to put the task in a PAUSE state, waiting for the user to click on the continue icon and optionnaly input some parameters
 */

$ret = prepare_json_response(PAUSED, 'Task pause', $context, true);
echo "$ret\n";

?>
