<?php
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args()
{

   create_var_def('action', 'String');
   create_var_def('target_int', 'String');
   create_var_def('proto', 'String');
   create_var_def('source_net', 'String');
   create_var_def('source_port', 'String');
   create_var_def('source_addr', 'String');
   create_var_def('dst_net', 'String');
   create_var_def('dst_addr', 'String');
   create_var_def('dst_port', 'String');
   create_var_def('descr', 'String');

}
$device_id=$context['device_id'];
logToFile("checking device: $device_id");
$device_id = getIdFromUbiId ($device_id);
$object_id = time();
$context['policy_id']=$object_id;
logTOFile("FIrewall tracker id is: $object_id");
$micro_service_vars_array = array();
$micro_service_vars_array['object_id']   = $object_id;
$micro_service_vars_array['action']      = $context['action'];
$micro_service_vars_array['target_int']  = $context['target_int'];
$micro_service_vars_array['proto']       = $context['proto'];
$micro_service_vars_array['source_net']  = isset($context['source_net'])? $context['source_net'] : "" ;
$micro_service_vars_array['source_port'] = isset($context['source_port'])? $context['source_port'] : "" ;
$micro_service_vars_array['source_addr'] = isset($context['source_addr'])? $context['source_addr'] : "" ;
$micro_service_vars_array['dst_net']     = isset($context['dst_net'])? $context['dst_net'] : "" ;
$micro_service_vars_array['dst_addr']    = isset($context['dst_addr'])? $context['dst_addr'] : "" ;
$micro_service_vars_array['dst_port']    = isset($context['dst_port'])? $context['dst_port'] : "" ;
$micro_service_vars_array['descr']       = isset($context['descr'])? $context['descr'] : "" ;
$ms_obj = array('fw_policy' => array($object_id => $micro_service_vars_array));


$response = execute_command_and_verify_response($device_id, CMD_CREATE, $ms_obj, "Creating FW Policy");
$response = json_decode($response, true);

logToFile(debug_dump($response,"**********Firewall policy***************\n"));

if($response['wo_status'] !== ENDED)
{				
	$response = prepare_json_response($response['wo_status'], "Failed to Create FW policy", $context, true);	
	echo $response;
	exit;
}

$response = prepare_json_response($response['wo_status'], "Successfully Created Firewall policy", $context, true);		
echo $response;
?>

