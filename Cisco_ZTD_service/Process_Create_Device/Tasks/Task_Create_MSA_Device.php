<?php

/**
 * This file is necessary to include to use all the in-built libraries of /opt/fmc_repository/Reference/Common
 */
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
define('WORK_ORDER_REF', "Test_ZTD_WO");

/**
 * List all the parameters required by the task
 */
function list_args()
{
  	create_var_def('hostname', 'String');
	create_var_def('mgmt_ip', 'IpAddress');
	create_var_def('mgmt_mask', 'IpMask');
	create_var_def('serialnum', 'String');
	create_var_def('enable_ztd', 'Boolean');
	create_var_def('login', 'String');
	create_var_def('password', 'String');
	create_var_def('password_admin', 'Password');
}

if(isset($parameters)){
$context['serialnum']=$parameters['serialnum'];
$context['src_ip']=$parameters['src_ip'];	
}

check_mandatory_param('hostname');
check_mandatory_param('mgmt_ip');
check_mandatory_param('mgmt_mask');
check_mandatory_param('serialnum');
check_mandatory_param('enable_ztd');
check_mandatory_param('login');
check_mandatory_param('password');
check_mandatory_param('password_admin');


function setHostnameToDevice($dev_seq_num, $host_name, $context){
	$output_array = array ();
	$cmd_line = "/opt/ubi-jentreprise/bin/api/devicefields/setHostname.sh $dev_seq_num $host_name";

	exec ( $cmd_line, $output_array );

	// cho "ret=$ret\n";
	if (empty ( $output_array )) {
		$msg = "Error setting device hostname:$host_name to device:$dev_seq_num";
		$ret = prepare_json_response ( FAILED, $msg, $context, true );
	} else {
		$is_complete = false;
		foreach ( $output_array as $line ) {
			// 			if (preg_match ( "setSerialNumberResponse", $line ) > 0) {
			if(strpos($line, 'setHostnameResponse') !== false){
				// Success
				$msg = "hostname:$host_name set to the device:$dev_seq_num";
				$ret = prepare_json_response ( ENDED, $msg, $context, true );
				$is_complete = true;
				break;
			}
		}
		if($is_complete === false){
			$msg = "Error setting device hostname:$host_name to device:$dev_seq_num";
			$ret = prepare_json_response ( FAILED, $msg, $context, true );
		}
	}
	return $ret;
}

function addSerialToDevice($dev_seq_num, $serial_num,$context){
	$output_array = array ();
	$cmd_line = "/opt/ubi-jentreprise/bin/api/devicefields/setSerialNumber.sh $dev_seq_num $serial_num";

	exec ( $cmd_line, $output_array );

	// cho "ret=$ret\n";
	if (empty ( $output_array )) {
		$msg = "Error setting device serial number:$serial_num to device:$dev_seq_num";
		$ret = prepare_json_response ( FAILED, $msg, $context, true );
	} else {
		$is_complete = false;
		foreach ( $output_array as $line ) {
			// 			if (preg_match ( "setSerialNumberResponse", $line ) > 0) {
			if(strpos($line, 'setSerialNumberResponse') !== false){
				// Success
				$msg = "Serial no.$serial_num is added to the device:$dev_seq_num";
				$ret = prepare_json_response ( ENDED, $msg, $context, true );
				$is_complete = true;
				break;
			}
		}
		if($is_complete === false){
			$msg = "Error setting device serial number:$serial_num to device:$dev_seq_num";
			$ret = prepare_json_response ( FAILED, $msg, $context, true );
		}
	}
	return $ret;
}

function addDeviceToWorkorder($dev_seq_num, $work_order_ref,$context){
	$output_array = array();
	$cmd_line="/opt/ubi-ztd/bin/addDeviceToWorkOrder.sh $work_order_ref $dev_seq_num";

	exec($cmd_line,$output_array);

	#echo "ret=$ret\n";
	if (empty($output_array)){
	$msg="Device:$dev_seq_num added to workorder:$work_order_ref";
	$ret = prepare_json_response(ENDED, $msg, $context, true);
	}else{
	/*
		* foreach ($output_array as $line) { echo "Line:$line\n"; }
	*/
	$msg = "Error adding Device:$dev_seq_num to workorder:$work_order_ref";
	$ret = prepare_json_response ( FAILED, 'Error', $context, true );
}

return $ret;
}

$customer_id = $context['UBIQUBEID'];
$customer_id = substr($customer_id,4);
$managed_device_name = $context['hostname'];
$manufacturer_id = 1;
$model_id=113;
$login=$context['login'];
$password=$context['password'];
$password_admin=$context['password_admin'];
$device_ip_address = $context['mgmt_ip'];
$serial_num=$context['serialnum'];

$response = _device_create($customer_id, $managed_device_name, $manufacturer_id,
$model_id, $login, $password, $password_admin, $device_ip_address);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}
$created_device_id = $response['wo_newparams']['entity']['externalReference'];
$context['device_id']= $created_device_id;
$created_seq_num= $response['wo_newparams']['entity']['id'];
$wo_comment = "DeviceID:".$created_device_id;
logToFile($wo_comment);
$response = json_encode($response);
// $response = prepare_json_response(ENDED, "MSA Device created successfully.\n" . $wo_comment, $context, true);
//Device created, now add this device to workorder
$add_wo_response = addDeviceToWorkorder($created_seq_num,WORK_ORDER_REF,$context);
$add_wo_response = json_decode($add_wo_response, true);
if ($add_wo_response['wo_status'] !== ENDED) {
	$add_wo_response = json_encode($add_wo_response);
	//Do device creation cleanup if necessary, not handled now
	echo $add_wo_response;
	exit;
}
$wo_comment = "DeviceID:$created_device_id added to workorder";
logToFile($wo_comment);
//Add serial number ot the device
$add_serial_response = addSerialToDevice($created_seq_num,$serial_num,$context);
$add_serial_response = json_decode($add_serial_response, true);
if ($add_serial_response['wo_status'] !== ENDED) {
	$add_serial_response = json_encode($add_serial_response);
	//Do device creation cleanup if necessary, not handled now
	echo $add_serial_response;
	exit;
}
$wo_comment = "Serial number updated";
logToFile($wo_comment);

$setHostname_response = setHostnameToDevice($created_seq_num, $managed_device_name, $context);
$setHostname_response = json_decode($setHostname_response, true);
if ($setHostname_response['wo_status'] !== ENDED) {
	$setHostname_response = json_encode($setHostname_response);
	//Do device creation cleanup if necessary, not handled now
	echo $setHostname_response;
	exit;
}
$wo_comment = "Hostname updated";
logToFile($wo_comment);


$ztd_flag=$context['enable_ztd'];
$msg="ZTD disabled";
if($ztd_flag === 'true'){
	$cmd_line="/opt/ubi-ztd/bin/set_ztd_enabled.sh $created_device_id 1";
	shell_exec($cmd_line);
	$msg="ZTD enabled";
}
else{
	$cmd_line="/opt/ubi-ztd/bin/set_ztd_enabled.sh $created_device_id 0";
	shell_exec($cmd_line);
}
logToFile($msg);

$message = "Device: $created_device_id created for the ZTD request coming from device with serial number:$serial_num";
$response = prepare_json_response(ENDED, $message, $context, true);
echo $response;

?>