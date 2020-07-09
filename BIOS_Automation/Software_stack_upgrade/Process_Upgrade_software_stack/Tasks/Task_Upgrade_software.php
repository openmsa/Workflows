<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/Common/Library/msa_common.php';
require_once '/opt/fmc_repository/Process/F5N/Process_Upgrade_software_stack/common.php';

/*
The task identifies the following things:
 - Identify current software stack;
 - Identify upgrade stages - what intermediate upgrade steps should be performed to upgrade a server to last software;
 - Validate a possibility to perform whole upgrade cycle comparing each software dependencies one by one.  
*/


$microservices_array   = $context['microservices_array'];
$ms_software_inventory = $microservices_array['Software inventory'];
$device_id             = $context['device_id'];
$model_dir_file_path   = $context['model_dir_file_path'];

//Getting current software stack
$response = update_asynchronous_task_details($context, "Getting current software stack... ");
$context['current_sw_stack'] = $current_sw_stack = get_current_sw_stack($device_id, $ms_software_inventory);
$current_sw_version = get_version($model_dir_file_path, $current_sw_stack);
$response = update_asynchronous_task_details($context, "Getting current software stack... ".$current_sw_version);
sleep(5);

//Getting upgrade stages
$response = update_asynchronous_task_details($context, "Getting upgrade stages... ");
$context['upgrade_stages'] = $upgrade_stages = get_possible_sw_stack($model_dir_file_path, $current_sw_version);

/*
If there are upgrade stages, then validate upgrade possibility - compare prerequisities for each software component one-by-one. 
If there isn't any upgrade stage, no upgrade is needed.
*/

if (!empty($upgrade_stages)) {
  $context['is_upgrade_needed'] = "True";
  $details = $current_sw_version;
  foreach ($upgrade_stages as $stack) {
    $details .= " -> ".$stack;
  }
  $response = update_asynchronous_task_details($context, "Getting upgrade stages... ".$details);
  sleep(5);
  $response = update_asynchronous_task_details($context, "Validate possibility to upgrade... ");
  
//$stop_upgrade_array is array of software components what don't have dependencies satisfied
  $stop_upgrade_array = array();
  foreach ($upgrade_stages as $num => $new_sw_stack) {
    
    if ($num == 0) {
      $original_sw_stack = $current_sw_version;
    } else {
      $original_sw_stack = $upgrade_stages[$num-1];
    }
    
    $dependencies_array = validate_upgrade_possibility($model_dir_file_path, $original_sw_stack, $new_sw_stack);
    
    if (empty($dependencies_array)) {
      $details = "Validate possibility to upgrade...\nUpgrade dependencies from ".$original_sw_stack." to ".$new_sw_stack." have been met";
      $response = update_asynchronous_task_details($context, $details);
      sleep(5);
    } else {
      $details = "Validate possibility to upgrade... \nUpgrade dependencies from ".$original_sw_stack." to ".$new_sw_stack." have not been met for ".$dependencies_array['sw_type']."\nRequired version: ".$dependencies_array['required_version'].", but original version is ".$dependencies_array['original_version'];
      $response = update_asynchronous_task_details($context, $details);
      $stop_upgrade_array[] = array("original_stack" => $original_sw_stack, "new_stack" => $new_sw_stack, "unmet_dependencies" => $dependencies_array);
      sleep(5);   
    }
  }

//If there is not any unsatisfied dependencies, end-to-end upgrade is possible, move to next task
  if (empty($stop_upgrade_array)) {
    task_success("Validate possibility to upgrade...\nAll dependencies have been met. Move to upgrade process");
  } else {
    $wo_comment = '';
        foreach ($stop_upgrade_array as $num => $vars) {
      $wo_comment .= "Validate possibility to upgrade... \nUpgrade stage from ".$vars['original_stack']." to ".$vars['new_stack'].". The following dependencies are not met:\n". "Type: ".$vars['unmet_dependencies']['sw_type']." original version: ".$vars['unmet_dependencies']['original_version']." Required version: ".$vars['unmet_dependencies']['required_version']."\n";
    }
    task_error($wo_comment);
  }
} else {
  $context['is_upgrade_needed'] = "False";
  task_success("Getting upgrade stages...\nCurrent version is the latest one. Upgrade isn't needed.");
}


?>