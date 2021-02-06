<?php
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args()
{
	create_var_def('device_switch', 'Device');
	create_var_def('vland_id',     'String');
	create_var_def('vlan_name', 'String');

}
$device_id = substr($context['device_id'], 3);

$micro_service_vars_array = array();


$managed_entity = array('VLAN' => array(""=> $micro_service_vars_array));


$response = execute_command_and_verify_response($device_id, CMD_CREATE, $managed_entity , "CREATE VLAN");
$response = json_decode($response, true);

logToFile(debug_dump($response,"*************************\n"));

if($response['wo_status'] !== ENDED)
{				
	$response = prepare_json_response($response['wo_status'], "Failed to update switch", $context, true);	
	echo $response;
	exit;
}

$response = prepare_json_response($response['wo_status'], "Successfully updated switch", $context, true);		
echo $response;
?>

