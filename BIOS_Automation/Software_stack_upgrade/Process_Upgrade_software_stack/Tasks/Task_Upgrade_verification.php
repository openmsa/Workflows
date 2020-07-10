<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/Common/Library/msa_common.php';
require_once '/opt/fmc_repository/Process/BIOS_Automation/Software_stack_upgrade/Process_Upgrade_software_stack/common.php';

/*
The task performs upgrade validation comparing latest software version and cthe current ones one-by-one
*/


$microservices_array   = $context['microservices_array'];
$ms_software_inventory = $microservices_array['Software inventory'];
$device_id             = $context['device_id'];
$model_dir_file_path   = $context['model_dir_file_path'];


if ($context['is_upgrade_needed'] === "False") {
  task_success('Verification is not needed');
}

$upgrade_stages       = $context['upgrade_stages'];
ksort($upgrade_stages);
//Grab current software stack
$response = update_asynchronous_task_details($context, "Getting current software stack... ");
if ($context['is_emulation'] === 'true') {
    $current_sw_stack = $context['current_sw_stack'];    
} else {
    $current_sw_stack = get_current_sw_stack($device_id, $ms_software_inventory);
}
$current_sw_version = get_version($model_dir_file_path, $current_sw_stack);
$response = update_asynchronous_task_details($context, "Getting current software stack... ".$current_sw_version);
sleep(5);

//Grab latest stack version and validate each software component version one by one
$latest_stack = rtrim(file_get_contents($model_dir_file_path."latest"));
if ($latest_stack === $current_sw_version) {
 	$response = update_asynchronous_task_details($context, "Current stack is latest. Verify software one by one...");
 	sleep(5);
 	$stack_description_path = $model_dir_file_path.$current_sw_version."/stack_description.json";
 	$stack_description = json_decode(file_get_contents($stack_description_path), True);
 	$temp_array = array();
  	foreach ($current_sw_stack as $sw_type => $version) {
		$response = update_asynchronous_task_details($context, "Current stack is latest. Verifying ".$sw_type."... ");
		sleep(2);
    	reset($stack_description['components']);
    	while ((list($num, $properties) = each($stack_description['components']) and empty($temp_array))) {
    		if ($properties['type'] === $sw_type) {
    			if ($properties['version'] !== $version) {
    				$response = update_asynchronous_task_details($context, "Current stack is latest. Verifying ".$sw_type."... NOT OK");
    				sleep(2);
    				$temp_array[$sw_type] = array('current_version' => $version, 'stack_version' => $properties['version']);
    			} else {
    				$response = update_asynchronous_task_details($context, "Current stack is latest. Verifying ".$sw_type."... OK");
    				sleep(2);
    			}
    		}
		}
	}
	if (empty($temp_array)) {
		task_success("Server upgrade to last software stack ".$current_sw_version." sucessfully.");
	} else {
		$string = "Some software components are not upgraded sucessfully:\n";
		foreach ($temp_array as $sw_type => $vars) {
			$string .= "Software ".$sw_type.": Current version is ".$vars['current_version'].", but stack version is ".$vars['stack_version'];
		}
		task_error($string);
	}
} else {
	task_error("Upgrade has not been finished sucessfully. Current stack is".$current_sw_version.", but latest stack is ".$latest_stack);
}

?>