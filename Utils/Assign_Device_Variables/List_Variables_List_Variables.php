<?php


require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/Common/Library/msa_common.php';


/*
The process recieves server IP and MAC address as parameters
*/
function list_args()
{
}

unset($context['variables']);

$device_id = $context['device_id'];

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
		logToFile(debug_dump($context, "CONTEXT: \n"));

task_success('The variable listed in process log file');

?>