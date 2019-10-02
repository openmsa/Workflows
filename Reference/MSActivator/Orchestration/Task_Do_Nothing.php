<?php
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

// List all the parameters required by the task
function list_args()
{}

// End of the task do not modify after this point
$ret = prepare_json_response(ENDED, 'OK', $context);
echo "$ret\n";
?>