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
$server=$context['server'];
$server=getIdFromUbiId($server);
$vms=$context['vms'];
foreach($vms as $vm){
  $ms_params=array();
  $ms_params['object_id']=$vm['vm_id'];
  $ms_params['power_state']="POWERED_OFF";
  $ms_obj=array("vm" => array($vm['vm_id'] => $ms_params));
  $response = execute_command_and_verify_response($server, CMD_DELETE, $ms_obj, "VM OFF");
}

task_success('VMs Deleted');
?>