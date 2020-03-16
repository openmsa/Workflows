<?php
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args()
{
	create_var_def('device_router', 'Device');
}
$device_id = substr($context['device_id'], 3);
$object_id = $context['vnfr_id'];
$micro_service_vars_array = array();
$micro_service_vars_array['object_id']		= $context['vnfr_id'];


$managed_entity = array('VNF_instances' => array($object_id => $micro_service_vars_array));


$response = execute_command_and_verify_response($device_id, CMD_CREATE, $managed_entity , "CREATE VNF_instances");
$response = json_decode($response, true);

logToFile(debug_dump($response,"*************************\n"));

if($response['wo_status'] !== ENDED)
{				
	$response = prepare_json_response($response['wo_status'], "Failed to update router", $context, true);	
	echo $response;
	exit;
}

$response = prepare_json_response($response['wo_status'], "Successfully updated router", $context, true);		
echo $response;
?>

