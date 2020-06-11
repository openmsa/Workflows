<?php
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args()
{
}


function cidr2NetmaskAddr ($bitcount) {

      $netmask = str_split (str_pad (str_pad ('', $bitcount, '1'), 32, '0'), 8);

    foreach ($netmask as &$element)
      $element = bindec ($element);

    return join ('.', $netmask);

 }



$device_id = substr($context['device_id_cp'], 3);
$fullmask = cidr2NetmaskAddr($context['masklength']);
logToFile(debug_dump($fullmask ,"*********** TESTdata**************\n"));


$micro_service_vars_array = array();
$micro_service_vars_array['object_id']           = $context['net_name'];
$micro_service_vars_array['subnet4']      = $context['address'];
$micro_service_vars_array['subnet_mask']     =$fullmask;


$DATA = array('Network' => array("" => $micro_service_vars_array));


$response = execute_command_and_verify_response($device_id, CMD_CREATE, $DATA, "CREATE Network");
$response = json_decode($response, true);
logToFile(debug_dump($response ,"*********** TESTdata**************\n"));
//task_exit(ENDED,"Successfully Added Network");


if($response['wo_status'] !== ENDED)
{       
  $response = prepare_json_response($response['wo_status'], "Failed to Add Network", $context, true); 
  echo $response;
  exit;
}


$response = prepare_json_response($response['wo_status'], "Successfully Added Network", $context, true);    
echo $response;

?>

