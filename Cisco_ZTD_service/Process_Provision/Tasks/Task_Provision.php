<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args() {
	create_var_def('device_id', 'Device');
	create_var_def('src_ip', 'IpAddress');
	create_var_def('serialnum', 'String');
	create_var_def('enable_ztd', 'Boolean');
}
function isZtdEnabled($device_id){
	$cmd_line="/opt/ubi-ztd/bin/is_ztd_enabled.sh $device_id";
	$status=shell_exec($cmd_line);
	return $status;
}

function get_xml_tag($xml_input, $tag_name){
	$ret_index=strpos($xml_input,"<$tag_name>");
    $ret_enc_index=strpos($xml_input,"</$tag_name>");
    $ret_len=$ret_enc_index-$ret_index-strlen($tag_name)-2;
    $ret_str=substr($xml_input,$ret_index+strlen($tag_name)+2,$ret_len);
    return $ret_str;
}

check_mandatory_param('device_id');
check_mandatory_param('src_ip');
check_mandatory_param('serialnum');
check_mandatory_param('enable_ztd');

$src_ip=$context['src_ip'];
$serialnum=$context['serialnum'];
$ztd_flag=$context['enable_ztd'];
$isr_login="cisco";
$isr_passwd="cisco";
$isr_admin_passwd="cisco";
$dev_id=$context['device_id'];
$PROCESSINSTANCEID = $context['PROCESSINSTANCEID'];
$EXECNUMBER = $context['EXECNUMBER'];
$TASKID = $context['TASKID'];
$process_params = array('PROCESSINSTANCEID' => $PROCESSINSTANCEID,
						'EXECNUMBER' => $EXECNUMBER,
						'TASKID' => $TASKID);

$is_ztd_enabled = isZtdEnabled($dev_id);
$is_ztd_enabled = trim($is_ztd_enabled);
logToFile("is_ztd_enabled:$is_ztd_enabled || ztd_flag:$ztd_flag ");
if($ztd_flag !== 'true' || $is_ztd_enabled !== '1'){
	$message = "ZTD not enabled on device:$dev_id";
	$ret = prepare_json_response(FAILED, $message, $context, true);
	echo "$ret\n";
	exit;
}


$device_id = substr($dev_id, 3);
//Launch unlockprovisioning for the device
$unlock_cmd="/opt/sms/bin/sms -e UNLOCKPROVISIONING -i $device_id";
$unlock_res=shell_exec($unlock_cmd);
$message = "UNLOCKPROVISIONING:$unlock_res";
update_asynchronous_task_details($process_params, $message);

//Launch firmware upgrade for the device
/* $fmwr_cmd="/opt/sms/bin/sms -e JSAUPDATEFIRMWARE -i $dev_id ip=$src_ip,login=$isr_login,pwd=$isr_passwd,admin_passwd=$isr_admin_passwd,NO_REBOOT";
update_asynchronous_task_details($process_params, $fmwr_cmd);
$fmwr_res=shell_exec($fmwr_cmd);


//Check for the firmware upgrade status
$frmwr_status_cmd="/opt/sms/bin/sms -e CHECKUPDATEFIRMWARE -i $dev_id | sed -n '3p'";
$frmwr_status='W';
while($frmwr_status === "W"){

	$frmwr_status=shell_exec($frmwr_status_cmd);
	sleep(5);
}
if($frmwr_status !== "E"){
	$message = "Firmware update of the device:$dev_id, failed";
	$ret = prepare_json_response(FAILED, $message, $context, true);
	echo "$ret\n";
	exit;
} */
//Launch initial provisioning using cli
$init_prov_cmd="/opt/sms/bin/sms -e PROVISIONING -i $dev_id -c \"$src_ip $isr_login $isr_passwd $isr_admin_passwd\"";
$status=shell_exec($init_prov_cmd);
if(strpos($status, 'FAIL') !== false){
	$message = "Initial provisioning of the device:$dev_id failed, please check the device status";
	$ret = prepare_json_response(FAILED, $message, $context, true);
	shell_exec("rm -f /opt/ubi-ztd/var/lock/$serialnum.lock");
	echo "$ret\n";
	exit;
}
$message = "Provisioning of the device:$dev_id started...";
update_asynchronous_task_details($process_params, $message);

//Wait for provisioning to complete
$response = wait_for_provisioning_completion($device_id, $process_params);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	shell_exec("rm -f /opt/ubi-ztd/var/lock/$serialnum.lock");
	echo $response;
	exit;
}
$wo_comment = $response['wo_comment'];
$cmd_line="/opt/ubi-ztd/bin/set_ztd_enabled.sh $dev_id 0";
shell_exec($cmd_line);
$response = prepare_json_response(ENDED, "MSA Device $device_id Provisioned successfully.\n" . $wo_comment, $context, true);
shell_exec("rm -f /opt/ubi-ztd/var/lock/$serialnum.lock");
echo $response;

?>