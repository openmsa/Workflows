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
  create_var_def('policy_id', 'Integer');
}

$id=$context['policy_id'];
$grp_name=$context['grp_name'];
$device_id=$context['device_id'];
$device_id = preg_replace('/[A-Z]+/', '', $device_id);

$fw_policy=array();
$fw_policy['name']='URL_Filter';
$fw_policy['srcintf']='port2';
$fw_policy['dstintf']='port3';
$fw_policy['srcaddr']='all';
$fw_policy['dstaddr']="$grp_name";
$fw_policy['service']='ALL';
$fw_policy['status']='true';
$fw_policy['comments']='URL Filtering policy';
$fw_policy['action']='deny';
$fw_policy['logtraffic']='all';
$fw_policy['move_selector']='before';
$fw_policy['move_index']='102';

$cmd_obj=array("firewall_policy" => array("$id" => $fw_policy));
$response = execute_command_and_verify_response($device_id, CMD_CREATE, $cmd_obj, "FW POLICY CREATE");
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}

/**
 * End of the task (choose one)
 */
task_success("Firewall policy Created");
?>