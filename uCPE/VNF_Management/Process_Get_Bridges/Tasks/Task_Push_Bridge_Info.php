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
$sleep = rand(5,15);
sleep($sleep);
$device_id = substr($context['device_id'], 3);
$bridges = $context['connection_info']['results'];

foreach($bridges as $bridge)
{
    $objects=array();
    $name = $bridge['name'];
    $objects['object_id']= $bridge['name'];	
    
    $cmd_obj = array("Bridge_Values" => array("$name" => $objects));
    $response = execute_command_and_verify_response($device_id, CMD_CREATE, $cmd_obj, "CREATE Bridge_values");
    $response = json_decode($response, true);

if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}


}


task_success('Task OK');

?>