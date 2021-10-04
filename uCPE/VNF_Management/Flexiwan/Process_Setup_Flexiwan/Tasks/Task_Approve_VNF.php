<?php
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args()
{

   create_var_def('name', 'String');
   create_var_def('defaultRoute', 'IpAddress');
   create_var_def('isApproved', 'Boolean');

}
$device_id = substr($context['device_id'], 3);
$object_id = $context['flex_vnfid'];
$micro_service_vars_array = array();
$micro_service_vars_array['object_id']		= $context['flex_vnfid'];
$micro_service_vars_array['name']		= $context['name'];
if($context['defaultRoute'] != "")
{
	$micro_service_vars_array['defaultRoute']	= $context['defaultRoute'];
}
$micro_service_vars_array['isApproved']		= $context['isApproved'];

$VNF = array('Devices' => array($object_id => $micro_service_vars_array));


$response = execute_command_and_verify_response($device_id, CMD_UPDATE, $VNF, "UPDATE Devices");
$response = json_decode($response, true);

logToFile(debug_dump($response,"************Approve Flexiedge*************\n"));

if($response['wo_status'] !== ENDED)
{				
	$response = prepare_json_response($response['wo_status'], "Failed to Approve Flexiwan VNF", $context, true);	
	echo $response;
	exit;
}

$response = prepare_json_response($response['wo_status'], "Successfully Approved Flexiwan VNF", $context, true);		
echo $response;
?>

