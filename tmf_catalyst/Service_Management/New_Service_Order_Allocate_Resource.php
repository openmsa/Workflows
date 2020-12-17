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
//This Task will create with a new Network Resource or allocate a free access infra resource
//based on the whether the request is for access line or for VPN

if(empty($context['LineId'])){
  //Begin Access line resource allocation
  $context['isVpnRequest']="No";
  $ubi_id=$context['UBIQUBEID'];
  //Find a free Access infra resource
  $response=_orchestration_list_service_instances ($ubi_id);
  $response=json_decode($response,true);
  if($response['wo_status'] !== 'ENDED'){
    logTofile("Could not list the WF instances");
  }
  $wf_list=$response['wo_newparams'];
  $available_resource='';

  foreach($wf_list as $wf){
    $service_id=$wf['id'];
    logToFile("Reading id: $service_id");
    if($wf['name'] === 'Process/Access_Infra_Resources/Access_Infra_Resources' && $wf['state'] === 'ACTIVE'){
      logToFile("Matching Reading id: $service_id");
      $resp=_orchestration_get_service_variables_by_service_id ($service_id);
      $resp=json_decode($resp,true);
      //logToFile(debug_dump($resp,"**************Response**********\n"));
      $item=$resp['wo_newparams'];
      foreach($item as $key => $val){
        if($val['name'] === 'status' && $val['value'] === 'free'){
          $available_resource=$service_id;
          foreach($item as $k =>$v){
            if($v['name'] === 'vlan'){
              $context['vlan']=$v['value'];
              break;
            }
          }
          break;
        }
      }
    }
    if($service_id === $available_resource ){
      logToFile("Found free access resource: $available_resource");
      $context['LineId']=$service_id;
      break;
    }
  }
  //Now we have found the free resource, allocate that resource
  if(empty($context['LineId'])){
    task_error('No Access infra resource available');
  }
  $res_id=$context['LineId'];
  $process_name='Process/Access_Infra_Resources/Allocate';
  $body=array();
  $body['sub_order']=$context['suborder_id'];
  $body['service_order']=$context['service_order_id'];
  //$body['port']='FastEthernet0/10';
  $json_body=json_encode($body);
  _orchestration_launch_process_instance ($ubi_id, $res_id, $process_name, $json_body);
  task_success('Infra resource found and allocated');
}
//End Access line resource allocation
else{
  $context['isVpnRequest']="Yes";
  //Begin Network Resource allocation
  //Create new network resource instance to create a static route with the network interface
  //Store the WF isntace idas VPN ID/netowrk ID
  $sub_order=$context['suborder_id'];
  $order=$context['service_order_id'];
  //$dst="192.168.".rand(2,254).".".rand(2,254);
  //$rtr="UBI1272";
  $service_name="Process/Network_Resources/Network_Resources";
  $process_name="Process/Network_Resources/Create_Network_Resource";
  $body=array();
  //$body['rtr']=$rtr;
  $body['service_order']=$order;
  $body['sub_order']=$sub_order;
  //$body['dst']=$dst;
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
  $context['nw_grp_id']=$nw_id;
  task_success("Network Resource created: $nw_id");
  //End Network resource alloaction
}



?>