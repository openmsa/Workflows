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

  create_var_def('wf_name', 'String');
}
$wf=$context['wf_name'];
$ubi_id=$context['UBIQUBEID'];
$msa_rest_api = "orchestration/v1/service/instance/archived?ubiId=$ubi_id&serviceName=$wf";
$curl_cmd = create_msa_operation_request(OP_DELETE, $msa_rest_api);
$response = perform_curl_operation($curl_cmd, "EMPTY ARCHIVED SERVICE INSTANCES");
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
  $response = json_encode($response);
  return $response;
}

task_success('Bin Emptied');
?>