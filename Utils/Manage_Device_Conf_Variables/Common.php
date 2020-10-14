<?php


require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/Common/Library/msa_common.php';
require_once 'Common.php';


function update_var_array($device_id)
{
	global $context;

	$response = _configuration_variable_list ($device_id);
	logToFile(debug_dump($response, "VAR LIST\n"));

	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		echo $response;
		exit();
	}
	if (isset($response['wo_newparams']) && ! empty($response['wo_newparams'])) {
	$index = 0;
	foreach ($response['wo_newparams'] as &$conf_variable) {
			$name = $conf_variable['name'];
			$value = $conf_variable['value'];
			$context['variables'][$index]['name'] = $name;
			$context['variables'][$index]['value'] = $value;
			$index++;
		}
	}
}
