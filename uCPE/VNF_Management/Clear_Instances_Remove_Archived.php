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


$msa_rest_api = "/orchestration/v1/service/instance/archived";

$customer_id = $context["customer_id"];
$serviceName = 'Process/ENEA/VNF_Management.xml';
$array = array(
    'ubiId' => $customer_id,
    'serviceName' => $serviceName
);

$json = json_encode($array);
$curl_cmd = create_msa_operation_request(OP_DELETE, $msa_rest_api, $json);
$response = perform_curl_operation($curl_cmd, "DELETE SERVICE INSTANCES");
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) 
{
    $response = json_encode($response);
    return $response;
}
$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);

/**
 * End of the task (choose one)
 */
task_success('Task OK');
task_error('Task FAILED');
?>