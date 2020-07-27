<?php

require_once COMMON_DIR . 'curl_performer.php';

/**
 * curl -XPUT -u ncroot:ubiqube 'http://localhost:10080/ubi-api-rest/variables/{deviceId}/{name}?value={value}&type={$type}&comment={comment}'
 */
function _configuration_variable_create ($device_id, $name, $value, $type ="String", $comment = "") {

	$msa_rest_api = "variables/{$device_id}/{$name}?value={$value}&type={$type}&comment={$comment}";
	$curl_cmd = create_msa_operation_request(OP_PUT, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "CREATE CONFIGURATION VARIABLE");
	return $response;
}

/**
 * curl -XDELETE -u ncroot:ubiqube 'http://localhost:10080/ubi-api-rest/variables/{deviceId}/{name}'
 */
function _configuration_variable_delete ($device_id, $name) {

	$msa_rest_api = "variables/{$device_id}/{$name}";
	$curl_cmd = create_msa_operation_request(OP_DELETE, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "DELETE CONFIGURATION VARIABLE");
	return $response;
}

/**
 * curl -XGET -u ncroot:ubiqube 'http://localhost:10080/ubi-api-rest/variables/{deviceId}'
 */
function _configuration_variable_list ($device_id) {

	$msa_rest_api = "v1/configuration-variable/{$device_id}";
	$curl_cmd = create_msa_operation_request(OP_GET, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "LIST CONFIGURATION VARIABLES");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

/**
 * curl -XGET -u ncroot:ubiqube 'http://localhost:10080/ubi-api-rest/variables/{deviceId}/{name}'
 */
function _configuration_variable_read ($device_id, $name) {

	$msa_rest_api = "variables/{$device_id}/{$name}";
	$curl_cmd = create_msa_operation_request(OP_GET, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "READ CONFIGURATION VARIABLE");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

?>