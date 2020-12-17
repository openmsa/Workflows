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
//Create new network resource instance to create a static route with the network interface
//Store the WF isntace idas VPN ID/netowrk ID
$sub_order=$context['nw_sub_order_id'];
$order=$context['order_id'];
$dst="192.168.".rand(2,254).".".rand(2,254);
$rtr="UBI1272";
$service_name="Process/Network_Resources/Network_Resources";
$process_name="Process/Network_Resources/Create_Network_Resource";
$body=array();
$body['rtr']=$rtr;
$body['service_order']=$order;
$body['sub_order']=$sub_order;
$body['dst']=$dst;
$json_body=json_encode($body);
$ubiqube_id=$context['UBIQUBEID'];
$response =_orchestration_execute_service ($ubiqube_id, $service_name, $process_name, $json_body);
$response=json_decode($response,true);
if($response['wo_status'] !=='ENDED'){
  $response=json_encode($response);
  task_error($response);
}
logToFile(debug_dump($response,"**************Response**********\n"));
$nw_id=$response['wo_newparams']['serviceId']['id'];
$context['nw_id']=$nw_id;
task_success("Netowrk Resource created: $nw_id");
?>