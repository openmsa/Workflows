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
  /**
   * You can use var_name convention for your variables
   * They will display automaticaly as "Var Name"
   * The allowed types are:
   *    'String', 'Boolean', 'Integer', 'Password', 'IpAddress',
   *    'IpMask', 'Ipv6Address', 'Composite', 'OBMFRef', 'Device'
   *    
   * Add as many variables as needed
   */
  create_var_def('serialnum', 'String');
  create_var_def('src_ip', 'IpAddress');
}


if(isset($parameters)){
$context['serialnum']=$parameters['serialnum'];
$context['src_ip']=$parameters['src_ip'];	
}



function isZtdEnabled($device_id){
	$cmd_line="/opt/ubi-ztd/bin/is_ztd_enabled.sh $device_id";
	$status=shell_exec($cmd_line);
	return $status;
}
function fetch_device_by_serial_num($serialnum){
// 		$cmd="/opt/ubi-ztd/bin/device_id_by_serialnum.sh $serialnum '--use-work-orders'";
	$cmd="/opt/ubi-ztd/bin/device_id_by_serialnum.sh $serialnum";
$dev_id=shell_exec($cmd);
return $dev_id;
}

function addDeviceToWorkorder($dev_seq_num, $work_order_ref){
	$cmd_line="/opt/ubi-ztd/bin/addDeviceToWorkOrder.sh $work_order_ref $dev_seq_num";
	$context_tmp = array();
	$output_array=shell_exec($cmd_line);

	#echo "ret=$ret\n";
	if (empty($output_array)){
		$msg="Device:$dev_seq_num added to workorder:$work_order_ref";
		$ret = prepare_json_response(ENDED, $msg, $context_tmp, true);
	}else{
		/*
		 * foreach ($output_array as $line) { echo "Line:$line\n"; }
		*/
		$msg = "Error adding Device:$dev_seq_num to workorder:$work_order_ref";
		$ret = prepare_json_response ( FAILED, $msg, $context_tmp, true );
	}
}
/**
 * A function to check whether all the mandatory parameters are present in user-input
 *
 * The function needs to be called for each mandatory parameter.
 * This function call prevents the Task execution whenever there is a mandatory parameter missing,
 * and gives error at the beginning itself preventing any issues in-between/end of the Task due to a missing mandatory parameter.
 *
 *
 * NOTE : There might be cases where conditions are required.
 * For ex. if (empty($context['var_name']) || (empty($context['var_name2']) && empty($context['var_name3']))) => FAIL [Don't proceed]
 * Such cases need to be handled as per the Task logic
 */
check_mandatory_param('serialnum');
check_mandatory_param('src_ip');

/** 
 * $context => Service Context variable per Service Instance
 * All the user-inputs of Tasks are automatically stored in $context
 * Also, any new variables should be stored in $context which are used across Service Instance
 * The variables stored in $context can be used across all the Tasks and Processes of a particular Service
 * Update $context array [add/update/delete variables] as per requirement
 * 
 * ENTER YOUR CODE HERE
 */

$PROCESSINSTANCEID = $context['PROCESSINSTANCEID'];
$EXECNUMBER = $context['EXECNUMBER'];
$TASKID = $context['TASKID'];
$process_params = array('PROCESSINSTANCEID' => $PROCESSINSTANCEID,
		'EXECNUMBER' => $EXECNUMBER,
		'TASKID' => $TASKID);

// $context['var_name2'] = $context['var_name2'] + 1;
$serial_number=$context['serialnum'];
$device_ip=$context['src_ip'];


$device_id=fetch_device_by_serial_num($serial_number);
$device_id=trim($device_id);

if($device_id === ""){
	$message = "For the request coming from $device_ip, no device found in MSA with Serial number: $serial_number";
	$ret = prepare_json_response(FAILED, $message, $context, true);
	echo "$ret\n";
	exit;
}
$message = "Device $device_id found for the request coming from $device_ip, with Serial number: $serial_number";
update_asynchronous_task_details($process_params, $message);
// $ret = prepare_json_response(ENDED, $message, $context, true);
// echo "$ret\n";

$context['device_id']=$device_id;

$dev_seq_num = substr($device_id,3);


$response = _device_read_by_id ($dev_seq_num);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}
$context['mgmt_ip']=$response['wo_newparams']['managementAddress'];
$context['login']=$response['wo_newparams']['login'];
$context['password']=$response['wo_newparams']['password'];
$context['password_admin']=$response['wo_newparams']['passwordAdmin'];

$ztd_status=isZtdEnabled($device_id);
$ztd_status=trim($ztd_status);
logToFile("ztd_status:=>$ztd_status::");
if($ztd_status === ''){
	logToFile("Device not added to workorder");
	
	$context['enable_ztd'] = false;
		// Device already created, now add this device to workorder
	$add_wo_response = addDeviceToWorkorder ( $dev_seq_num, WORK_ORDER_REF, $context );
	
} elseif ($ztd_status === '0'){
	logToFile("ztd_status=$ztd_status::false");
	$context['enable_ztd'] = false;
}else{
	logToFile("ztd_status=$ztd_status::true");
	$context['enable_ztd'] = true;
}

logToFile("Device added to workorder");
$dev_ext_ref=$response['wo_newparams']['externalReference'];


/* //Trigger provisioning process of same service instance
$customer_id=$context['UBIQUBEID'];
$external_ref=substr($customer_id,4);
$service_name="Process/Cisco_ZTD_service/Cisco_ZTD_Service";
$service_ref=$serial_number;
$add_service_array = array();
$add_service_array['device_id'] = $context['device_id'];
$add_service_array['src_ip'] = $context['src_ip'];
$add_service_array['serialnum'] = $context['serialnum'];
$json_body = json_encode($add_service_array);
$response= _orchestration_execute_service_by_reference($external_ref, $service_ref, $service_name, Process/Cisco_ZTD_service/Process_Provision, $json_body);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
} */
$message = "ZTD request verified for device with serial number:$serial_number and identfied the device:$device_id";
$response = prepare_json_response(ENDED, $message, $context, true);
echo $response;



?>