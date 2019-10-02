<?php

require_once COMMON_DIR . 'curl_performer.php';

/**
 * Create Delegation Profile
 * 
 * curl -u ncroot:NCROOT_PWD  -XPUT "http://localhost:10080/ubi-api-rest/delegation/{prefix}?name={name}"
 */
function _delegation_profile_create ($operator_prefix, $name) {

	$msa_rest_api = "delegation/{$operator_prefix}?name={$name}";
	$curl_cmd = create_msa_operation_request(OP_POST, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "CREATE DELEGATION PROFILE");
	return $response;
}

/**
 * Delete Delegation Profile by Id
 *
 * curl -u ncroot:NCROOT_PWD  -XDELETE "http://localhost:10080/ubi-api-rest/delegation/{id}"
 */
function _delegation_profile_delete_by_id ($delegation_profile_id) {

	$msa_rest_api = "delegation/{$delegation_profile_id}";
	$curl_cmd = create_msa_operation_request(OP_DELETE, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "DELETE DELEGATION PROFILE BY ID");
	return $response;
}

/**
 * Add Delegation to profile
 * 
 * curl -u ncroot:NCROOT_PWD  -XPUT "http://localhost:10080/ubi-api-rest/delegation/{id}/{category}/{subCategory}/{action}?right={right}"
 */
function _delegation_profile_update_delegation ($delegation_profile_id, $category, $sub_category, $action, $right) {

	$msa_rest_api = "delegation/{$delegation_profile_id}/{$category}/{$sub_category}/{$action}?right={$right}";
	$curl_cmd = create_msa_operation_request(OP_PUT, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "ADD DELEGATION TO PROFILE");
	return $response;
}

/**
 * Set Delegation Profile to Customer by Manager
 *
 * curl -u ncroot:NCROOT_PWD  -XPUT "http://localhost:10080/ubi-api-rest/delegation/{id}/{managerId}/{customerId}"
 */
function _delegation_profile_set_to_customer_by_manager ($delegation_profile_id, $manager_id, $customer_id) {

	$msa_rest_api = "delegation/{$delegation_profile_id}/{$manager_id}/{$customer_id}";
	$curl_cmd = create_msa_operation_request(OP_PUT, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "SET DELEGATION PROFILE TO CUSTOMER BY MANAGER");
	return $response;
}

?>