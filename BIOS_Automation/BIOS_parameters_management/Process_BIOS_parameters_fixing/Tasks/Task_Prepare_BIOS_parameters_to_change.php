<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/Common/Library/msa_common.php';

//Retrive variables from $context and define the new ones
$change_candidate = '';
$bios_parameters = $context['bios_parameters_array'];
$device_id = $context['device_id'];
$microservices_array = $context['microservices_array'];
$ms_bios_params = $microservices_array['BIOS parameters manipulation'];


//Import BIOS values from microservice
$response = update_asynchronous_task_details($context, "Importing BIOS parameters... ");
$response = json_decode(import_objects($device_id, array($ms_bios_params)), True);
$current_bios_parameters = $response['wo_newparams'][$ms_bios_params];
$response = update_asynchronous_task_details($context, "Importing BIOS parameters... OK");
sleep(3);

//For each required BIOS parameter check whether is required value equal the original one
$response = update_asynchronous_task_details($context, "Identify BIOS parameters to change... ");
foreach ($bios_parameters as $parameter_name => &$parameter_values) {
	if (array_key_exists($parameter_name, $current_bios_parameters)) {
		$parameter_values['Original Value'] = $current_bios_parameters[$parameter_name]['value'];
		if ($parameter_values['Original Value'] !== $parameter_values['Required Value']) {
			$parameter_values['was_it_changed'] = "true";
			$change_candidate .= $parameter_name.", ";
		}
	}
}
unset($parameter_name);
unset($parameter_values);
$response = update_asynchronous_task_details($context, "Identify BIOS parameters to change... OK");
sleep(3);

//Update array in $context
$context['bios_parameters_array'] = $bios_parameters;

if ($change_candidate) {
	task_success("There are following BIOS options will be changed:\n".$change_candidate);
} else {
	task_success("All BIOS options are in reqiured state\n");
}

?>