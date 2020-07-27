<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/Common/Library/msa_common.php';


//Retrive variables from $context and define the new ones
$modifying_failed = '';
$device_id = $context['device_id'];
$bios_parameters = $context['bios_parameters_array'];
$microservices_array = $context['microservices_array'];
$ms_server_inventory = $microservices_array['Server inventory'];
$ms_server_power = $microservices_array['Server power managment'];
$ms_bios_params = $microservices_array['BIOS parameters manipulation'];

$response = update_asynchronous_task_details($context, "Device syncing... ");

//Sync up the ME MSs
$response = json_decode(synchronize_objects_and_verify_response($device_id), true);
if ($response['wo_status'] !== ENDED) {
  $response = json_encode($response);
  echo $response;
  exit;
}

//Sync up the referenced MSs
$response = json_decode(synchronize_objects_and_verify_response($device_id), true);
if ($response['wo_status'] !== ENDED) {
  $response = json_encode($response);
  echo $response;
  exit;
}
$response = update_asynchronous_task_details($context, "Device syncing... OK");
sleep(3);

//Import current server power state
$response = json_decode(import_objects($device_id, array($ms_server_inventory)), True);
$object_ids_array = $response['wo_newparams'][$ms_server_inventory];
$object_params = current($object_ids_array);
$server_object_id = $object_params['object_id'];
$server_power_state = $object_params['power_state'];
//Import BIOS values from microservice
$response = json_decode(import_objects($device_id, array($ms_bios_params)), True);
$current_bios_parameters = $response['wo_newparams'][$ms_bios_params];


//For each required BIOS parameter check whether is required value equal the original one
$response = update_asynchronous_task_details($context, "Verifying BIOS parameters... ");
foreach ($bios_parameters as $parameter_name => &$parameter_values) {
  if ($parameter_values['was_it_changed'] === "true") {
    if (array_key_exists($parameter_name, $current_bios_parameters)) {
      $response = update_asynchronous_task_details($context, "Verifying BIOS parameters... ".$parameter_name.": Required value: ".$parameter_values['Required Value']." Current value:".$current_bios_parameters[$parameter_name]['value']."... ");
      if ($current_bios_parameters[$parameter_name]['value'] !== $parameter_values['Required Value']) {
        $modifying_failed .= $parameter_name.", ";
        $response = update_asynchronous_task_details($context, "Verifying BIOS parameters... ".$parameter_name.": Required value: ".$parameter_values['Required Value']." Current value:".$current_bios_parameters[$parameter_name]['value']."... Failed");
      } else {
        $response = update_asynchronous_task_details($context, "Verifying BIOS parameters... ".$parameter_name.": Required value: ".$parameter_values['Required Value']." Current value:".$current_bios_parameters[$parameter_name]['value']."... OK");
      }
    }
  }
}
unset($parameter_name);
unset($parameter_values);


if ($modifying_failed !== '') {
  task_error('The following BIOS params were not changed'.$modifying_failed);
} else {
  if ($server_power_state == 'On') {
    task_success('BIOS params have been changed sucessfully. Server has been turned on');
  } else {
    task_error("Server is not turned on. Current state is ".$server_power_state);
  }
}

?>