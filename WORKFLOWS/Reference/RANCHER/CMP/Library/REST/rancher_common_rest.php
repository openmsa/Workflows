<?php 

require_once '/opt/fmc_repository/Process/Reference/RANCHER/CMP/Library/REST/utility.php';

function rancher_object_get ($rancher_rest_api, $object_name) {

	$curl_cmd = create_rancher_operation_request(OP_GET, $rancher_rest_api);
	$response = perform_curl_operation($curl_cmd, strtoupper($object_name) . " GET");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

function rancher_object_delete ($rancher_rest_api, $object_name) {

	$curl_cmd = create_rancher_operation_request(OP_DELETE, $rancher_rest_api);
	$response = perform_curl_operation($curl_cmd, strtoupper($object_name) . " DELETE");
	return $response;
}

function _rancher_host_configure ($project_id, $hostname = "", $id = "", $name = "", $labels = array()) {

	$rancher_rest_api = "projects/{$project_id}/hosts";
	
	$parameters = array();
	if ($hostname !== "") {
		$parameters['hostname'] = $hostname;
	}
	if ($name !== "") {
		$parameters['name'] = $name;
	}
	if (!empty($labels)) {
		$parameters['labels'] = $labels;
	}
	
	$operation = OP_POST;
	if ($id !== "") {
		$operation = OP_PUT;
		$rancher_rest_api .= "/{$id}";
	}

	$curl_cmd = create_rancher_operation_request($operation, $rancher_rest_api, json_encode($parameters));
	$response = perform_curl_operation($curl_cmd, "RANCHER : HOST CONFIGURE");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

function _rancher_stack_configure ($project_id, $name = "", $id = "", $docker_compose = "", $external_id = "", $group = "",
									$start_on_create = "") {

	$rancher_rest_api = "projects/{$project_id}/stacks";

	$parameters = array();
	if ($name !== "") {
		$parameters['name'] = $name;
	}
	if ($start_on_create !== "") {
		$parameters['startOnCreate'] = $start_on_create;
	}
	if ($docker_compose !== "") {
		$parameters['dockerCompose'] = $docker_compose;
	}
	if ($external_id !== "") {
		$parameters['externalId'] = $external_id;
	}
	if ($group !== "") {
		$parameters['group'] = $group;
	}

	$operation = OP_POST;
	if ($id !== "") {
		$operation = OP_PUT;
		$rancher_rest_api .= "/{$id}";
	}
	
	$curl_cmd = create_rancher_operation_request($operation, $rancher_rest_api, json_encode($parameters));
	$response = perform_curl_operation($curl_cmd, "RANCHER : STACK CONFIGURE");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

function _rancher_volume_configure ($project_id, $name = "", $id = "", $size_mb = "", $driver = "", 
									$host_id = "", $stack_id = "") {

	$rancher_rest_api = "projects/{$project_id}/volumes";

	$parameters = array();
	if ($name !== "") {
		$parameters['name'] = $name;
	}
	if ($size_mb !== "") {
		$parameters['sizeMb'] = $size_mb;
	}
	if ($driver !== "") {
		$parameters['driver'] = $driver;
	}
	if ($host_id !== "") {
		$parameters['hostId'] = $host_id;
	}
	if ($stack_id !== "") {
		$parameters['stackId'] = $stack_id;
	}

	$operation = OP_POST;
	if ($id !== "") {
		$operation = OP_PUT;
		$rancher_rest_api .= "/{$id}";
	}

	$curl_cmd = create_rancher_operation_request($operation, $rancher_rest_api, json_encode($parameters));
	$response = perform_curl_operation($curl_cmd, "RANCHER : VOLUME CONFIGURE");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

function _rancher_service_configure ($project_id, $name = "", $id = "", $scale = "", $stack_id = "") {

	$rancher_rest_api = "projects/{$project_id}/services";

	$parameters = array();
	if ($name !== "") {
		$parameters['name'] = $name;
	}
	if ($scale !== "") {
		$parameters['scale'] = $scale;
	}
	if ($stack_id !== "") {
		$parameters['stackId'] = $stack_id;
	}

	$operation = OP_POST;
	if ($id !== "") {
		$operation = OP_PUT;
		$rancher_rest_api .= "/{$id}";
	}

	$curl_cmd = create_rancher_operation_request($operation, $rancher_rest_api, json_encode($parameters));
	$response = perform_curl_operation($curl_cmd, "RANCHER : SERVICE CONFIGURE");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

function _rancher_registration_token_create ($project_id, $name = "") {

	$rancher_rest_api = "projects/{$project_id}/registrationTokens";

	$parameters = array();
	if ($name !== "") {
		$parameters['name'] = $name;
	}

	$curl_cmd = create_rancher_operation_request(OP_POST, $rancher_rest_api, json_encode($parameters));
	$response = perform_curl_operation($curl_cmd, "RANCHER : REGISTRATION-TOKEN CREATE");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

?>
