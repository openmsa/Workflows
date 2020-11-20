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
 
  create_var_def('sw', 'Device');
  create_var_def('vlan', 'String');
}
//Import all interfaces
$vlan=$context['vlan'];
$dev=$context['sw'];
$dev=getidFromUbiId("$dev");
$res=import_objects($dev,array('vlan_to_int'));
$res=json_decode($res,true);

$obj_list=$res['wo_newparams']['vlan_to_int'];
$sw_int='';
foreach($obj_list as $objid => $obj_values){
  //Find out which interface is not associated with any vlan which we encounter first and select it
  if(empty($obj_values['vlan']) || $obj_values['vlan'] == 1){
    $sw_int=$obj_values['object_id'];
    break;
  }
}
if(empty($sw_int)){
 task_error('No Free interface available');
}
//Assign vlan 10 to the selected port using the update method
$obj_params=array();
$obj_params['object_id']=$sw_int;
$obj_params['vlan']=$vlan;
$cmd_obj=array("vlan_to_int" => array("$sw_int" => $obj_params));
$response = execute_command_and_verify_response($dev, CMD_UPDATE, $cmd_obj, "Interface VLAN update");
//$sw_int='gig0/1';
/**
 * End of the task (choose one)
 */
task_success("Switch updated with vlan $vlan for interface: $sw_int");
?>