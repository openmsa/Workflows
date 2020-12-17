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
  create_var_def('service_order_id', 'String');
  create_var_def('service_type', 'String');
//  create_var_def('region_id', 'String');
}
$service_name="Process/Resources_Management/Resources_Management";
$process_name="Process/Resources_Management/Allocate_New_Resources";
$body=array();
$body['order_id']=$context['service_order_id'];
$body['infra_order_id']=$context['ho_suborder_id'];
$body['nw_sub_order_id']=$context['vpn_suborder_id'];

$json_body=json_encode($body);
$ubiqube_id=$context['UBIQUBEID'];
$response =_orchestration_execute_service ($ubiqube_id, $service_name, $process_name, $json_body);
$response=json_decode($response,true);
if($response['wo_status'] !=='ENDED'){
  $response=json_encode($response);
  task_error($response);
}
//logToFile(debug_dump($response,"**************Response**********\n"));
$res_id=$response['wo_newparams']['serviceId']['id'];
$context['res_id']=$res_id;
sleep(10);
$resp=_orchestration_get_service_variables_by_service_id ($res_id);
$resp=json_decode($resp,true);
//logToFile(debug_dump($resp,"**************Response**********\n"));
$item=$resp['wo_newparams'];
    foreach($item as $key => $val){
  if($val['name'] === 'nw_id'){
    $network_res_id=$val['value'];
  }
  if($val['name'] === 'vlan'){
    $vlan_id=$val['value'];
  }
}
$context['vlan']=$vlan_id;
$context['nw_grp_id']=$network_res_id;
//If resource set available
$context['status']='confirmed';

//If resource set is not available
//Notify Resource Availability as negative
//task_error('No Resources available');

//Notify Resource Availability
task_success('Resources allocated and Order Confirmed');

?>