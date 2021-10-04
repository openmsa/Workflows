<?php

/**
 * This file is necessary to include to use all the in-built libraries of /opt/fmc_repository/Reference/Common
 */
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

/**
 * List all the parameters required by the task
 */
function list_args()
{
  
}

$device_id = substr($context['device_id'], 3);
$connections = $context['fin_connection_values'];
ksort($connections);
foreach($connections as $row)
{
    $objects=array();
    $objects['object_id']= $row;	
    
    $cmd_obj = array("Connection_values" => array("$row" => $objects));
    $response = execute_command_and_verify_response($device_id, CMD_CREATE, $cmd_obj, "CREATE Connection_values");
    $response = json_decode($response, true);

	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		echo $response;
		exit;
	}

}

task_success('Task OK');

?>