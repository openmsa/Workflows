<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/Common/Library/msa_common.php';

//Retrive variables from $context and define the new ones
$delay = 5;
$bios_parameters = $context['bios_parameters_array'];
$device_id = $context['device_id'];
$microservices_array = $context['microservices_array'];
$ms_bios_params = $microservices_array['BIOS parameters manipulation'];

//Rollback to original value each parameter what has was_it_changed true
foreach ($bios_parameters as $parameter_name => $parameter_values) {
	if ($parameter_values['was_it_changed'] === "true") {

		$micro_service_vars_array = array ();
		$micro_service_vars_array ['object_id'] = $parameter_name;
		$micro_service_vars_array ['value'] = $parameter_values['Original Value'];
		$ms_array = array($ms_bios_params => array ($parameter_name => $micro_service_vars_array));
		$response = json_decode(execute_command_and_verify_response ( $device_id, CMD_UPDATE, $ms_array, "UPDATE BIOS parameter ".$parameter_name." to ".$parameter_values['Original Value']), True);
    	if ($response['wo_status'] !== ENDED) {
    	    $response = json_encode($response);
    	    echo $response;
    	    exit;
    	}
	}
	sleep($delay);
}

task_success('BIOS parameters have been changed succesfully. Server will be rebooted');

?>