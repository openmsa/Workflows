<?php
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

//Grab variable from context
$device_id = $context['device_id'];

//Retrive variables from $context and define the new ones
$PROCESSINSTANCEID = $context['PROCESSINSTANCEID'];
$EXECNUMBER = $context['EXECNUMBER'];
$TASKID = $context['TASKID'];
$process_params = array('PROCESSINSTANCEID' => $PROCESSINSTANCEID,
                        'EXECNUMBER' => $EXECNUMBER,
                        'TASKID' => $TASKID);

//Extract numeric customer ID
if (preg_match('/.{3}\D*?(\d+)/', $context['UBIQUBEID'], $matches) === 1) {
	$customer_db_id = $context['customer_db_id'] = $matches[1];
} else {
	$customer_db_id = $context['customer_db_id'] = -1;
}

if ($context['do_import_hosts']) {
	$announce = update_asynchronous_task_details($context, "Extract host list from ansible server... ");
	
	//Sync microservices
	$response = json_decode(synchronize_objects_and_verify_response($device_id), true);
	if ($response['wo_status'] !== ENDED) {
	       $response = json_encode($response);
	       echo $response;
	       exit;
	}
	
	$response = json_decode(import_objects($device_id, array('Read_hosts_file')), True);
	$object_ids_array = $response['wo_newparams']['Read_hosts_file'];
	
	foreach ($object_ids_array as $object => $object_details) {
	  $host_group_name = $object_details['object_id'];
	  foreach ($object_details['host_list'] as $index => $host_detials) {
	    $host_name = $host_detials['host'];
	    $host_username = $host_detials['ansible_user'];
	    $host_password = $host_detials['ansible_ssh_pass'];
	    $me_name = $host_group_name.'['.$host_name.']';
	    $me_ext_reference = hash('crc32', md5($me_name));
	    $response = json_decode(_device_create($customer_db_id,
			   			      			       $me_name,
	                                           $context['linux_manufacturer_id'],
			   			      			       $context['linux_model_id'],
			   			      			       $host_username,
			   			      			       $host_password,
	                                           $host_password,
			   			      			       $host_name,
			   			      			       $me_ext_reference,
		                                   	   "true",
		                                   	   "true",
		                                   	   "true",
		                                   	   "true",
		                                   	   "public",
	    	                               	   "",
	    	                               	   '22'
			 			  					                  ), 
	    	                       True);
	      if ($response['wo_status'] !== ENDED) {
			$response = json_encode($response);
			echo $response;
			exit;
		  }
		
		
		  //Extract device id and put into $context()
		  $host_device_id = $response['wo_newparams']['entity']['id'];
	      //Gather Device ID (numeric) from procvided ID
	      preg_match("/\S*?(?<device_id>\d+?)$/", $host_device_id, $matches);
	      $host_device_id = $matches['device_id'];
	    
	      //Retrive all configuration profiles of the customer and find out the one what has same name as required
	      $profile_list = _profile_configuration_list_by_customer_id($customer_db_id);
	      $profile_reference = 'NULL';
	      foreach ($profile_list as $profile_number => $profile_details) {
	      	if ($profile_details['name'] === $context['linux_profile_name']) {
	            $profile_reference = $context['profile_reference'] = $profile_details['externalReference'];
	          }
	      }
		
		//Attach configuration profile to managed device if reference has been found
	    if ($profile_reference != 'NULL') {
		   $response = json_decode(_profile_attach_to_device_by_reference ($profile_reference, $me_ext_reference), True);
		   if ($response['wo_status'] !== ENDED) {
		      echo $response;
		   }
	    } else {
	       task_failed("Configration profile is has not been found");
	    }
	
		$response = update_asynchronous_task_details($context, "Attaching configuration profile... OK");
		sleep(3);
		
		$response = update_asynchronous_task_details($context, "Activating device... ");
		
		//Make initial provisioning
		$response = json_decode(_device_do_initial_provisioning_by_id($host_device_id), True);
		if ($response['wo_status'] !== ENDED) {
		  echo $response;
		  exit;
		}
	    
	  }
	}
	
	$announce = update_asynchronous_task_details($context, "Extract host list from ansible server... OK");
	
	//Finish the task
	task_success('Success. Ansible host are imported.');
} else {
	task_success('Success. Host import is not needed.');
}
?>