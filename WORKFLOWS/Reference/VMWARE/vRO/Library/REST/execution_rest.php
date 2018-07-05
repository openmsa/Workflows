<?php 

require_once '/opt/fmc_repository/Process/Reference/VMWARE/vRO/Library/REST/utility.php';

function _execution_start_workflow ($workflow_id, $parameters = array()) {

	$vro_rest_api = "workflows/{$workflow_id}/executions";
	$curl_cmd = create_vro_operation_request(OP_POST, $vro_rest_api, json_encode($parameters));
	$response = perform_curl_operation($curl_cmd, "vRO : START WORKFLOW EXECUTION");
	return $response;
}

function _execution_answer_user_interaction ($workflow_id, $execution_id, $parameters = array()) {

	$vro_rest_api = "workflows/{$workflow_id}/executions/{$execution_id}/interaction";
	$curl_cmd = create_vro_operation_request(OP_POST, $vro_rest_api, json_encode($parameters));
	$response = perform_curl_operation($curl_cmd, "vRO : ANSWER WORKFLOW USER INTERACTION");
	return $response;
}

?>