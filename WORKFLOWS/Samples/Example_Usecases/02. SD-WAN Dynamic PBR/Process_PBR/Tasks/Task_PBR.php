<?php
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/function/device_lock.php';
require_once '/opt/fmc_repository/Process/function/device_release.php';
require '/opt/fmc_repository/Process/function/config.php';

// CONSTANT VALUES for this workflow
$ENTRY_ID_NAME  = 'entry_id';                 // entry_id
$csv_source     = '/home/ncuser/nfa_pbr.csv'; // Event => PBR-entry conversion data
$object_name    = 'scenarios';            // PBR object name (for UPDATE/IMPORT) 
$target_event   = 'nfaTrafficThreshExceeded'; // target event


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

function list_args()
{
  create_var_def('device_id', 'Device');
  create_var_def('target_device', 'String');
  create_var_def('date', 'String');
  create_var_def('rule', 'String');
  create_var_def('policy', 'String');
  create_var_def('list.0.object_id', 'String');
  create_var_def('list.0.enable', 'String');
}

// input end

// select device start
$PROCESSINSTANCEID = $context['PROCESSINSTANCEID'];
$EXECNUMBER= $context['EXECNUMBER'];
$TASKID    = $context['TASKID'];
$process_params = array('PROCESSINSTANCEID' => $PROCESSINSTANCEID,
                                                'EXECNUMBER' => $EXECNUMBER,
                                                'TASKID' => $TASKID);

$source_id = substr($context['device_id'],3);    // NFA's device ID
$device_id = substr($PFC_SCC_SERVER, 3);         // SC-IX's device ID
// select device end

// LOG information
$date      = $context['date'];
$rule      = $context['rule'];
$policy    = $context['policy'];

// save common context data
$context['target_device'] = $PFC_SCC_SERVER;

// data prepare end

// read CSV file
function my_read_csv($csv_source){

  if(!($fp = fopen($csv_source, "r"))){
    return false;
  }

  $header     = fgetcsv($fp);
  $count      = count($header);
  $header_key = $header[0];

  $data_array = array();

  while(($read_data = fgetcsv($fp, 0, ",")) !== FALSE){
    $read_count  = count($read_data);
    $data_tmp    = array();
    for($i = 0; $i < $read_count; $i++){
      if(empty($data_tmp[$header[$i]])){
        $data_tmp[$header[$i]][0] = $read_data[$i];
      }
      else {
        array_push($data_tmp[$header[$i]], $read_data[$i]);
      }
    }

    // swap index and key-name
    $data2store   = array();
    foreach($data_tmp as $key => $item_array){
      foreach($item_array as $index => $item){
        if($key !== $header_key){
          $data2store[$index][$key] = $item;
        }
      }
    }

    // add entry
    $data_array[$read_data[0]] = $data2store;
  }

  fclose($fp);

  return $data_array;
}

$event_table = my_read_csv($csv_source);

// CSV file read end

$response_message = "";
$status = "";


// main start

logToFile(__FILE__ . ':' . __LINE__ . "\n" . 'context:' . print_r($context, true));
logToFile(__FILE__ . ':' . __LINE__ . "\n" . 'read_csv:' . print_r($event_table, true));


if($event_table === false) {                     // CSV file error
  $response_message = $response_message . "Operation failed: cannot open CSV file: " . $csv_source . "\n";
  $status = "FAILED";

  // Construct context data
  $context['list'][0]['object_id'] = "CSV OPEN ERROR";
  $context['list'][0]['enable']    = '';
  logToFile(__FILE__ . ':' . __LINE__ . "\n" . 'response_message:' . $response_message);
}
else if ($rule !== $target_event){               // ``rule'' is not 'nfaTrafficThreshExceeded'
  $response_message = $response_message . "Operation failed: illegal rule detected (rule expected $target_event but recieved $rule)\n";
  $status = "FAILED";

  // Construct context data
  $context['list'][0]['object_id'] = "ILLEGAL RULE";
  $context['list'][0]['enable']    = '';
  logToFile(__FILE__ . ':' . __LINE__ . "\n" . 'response_message:' . $response_message);
}
else if(empty($event_table[$policy])){      // No entry found in CSV
  $response_message = $response_message . "Operation failed: policy $policy does not found in CSV ($csv_source).\n";
  $status = "FAILED";

  // Construct context data
  $context['list'][0]['object_id'] = "NO POLICY FOUND";
  $context['list'][0]['enable']    = '';
  logToFile(__FILE__ . ':' . __LINE__ . "\n" . 'response_message:' . $response_message);

  // send syslog
  /*
  openlog("NFA_PBR", LOG_PID | LOG_PERROR, LOG_LOCAL0);

  $date = date("Y/m/d H:i:s");
  syslog(LOG_WARNING, "Policy ($policy) does not found in CSV ($csv_source).");

  closelog();
  */
}
else{                                       // main 

  // prepare UPDATE

  // create UPDATE object-item list
  $object_array  = array();
  $loop_count    = 0;
  foreach($event_table[$policy] as $item){
    $array_item  = array();

    $object_id               = array_key_exists('entry_id', $item)? $item['entry_id'] : '';
    $array_item["object_id"] = $object_id;
    $array_item["enable"]    = array_key_exists('enable_parameter', $item)? $item['enable_parameter'] : '';

    // save $context
    $context['list'][$loop_count]['object_id'] = $array_item['object_id'];
    $context['list'][$loop_count]['enable']    = $array_item['enable'];

    $object_array[$object_id]= $array_item;
    $loop_count++;
  }
  logToFile(__FILE__ . ':' . __LINE__ . "\n" . 'Update table: ' . print_r($object_array, true));

  // Checking that every parameters are not empty.
  $flag_continue_to_update = true;       // if false one or more items are empty, so do not UPDATE.
  $loop_count    = 0;
  foreach($object_array as $item){
    logToFile(__FILE__ . ':' . __LINE__ . "\n" . 'In foreach loop: item = ' . print_r($item, true));
    foreach($item as $key => $item2){    // item2: value of object_id or enable
      if(empty($item2)){
        logToFile(__FILE__ . ':' . __LINE__ . "\n" . 'In foreach2 loop: Empty!!!!' . "\n");
        $flag_continue_to_update = false;
        // Error notification via $context
        $context['list'][$loop_count][$key] = 'EMPTY ITEM ERROR';
      }
    }
    $loop_count++;
  }

  logToFile(__FILE__ . ':' . __LINE__ . "\n" . 'Empty check complete: flag = ' . print_r($flag_continue_to_update,true) );

  if($flag_continue_to_update){
    // Multiple object_id to UPDATE
    $update_array  = array($object_name => $object_array);

    // Execute UPDATE
    logToFile(__FILE__ . ':' . __LINE__ . "\n" . 'UPDATE ' . $object_name . ':param=' . print_r($update_array, true));

    $response = execute_command_and_verify_response($device_id, CMD_UPDATE, $update_array, "UPDATE $object_name");
    $response = json_decode($response, true);
    logToFile(__FILE__ . ':' . __LINE__ . ':response=' . print_r($response, true));

    // response analyze
    if ($response["wo_status"] == "FAIL"){
      $response_message = $response_message . "Operation failed: during UPDATE object (object_name=$object_name).\n";
      $status = "FAILED";
    }
    else { // Success
      $response_message = $response_message . "Operation successfully completed.\n";
      $status = "ENDED";

      // IMPORT updated data
      $import_list   = array($object_name);
      $response_json = import_objects($device_id, $import_list);
      $response      = json_decode($response_json, true);
      logToFile(__FILE__ . ':' . __LINE__ . "\n" . 'DEBUG: ' . debug_dump($response)  . "\n");
    }
  }
  else{    // NOT UPDATED! Empty parameter(s) found.
    logToFile(__FILE__ . ':' . __LINE__ . "\n" . 'object_array = ' . debug_dump($object_array)  . "\n");
    $response_message = $response_message . "Empty parameter found in CSV.\n";
    $status = "FAILED";
  }
}


$ret = prepare_json_response($status, $response_message, $context, true);
echo "$ret\n";

// unlock
device_release($lock_device);
//Lock End


?>
