<?php
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/function/device_lock.php';
require_once '/opt/fmc_repository/Process/function/device_release.php';
require '/opt/fmc_repository/Process/function/config.php';

function list_args()
{
  create_var_def('customer_id', 'Customer');
}

function _lookup_list_devices_by_customer ($customer_reference) {
  $msa_rest_api = "lookup/customer/devices/reference/{$customer_reference}";
  $curl_cmd = create_msa_operation_request(OP_GET, $msa_rest_api);
  $response = perform_curl_operation($curl_cmd, "LIST DEVICES BY CUSTOMER REFERENCE");
  $response = json_decode($response, true);
  if ($response['wo_status'] !== ENDED) {
    $response = json_encode($response);
    return $response;
  }
  $response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
  return $response;
}

$HTTP_HOST = get_vars_value(WEB_NODE_PRIV_IP);
$HTTP_PORT = get_vars_value(WEB_NODE_HTTP_PORT);
$USERNAME = "ncroot";
$hash = get_vars_value(NCROOT_PASSWORD_VARIABLE);
$script = "/opt/configurator/script/encp.sh ".$hash; 
$NCROOT_PASSWORD = exec($script);


$PROCESSINSTANCEID = $context['PROCESSINSTANCEID'];
$EXECNUMBER = $context['EXECNUMBER'];
$TASKID = $context['TASKID'];
$process_params = array('PROCESSINSTANCEID' => $PROCESSINSTANCEID,
                                                'EXECNUMBER' => $EXECNUMBER,
                                                'TASKID' => $TASKID);

$customer_id = $context['customer_id'];
$device_array = _lookup_list_devices_by_customer($customer_id);
$device_array = json_decode($device_array, true);

logToFile(__FILE__ . ':' . __LINE__ . "\n" . 'Customer: ' . $customer_id  . "\n");
logToFile(__FILE__ . ':' . __LINE__ . "\n" . 'Lookup_response: ' . debug_dump($device_array)  . "\n");

$response_message = "";
$status = "";
$status_check = "";

foreach($device_array['wo_newparams'] as $device_item){

  $device_id = $device_item['id'];
  
  // lock device
  $lock_device = device_lock($device_item['ubiId']);
  if($lock_device === FALSE){
    $response_message = "Lock file could not open.";
    $status = "FAILED";
    $ret = prepare_json_response($status, $response_message, $context, true);
    echo "$ret\n";
    exit;
  }

  $url = "http://$HTTP_HOST:$HTTP_PORT/ubi-api-rest/device/id/$device_id";

  // curl access start
  $curl_obj = curl_init();
  curl_setopt($curl_obj, CURLOPT_URL, $url);
  curl_setopt($curl_obj, CURLOPT_USERPWD, "$USERNAME:$NCROOT_PASSWORD");
  curl_setopt($curl_obj, CURLOPT_RETURNTRANSFER, 1);
  curl_setopt($curl_obj, CURLOPT_HTTPGET, 1);
  $response_json = curl_exec($curl_obj);
  curl_close($curl_obj);
  // curl end

  logToFile(__FILE__ . ':' . __LINE__ . "\n" . 'Lookup_response: ' . debug_dump($response_json)  . "\n");

  $curl_response = json_decode($response_json, true);
  logToFile(__FILE__ . ':' . __LINE__ . "\n" . 'Lookup_response: ' . debug_dump($curl_response)  . "\n");
  
  $device_name = preg_replace('/\s/', '_', $curl_response['name']);
  
  $return_code = 0;
  $target_catalyst = $curl_response['managementAddress'];
  $catalyst_user = $curl_response['login'];
  $catalyst_pass = $curl_response['password'];
  $catalyst_enable = $curl_response['passwordAdmin'];
  $tftp_path = "tftp://" . $tftp . "/" . $device_name . "_" . date('Ymd') . ".cfg";

  $manufacturerId = $curl_response["manufacturerId"];
  $modelId = $curl_response["modelId"];

  if($manufacturerId == "1" && $modelId == "104"){

    $return_code = 0;
    ob_start();
    passthru("/opt/fmc_repository/Process/Process_TFTP/Tasks/catalyst_tftp.sh $target_catalyst $catalyst_user $catalyst_pass $catalyst_enable $tftp_path 2>&1", $return_code);
    $output = ob_get_contents();
    ob_end_clean();

    if($return_code !== 0){
      $status_check = "FAILED";
      $response_message = $response_message . $curl_response['name'] . " (" . $device_item['ubiId'] . ") failed.\n"; 
    }
    else{  // success
      $status = "ENDED";
    }
    
    //unlock
    device_release($lock_device);

  } else {
    $status = "ENDED";
  }

}

logToFile(__FILE__ . ':' . __LINE__ . "\n" . 'Output: ' . debug_dump($output)  . "\n");

if($status_check == "FAILED"){
  $status = "FAILED";
}

if($status == ""){
  $status = "ENDED";
  $response_message = "This Customer doesn't have any devices so no operation was performed.";
} else if($status === "ENDED") {
  $response_message = "Configuration copy succeeded.";
}

$ret = prepare_json_response($status, $response_message, $context, true);
echo "$ret\n";

?>