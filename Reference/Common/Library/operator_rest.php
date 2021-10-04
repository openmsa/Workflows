<?php

require_once COMMON_DIR . 'curl_performer.php';

/**
 * Create Operator
 *
 * curl -u ncroot:ubiqube  -XPOST http://localhost:10080/ubi-api-rest/operator/{prefix}?name={$name}
 */
function _operator_create ($operator_prefix, $name) {

	$msa_rest_api = "operator/{$operator_prefix}?name={$name}";
	$curl_cmd = create_msa_operation_request(OP_POST, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "OPERATOR CREATE");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

/**
 * Update Operator
 *
 * curl -u ncroot:ubiqube  -XPUT http://localhost:10080/ubi-api-rest/operator/{prefix}?name={$name}
 */
function _operator_update ($operator_prefix, $name) {

	$msa_rest_api = "operator/{$operator_prefix}?name={$name}";
	$curl_cmd = create_msa_operation_request(OP_PUT, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "OPERATOR UPDATE");
	return $response;
}

/**
 * Delete Operator by Prefix
 * 
 * curl -u ncroot:ubiqube  -XDELETE http://localhost:10080/ubi-api-rest/operator/{prefix}
 */
function _operator_delete ($operator_prefix, $force = "false") {

	$msa_rest_api = "operator/{$operator_prefix}?force={$force}";
	$curl_cmd = create_msa_operation_request(OP_DELETE, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "DELETE OPERATOR BY PREFIX");
	return $response;
}

/**
 * Get Operator by prefix
 * 
 * curl -u ncroot:ubiqube  -XGET http://localhost:10080/ubi-api-rest/operator/{prefix}
 */
function _operator_read_by_prefix ($operator_prefix) {

	$msa_rest_api = "operator/{$operator_prefix}";
	$curl_cmd = create_msa_operation_request(OP_GET, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "READ OPERATOR BY PREFIX");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

?>