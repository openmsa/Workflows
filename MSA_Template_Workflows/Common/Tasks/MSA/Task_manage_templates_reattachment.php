<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args()
{
}

$device_id = substr($context['device_id'], 3);
$attached_msa_templates = $context['attached_msa_templates'];

foreach ($attached_msa_templates as $attached_msa_template) {
	/**
	 * TODO : Is there a way to get each attached template's position ?
	 * =====> If yes, then change "AUTO" with respective position of each template
	 */
	$response = _device_configuration_attach_file_to_device($device_id, $attached_msa_template['uri'], "AUTO");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		echo $response;
		exit;
	}
}

$response = prepare_json_response(ENDED, "Original Templates attached successfully to the device", $context, true);
echo $response;

?>
