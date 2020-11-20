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
  create_var_def('vm_num', 'String');
  create_var_def('server', 'Device');
  create_var_def('name', 'String');
  create_var_def('template', 'String');
  create_var_def('cpu', 'String');
  create_var_def('memory', 'String');
  create_var_def('host', 'String');
  create_var_def('datastore', 'String');
  create_var_def('folder', 'String');
  create_var_def('networks.0.network', 'String');
  create_var_def('networks.0.ip', 'String');
  create_var_def('networks.0.mask', 'String');
  create_var_def('networks.0.gw', 'String');
  create_var_def('networks.0.int', 'String');
}
// MSA device creation parameters
$num=$context['vm_num'];
$customer_id = $context['UBIQUBEID'];
$customer_id = getIdFromUbiId("$customer_id");
$manufacturer_id = "14020601";
$model_id = "14020601";
$login = "root";
$password = '123456';
$password_admin = '123456';
$networks=$context['networks'];
$ip_addr=$networks[0]['ip'];
$octets=explode('.',$ip_addr);
$vms=array();
//$device_ip_address = $context['networks'];
 $managed_device_name = $context['name'];

for ($i=0; $i < $num; $i++){
  $me_name = "$managed_device_name"."_"."$i";
  $device_external_reference =  $me_name;
  $fourth_oct=$octets[3]+$i;
  $device_ip_address="$octets[0].$octets[1].$octets[2].$fourth_oct";
  $response = _device_create($customer_id, $me_name, $manufacturer_id, $model_id, $login, $password, $password_admin, $device_ip_address, $device_external_reference);
  $response = json_decode($response, true);
  if ($response['wo_status'] !== ENDED) {
      $response = json_encode($response);
      echo $response;
      exit;
  }

  $device_id = $response['wo_newparams']['entity']['id'];
  $item=array();
  $item['device_id']=$device_id;
  array_push($vms,$item);
  $wo_comment = "Device ID : $device_id";
  logToFile($wo_comment);
  //Setup config variables for this ME
  $device_id=getIdFromUbiId($device_id);
  $m=0;
  foreach($networks as $item){
    if($m==0){
      $ip=$device_ip_address;
    }else{
      $ip=$item['ip'];
      $soctets=explode('.',$ip);
      $sfourth_oct=$soctets[3]+$i;
      $ip="$soctets[0].$soctets[1].$soctets[2].$sfourth_oct";
    }
    $name=$item['int'];
    $mask=$item['mask'];
    $gw=$item['gw'];
    _configuration_variable_create ($device_id, "ints.$m.ip", $ip, $type ="String", $comment = "");
    _configuration_variable_create ($device_id, "ints.$m.name", $name, $type ="String", $comment = "");
    _configuration_variable_create ($device_id, "ints.$m.gw", $gw, $type ="String", $comment = "");
    _configuration_variable_create ($device_id, "ints.$m.mask", $mask, $type ="String", $comment = "");
    $m += 1;
  }

}
//Save the list of VMs in $context
$context['vms'] = $vms;
$response = prepare_json_response(ENDED, "MSA Device/s created successfully", $context, true);
echo $response;
?>