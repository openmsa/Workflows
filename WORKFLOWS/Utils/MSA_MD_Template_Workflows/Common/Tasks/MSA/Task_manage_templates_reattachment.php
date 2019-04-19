<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args()
{
}

$devices = $context['devices'];

foreach ($devices as $device){
	$device_name = $device['device_id'];
	$device_id = substr($device['device_id'], 3);
	
	if(!isset($context['attached_msa_templates'][$device_name])) {
		continue;
	}
	$attached_msa_templates = $context['attached_msa_templates'][$device_name];

	foreach ($attached_msa_templates as $attached_msa_template) {
		/**
		 * TODO : Is there a way to get each attached template's position ?
		 * =====> If yes, then change "AUTO" with respective position of each template
		 */
		logToFile("".print_r($attached_msa_template, true));
		$response = _device_configuration_attach_file_to_device($device_id, $attached_msa_template['uri'], "AUTO");
		$response = json_decode($response, true);
		if ($response['wo_status'] !== ENDED) {
			$response = json_encode($response);
			echo $response;
			exit;
		}
	}
}

$response = prepare_json_response(ENDED, "Original Templates attached successfully to the device", $context, true);
echo $response;

?>
