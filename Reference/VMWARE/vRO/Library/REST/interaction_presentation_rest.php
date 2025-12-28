<?php

require_once '/opt/fmc_repository/Process/Reference/OPENSTACK/Library/REST/utility.php';

function _interaction_presentation_start ($workflow_id, $execution_id, $parameters = array()) {

	$vro_rest_api = "workflows/{$workflow_id}/executions/{$execution_id}/interaction/presentation/instances";
	$curl_cmd = create_vro_operation_request(OP_POST, $vro_rest_api, json_encode($parameters));
	$response = perform_curl_operation($curl_cmd, "vRO : START WORKFLOW INTERACTION PRESENTATION");
	return $response;
}

function _interaction_presentation_update ($workflow_id, $execution_id, $presentation_execution_id, $parameters = array()) {

	$vro_rest_api = "workflows/{$workflow_id}/executions/{$execution_id}/interaction/presentation/instances/{$presentation_execution_id}";
	$curl_cmd = create_vro_operation_request(OP_POST, $vro_rest_api, json_encode($parameters));
	$response = perform_curl_operation($curl_cmd, "vRO : UPDATE WORKFLOW INTERACTION PRESENTATION");
	return $response;
}

?>