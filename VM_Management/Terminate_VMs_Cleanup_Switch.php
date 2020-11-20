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
$dev=$context['sw'];
$dev=getIdFromUbiId($dev);
$sw_int=$context['sw_int'];
$obj_params=array();
$obj_params['object_id']=$sw_int;
$obj_params['vlan']='false';
$obj_params['description']='';
$cmd_obj=array("interface" => array("$sw_int" => $obj_params));
$response = execute_command_and_verify_response($dev, CMD_UPDATE, $cmd_obj, "Interface VLAN update");
task_success("VLAN removed from the switch interface $sw_int");
?>