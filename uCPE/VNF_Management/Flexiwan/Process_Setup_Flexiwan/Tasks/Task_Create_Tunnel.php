<?php
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args()
{
}
sleep(15);
$device_id = substr($context['device_id'], 3);
$object_id = $context['flex_vnfid'];
$micro_service_vars_array = array();
$micro_service_vars_array['Device1']		=  $context['flex_vnfid'];
$micro_service_vars_array['Device2']		=  $context['flex_vnfid2'];
$micro_service_vars_array['Organisation']	=  $context['flex_org'];


$VNF = array('Tunnels' => array("" => $micro_service_vars_array));


$response = execute_command_and_verify_response($device_id, CMD_CREATE, $VNF, "CREATE Tunnels");
$response = json_decode($response, true);

logToFile(debug_dump($response,"***********Create Tunnel**************\n"));

if($response['wo_status'] !== ENDED)
{				
	$response = prepare_json_response($response['wo_status'], "Failed to Create Tunnel", $context, true);	
	echo $response;
	exit;
}

$response = prepare_json_response($response['wo_status'], "Successfully Created Tunnel", $context, true);		
echo $response;

?>

