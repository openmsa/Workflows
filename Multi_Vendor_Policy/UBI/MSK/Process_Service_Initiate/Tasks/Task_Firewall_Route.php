<?php
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args()
{
}


$device_id = substr($context['fw_device'], 3);

$micro_service_vars_array = array();
$micro_service_vars_array['object_id'] 	= $context['service_id'];
$micro_service_vars_array['next_hop']  = $context['rtr_fw_int_ip'];
$micro_service_vars_array['interface'] 	= $context['fw_rtr_int'];
$micro_service_vars_array['destination'] = $context['service_subnet_ip'];

$micro_service_vars_array['destination'].='/';
$micro_service_vars_array['destination'].=$context['service_subnet_masklen'];


$managed_entity = array('static_route' => array($context['service_id'] => $micro_service_vars_array));


$response = execute_command_and_verify_response($device_id, CMD_CREATE, $managed_entity , "CREATE static_route");
$response = json_decode($response, true);

logToFile(debug_dump($response,"*************************\n"));

if($response['wo_status'] !== ENDED)
{				
	$response = prepare_json_response($response['wo_status'], "Failed to create static route", $context, true);	
	echo $response;
	exit;
}

$response = prepare_json_response($response['wo_status'], "Successfully  create static route", $context, true);		
echo $response;
?>

