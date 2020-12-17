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
/*
//Delete the Static route
$rtr=$context['rtr'];
$dst=$context['dst'];
$dev=getIdFromUbiId($rtr);
$obj_arr=array("static_route" => array("$dst"=>array()));
$response = execute_command_and_verify_response($dev, CMD_DELETE, $obj_arr, "STATIC ROUTE DELETE");
*/
task_success('Task OK');
//task_error('Task FAILED');
?>