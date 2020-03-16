<?php
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args()
{
}
$device_id = substr($context['sw_device'], 3);
$micro_service_port= array();
$micro_service_port['object_id'] = $context['lan_port'];

	//===================== create vlan==============================================================

	$micro_service_vlan= array();
	$micro_service_vlan['object_id'] = $context['sw_vlan_name'];
	$micro_service_vlan['vlanid'] = $context['VLAN'];
	$micro_service_vlan['description'] = $context['sw_vlan_description'];

	$managed_entity = array('VLAN' => array(""=> $micro_service_vlan));
	$response = execute_command_and_verify_response($device_id, CMD_CREATE, $managed_entity , "CREATE VLAN");
	$response = json_decode($response, true);

	logToFile(debug_dump($response,"*************************\n"));

	if($response['wo_status'] !== ENDED)
	{				
		$response = prepare_json_response($response['wo_status'], "Failed to create switch vlan", $context, true);	
		echo $response;
		exit;
	}
	$micro_service_port['vlanid'] = $context['VLAN'];


//===========================create port========================================================
/*$micro_service_port= array();
$micro_service_port['object_id'] = $context['lan_port'];
$micro_service_port['vlanid'] = $context['VLAN'];

$managed_entity = array('Switchport_Access' => array(""=> $micro_service_port));
$response = execute_command_and_verify_response($device_id, CMD_CREATE, $managed_entity , "CREATE Switchport_Access");
$response = json_decode($response, true);

logToFile(debug_dump($response,"*************************\n"));

if($response['wo_status'] !== ENDED)
{				
	$response = prepare_json_response($response['wo_status'], "Failed to create switch port", $context, true);	
	echo $response;
	exit;
}*/

$response = prepare_json_response($response['wo_status'], "Successfully updated switch", $context, true);		
echo $response;
?>
