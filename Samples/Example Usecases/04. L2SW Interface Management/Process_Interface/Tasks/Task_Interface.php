<?php
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/function/device_lock.php';
require_once '/opt/fmc_repository/Process/function/device_release.php';

// input start
function list_args()
{
  create_var_def('device_id', 'Device');
  create_var_def('list.0.object_id', 'Micro Service Reference');
  create_var_def('list.0.description', 'String');
  create_var_def('list.0.mode', 'String');
  create_var_def('list.0.trunk_vlan', 'String');
  create_var_def('list.0.access_vlan', 'String');
  create_var_def('list.0.shut', 'String');
  create_var_def('list.0.speed', 'String');
  create_var_def('list.0.duplex', 'String');
} 
// input end

// select device start
$PROCESSINSTANCEID = $context['PROCESSINSTANCEID'];
$EXECNUMBER = $context['EXECNUMBER'];
$TASKID = $context['TASKID'];
$process_params = array('PROCESSINSTANCEID' => $PROCESSINSTANCEID,
                                                'EXECNUMBER' => $EXECNUMBER,
                                                'TASKID' => $TASKID);

if(empty($context['list'])){
  $context['list'] = array();
}

$device_id = substr($context['device_id'],3);

$response_message = "";
$status = "";

// lock device
$lock_device = device_lock($context['device_id']);
if($lock_device === FALSE){
  $response_message = "Lock file could not open.";
  $status = "FAILED";
  $ret = prepare_json_response($status, $response_message, $context, true);
  echo "$ret\n";
  device_release($lock_device);
  exit;
}

foreach($context['list'] as $list) {

  logToFile(__FILE__ . ':' . __LINE__ . "\n" . 'CREATE ' . $list . ':param=' . debug_dump($list));

  $object_name = "cmn_interface";

  $object_id = $list['object_id'];
  $cmn_int_description = $list['description'];
  $cmn_int_mode = $list['mode'];
  $cmn_int_access_vlan = $list['access_vlan'];
  $cmn_int_trunk_vlan = $list['trunk_vlan'];
  $cmn_int_state = $list['shut'];
  $cmn_int_speed = $list['speed'];
  $cmn_int_duplex = $list['duplex'];
  $array = array();

  if($object_id == "FastEthernet0"){
      $response_message = $response_message . "Object $object_name : $object_id update failed on the device $device_id \n";
      $status = "FAILED";
      device_release($lock_device);
      exit;
  }

  $array["object_id"] = $object_id;
  $array["cmn_int_description"] = $cmn_int_description;
  $array["cmn_int_mode"] = $cmn_int_mode;
  $array["cmn_int_access_vlan"] = $cmn_int_access_vlan;
  $array["cmn_int_trunk_vlan"] = $cmn_int_trunk_vlan;
  $array["cmn_int_shut"] = $cmn_int_state;
  $array["cmn_int_speed"] = $cmn_int_speed;
  $array["cmn_int_duplex"] = $cmn_int_duplex;
  $array = array($object_name => array($object_id => $array));

  logToFile(__FILE__ . ':' . __LINE__ . "\n" . 'UPDATE ' . $object_name . ':param=' . debug_dump($array));

  if(isset($array[$object_name])){

    $response = execute_command_and_verify_response($device_id, CMD_UPDATE, $array, "UPDATE $object_name");
    $response = json_decode($response, true);
    logToFile(__FILE__ . ':' . __LINE__ . ':response=' . debug_dump($response));

    if ($response["wo_status"] == "FAIL") {
      $response_message = $response_message . "Object $object_name : $object_id update failed on the device $device_id \n";
      $status = "FAILED";
      break;
    } else {
      $response_message = $response_message . "Object $object_name : $object_id updated successfully on the device $device_id \n";
      $status = "ENDED";
    }

  } 

}

// unlock
device_release($lock_device);

$ret = prepare_json_response($status, $response_message, $context, true);
echo "$ret\n";

?>
