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
$device_id = substr($context['device_id'], 3);
$object_id = $context['flex_vnfid'];
$micro_service_vars_array = array();
$micro_service_vars_array['object_id'] = $object_id;
$VNF = array('_Flexiwan_DeviceInterfaces' => array("$object_id" => $micro_service_vars_array));
//_order_command_synchronize ($device_id);
$arr= array("_Flexiwan_DeviceInterfaces");
$response = import_objects($device_id, $arr);
$response = execute_command_and_verify_response($device_id, CMD_UPDATE, $VNF, "UPDATE Devices");
$response = json_decode($response, true);
logToFile(debug_dump($response,"************Assign Interfaces Flexiedge*************\n"));
if($response['wo_status'] !== ENDED)
{				
	$response = prepare_json_response($response['wo_status'], "Failed to Assign interfaces for the Flexiwan VNF", $context, true);	
	echo $response;
	exit;
}
task_success('Interfaces Assigned to the flexiedge device');
?>