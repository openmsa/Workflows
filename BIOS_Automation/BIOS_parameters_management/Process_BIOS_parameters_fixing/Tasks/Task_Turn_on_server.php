<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/Common/Library/msa_common.php';


//Retrive variables from $context and define the new ones
$device_id = $context['device_id'];
$microservices_array = $context['microservices_array'];
$ms_server_inventory = $microservices_array['Server inventory'];
$ms_server_power = $microservices_array['Server power managment'];

//Check current server power state (should be Off), but smthg happens
//Import current server power state
$response = json_decode(import_objects($device_id, array($ms_server_inventory)), True);
$object_ids_array = $response['wo_newparams'][$ms_server_inventory];
$object_params = current($object_ids_array);
$server_object_id = $object_params['object_id'];
$server_power_state = $object_params['power_state'];


if ($server_power_state !== 'Off') {
	$action = 'ForceRestart';
	$micro_service_vars_array = array ();
	$micro_service_vars_array ['object_id'] = $action;
	$micro_service_vars_array ['action'] = $action;
	$ms_array = array($ms_server_power => array ($action => $micro_service_vars_array));
	
	$response = json_decode(execute_command_and_verify_response ( $device_id, CMD_CREATE, $ms_array, "CREATE server power state - ".$action ), True);
    if ($response['wo_status'] !== ENDED) {
        $response = json_encode($response);
        echo $response;
        exit;
    	} 
    } else {
    	$action = 'ForceOn';
		$micro_service_vars_array = array ();
		$micro_service_vars_array ['object_id'] = $action;
		$micro_service_vars_array ['action'] = $action;
		$ms_array = array($ms_server_power => array ($action => $micro_service_vars_array));
		$response = json_decode(execute_command_and_verify_response ( $device_id, CMD_CREATE, $ms_array, "CREATE 	server power state  - ".$action ), True);
    	if ($response['wo_status'] !== ENDED) {
    	    $response = json_encode($response);
    	    echo $response;
    	    exit;
    }
}

task_success('Server has been turned on. Modify default BMC password next');

?>