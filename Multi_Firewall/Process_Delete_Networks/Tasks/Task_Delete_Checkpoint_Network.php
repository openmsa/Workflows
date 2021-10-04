<?php
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args()
{

}
$device_id = substr($context['device_id_cp'], 3);

$micro_service_vars_array = array();
$micro_service_vars_array['object_id']    = $context['net_name'];
$object_id =  $context['net_name'];


$DATA = array('Network' => array($object_id => $micro_service_vars_array));


$response = execute_command_and_verify_response($device_id, CMD_DELETE, $DATA, "DELETE Network");
$response = json_decode($response, true);

if($response['wo_status'] !== ENDED)
{       
  $response = prepare_json_response($response['wo_status'], "Failed to Delete Network", $context, true);  
  echo $response;
  exit;
}

$response = prepare_json_response($response['wo_status'], "Successfully Delete Network", $context, true);   
echo $response;
?>

