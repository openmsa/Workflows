<?php

require_once COMMON_DIR . 'curl_performer.php';


/**
 * Create Customer
 * 
 * curl -u ncroot:ubiqube  -H "Content-Type: application/json" -XPOST 'http://localhost:10080/ubi-api-rest/customer/{prefix}?name={name}&reference={reference}' -d '
    {
        "name": "contactName",
        "firstName": "contactFirstName",
        "address": {
            "streetName1": "sn1",
            "streetName2": "sn2",
            "streetName3": "sn3",
            "city": "city123",
            "zipCode": "zip123",
            "country": "Country098",
            "fax": "1233",
            "email": "contact@company.com",
            "phone": "123"
        }

    }
 *
 */
function _customer_create ($operator_prefix, $customer_name, $external_reference = "", $contact_details = "{}") {

	$msa_rest_api = "customer/{$operator_prefix}?name={$customer_name}&reference={$external_reference}";
	$curl_cmd = create_msa_operation_request(OP_POST, $msa_rest_api, $contact_details);
	$response = perform_curl_operation($curl_cmd, "CREATE CUSTOMER");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

/**
 * Update Customer by Id
 *
 * curl -u ncroot:ubiqube  -XDELETE http://localhost:10080/ubi-api-rest/customer/id/{id}?name={name}
 */
function _customer_update_by_id ($customer_id, $name) {

	$msa_rest_api = "customer/id/{$customer_id}?name={$name}";
	$curl_cmd = create_msa_operation_request(OP_PUT, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "UPDATE CUSTOMER BY ID");
	return $response;
}

/**
 * Delete Customer by Id
 * 
 * curl -u ncroot:ubiqube  -XDELETE http://localhost:10080/ubi-api-rest/customer/id/{id}
 */
function _customer_delete_by_id ($customer_id) {

	$msa_rest_api = "customer/id/{$customer_id}";
	$curl_cmd = create_msa_operation_request(OP_DELETE, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "DELETE CUSTOMER BY ID");
	return $response;
}

/**
 * Delete Customer by Reference
 *
 * curl -u ncroot:ubiqube  -XDELETE http://localhost:10080/ubi-api-rest/customer/reference/{id}
 */
function _customer_delete_by_reference ($customer_reference) {

	$msa_rest_api = "customer/reference/{$customer_reference}";
	$curl_cmd = create_msa_operation_request(OP_DELETE, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "DELETE CUSTOMER BY REFERENCE");
	return $response;
}

/**
 * curl -u ncroot:Ub1qub3  -XGET http://localhost:80/ubi-api-rest/customer/id/104
 * 
 */
function _customer_read_by_id ($customer_id) {
	
	$msa_rest_api = "customer/id/{$customer_id}";
	$curl_cmd = create_msa_operation_request(OP_GET, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "READ CUSTOMER BY ID");
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
 curl -u ncroot:ubiqube  -X GET http://localhost:8080/ubi-api-rest/customer/reference/NCSA4034
 </pre>
 *
 * @param unknown $customer_reference
 * @return Ambigous <unknown, mixed>
 */
function _customer_read_by_reference ($customer_reference) {

	$msa_rest_api = "customer/reference/{$customer_reference}";
	$curl_cmd = create_msa_operation_request(OP_GET, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "READ BY CUSTOMER REFERENCE");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

/**
 * Add a new Configuration Variable to the Customer [by reference]
 * 
 * curl -u ncroot:ubiqube  -XPUT http://localhost:10080/ubi-api-rest/customer/{reference}/variables?name={name}&value={value}
 */
function _customer_add_configuration_variable ($customer_reference, $name, $value) {

	$msa_rest_api = "customer/reference/{$customer_reference}/variables?name={$name}&value={$value}";
	$curl_cmd = create_msa_operation_request(OP_PUT, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "ADD CUSTOMER CONFIGURATION VARIABLE");
	return $response;
}

/**
 * List Customer Configuration Variables
 *
 * curl -u ncroot:ubiqube  -XGET http://localhost:10080/ubi-api-rest/customer/id/{id}/variables
 */
function _customer_list_configuration_variables ($customer_id) {

	$msa_rest_api = "customer/id/{$customer_id}/variables";
	$curl_cmd = create_msa_operation_request(OP_GET, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "LIST CUSTOMER CONFIGURATION VARIABLES");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

/**
 * Read Customer Configuration Variable
 *
 * curl -u ncroot:ubiqube  -XGET http://localhost:10080/ubi-api-rest/customer/id/{id}/variables/{name}
 */
function _customer_read_configuration_variable ($customer_id, $name) {

	$msa_rest_api = "customer/id/{$customer_id}/variables/{$name}";
	$curl_cmd = create_msa_operation_request(OP_GET, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "READ CUSTOMER CONFIGURATION VARIABLE");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

/**
 * Delete Customer Configuration Variable
 *
 * curl -u ncroot:ubiqube  -XDELETE http://localhost:10080/ubi-api-rest/customer/{reference}/variables/{name}
 */
function _customer_delete_configuration_variable ($customer_reference, $name) {

	$msa_rest_api = "customer/reference/{$customer_reference}/variables/{$name}";
	$curl_cmd = create_msa_operation_request(OP_DELETE, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "DELETE CUSTOMER CONFIGURATION VARIABLE");
	return $response;
}

/**
 * Attach a profile to the Customer [by reference]
 *
 * curl -u ncroot:ubiqube  -XPUT http://localhost:10080/ubi-api-rest/customer/{reference}/attach?profile={profileReference}
 */
function _customer_attach_profile ($customer_reference, $profile_reference) {

	$msa_rest_api = "customer/{$customer_reference}/attach?profile={$profile_reference}";
	$curl_cmd = create_msa_operation_request(OP_PUT, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "ATTACH A PROFILE TO CUSTOMER");
	return $response;
}

/**
 * Detach a profile from the Customer [by reference]
 *
 * curl -u ncroot:ubiqube  -XPUT http://localhost:10080/ubi-api-rest/customer/{reference}/detach?profile={profileReference}
 */
function _customer_detach_profile ($customer_reference, $profile_reference) {

	$msa_rest_api = "customer/{$customer_reference}/detach?profile={$profile_reference}";
	$curl_cmd = create_msa_operation_request(OP_PUT, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "DETACH A PROFILE FROM CUSTOMER");
	return $response;
}

?>