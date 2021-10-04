<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/Common/Library/msa_common.php';

//Retrive variables from $context and define the new ones
$microservices_array = $context['microservices_array'];
$ms_server_inventory = $microservices_array['Server inventory'];
$ms_server_power = $microservices_array['Server power managment'];
$device_id = $context['device_id'];
//How much we are waiting 
$delay = 15;

if (array_key_exists('Job manager', $microservices_array)) {
    $ms_job_manager = $microservices_array['Job manager']; 
}


#Check unfinished BIOS configuration jobs
if ($context['job_management'] == 'True') {
    $are_all_job_completed = True;
    $response = update_asynchronous_task_details($context, "Check existed BIOS jobs... ");
    $response = json_decode(import_objects($device_id, array($ms_job_manager)), True);
    if (array_key_exists($ms_job_manager, $response['wo_newparams'])) {
    	$current_job = $response['wo_newparams'][$ms_job_manager];
    	foreach ($current_job as $job_name => $job_params) {
      	  if (array_key_exists('type', $job_params) and array_key_exists('state', $job_params)) {
      		if ($job_params['type'] == 'BIOSConfiguration' and $job_params['state'] != 'Completed') {
        			$are_all_job_completed = False;
      		}
      	  }
    	}
    }
  if (!$are_all_job_completed) {
    task_error('Server has some BIOS configuration jobs unfinished. Please review the jobs and finish them before to start the workflow again.');
  }
}


//Import current server power state
$response = update_asynchronous_task_details($context, "Import current power state... ");
$response = json_decode(import_objects($device_id, array($ms_server_inventory)), True);
$object_ids_array = $response['wo_newparams'][$ms_server_inventory];
$object_params = current($object_ids_array);
$server_object_id = $object_params['object_id'];
$server_power_state = $object_params['power_state'];
$response = update_asynchronous_task_details($context, "Import current power state... ".$server_power_state);

//Shutdown server if it is turned on now
if (strtolower($server_power_state) !== 'off') {
	$response = update_asynchronous_task_details($context, "Import current power state... ".$server_power_state." Shutting down...");
	if ($context['mgmt_interface'] == 'REDFISH') {
       $action = 'ForceOff';
    }
    if ($context['mgmt_interface'] == 'IPMI') {
       $action = 'off';
    }
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
	$response = update_asynchronous_task_details($context, "Import current power state... ".$server_power_state." Shutting down... OK");
  
	$response = update_asynchronous_task_details($context, "Waiting ".$delay." seconds to be sure that server has been shutted down properlly");
    //Sleep $delay seconds to be sure that server has been gone down
	sleep($delay);

	//Sync microservices
	$response = json_decode(synchronize_objects_and_verify_response($device_id), true);
	if ($response['wo_status'] !== ENDED) {
        $response = json_encode($response);
        echo $response;
        exit;
	}
  
  	//Sync refernced MSs
	$response = json_decode(synchronize_objects_and_verify_response($device_id), true);
	if ($response['wo_status'] !== ENDED) {
        $response = json_encode($response);
        echo $response;
        exit;
	}

	//Retrive server power status again
	$response = json_decode(import_objects($device_id, array($ms_server_inventory)), True);
	$object_ids_array = $response['wo_newparams'][$ms_server_inventory];
	$object_params = current($object_ids_array);
	$server_object_id = $object_params['object_id'];
	$server_power_state = $object_params['power_state'];
}


if (strtolower($server_power_state) === 'off') {
	task_success('Server is shutted down now');
} else {
	task_error('Server is staying up');
}

?>