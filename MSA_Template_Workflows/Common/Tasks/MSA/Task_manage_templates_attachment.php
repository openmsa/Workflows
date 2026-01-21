<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args()
{
	create_var_def('position', 'String');
}

check_mandatory_param('position');

$response = _orchestration_get_process_instance($context['PROCESSINSTANCEID']);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}
$process_name = $response['wo_newparams']['processId']['name'];
$template_name = substr($process_name, strpos($process_name, "Process_") + 8);
$context['template_name'] = $template_name;

$current_template_uri = "";
$msa_templates = $context['msa_templates'];
foreach ($msa_templates as $index => $element) {
	$uri = $element['uri'];
	if (strpos($uri, $template_name) !== false) {
		$current_template_uri = $uri;
		break;
	}
}

$device_id = substr($context['device_id'], 3);
$response = _device_configuration_list_files_by_id($device_id);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}

$attached_msa_templates_index = 0;
foreach ($response['wo_newparams'] as $uri) {
	if (strpos($uri, "Configuration") === 0) {
		$context['attached_msa_templates'][$attached_msa_templates_index++]['uri'] = $uri;
		$response = _device_configuration_detach_file_from_device($device_id, $uri);
		$response = json_decode($response, true);
		if ($response['wo_status'] !== ENDED) {
			$response = json_encode($response);
			echo $response;
			exit;
		}
	}
}

$response = _device_configuration_attach_file_to_device($device_id, "Configuration/{$current_template_uri}", $context['position']);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}

$response = prepare_json_response(ENDED, "Template $template_name attached successfully to the device", $context, true);
echo $response;

?>
