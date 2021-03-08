<?php
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';


if ($context['do_monitor_changes'] !== 'false') {
	$microservice_name_prefix = $context['microservice_name_prefix'];
	$microservice_file = $context['read_playbook_file'];
	$microservice_name = $context['microservice_name'];
	$variable_skeleton = $context['variable_skeleton'];
	$microservice_skeleton = $context['microservice_skeleton'];
	$microservice_dir = $context['microservice_dir'];
	$device_id = $context['device_id'];
	$processName = $context['processName'];
	$service_id = $context['service_id'];
	$ubiqube_id = $context['UBIQUBEID'];
	$playbook_attributes_array = $context['playbook_attributes_array'];
	$do_monitor_changes = True;
	$monitoring_delay = $context['monitoring_delay'];
} else {
    $do_monitor_changes = False;
}


while ($do_monitor_changes) {
  
  //Syncing Ansible host
  $announce = update_asynchronous_task_details($context, "Syncing Ansible host... ");
  $response = json_decode(synchronize_objects_and_verify_response($device_id), true);
  sleep(15);
  if ($response['wo_status'] !== ENDED) {
 		echo json_encode($response);
 		exit;
  }
  $response = json_decode(import_objects($device_id, array('Retrieve_playbook_files_list')), True);
  $object_ids_array = $response['wo_newparams']['Retrieve_playbook_files_list'];
  $announce = update_asynchronous_task_details($context, "Syncing Ansible host... OK");
  
  /*
  Iterate each playbook. If the playbook exists in $context, then check md5 sum next.
  If md5 sums are different, it means the file was changed. In the case new MS is created.
  If there isnt the file in $context, then it is new file, we create new microservice.
  */
  foreach ($object_ids_array as $object_id => $object_details) {
  	$announce = update_asynchronous_task_details($context, "Checking file ".$object_details['object_id'].'... ');
    if (array_key_exists(md5($object_details['object_id']), $playbook_attributes_array)) {
      //The file already exists, check md5 sum
      if ($object_details['md5sum'] !== $playbook_attributes_array[md5($object_details['object_id'])]['playbook_attributes']['md5sum']) {
        //The file was changed, create new microservice.
        $announce = update_asynchronous_task_details($context, "Checking file ".$object_details['object_id'].'... file was modifyed. Create new microservice...');
        $playbook_attributes_array[md5($object_details['object_id'])]['playbook_attributes']['md5sum'] = $object_details['md5sum'];
        $attributes_to_create_microservice = array('playbook'               => $playbook_attributes_array[md5($object_details['object_id'])]['playbook_attributes']['path'],
                                                   'microservice_name'      => $playbook_attributes_array[md5($object_details['object_id'])]['microservice_attributes']['name'],
                                                   'microservice_skeleton' => $microservice_skeleton
                                                 );
 
        $result = _orchestration_launch_process_instance($ubiqube_id, $service_id, $processName, json_encode($attributes_to_create_microservice));
        sleep(15);
      $announce = update_asynchronous_task_details($context, "Checking file ".$object_details['object_id'].'... file was modifyed. Create new microservice... DONE');
        
      }
    } else {
      //This is new file, create new micorservice
      $announce = update_asynchronous_task_details($context, "Checking file ".$object_details['object_id'].'... new file. Create new microservice...');
      //Create new microservice
      $playbook_attributes_array[md5($object_details['object_id'])] = array('playbook_attributes' => array(),
                                                                            'microservice_attributes' => array()
                                                                            );
      $playbook_attributes_array[md5($object_details['object_id'])]['playbook_attributes']['path'] = $object_details['object_id'];
      $playbook_attributes_array[md5($object_details['object_id'])]['playbook_attributes']['md5sum'] = $object_details['md5sum'];
   
   
      //Create microservice name
      $result = preg_match('|^(\S+?)([^/]+?\.yml)|', $object_details['object_id'], $matches);
      $playbook_microservice_name = $microservice_name_prefix.' (based on '.str_replace('.yml', '', $matches[2]).')';
      $playbook_attributes_array[md5($object_details['object_id'])]['microservice_attributes']['name'] = $playbook_microservice_name;
     
      //Gather microservice skeleton path and name
      $result = preg_match('|^(\S+?)([^/]+?\.xml)|', $microservice_skeleton, $matches);
      $microservice_skeleton_path = $matches[1];
      $microservice_skeleton_name = $matches[2];
      //Sanitize file name
      $playbook_microservice_file_name = $playbook_microservice_name;
      $playbook_microservice_file_name = preg_replace('/[| @()]/', '_', $playbook_microservice_file_name).'.xml';
      $playbook_attributes_array[md5($object_details['object_id'])]['microservice_attributes']['file_name'] = $playbook_microservice_file_name;
      $playbook_attributes_array[md5($object_details['object_id'])]['microservice_attributes']['path'] = $microservice_dir.$playbook_microservice_file_name;
   
      $attributes_to_create_microservice = array('playbook'           => $playbook_attributes_array[md5($object_details['object_id'])]['playbook_attributes']['path'],
                                                 'microservice_name'      => $playbook_attributes_array[md5($object_details['object_id'])]['microservice_attributes']['name'],
                                                 'microservice_skeleton' => $microservice_skeleton
                                                );
 
      $result = _orchestration_launch_process_instance($ubiqube_id, $service_id, $processName, json_encode($attributes_to_create_microservice));
      sleep(15);
      $announce = update_asynchronous_task_details($context, "Checking file ".$object_details['object_id'].'... new file. Create new microservice... DONE');
    }
  }
  $context['playbook_attributes_array'] = $playbook_attributes_array;
  $announce = update_asynchronous_task_details($context, "Sleeping ".$monitoring_delay."... ");
  sleep($monitoring_delay);
  $announce = update_asynchronous_task_details($context, "Sleeping ".$monitoring_delay."... OK");
  $do_monitor_changes = $context['do_monitor_changes'];
}

//Finish task
task_success('Success. Monitoring has been stopped');
?>