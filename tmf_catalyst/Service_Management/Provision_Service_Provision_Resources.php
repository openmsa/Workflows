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
$res_id=$context['res_id'];
$process_name="Process/Resources_Management/Update_Allocation";
$ubiqube_id=$context['UBIQUBEID'];
$response =_orchestration_launch_process_instance ($ubiqube_id, $res_id, $process_name, $json_body = "{}");
$response=json_decode($response,true);
if($response['wo_status'] !=='ENDED'){
  $response=json_encode($response);
  task_error($response);
}
//NW resources provisioned now, we need to take care of the container part here

task_success('Task OK');
//task_error('Task FAILED');
?>