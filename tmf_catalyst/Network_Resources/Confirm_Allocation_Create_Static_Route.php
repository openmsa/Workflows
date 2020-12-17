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
/*$mask="255.255.255.255";
$dst=$context['dst'];
$rtr=$context['rtr'];
$dev=getIdFromUbiId($rtr);
$int='GigabitEthernet0/0';
//Create static route on the router
$ms_arr=array();
$ms_arr['object_id']=$dst;
$ms_arr['mask']=$mask;
$ms_arr['gateway']=$int;
$ms_obj=array();
$cmd_obj=array("static_route" => array("$dst" => $ms_arr));
$response = execute_command_and_verify_response($dev, CMD_CREATE, $cmd_obj, "STATIC ROUTE CREATE");
*/
$context['status']="allocated";

task_success('Static Route Created');
//task_error('Task FAILED');
?>