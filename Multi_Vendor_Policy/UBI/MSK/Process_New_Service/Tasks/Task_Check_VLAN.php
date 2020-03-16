<?php

/**
 * This file is necessary to include to use all the in-built libraries of /opt/fmc_repository/Reference/Common
 */
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';


/**
 * List all the parameters required by the task
 */
function list_args()
{}

if(isset($parameters) ){
    $context['rtr_device'] = $parameters['rtr_device'];
 }

$device_id = substr($context['rtr_device'], 3);

$response = synchronize_objects_and_verify_response($device_id);
$response = json_decode($response, true);

$routingInterfaces = $response['wo_newparams']['RoutingSubinterface'];

//check if vlan in use if not use
$vlan = 5;
foreach($routingInterfaces as $interface)
{
    if(!is_null($interface['VLAN']) )
    {
	if($vlan == $interface['VLAN'])
	{
	   $vlan = $interface['VLAN'] +1;
	}
    }

}
$context['VLAN'] = $vlan;
logToFile(debug_dump($vlan,"=============================Response======================================="));

if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}

task_exit(ENDED, "Synchronisation to router successfull.");

?>
