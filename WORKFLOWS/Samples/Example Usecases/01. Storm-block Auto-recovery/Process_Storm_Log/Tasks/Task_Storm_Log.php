<?php
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/function/device_lock.php';
require_once '/opt/fmc_repository/Process/function/same_port_lock.php';
require_once '/opt/fmc_repository/Process/function/device_release.php';
require_once '/opt/fmc_repository/Process/function/port_replace.php';
require '/opt/fmc_repository/Process/function/config.php';

function list_args()
{
  create_var_def('device_id', 'Device');
  create_var_def('date', 'String');
}

// input end

// select device start
$PROCESSINSTANCEID = $context['PROCESSINSTANCEID'];
$EXECNUMBER = $context['EXECNUMBER'];
$TASKID = $context['TASKID'];
$process_params = array('PROCESSINSTANCEID' => $PROCESSINSTANCEID,
                                                'EXECNUMBER' => $EXECNUMBER,
                                                'TASKID' => $TASKID);
if($sleep_time > 0){
  logToFile(__FILE__ . ':' . __LINE__ . "\n" . 'sleeping ' . $sleep_time . " seconds.\n");
}

sleep($sleep_time);

$HTTP_HOST = get_vars_value(WEB_NODE_PRIV_IP);
$HTTP_PORT = get_vars_value(WEB_NODE_HTTP_PORT);
$USERNAME = "ncroot";
$hash = get_vars_value(NCROOT_PASSWORD_VARIABLE);
$script = "/opt/configurator/script/encp.sh ".$hash; 
$NCROOT_PASSWORD = exec($script);

$device_id = substr($context['device_id'],3);
// select device end

$date = $context['date'];
// data prepare end

$url = "http://localhost:9200/ubilogs-*/_search";

// JSON query
$request_json = '{"query":
{ "bool": {
      "filter": [
        {
          "term": {
            "date": "' . $date . '"
          }
        },
        {
          "term": {
            "device_id": "' . $context['device_id'] . '"
          }
        }
      ]
    }
  },
  "_source" : [ "date", "rawlog" ,"rule" ]
}';

logToFile(__FILE__ . ':' . __LINE__ . "\n" . 'DEBUG: ' . $request_json . "\n");

// curl access start
$curl_obj = curl_init();
curl_setopt($curl_obj, CURLOPT_URL, $url);
curl_setopt($curl_obj, CURLOPT_RETURNTRANSFER, 1);
curl_setopt($curl_obj, CURLOPT_POST, 1);
curl_setopt($curl_obj, CURLOPT_POSTFIELDS, $request_json);
$response_json = curl_exec($curl_obj);
curl_close($curl_obj);
// curl end

$elastic_response = json_decode($response_json, true);

logToFile(__FILE__ . ':' . __LINE__ . "\n" . 'DEBUG: ' . debug_dump($elastic_response) . "\n");

// get device information start
$url2 = "http://$HTTP_HOST:$HTTP_PORT/ubi-api-rest/device/id/$device_id";

// curl access start
$curl_obj2 = curl_init();
curl_setopt($curl_obj2, CURLOPT_URL, $url2);
curl_setopt($curl_obj2, CURLOPT_USERPWD, "$USERNAME:$NCROOT_PASSWORD");
curl_setopt($curl_obj2, CURLOPT_RETURNTRANSFER, 1);
curl_setopt($curl_obj2, CURLOPT_HTTPGET, 1);
$response_json2 = curl_exec($curl_obj2);
curl_close($curl_obj2);
// curl end

$device_response = json_decode($response_json2, true);
logToFile(__FILE__ . ':' . __LINE__ . "\n" . 'Lookup_response: ' . debug_dump($device_response)  . "\n");

$device_name = $device_response["name"];
// get device information end


// Create Int List ($date => $ip)
$int_list = array();
$down_int = "";

if(!empty($elastic_response['hits']['hits'])){
  foreach($elastic_response['hits']['hits'] as $key => $value){
    $rawlog = $value['_source']['rawlog'];
    $matches = array();
    logToFile(__FILE__ . ':' . __LINE__ . "\n" . 'DEBUG: ' . $rawlog . "\n");
    preg_match('/.*putting (?P<down_int>\S+) in .*/', $rawlog, $matches);
    if(isset($matches['down_int'])){
      $down_int = $matches['down_int'];
      $int_list[$down_int] = $down_int;
    } else {
      continue;
    }
  }
}
// Create Int List end

logToFile(__FILE__ . ':' . __LINE__ . "\n" . 'DEBUG: ' . debug_dump($int_list) . "\n");

$response_message = "";
$status = "";
$object_id = "";

$loop_count = 0;
$error_list = array();

// lock device
$lock_device = device_lock($context['device_id']);
if($lock_device === FALSE){
  $response_message = "Lock file could not open.";
  $status = "FAILED";
  $ret = prepare_json_response($status, $response_message, $context, true);
  echo "$ret\n";
  exit;
}

$object_name = "cmn_interface";
$import_list = array($object_name);
// Import
$response_json = import_objects($device_id, $import_list);
$import_response = json_decode($response_json, true);

logToFile(__FILE__ . ':' . __LINE__ . "\n" . 'DEBUG: ' . debug_dump($import_response)  . "\n");

if ($import_response['wo_status'] !== "ENDED") {
  $wo_comment = "IMPORT of the $object_name failed. Hence ending the process as a failure.\n";
  $response = prepare_json_response(FAILED, $wo_comment, $context, true);
  echo $response;
  exit;
}

$int_array = array();

foreach($int_list as $v){
  $interface = port_replace($v, $import_response['wo_newparams'][$object_name]);
  if(!empty($interface)){
    $int_array[$interface] = $interface;
  }
}

logToFile(__FILE__ . ':' . __LINE__ . "\n" . 'DEBUG: ' . debug_dump($int_array)  . "\n");

foreach($int_array as $list){
  $object_id = $list;

  $lock_port = same_port_lock($object_id, $date, $context['device_id']);
  
  logToFile(__FILE__ . ':' . __LINE__ . "\n" . 'Lock Port: ' . $lock_port . "\n");
  
  if(!empty($lock_port)){
    continue;
  }
  
  $device_info = array();
  $device_info = $import_response['wo_newparams'][$object_name];
  logTofile(debug_dump($device_info, "device_info"));
  
  $description = $device_info[$object_id]['cmn_int_description'];
  $mode = $device_info[$object_id]['cmn_int_mode'];
  if(!empty($device_info[$object_id]['cmn_int_access_vlan'])){
    $access_vlan = $device_info[$object_id]['cmn_int_access_vlan'];
  }
  $trunk_vlan = $device_info[$object_id]['cmn_int_trunk_vlan'];
  $state = $device_info[$object_id]['cmn_int_shut'];
  $speed = $device_info[$object_id]['cmn_int_speed'];
  $duplex = $device_info[$object_id]['cmn_int_duplex'];

  $context['list'][$loop_count]['before_object_id'] = $object_id;
  $context['list'][$loop_count]['before_description'] = $description;
  $context['list'][$loop_count]['before_state'] = $state;

  $object_array = array(); 

  $array_item = array();
  $array_item["object_id"] = $object_id;
  $array_item["cmn_int_description"] = "Error:".$description;
  $array_item["cmn_int_mode"] = $mode;
  if(isset($access_vlan)){
    $array_item["cmn_int_access_vlan"] = $access_vlan;
  }
  $array_item["cmn_int_trunk_vlan"] = $trunk_vlan;
  $array_item["cmn_int_shut"] = "shutdown";
  $array_item["cmn_int_speed"] = $speed;
  $array_item["cmn_int_duplex"] = $duplex;
  $object_array[$object_id] = $array_item;

  $array = array($object_name => $object_array);

  logToFile(__FILE__ . ':' . __LINE__ . "\n" . 'UPDATE ' . $object_name . ':param=' . debug_dump($array));

  // Update
  $response = execute_command_and_verify_response($device_id, CMD_UPDATE, $array, "UPDATE $object_name");
  $response = json_decode($response, true);
  logToFile(__FILE__ . ':' . __LINE__ . ':response=' . debug_dump($response));

  if($response["wo_status"] == "FAIL"){
    $response_message = $response_message . "Object $object_name : Port $object_id was not automatically re-opened on the device " . $device_name . "\n";
    $loop_count++;
    $error_list[$object_id] = $object_id;
    continue;
  }

  // Import
  $response = execute_command_and_verify_response($device_id, CMD_IMPORT, $array, "IMPORT $object_name : $object_id");
  $response = json_decode($response, true);
  
  logToFile(__FILE__ . ':' . __LINE__ . ':response=' . debug_dump($response));
  
  $recover_device_info = $response['wo_newparams'][$object_name];
  logTofile(debug_dump($recover_device_info, "device_info"));

  $context['list2'][$loop_count]['after_object_id'] = $recover_device_info[$object_id]['object_id'];
  $context['list2'][$loop_count]['after_description'] = $recover_device_info[$object_id]['cmn_int_description'];
  $context['list2'][$loop_count]['after_state'] = $recover_device_info[$object_id]['cmn_int_shut'];

  $loop_count++;

  $response_message = $response_message . "Object $object_name : Port $object_id was automatically re-opened on the device " . $device_name . "\n";
}

// unlock
device_release($lock_device);


logToFile(__FILE__ . ':' . __LINE__ . ':Error_Port' . debug_dump($error_list));

$error_port = "";
$skip_port = "";


if(!empty($error_list)){
  $error_port = implode(',', $error_list);
  $response_message = $response_message . $error_port. " Error.\n";
  $status = "FAILED";
} else {
  $status = "ENDED";
}


$ret = prepare_json_response($status, $response_message, $context, true);
logToFile(__FILE__ . ':' . __LINE__ . ':response=' . debug_dump($ret));
echo "$ret\n";

?>
