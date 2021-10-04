<?php
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args()
{
}
$device_id = substr($context['device_id'], 3);
$object_id = $context['flex_vnfid'];
$micro_service_vars_array = array();
$micro_service_vars_array['object_id']		= $context['flex_vnfid'];
$micro_service_vars_array['upstate']		=  "start";
$micro_service_vars_array['org']		=  $context['flex_org'];

$VNF = array('DeviceStatus' => array($object_id => $micro_service_vars_array));


$response = execute_command_and_verify_response($device_id, CMD_UPDATE, $VNF, "UPDATE DeviceStatus");
$response = json_decode($response, true);

logToFile(debug_dump($response,"***********Start Flexiedge**************\n"));

if($response['wo_status'] !== ENDED)
{				
	$response = prepare_json_response($response['wo_status'], "Failed to Start Flexiwan-Edge", $context, true);	
	echo $response;
	exit;
}

$response = prepare_json_response($response['wo_status'], "Successfully started Flexiwan-Edge", $context, true);		
echo $response;
?>

