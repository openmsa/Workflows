<?php

require_once COMMON_DIR . 'curl_performer.php';

/**
 * curl -u ncroot:ubiqube  -XPOST http://localhost:10080/ubi-api-rest/widget_portal/{canvasId}?prefix={prefix}&name={name}
 * 
 */
function _canvas_attach_to_operator ($canvas_id, $operator_prefix, $canvas_name) {

	$msa_rest_api = "widget_portal/{$canvas_id}?prefix={$operator_prefix}&name={$canvas_name}";
	$curl_cmd = create_msa_operation_request(OP_PUT, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "ATTACH CANVAS TO OPERATOR");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

/**
 * curl -u ncroot:NCROOT_PWD  -XDELETE "http://localhost:10080/ubi-api-rest/widget_portal/{canvasId}"
 * 
 */
function _canvas_delete ($canvas_id) {

	$msa_rest_api = "widget_portal/{$canvas_id}";
	$curl_cmd = create_msa_operation_request(OP_DELETE, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "DELETE CANVAS");
	return $response;
}

/**
 * curl -u ncroot:NCROOT_PWD  -XPOST "http://localhost:10080/ubi-api-rest/widget_portal/{canvasId}/attach?reference={customerReference}"
 * 
 */
function _canvas_attach_to_customer ($canvas_id, $customer_reference) {

	$msa_rest_api = "widget_portal/{$canvas_id}/attach?reference={$customer_reference}";
	$curl_cmd = create_msa_operation_request(OP_PUT, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "ATTACH CANVAS TO CUSTOMER");
	return $response;
}

/**
 * curl -u ncroot:NCROOT_PWD  -XPOST "http://localhost:10080/ubi-api-rest/widget_portal/{canvasId}/detach?reference={customerReference}"
 * 
 */
function _canvas_detach_from_customer ($canvas_id, $customer_reference) {

	$msa_rest_api = "widget_portal/{$canvas_id}/detach?reference={$customer_reference}";
	$curl_cmd = create_msa_operation_request(OP_PUT, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "DETACH CANVAS FROM CUSTOMER");
	return $response;
}

?>