<?php
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args()
{}

$ret = prepare_json_response(PAUSED, 'Paused : Waiting for user action', $context);
echo "$ret\n";
?>