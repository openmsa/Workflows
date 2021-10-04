<?php

/**
 * This file is necessary to include to use all the in-built libraries of /opt/fmc_repository/Reference/Common
 */
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/Common/Library/msa_common.php';

/**
 * List all the parameters required by the task
 */
function list_args()
{
   create_var_def('device_id', 'Device');
   create_var_def('exec_delay', 'Device');
}

if(isset($parameters) ){
    $context['device_id'] = $parameters['device_id'];
 }
check_mandatory_param("device_id");

$device_id = substr($context['device_id'], 3);

$exec_delay = $context['exec_delay'];
sleep($exec_delay);

/**
* call to Microservice IMPORT to synchronize the MSA database with the managed UcpeManager VIM
*/
$response = synchronize_objects_and_verify_response($device_id);

//$context["SERVICEINSTANCEREFERENCE"] = $context["vnf_name"];


logToFile(debug_dump($context['UBIQUBEID'],"===============service ubiqube id================\n"));
logToFile(debug_dump($context['service_id'],"===============service id================\n"));
logToFile(debug_dump($context['vnf_name'],"===============service vnfname================\n"));


$response = _orchestration_update_service_instance_reference ($context['UBIQUBEID'], $context['service_id'], $context['vnf_name']);

logToFile(debug_dump($response,"===============service instance ref update================"));

$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}

$response = prepare_json_response(ENDED, "Synchronisation to uCPE Manager successfull.\n", $context, true);
   echo $response;

?>
