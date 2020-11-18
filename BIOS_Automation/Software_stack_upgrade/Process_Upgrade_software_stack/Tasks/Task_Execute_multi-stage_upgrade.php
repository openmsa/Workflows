<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/Common/Library/msa_common.php';
require_once '/opt/fmc_repository/Process/BIOS_Automation/Software_stack_upgrade/Process_Upgrade_software_stack/common.php';

/*
The task performs upgrade process for each stage.
Dependencies between components are chacked on each upgrade stage
*/

$microservices_array   = $context['microservices_array'];
$ms_software_inventory = $microservices_array['Software inventory'];
$device_id             = $context['device_id'];
$model_dir_file_path   = $context['model_dir_file_path'];
$current_sw_stack = $context['current_sw_stack'];

if ($context['is_upgrade_needed'] === "False") {
  task_success('Upgrade is not needed');
}

$upgrade_stages       = $context['upgrade_stages'];
ksort($upgrade_stages);

//Loop through upgrade stages
foreach ($upgrade_stages as $num => $stack_version) {
  $prefix = "PREPARING UPGRADE...\n";
  
//Extract current software stack
  $response = update_asynchronous_task_details($context, $prefix."Getting current software stack... ");
  $current_sw_version = get_version($model_dir_file_path, $current_sw_stack);
  $details = $prefix."Current software stack is ".$current_sw_version;
  $response = update_asynchronous_task_details($context, $details);
  sleep(5);
  
//Identify current upgrade stage
  $prefix = "UPGRADE IN PROGRESS | ".$current_sw_version." -> ".$stack_version."\n";

//Check dependencies between current software stack and next software stack
  $details = $prefix."Checking dependencies... ";
  $response = update_asynchronous_task_details($context, $details);
  sleep(5);  
  $prerequisite_check = check_prerequisites($model_dir_file_path.$stack_version, $current_sw_stack);
  
//If a software component dependencies isn't satisfied, do not go to upgrade
  $go_upgrade = "True";
  foreach ($prerequisite_check as $sw_type => $vars) {
    if (!empty($vars)) {
      if ($vars['is_prerequisite_met'] === "False") {
        $go_upgrade = "False";
      }
    }
  }

//If all dependencies are satisfied, start upgrade process for each software component in stack   
  if ($go_upgrade) {
    $details = $prefix."Dependencies have been met. Starting upgrade ".$current_sw_version;
    $response = update_asynchronous_task_details($context, $details);
    sleep(5);  
    $upgrade_array = prepare_upgrade($prerequisite_check, $model_dir_file_path.$stack_version);
    make_upgrade($prefix, $context, $upgrade_array, $model_dir_file_path.$stack_version);
  }
  if ($context['is_emulation'] === "True") {
    $current_sw_stack = get_current_sw_stack_fake($prerequisite_check);
  } else {
    $current_sw_stack = get_current_sw_stack($device_id, $ms_software_inventory);
  }

}


$context['current_sw_stack'] = $current_sw_stack;
task_success($prefix.'Upgrade process has been finished. Move to validation step.');
?>