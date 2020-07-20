<?php
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args()
{
}
$device_id = substr($context['device_id'], 3);
$object_id = $context['staticroute_id'];
$micro_service_vars_array = array();
$micro_service_vars_array['Devices']		=  $context['flex_vnfid'];
$micro_service_vars_array['Organisation']	=  $context['flex_org'];

$micro_service_vars_array['object_id']		=  $object_id;


$VNF = array('StaticRoutes' => array("$object_id" => $micro_service_vars_array));


$response = execute_command_and_verify_response($device_id, CMD_DELETE, $VNF, "DELETE StaticRoutes");
$response = json_decode($response, true);

logToFile(debug_dump($response,"*************************\n"));

if($response['wo_status'] !== ENDED)
{				
	$response = prepare_json_response($response['wo_status'], "Failed to delete Static route", $context, true);	
	echo $response;
	exit;
}

$response = prepare_json_response($response['wo_status'], "Successfully Deleted Static Route", $context, true);		
echo $response;
?>

