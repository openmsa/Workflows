<?php

require_once COMMON_DIR . 'curl_performer.php';

/**
 * curl -u ncroot:ubiqube  -XPOST http://MSA_IP/ubi-api-rest/sms/cmd/{command}/{deviceId}?params={params}
 *
 */
function _secengine_perform_command_on_device ($device_id, $command, $params = "", $connection_timeout = 60, $max_time = 60) {

	$msa_rest_api = "sms/cmd/{$command}/{$device_id}";
	if ($params !== "") {
		$msa_rest_api .= "?params=$params";
	}
	$curl_cmd = create_msa_operation_request(OP_POST, $msa_rest_api, "", $connection_timeout, $max_time);
	$response = perform_curl_operation($curl_cmd, "PERFORM SMS COMMAND ON DEVICE");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

/**
 * curl -u ncroot:ubiqube  -XPOST http://MSA_IP/ubi-api-rest/sms/verb/{verb}/{deviceId}?params={params}
 *
 */
function _secengine_perform_verb_on_device ($device_id, $verb, $params = "", $connection_timeout = 60, $max_time = 60) {

	$msa_rest_api = "sms/verb/{$verb}/{$device_id}";
	if ($params !== "") {
		$msa_rest_api .= "?params=$params";
	}
	$curl_cmd = create_msa_operation_request(OP_POST, $msa_rest_api, "", $connection_timeout, $max_time);
	$response = perform_curl_operation($curl_cmd, "PERFORM SMS VERB");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

?>