<?php
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args()
{
}

$device_id = substr($context['device_id'], 3);

//import MS for tunnels to get all info 
$arr= array("Tunnels");
$response = import_objects($device_id, $arr);


//$response = _device_read_by_id($device_id);
$response = json_decode($response, true);
if($response['wo_status'] !== ENDED)
{				
	$response = prepare_json_response($response['wo_status'], "Failed to delete Tunnel", $context, true);	
	echo $response;
	exit;
}

$tunnels = $response["wo_newparams"]["Tunnels"];
$tunnelDevices =array($context['flex_vnfid2'],$context['flex_vnfid']);
$object_id =  "";
foreach($tunnels as $row)
{
  
	if(in_array($row["deviceA_id"],$tunnelDevices) && in_array($row["deviceB_id"],$tunnelDevices))
	{
	   $object_id = $row["object_id"];
	}
	logToFile(debug_dump($row,"************ROW*************\n"));
}
//------------------------------------------


$micro_service_vars_array = array();
$micro_service_vars_array['object_id']	= $object_id;
$micro_service_vars_array['Tunnels']	=  $context['flex_org'];
$micro_service_vars_array['object_id']	=  $object_id;

$VNF = array('Tunnels' => array("$object_id" => $micro_service_vars_array));

$response = execute_command_and_verify_response($device_id, CMD_DELETE, $VNF, "DELETE Tunnels");
$response = json_decode($response, true);

logToFile(debug_dump($response,"*************************\n"));

if($response['wo_status'] !== ENDED)
{				
	$response = prepare_json_response($response['wo_status'], "Failed to delete Tunnel", $context, true);	
	echo $response;
	exit;
}

$response = prepare_json_response($response['wo_status'], "Successfully Deleted Tunnel", $context, true);		
echo $response;
?>

