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

check_mandatory_param("device_id_pa");

$device_id = substr($context['device_id_pa'], 3);


/**
* call to Microservice IMPORT to synchronize the MSA database with the managed UcpeManager VIM
*/
$response = synchronize_objects_and_verify_response($device_id);


$response = _device_read_by_id($device_id);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}

task_exit(ENDED, "Synchronisation to Paloalto successfull.");

?>
