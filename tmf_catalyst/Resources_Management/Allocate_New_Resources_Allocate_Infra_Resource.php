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
    $context['al_id']=$service_id;
    break;
  }
}
//Now we have found the free resource, allocate that resource
if(empty($context['al_id'])){
  task_error('No Access infra resource available');
}
$res_id=$context['al_id'];
$process_name='Process/Access_Infra_Resources/Allocate';
$body=array();
$body['sub_order']=$context['infra_order_id'];
$body['service_order']=$context['order_id'];
$body['port']='FastEthernet0/10';
$json_body=json_encode($body);
 _orchestration_launch_process_instance ($ubi_id, $res_id, $process_name, $json_body);
task_success('Infra resource found and allocated');
?>