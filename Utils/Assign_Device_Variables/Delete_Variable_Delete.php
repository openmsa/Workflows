<?php


require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/Common/Library/msa_common.php';


function list_args()
{
  create_var_def('variable_name', 'String');
}


$device_id = $context['device_id'];
$variable_name = $context['variable_name'];
$variable_value = $context['variable_value'];

_configuration_variable_delete ($device_id, $variable_name);

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
task_success('The variable '.$variable_name.' with value '.$variable_value.' has been successfully deleted from device '.$device_id.' ');

?>