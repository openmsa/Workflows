<?php

require_once '/opt/fmc_repository/Process/Reference/OPENSTACK/Library/REST/utility.php';

function _presentation_start ($workflow_id, $parameters = array()) {

	$vro_rest_api = "workflows/{$workflow_id}/presentation/instances";
	$curl_cmd = create_vro_operation_request(OP_POST, $vro_rest_api, json_encode($parameters));
	$response = perform_curl_operation($curl_cmd, "vRO : START WORKFLOW PRESENTATION");
	return $response;
}

function _presentation_update ($workflow_id, $execution_id, $parameters = array()) {

	$vro_rest_api = "workflows/{$workflow_id}/presentation/instances/{$execution_id}";
	$curl_cmd = create_vro_operation_request(OP_POST, $vro_rest_api, json_encode($parameters));
	$response = perform_curl_operation($curl_cmd, "vRO : UPDATE WORKFLOW PRESENTATION");
	return $response;
}

?>