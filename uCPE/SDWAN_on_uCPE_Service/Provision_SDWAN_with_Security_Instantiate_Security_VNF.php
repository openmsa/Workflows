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
  
  create_var_def('target_site', 'Device');
  create_var_def('fw_vnf_name', 'String');
}

$input_params=array();
$input_params['device_id']=$context['target_site'];
$input_params['exec_delay']='1';
$input_params['manufacturer_id']='200425';
$input_params['model_id']='200425';
$input_params['device_ip_address']='192.168.0.242';
$input_params['login']='admin';
$input_params['password']='pfsense';
$input_params['new_password']='pfsense';
$input_params['vnf_descriptor']='1d260361-950f-11ea-951d-005056b2c593';
$input_params['ucpe_devices']='1010';
$input_params['cloud_init']=' /opt/fmc_repository/Datafiles/ENEA/pfsense-nodhcp.iso';
$input_params['vnf_name']=$context['fw_vnf_name'];
$input_params['conf_profile_reference']='UBIPR240';
$input_params['nics_1_id']='lan';
$input_params['nics_1_type']='Dpdk';
$input_params['nics_1_interfacename']='svc_br';
$input_params['nics_2_id']='wan';
$input_params['nics_2_type']='Dpdk';
$input_params['nics_2_interfacename']='lan_br';
$input_params['nics_3_id']='mgmt';
$input_params['nics_3_type']='Dpdk';
$input_params['nics_3_interfacename']='svc_br';

$service_name='Process/ENEA/VNF_Management/VNF_Management';
$process_name='Process/ENEA/VNF_Management/Process_Create_new_VNF';
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
$context['fw_wf_id']=$fw_wf_id;
$response = wait_for_process_completion($fw_pid, $context);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
  task_error($response['wo_comment']);
}
$dev_resp=_orchestration_get_service_variable_by_service_id_variable_name ($fw_wf_id, 'vnf_device_id');
$dev_resp=json_decode($dev_resp,true);
$fw_me=$dev_resp['wo_newparams']['vnf_device_id'];
$context['security_me']=$fw_me;
$context['fw_wf_id']=$fw_wf_id;
task_success("SDWAN VNF Instantiated : $fw_wf_id");
//task_error('Task FAILED');
?>