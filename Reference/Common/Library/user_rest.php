<?php

require_once COMMON_DIR . 'curl_performer.php';

/**
 * curl -u ncroot:ubiqube  -H "Content-Type: application/json" -XPOST
 * 'http://MSA_IP/ubi-api-rest/user/manager/SFR?name=restManager&login=afo_manager_rest&password=ubiqube38&reference=SFRA3&delegationProfileId=123&priviledged=true' -d
 * '[{"customerReference": "ABC"}, {"customerReference": "XYZ"}]'
 */
function _manager_create ($prefix, $name, $login = "", $password = "", $reference = "", $delegation_profile_id = 0, $privileged = "false", $customer_references = "[]") {
	$msa_rest_api = "user/manager/{$prefix}?name={$name}&login={$login}&password={$password}&reference={$reference}&delegationProfileId={$delegation_profile_id}&privileged={$privileged}";
	$curl_cmd = create_msa_operation_request(OP_POST, $msa_rest_api, $customer_references);
	$response = perform_curl_operation($curl_cmd, "CREATE MANAGER");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

/**
 * Delete Manager by Login
 * 
 * curl -u ncroot:ubiqube  -XDELETE http://localhost:10080/ubi-api-rest/user/login/{login}
 */
function _manager_delete_by_login ($login) {
	$msa_rest_api = "user/login/{$login}";
	$curl_cmd = create_msa_operation_request(OP_DELETE, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "DELETE MANAGER BY LOGIN");
	return $response;
}

/**
 * Delete Manager by Id
 *
 * curl -u ncroot:ubiqube  -XDELETE http://localhost:10080/ubi-api-rest/user/id/{id}
 */
function _manager_delete_by_id ($id) {
	$msa_rest_api = "user/id/{$id}";
	$curl_cmd = create_msa_operation_request(OP_DELETE, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "DELETE MANAGER BY ID");
	return $response;
}

/**
 * Delete Manager by Reference
 *
 * curl -u ncroot:ubiqube  -XDELETE http://localhost:10080/ubi-api-rest/user/reference/{reference}
 */
function _manager_delete_by_reference ($reference) {
	$msa_rest_api = "user/reference/{$reference}";
	$curl_cmd = create_msa_operation_request(OP_DELETE, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "DELETE MANAGER BY REFERENCE");
	return $response;
}

/**
 * curl -u ncroot:Ub1qub3  -XGET http://localhost:80/ubi-api-rest/user/id/104
 *
 */
function _manager_read_by_id ($manager_id) {

	$msa_rest_api = "user/id/{$manager_id}";
	$curl_cmd = create_msa_operation_request(OP_GET, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "READ MANAGER BY ID");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

/**
 * curl -u ncroot:Ub1qub3  -XGET http://localhost:80/ubi-api-rest/lookup/managers
 *
 */
function _get_all_manager () {

	$msa_rest_api = "lookup/managers";
	$curl_cmd = create_msa_operation_request(OP_GET, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "GET ALL MANAGERS");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

/**
 <pre>
 curl -u ncroot:ubiqube  -X GET http://localhost:8080/ubi-api-rest/user/reference/ADMIN_MAN
 </pre>
 *
 */
function _manager_read_by_reference ($manager_reference) {

	$msa_rest_api = "user/reference/{$manager_reference}";
	$curl_cmd = create_msa_operation_request(OP_GET, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "READ BY MANAGER REFERENCE");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

/**
 * curl -u ncroot:Ub1qub3  -XGET http://localhost:80/ubi-api-rest/user/login/ADMIN_MAN
 *
 */
function _manager_read_by_login ($manager_login) {

	$msa_rest_api = "user/login/{$manager_login}";
	$curl_cmd = create_msa_operation_request(OP_GET, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "READ MANAGER BY LOGIN");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

/**
 * Attach Customers to Manager
 *    $manager_reference
 *    $customer_references should be a php array like ["customerReference": "ABC", "customerReference": "XYZ"]
 * curl -u ncroot:ubiqube  -XPUT http://localhost:10080/ubi-api-rest/user/manager/{managerReference}/customers/attach -d '["customerReference": "ABC", "customerReference": "XYZ"]'
 */
function _manager_attach_customers ($manager_reference, $customer_references) {
  $msa_rest_api = "user/manager/{$manager_reference}/customers/attach";
  $json =  '['.json_encode($customer_references).']';
  $curl_cmd = create_msa_operation_request(OP_PUT, $msa_rest_api, $json);
  $response = perform_curl_operation($curl_cmd, "ATTACH CUSTOMERS TO MANAGER");
  return $response;
}


/**
 * For the given manager, set the given delegationId to the given customer
 * curl -u ncroot:ubiqube  -XPUT -XPUT "http://MSA_IP/ubi-api-rest/delegation/{delegationId}/{managerId}/{customerId}" 
 */
function _manager_set_delegation_to_customer ($delegationId, $managerId, $customerId) {
  $msa_rest_api = "delegation/{$delegationId}/{$managerId}/{$customerId}";
  $curl_cmd = create_msa_operation_request(OP_PUT, $msa_rest_api);
  $response = perform_curl_operation($curl_cmd, "For MANAGER set the delegation for the given customer");
  return $response;
}


/**
 * Detach Customers from Manager
 *
 * curl -u ncroot:ubiqube  -XPUT http://localhost:10080/ubi-api-rest/user/manager/{managerReference}/customers/detach -d '["customerReference": "ABC", "customerReference": "XYZ"]'
 */
function _manager_detach_customers ($manager_reference, $customer_references) {
	$msa_rest_api = "user/manager/{$manager_reference}/customers/detach";
	$curl_cmd = create_msa_operation_request(OP_PUT, $msa_rest_api, $customer_references);
	$response = perform_curl_operation($curl_cmd, "DETACH CUSTOMERS FROM MANAGER");
	return $response;
}

/**
 * Update Manager Password
 *
 * curl -u ncroot:ubiqube  -XPUT http://localhost:10080/ubi-api-rest/user/manager_password/{id}?password={password}
 */
function _manager_update_password ($manager_id, $password) {
	$msa_rest_api = "user/manager_password/{$manager_id}?password={$password}";
	$curl_cmd = create_msa_operation_request(OP_PUT, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "UPDATE MANAGER PASSWORD");
	return $response;
}

/**
* Update Manager Delegation Profile
* 
* curl -X PUT "https://10.30.18.222/user/v1/updateManagerDelegationProfile?managerId=111&delegationProfile=122&callerLogin=ddd" -H "accept: application/json"
**/
function _manager_update_delegation_profile ($manager_id, $delegation_profile_id, $caller_login) {
        $msa_rest_api = "user/v1/updateManagerDelegationProfile?managerId={$manager_id}&delegationProfile={$delegation_profile_id}&callerLogin={$caller_login}";
        $curl_cmd = create_msa_operation_request(OP_PUT, $msa_rest_api);
        $response = perform_curl_operation($curl_cmd, "UPDATE MANAGER DELEGATION PROFILE");
        return $response;
}
?>