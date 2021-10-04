<?php

/**
 * This file is necessary to include to use all the in-built libraries of /opt/fmc_repository/Reference/Common
 */
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

/**
 * List all the parameters required by the task
 * No user input is necessary for this deletion process
 */
function list_args()
{
}

$customer_id = $context['customer_id'];
$customer_id_long = substr($customer_id, 4);

$response =_customer_delete_by_id($customer_id_long);

$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
        $response_task = json_encode($response);
        echo $response_task;
        exit;
}
$response_task = prepare_json_response(ENDED, "Customer deleted successfully.\n", $context, true);

echo $response_task;

/**
 * End of the task do not modify after this point
 */
task_exit(ENDED, "Customer deleted");

?>