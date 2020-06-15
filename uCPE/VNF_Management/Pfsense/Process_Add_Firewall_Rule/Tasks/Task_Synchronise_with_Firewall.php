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
   create_var_def('vnf_name', 'String');
   create_var_def('exec_delay', 'Integer');
}
$exec_delay = $context['exec_delay'];
sleep($exec_delay);


//vnf_device_id
$service = _orchestration_read_service_instance_by_reference ($context['UBIQUBEID'], $context['vnf_name']);

$response=json_decode($service, true);

$srv_id=$response['wo_newparams']['id'];

$dev_resp=_orchestration_get_service_variable_by_service_id_variable_name ($srv_id, 'vnf_device_id');

$dev_resp=json_decode($dev_resp,true);

$device_id=$dev_resp['wo_newparams']['vnf_device_id'];

$context['device_id']=$device_id;

$device_id = getIdFromUbiId ($device_id);

/**
* call to Microservice IMPORT to synchronize the MSA database with the PFsense firewall*/
$response = synchronize_objects_and_verify_response($device_id);

logToFile($response);

$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}

task_exit(ENDED, "Synchronisation to Firewall Successfull");

?>

