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
  
  create_var_def('device', 'String');

}

$id = substr($context['device'], 3);
$response = synchronize_objects_and_verify_response($id);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = prepare_json_response(FAILED, $response['wo_comment'], $context, true);
	echo $response;
	exit;
}


/**
 * End of the task (choose one)
 */
task_success('Task OK');
task_error('Task FAILED');
?>