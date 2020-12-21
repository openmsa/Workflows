<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/Common/Library/msa_common.php';


//Retrive variables from $context and define the new ones
$PROCESSINSTANCEID = $context['PROCESSINSTANCEID'];
$EXECNUMBER = $context['EXECNUMBER'];
$TASKID = $context['TASKID'];
$process_params = array('PROCESSINSTANCEID' => $PROCESSINSTANCEID,
                        'EXECNUMBER' => $EXECNUMBER,
                        'TASKID' => $TASKID);

if ($context['server_device'] === 'NULL') {
	$server_vendor = $context['server_vendor'];
    if ($context['mgmt_interface'] == 'REDFISH') {
	   $profile_name = $context['profile_name'] = strtolower('redfish_'.$server_vendor.'_profile');
    }
    if ($context['mgmt_interface'] == 'IPMI') {
	   $profile_name = $context['profile_name'] = strtolower('ipmi_'.$server_vendor.'_profile');
    }
	$device_id = $context['device_id'];
	$device_external_reference = $context['device_external_reference'];
	
	$response = update_asynchronous_task_details($context, "Attaching configuration profile... ");
    
    
    //Retrive all configuration profiles of the customer and find out the one what has same name as required
  	//Extract numeric customer ID
	if (preg_match('/.{3}\D*?(\d+)/', $context['UBIQUBEID'], $matches) === 1) {
		$customer_db_id = $context['customer_db_id'] = $matches[1];
	} else {
		$customer_db_id = $context['customer_db_id'] = -1;
	}
	
    $profile_list = _profile_configuration_list_by_customer_id($customer_db_id);
    $profile_reference = $context['profile_reference'] = 'NULL';
    logToFile(debug_dump($profile_list, 'DEBUG: Profile list'));
    foreach ($profile_list as $profile_number => $profile_details) {
    	if ($profile_details['name'] === $profile_name) {
          $profile_reference = $context['profile_reference'] = $profile_details['externalReference'];
        }
    }
	
	//Attach configuration profile to managed device if reference has been found
  if ($profile_reference != 'NULL') {
	$response = json_decode(_profile_attach_to_device_by_reference ($profile_reference, $device_external_reference), True);
	if ($response['wo_status'] !== ENDED) {
	  echo $response;
	}
  } else {
    task_failed("Configration profile not found");
  }

	$response = update_asynchronous_task_details($context, "Attaching configuration profile... OK");
	sleep(3);
	
	$response = update_asynchronous_task_details($context, "Activating managed entity... ");
	
	//Make initial provisioning
	$response = json_decode(_device_do_initial_provisioning_by_id($device_id), True);
	if ($response['wo_status'] !== ENDED) {
	  echo $response;
	  exit;
	}
	
	//Wait when provisioning will be completed
	$response = json_decode(wait_for_provisioning_completion($device_id, $process_params), True);
	if ($response['wo_status'] !== ENDED) {
	  echo json_encode($response);
	  exit;
	}
	
	$response = update_asynchronous_task_details($context, "Activating managed entity... OK");
	sleep(3);
	
	//Waiting until the managed device will be finally avaliable
	$response = json_decode(wait_for_device_reachability ($device_id, $process_params, $timeout = DEVICE_STATUS_CHANGE_TIMEOUT), True);
	if ($response['wo_status'] !== ENDED) {
	  echo $response;
	  exit;
	}
	
	sleep (30);
	
	$response = update_asynchronous_task_details($context, "Managed entity syncing... ");
	
	//Sync up the ME MSs
	$response = json_decode(synchronize_objects_and_verify_response($device_id), true);
	if ($response['wo_status'] !== ENDED) {
	  echo $response;
	  exit;
	}
	
	//Sync up the referenced MSs
	$response = json_decode(synchronize_objects_and_verify_response($device_id), true);
	if ($response['wo_status'] !== ENDED) {
	  echo $response;
	  exit;
	}
	
	$response = update_asynchronous_task_details($context, "Managed entity syncing... OK");
	sleep(3);
	  
	task_success("Managed Entity $device_id is activated and reachable.");
} else {
  task_success("Managed Entity  is already activated.");
}
	
?>