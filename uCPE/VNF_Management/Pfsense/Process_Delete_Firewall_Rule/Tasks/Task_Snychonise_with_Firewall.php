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
}

$device_id = $context['device_id'];

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

