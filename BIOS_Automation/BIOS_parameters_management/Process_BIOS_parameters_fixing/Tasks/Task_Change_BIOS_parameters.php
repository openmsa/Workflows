<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/Common/Library/msa_common.php';

//Retrive variables from $context and define the new ones
$delay = 5;
$bios_parameters = $context['bios_parameters_array'];
$device_id = $context['device_id'];
$microservices_array = $context['microservices_array'];
$ms_bios_params = $microservices_array['BIOS parameters manipulation'];
if (array_key_exists('Job manager', $microservices_array)) {
    $ms_job_manager = $microservices_array['Job manager']; 
}

if ($context['are_changes_needed'] == 'true') {
   //Change BIOS parameters for each parameter what has was_it_changed is True
   $response = update_asynchronous_task_details($context, "Modyfing BIOS parameters... ");
   foreach ($bios_parameters as $parameter_name => $parameter_values) {
   	if ($parameter_values['was_it_changed'] === "true") {
   		$response = update_asynchronous_task_details($context, "Modyfing BIOS parameters... ".$parameter_name."... ");
   		$micro_service_vars_array = array ();
   		$micro_service_vars_array ['object_id'] = $parameter_values['Object ID'];
           $micro_service_vars_array ['name'] = $parameter_name;
   		$micro_service_vars_array ['value'] = $parameter_values['Required Value'];
   		$ms_array = array($ms_bios_params => array ($parameter_values['Object ID'] => $micro_service_vars_array));
   		$response = json_decode(execute_command_and_verify_response ( $device_id, CMD_UPDATE, $ms_array, "UPDATE BIOS parameter ".$parameter_name." to ".$parameter_values['Required Value']), True);
       	if ($response['wo_status'] !== ENDED) {
       	    $response = json_encode($response);
       	    echo $response;
       	    exit;
       	}
         $response = update_asynchronous_task_details($context, "Modyfing BIOS parameters... ".$parameter_name."... OK");
   	}
   	sleep($delay);
       if ($context['mgmt_interface'] == 'IPMI') {
         $response = json_decode(synchronize_objects_and_verify_response($device_id), true);
         if ($response['wo_status'] !== ENDED) {
           $response = json_encode($response);
           echo $response;
           exit;
         }
       }
   }
   
   //Check if the paticular Redfish API implementation uses job manager to modify BIOS parameters
   if ($context['job_management'] == 'True') {
   		#Create new job for BIOS configuration
   			$response = update_asynchronous_task_details($context, "Creating Job... ");
   			$micro_service_vars_array = array ();
   			$micro_service_vars_array ['object_id'] = 'job';
   			$micro_service_vars_array ['type'] = 'BIOSConfiguration';
   			$ms_array = array($ms_job_manager => array ('job' => $micro_service_vars_array));
   			$response = json_decode(execute_command_and_verify_response ( $device_id, CMD_CREATE, $ms_array, "CREATE new job"), True);
       		if ($response['wo_status'] !== ENDED) {
       		    $response = json_encode($response);
       		    echo $response;
       		    exit;
       		}
   
       	$response = update_asynchronous_task_details($context, "Creating Job... OK");
       	sleep(3);
   
       	$response = update_asynchronous_task_details($context, "Verifying Job... ");
       	//Syncing microservices
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
   
   		$response = json_decode(import_objects($device_id, array($ms_job_manager)), True);
   		$current_job = $response['wo_newparams'][$ms_job_manager];
   
   		$is_job_scheduled = False;
   		foreach ($current_job as $job_name => $job_params) {
   			if ($job_params['type'] == 'BIOSConfiguration' and $job_params['state'] == 'Scheduled') {
   				$is_job_scheduled = True;
   			}
   
   		}
   
   		if ($is_job_scheduled) {
   			$response = update_asynchronous_task_details($context, "Verifying Job... OK");
   		} else {
     			task_error("A job to update BIOS parameters was not created successfully.");
   		}
   }
   task_success('BIOS parameters have been changed succesfully. Server will be rebooted');
} else {
   task_success('No changes are needed.');
}

?>