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
  create_var_def('sdwan_vnf_name', 'String');
}

$input_params=array();
$input_params['name']=$context['sdwan_vnf_name'];
$input_params['exec_delay']='1';
$input_params['defaultRoute']='192.168.0.10';
$input_params['isApproved']='true';
$input_params['destination_network']='48.0.0.3/16';
$input_params['gateway_ip']='192.168.0.10';
$input_params['device_id']='UBI633';


$service_name='Process/ENEA/VNF_Management/Flexiwan/Configure_Flexiwan';
$process_name='Process/ENEA/VNF_Management/Flexiwan/Process_Setup_Flexiwan';
$ubiqube_id=$context['UBIQUBEID'];


$json_body=json_encode($input_params);
$response=_orchestration_execute_service ($ubiqube_id, $service_name, $process_name, $json_body);
$response=json_decode($response,true);
if($response['wo_status'] !=='ENDED'){
  $response=json_encode($response);
  task_error($response);
}
logToFile(debug_dump($response,"**************Response**********\n"));
$sdwan_wf_id=$response['wo_newparams']['serviceId']['id'];
$sdwan_pid=$response['wo_newparams']['processId']['id'];
//$context['sdwan_wf_id']=$sdwan_wf_id;
$response = wait_for_process_completion($sdwan_pid, $context);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
  task_error($response['wo_comment']);
}

$context['sdwan_prov_id']=$sdwan_wf_id;

task_success('SDWAN Provisioning complete');
?>