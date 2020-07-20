<?php
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args()
{
	create_var_def('destination_network', 'String');
	create_var_def('gateway_ip', 'String');
}
$device_id = substr($context['device_id'], 3);
$object_id = $context['flex_vnfid'];
$micro_service_vars_array = array();
$micro_service_vars_array['Devices']		=  $context['flex_vnfid'];
$micro_service_vars_array['destination_network'] =  $context['destination_network'];
$micro_service_vars_array['Organisation']	=  $context['flex_org'];
$micro_service_vars_array['gateway_ip']	=  $context['gateway_ip'];


$VNF = array('StaticRoutes' => array("" => $micro_service_vars_array));


$response = execute_command_and_verify_response($device_id, CMD_CREATE, $VNF, "CREATE StaticRoutes");
$response = json_decode($response, true);

logToFile(debug_dump($response,"***********Create Static Route**************\n"));

if($response['wo_status'] !== ENDED)
{				
	$response = prepare_json_response($response['wo_status'], "Failed to create Static route", $context, true);	
	echo $response;
	exit;
}
$x = json_decode($response["wo_comment"]);
$context["staticroute_id"] = $x->_id;

$response = prepare_json_response($response['wo_status'], "Successfully Created Static Route", $context, true);		
echo $response;
?>

