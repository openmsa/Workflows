<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/Common/Library/msa_common.php';

//Retrive variables from $context and define the new ones
$delay = 90;
$device_id = $context['device_id'];
$microservices_array = $context['microservices_array'];
$username = $context['username'];
$server_ip_address = $context['server_ip_address'];
$server_mac_address = $context['server_mac_address'];

//Create new password
$response = update_asynchronous_task_details($context, "Creating new password... ");
//$new_password = trim(base64_encode(substr(md5($username.$server_ip_address.$server_mac_address), 0, 10)), '=');
$new_password = $context['password'];
$context['password'] = $new_password;
$response = update_asynchronous_task_details($context, "Creating new password... OK. The new password is ".$new_password);
sleep(3);


//Update BMC password on server
$response = update_asynchronous_task_details($context, "Updating the new password on BMC... ");
$micro_service_vars_array = array ();
$micro_service_vars_array ['object_id'] = $username;
$micro_service_vars_array ['password'] = $new_password;
$ms_array = array('redfish_server_accounts' => array ($username => $micro_service_vars_array));
$response = execute_command_and_verify_response( $device_id, CMD_UPDATE, $ms_array, "UPDATE password");

$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
    $response = json_encode($response);
    echo $response;
    exit;
}

//Update credentials on management entity
$response = json_decode(_device_update_credentials($device_id, $username, $new_password), true);

if ($response['wo_status'] !== ENDED) {
  $response = json_encode($response);
  echo $response;
  exit;
}

//Sleep before connect to BMC again
sleep($delay);
$response = update_asynchronous_task_details($context, "Updating the new password on BMC... OK");

task_success("BMC password was updated successfylly to ".$new_password."\n Verify BIOS parameters next.");

?>