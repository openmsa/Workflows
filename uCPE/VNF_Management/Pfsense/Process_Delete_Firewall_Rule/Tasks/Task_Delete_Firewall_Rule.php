<?php
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args()
{
}
$device_id=$context['device_id'];
$device_id = getIdFromUbiId ($device_id);
$object_id = $context['policy_id'];
$micro_service_vars_array = array();
$micro_service_vars_array['object_id']= $object_id;

$VNF = array('fw_policy' => array($object_id => $micro_service_vars_array));


$response = execute_command_and_verify_response($device_id, CMD_DELETE, $VNF, "Delete Firewall policy");
$response = json_decode($response, true);

logToFile(debug_dump($response,"*************************\n"));

if($response['wo_status'] !== ENDED)
{				
	$response = prepare_json_response($response['wo_status'], "Failed to delete FW policy $object_id", $context, true);	
	echo $response;
	exit;
}

$response = prepare_json_response($response['wo_status'], "Successfully deleted firewall policy $object_id", $context, true);		
echo $response;
?>

