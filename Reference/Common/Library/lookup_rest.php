<?php

require_once COMMON_DIR . 'curl_performer.php';


/**
 * List Device Ids by Customer External Reference
 * 
 * curl -u ncroot:ubiqube  -XGET http://localhost:10080/ubi-api-rest/lookup/customer/devices/reference/{customerReference}
 */
function _lookup_list_devices_by_customer_reference ($customer_reference) {
	$msa_rest_api = "lookup/customer/devices/reference/{$customer_reference}";
	$curl_cmd = create_msa_operation_request(OP_GET, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "LIST DEVICES BY CUSTOMER REFERENCE");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

/**
 * List Device Ids
 *
 * curl -u ncroot:ubiqube  -XGET http://localhost:10080/ubi-api-rest/lookup/devices
 */
function _lookup_list_device_ids () {
	$msa_rest_api = "lookup/devices";
	$curl_cmd = create_msa_operation_request(OP_GET, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "LIST DEVICE IDs");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

/**
 * List Customer Ids
 *
 * curl -u ncroot:ubiqube  -XGET http://localhost:10080/ubi-api-rest/lookup/customers
 */
function _lookup_list_customer_ids () {
	$msa_rest_api = "lookup/customers";
	$curl_cmd = create_msa_operation_request(OP_GET, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "LIST CUSTOMER IDs");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

/**
 * List Manager Ids
 *
 * curl -u ncroot:ubiqube  -XGET http://localhost:10080/ubi-api-rest/lookup/managers
 */
function _lookup_list_manager_ids () {
	$msa_rest_api = "lookup/managers";
	$curl_cmd = create_msa_operation_request(OP_GET, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "LIST MANAGER IDs");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

/**
 * List Operator Ids
 *
 * curl -u ncroot:ubiqube  -XGET http://localhost:10080/ubi-api-rest/lookup/manager/operators/id/{managerId}
 */
function _lookup_list_operator_ids ($manager_id) {
	$msa_rest_api = "lookup/manager/operators/id/{$manager_id}";
	$curl_cmd = create_msa_operation_request(OP_GET, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "LIST OPERATOR IDs");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

/**
 * List SecEngine Nodes
 *
 * curl -u ncroot:ubiqube  -XGET http://localhost:10080/ubi-api-rest/lookup/sec_nodes
 */
function _lookup_list_sec_nodes () {
	$msa_rest_api = "lookup/sec_nodes";
	$curl_cmd = create_msa_operation_request(OP_GET, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "LIST SEC NODES");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

/**
 * Get SecEngine Node by Device Id
 *
 * curl -u ncroot:ubiqube  -XGET http://localhost:10080/ubi-api-rest/lookup/v1/sec-node-by-device-id/{device_id}  
 *       "ipV6Mask": "64",
 *        "id": 1,
 *        "haStatusSecNode": 1,
 *        "haStatusRepNode": 0,
 *        "name": "ACS",
 *        "logAddress": "10.31.1.5",
 *        "smsAddress": "127.0.0.1",
 *        "alive": true
 */
function _lookup_get_sec_node_by_device_id ($device_id) {
	$msa_rest_api = "lookup/v1/sec-node-by-device-id/{$device_id}";
	$curl_cmd = create_msa_operation_request(OP_GET, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "GET SEC NODE BY DEVICE ID");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

?>