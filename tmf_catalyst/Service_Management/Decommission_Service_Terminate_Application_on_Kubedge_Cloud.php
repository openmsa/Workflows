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
$kub_dev='UBI1223';
$dev=getIdFromUbiId($kub_dev);
$obj_params=array();
$obj_params['object_id']='smart-educ-deployment';

$cmd_obj=array("K8_Deployment"=>array("smart-educ-deployment" => $obj_params));
$response = execute_command_and_verify_response($dev, CMD_DELETE, $cmd_obj, "UNDEPLOY CONTAINER");
task_success('Smart Education Application Teared on the Edge Cloud');
//$context['status']='provisioned';
//task_error('Task FAILED');
?>