<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/Common/Library/msa_common.php';

//Retrive variables from $context and define the new ones

$device_id = $context['device_id'];
$bios_parameters = $context['bios_parameters_array'];
$microservices_array = $context['microservices_array'];
$ms_server_inventory = $microservices_array['Server inventory'];
$ms_server_power = $microservices_array['Server power managment'];

//Check current server power state (should be Off), but smthg could happen
//Import current server power state
$response = update_asynchronous_task_details($context, "Checking server current power state... ");
$response = json_decode(import_objects($device_id, array($ms_server_inventory)), True);
$object_ids_array = $response['wo_newparams'][$ms_server_inventory];
$object_params = current($object_ids_array);
$server_object_id = $object_params['object_id'];
$server_power_state = $object_params['power_state'];
$response = update_asynchronous_task_details($context, "Checking server current power state... ".$server_power_state);
if ($server_power_state === 'Off') {
	$action = 'ForceOn';
  	$response = update_asynchronous_task_details($context, "Checking server current power state... ".$server_power_state." Lets use ".$action);
	$micro_service_vars_array = array ();
	$micro_service_vars_array ['object_id'] = $action;
	$micro_service_vars_array ['action'] = $action;
	$ms_array = array($ms_server_power => array ($action => $micro_service_vars_array));
	$response = json_decode(execute_command_and_verify_response ( $device_id, CMD_CREATE, $ms_array, "CREATE server power state  - ".$action ), True);
    if ($response['wo_status'] !== ENDED) {
        $response = json_encode($response);
        echo $response;
        exit;
    }
} else {
	$action = 'ForceRestart';
  	$response = update_asynchronous_task_details($context, "Checking server current power state... ".$server_power_state." Lets use ".$action);
	$micro_service_vars_array = array ();
	$micro_service_vars_array ['object_id'] = $action;
	$micro_service_vars_array ['action'] = $action;
	$ms_array = array($ms_server_power => array ($action => $micro_service_vars_array));
	$response = json_decode(execute_command_and_verify_response ( $device_id, CMD_CREATE, $ms_array, "CREATE server power state - ".$action), True);
    if ($response['wo_status'] !== ENDED) {
        $response = json_encode($response);
        echo $response;
        exit;
    }
}

task_success('The server has been rebooted. BIOS parameters will be verified next.');

?>