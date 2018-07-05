<?php

require_once COMMON_DIR . 'curl_performer.php';

/**
 * curl -u ncroot:ubiqube  -XGET http://localhost:10080/ubi-api-rest/orchestration/{ubiqubeId}/service/instance
 */
function _orchestration_list_service_instances ($ubiqube_id) {

	$msa_rest_api = "orchestration/{$ubiqube_id}/service/instance";
	$curl_cmd = create_msa_operation_request(OP_GET, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "LIST SERVICE INSTANCES");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

/**
 * curl -u ncroot:ubiqube  -XGET http://localhost:10080/ubi-api-rest/orchestration/{ubiqubeId}/service/instance/{serviceId}
 */
function _orchestration_read_service_instance ($ubiqube_id, $service_id) {

	$msa_rest_api = "orchestration/{$ubiqube_id}/service/instance/{$service_id}";
	$curl_cmd = create_msa_operation_request(OP_GET, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "READ SERVICE INSTANCE");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

/**
 * curl -u ncroot:ubiqube  -XGET http://localhost:10080/ubi-api-rest/orchestration/{externalReference}/service/instance/{serviceReference}
 */
function _orchestration_read_service_instance_by_reference ($external_reference, $service_reference) {

	$msa_rest_api = "orchestration/{$external_reference}/service/instance/reference/{$service_reference}";
	$curl_cmd = create_msa_operation_request(OP_GET, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "READ SERVICE INSTANCE BY REFERENCE");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

/**
 * curl -u ncroot:ubiqube  -XGET http://localhost:10080/ubi-api-rest/orchestration/service/variables/{serviceId}
 */
function _orchestration_get_service_variables_by_service_id ($service_id) {

	$msa_rest_api = "orchestration/service/variables/{$service_id}";
	$curl_cmd = create_msa_operation_request(OP_GET, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "GET SERVICE VARIABLES BY ID");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

/**
 * curl -u ncroot:ubiqube  -XGET http://localhost:10080/ubi-api-rest/orchestration/service/variables/{serviceId}/{variableName}
 */
function _orchestration_get_service_variable_by_service_id_variable_name ($service_id, $variable_name) {

	$msa_rest_api = "orchestration/service/variables/{$service_id}/{$variable_name}";
	$curl_cmd = create_msa_operation_request(OP_GET, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "GET SERVICE VARIABLE BY VARIABLE NAME");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

/**
 * curl -u ncroot:ubiqube  -XPOST 'http://127.0.0.1:10080/ubi-api-rest/orchestration/service/variables/{serviceId}/{variableName}?value={variableValue}'
 */
function _orchestration_update_service_variable ($service_id, $variable_name, $variable_value) {

	$msa_rest_api = "orchestration/service/variables/{$service_id}/{$variable_name}?value={$variable_value}";
	$curl_cmd = create_msa_operation_request(OP_POST, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "UPDATE SERVICE VARIABLE");
	return $response;
}

/**
 * curl -u ncroot:ubiqube  -XDELETE http://localhost:10080/ubi-api-rest/orchestration/{ubiqubeId}/service/instance/{serviceId}
 */
function _orchestration_delete_service_instance_by_id ($ubiqube_id, $service_id) {

	$msa_rest_api = "orchestration/{$ubiqube_id}/service/instance/{$service_id}";
	$curl_cmd = create_msa_operation_request(OP_DELETE, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "DELETE SERVICE INSTANCE BY SERVICE ID");
	return $response;
}

/**
 *  curl -u ncroot:ubiqube  -XGET http://localhost:10080/ubi-api-rest/orchestration/{ubiqubeId}/process/instances?serviceName={serviceName}&processName={processName}
 */
function _orchestration_list_process_instance ($ubiqube_id, $service_name, $process_name) {

	$msa_rest_api = "orchestration/{$ubiqube_id}/process/instances?serviceName={$service_name}&processName={$process_name}";
	$curl_cmd = create_msa_operation_request(OP_GET, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "LIST PROCESS INSTANCE");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

/**
	curl -u ncroot:ubiqube  -XPOST http://localhost:10080/ubi-api-rest/orchestration/service/execute/{ubiqubeId}?serviceName={serviceName}&processName={processName} -d '
	{
		"var1": "val1",
		"var2": "val2"
	}
	'
 */
function _orchestration_execute_service ($ubiqube_id, $service_name, $process_name, $json_body = "{}") {

	$msa_rest_api = "orchestration/service/execute/{$ubiqube_id}?serviceName={$service_name}&processName={$process_name}&serviceInstance=0";
	$curl_cmd = create_msa_operation_request(OP_POST, $msa_rest_api, $json_body);
	$response = perform_curl_operation($curl_cmd, "EXECUTE SERVICE");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

/**
	curl -u ncroot:ubiqube  -XPOST http://localhost:10080/ubi-api-rest/orchestration/service/execute/{ubiqubeId}?serviceName={serviceName}&processName={processName} -d '
	{
		"var1": "val1",
		"var2": "val2"
	}
	'
 */
function _orchestration_execute_service_by_instance ($ubiqube_id, $service_instance, $service_name, $process_name, $json_body = "{}") {
	$msa_rest_api = "orchestration/service/execute/{$ubiqube_id}?serviceName={$service_name}&processName={$process_name}&serviceInstance={$service_instance}";
	$curl_cmd = create_msa_operation_request(OP_POST, $msa_rest_api, $json_body);
	$response = perform_curl_operation($curl_cmd, "EXECUTE SERVICE");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

/**
	curl -u ncroot:ubiqube  -XPOST http://localhost:10080/ubi-api-rest/orchestration/service/execute/{ubiqubeId}?serviceName={serviceName}&processName={processName} -d '
	{
		"var1": "val1",
		"var2": "val2"
	}
	'
 */
function _orchestration_launch_sub_process ($ubiqube_id, $service_instance, $service_name, $process_name, $json_body = "{}") {
	$msa_rest_api = "orchestration/subprocess/execute/{$ubiqube_id}?serviceName={$service_name}&processName={$process_name}&serviceInstance={$service_instance}";
	$curl_cmd = create_msa_operation_request(OP_POST, $msa_rest_api, $json_body);
	$response = perform_curl_operation($curl_cmd, "EXECUTE SERVICE");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

/**
 * curl -u ncroot:ubiqube  -XPOST http://localhost:10080/ubi-api-rest/orchestration/service/execute/{externalReference}/{serviceExternalReference}?serviceName={serviceName}&processName={processName} -d '
 * {
 *   "var1": "val1",
 *   "var2": "val2"
 * }'
 *
 */
function _orchestration_execute_service_by_reference ($external_ref, $service_reference, $service_name, $process_name, $json_body = "{}") {

	$msa_rest_api = "orchestration/service/execute/{$external_ref}/{$service_reference}?serviceName={$service_name}&processName={$process_name}";
	$curl_cmd = create_msa_operation_request(OP_POST, $msa_rest_api, $json_body);
	$response = perform_curl_operation($curl_cmd, "EXECUTE SERVICE BY REFERENCE");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

/**
 * curl -u ncroot:ubiqube  -X GET  http://localhost:8080/ubi-api-rest/orchestration/process/instances/169871
 */
function _orchestration_list_process_instance_by_service_id ($service_id) {

	$msa_rest_api = "orchestration/process/instances/{$service_id}";
	$curl_cmd = create_msa_operation_request(OP_GET, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "LIST PROCESS INSTANCE BY SERVICE ID");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

/**
 * curl -u ncroot:ubiqube  -X GET  http://localhost:8080/ubi-api-rest/orchestration/process/instance/169871
 */
function _orchestration_get_process_instance ($process_id) {

	$msa_rest_api = "orchestration/process/instance/{$process_id}";
	$curl_cmd = create_msa_operation_request(OP_GET, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "GET PROCESS INSTANCE");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

/**
 * curl -u ncroot:ubiqube  -X PUT http://localhost:10080/ubi-api-rest/orchestration/process/instance/{processIntanceId}/task/{taskId}/execnumber/{execNumber}/update -d '{"details" : "details"}'
 */
function _orchestration_update_process_script_details ($process_instance_id, $task_id, $exec_number, $details = "") {

	$msa_rest_api = "orchestration/process/instance/{$process_instance_id}/task/{$task_id}/execnumber/{$exec_number}/update";
	$json = json_encode(array('details' => $details));
	$curl_cmd = create_msa_operation_request(OP_PUT, $msa_rest_api, $json);
	$response = perform_curl_operation($curl_cmd, "UPDATE PROCESS SCRIPT DETAILS");
	return $response;
}

/**
 * curl -u ncroot:ubiqube  -X PUT http://localhost:10080/ubi-api-rest/orchestration/{ubiqubeId}/service/instance/update/{serviceId}?serviceReference={serviceReference}
 */
function _orchestration_update_service_instance_reference ($ubiqube_id, $service_id, $service_reference = "") {

	$msa_rest_api = "orchestration/{$ubiqube_id}/service/instance/update/{$service_id}/?serviceReference={$service_reference}";
	$curl_cmd = create_msa_operation_request(OP_PUT, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "UPDATE SERVICE INSTANCE REFERENCE");
	return $response;
}

/**
 * curl -u ncroot:ubiqube  -X PUT http://localhost:10080/ubi-api-rest/orchestration/{ubiqubeId}/service/attach?uri={serviceUri}
 */
function _orchestration_service_attach ($ubiqube_id, $service_uri) {

	$msa_rest_api = "orchestration/{$ubiqube_id}/service/attach?uri={$service_uri}";
	$curl_cmd = create_msa_operation_request(OP_POST, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "ATTACH SERVICE TO CUSTOMER");
	return $response;
}

/**
 * curl -u ncroot:ubiqube  -X PUT http://localhost:10080/ubi-api-rest/orchestration/{ubiqubeId}/service/detach?uri={serviceUri}
 */
function _orchestration_service_detach ($ubiqube_id, $service_uri) {

	$msa_rest_api = "orchestration/{$ubiqube_id}/service/detach?uri={$service_uri}";
	$curl_cmd = create_msa_operation_request(OP_POST, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "DETACH SERVICE FROM CUSTOMER");
	return $response;
}

?>
