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
  create_var_def('fw_vnf_name', 'String');
}
$input_params=array();
$input_params['vnf_name']=$context['fw_vnf_name'];
$input_params['exec_delay']='1';
$input_params['action']='pass';
$input_params['target_int']='lan';
$input_params['proto']='tcp';
$input_params['source_port']='80';
$input_params['source_address']='43.3.0.0/16';
$input_params['dest_net']='lan';
$input_params['descr']='Pass network traffic';

$service_name='Process/ENEA/VNF_Management/Pfsense/Configure_Pfsense';
$process_name='Process/ENEA/VNF_Management/Pfsense/Process_Add_Firewall_Rule';
$ubiqube_id=$context['UBIQUBEID'];


$json_body=json_encode($input_params);
$response=_orchestration_execute_service ($ubiqube_id, $service_name, $process_name, $json_body);
$response=json_decode($response,true);
if($response['wo_status'] !=='ENDED'){
  $response=json_encode($response);
  task_error($response);
}
logToFile(debug_dump($response,"**************Response**********\n"));
$fw_wf_id=$response['wo_newparams']['serviceId']['id'];
$fw_pid=$response['wo_newparams']['processId']['id'];
//$context['fw_wf_id']=$fw_wf_id;
$response = wait_for_process_completion($fw_pid, $context);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
  task_error($response['wo_comment']);
}

$context['fw_prov_id']=$fw_wf_id;

task_success('Security Provisioning complete');
?>