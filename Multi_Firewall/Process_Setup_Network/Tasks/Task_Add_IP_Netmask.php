<?php
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args()
{

  create_var_def('net_name', 'String');  
  create_var_def('address', 'String');  
  create_var_def('masklength', 'String');  

}
$device_id = substr($context['device_id_pa'], 3);

$micro_service_vars_array = array();
$micro_service_vars_array['object_id']    = $context['net_name'];
$micro_service_vars_array['masklen']  = $context['masklength'];
$micro_service_vars_array['address']  = $context['address'];


$DATA = array('address_ip_netmask' => array("" => $micro_service_vars_array));


$response = execute_command_and_verify_response($device_id, CMD_CREATE, $DATA, "CREATE address_ip_netmask");
$response = json_decode($response, true);

if($response['wo_status'] !== ENDED)
{       
  $response = prepare_json_response($response['wo_status'], "Failed to Add IP Netmask", $context, true);  
  echo $response;
  exit;
}

$response = prepare_json_response($response['wo_status'], "Successfully Added IP Netmask", $context, true);   
echo $response;
?>

