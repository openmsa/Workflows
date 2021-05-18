<?php

require_once COMMON_DIR . 'curl_performer.php';

/**
 * Create Configuration Profile
 * 
 * curl -u ncroot:PWD  -XPOST "http://localhost:10080/ubi-api-rest/profile/configuration/{customerId}/{profileName}?reference={externalReference}&comment={comment}&manufacturerId={manufacturerId}&modelId={modelId}"
 */
function _profile_configuration_create ($customer_id, $profile_name, $reference = "", $comment = "", $manufacturer_id = "", $model_id = "") {

	$msa_rest_api = "profile/configuration/{$customer_id}/{$profile_name}?reference={$reference}&comment={$comment}";
	if (!empty($manufacturer_id) && !empty($model_id)) {
		$msa_rest_api .= "&manufacturerId={$manufacturer_id}&modelId={$model_id}";
	}
	$curl_cmd = create_msa_operation_request(OP_POST, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "CREATE CONFIGURATION PROFILE");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
        $response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}


/**
 * List all configuration profiles by customer ID
 *
 * curl -u ncroot:PWD  -XGET "http://localhost:10080/ubi-api-rest/conf-profile/v2/list/customer/{customerId}"
 */
function _profile_configuration_list_by_customer_id ($customer_id) {

        $msa_rest_api = "conf-profile/v2/list/customer/{$customer_id}";
        $curl_cmd = create_msa_operation_request(OP_GET, $msa_rest_api);
        $response = perform_curl_operation($curl_cmd, "LIST CONFIGURATION PROFILE");
        $response = json_decode($response, true);
        if ($response['wo_status'] !== ENDED) {
                $response = json_encode($response);
                return $response;
        }
        return json_decode($response['wo_newparams']['response_body'], true);
}

/**
 * List all configuration profiles by customer ID
 *
 * curl -u ncroot:PWD  -XGET "http://localhost:10080/ubi-api-rest/conf-profile/v2/list/customer/{customerId}"
 */
function _profile_configuration_list_by_customer_id ($customer_id) {

        $msa_rest_api = "conf-profile/v2/list/customer/{$customer_id}";
        $curl_cmd = create_msa_operation_request(OP_GET, $msa_rest_api);
        $response = perform_curl_operation($curl_cmd, "LIST CONFIGURATION PROFILE");
        $response = json_decode($response, true);
        if ($response['wo_status'] !== ENDED) {
                $response = json_encode($response);
                return $response;
        }
        return json_decode($response['wo_newparams']['response_body'], true);
}

/**
 * Attach Files to configuration profile
 * 
 * curl -u ncroot:ubiqube  -XPUT http://localhost:10080/ubi-api-rest/profile/configuration/attach/2355/files/AUTO  -d '
 * [
 *     { "uri": "Configuration/ABR/ABRA1570/FORTINET/Upload_1" },
 *     { "uri": "Configuration/ABR/ABRA1570/FORTINET/Upload_2" }
 * ]'
 */
function _profile_configuration_attach_files ($profile_id, $uris = array(), $position = "AUTO") {

	$msa_rest_api = "profile/configuration/attach/{$profile_id}/files/{$position}";
	$curl_cmd = create_msa_operation_request(OP_PUT, $msa_rest_api, json_encode($uris));
	$response = perform_curl_operation($curl_cmd, "ATTACH FILES TO CONFIGURATION PROFILE");
	return $response;
}

/**
 * Detach Files from configuration profile
 *
 * curl -u ncroot:ubiqube  -XPUT http://localhost:10080/ubi-api-rest/profile/configuration/detach/2355/files  -d '
 * [
 *     { "uri": "Configuration/ABR/ABRA1570/FORTINET/Upload_1" },
 *     { "uri": "Configuration/ABR/ABRA1570/FORTINET/Upload_2" }
 * ]'
 */
function _profile_configuration_detach_files ($profile_id, $uris = array()) {

	$msa_rest_api = "profile/configuration/detach/{$profile_id}/files";
	$curl_cmd = create_msa_operation_request(OP_PUT, $msa_rest_api, json_encode($uris));
	$response = perform_curl_operation($curl_cmd, "DETACH FILES FROM CONFIGURATION PROFILE");
	return $response;
}

/**
 * Delete Configuration Profile by Id
 * 
 * curl -u ncroot:PWD  -XDELETE "http://localhost:10080/ubi-api-rest/profile/configuration/{customerId}/{profileId}"
 */
function _profile_configuration_delete_by_id ($customer_id, $profile_id) {

	$msa_rest_api = "profile/configuration/{$customer_id}/{$profile_id}";
	$curl_cmd = create_msa_operation_request(OP_DELETE, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "DELETE CONFIGURATION PROFILE BY ID");
	return $response;
}

/**
 * Export Monitoring Profile
 * 
 * curl -u ncroot:PWD  -XPOST "http://localhost:10080/ubi-api-rest/profile/monitoring/export/{profileId}"
 */
function _profile_monitoring_export ($profile_id) {

	$msa_rest_api = "profile/monitoring/export/{$profile_id}";
	$curl_cmd = create_msa_operation_request(OP_POST, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "EXPORT MONITORING PROFILE");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

/**
 * Import Monitoring Profile
 *
 * curl -u ncroot:PWD  -XPOST "http://localhost:10080/ubi-api-rest/profile/monitoring/import/{customerId}/{profileName}"
 */
function _profile_monitoring_import ($customer_id, $profile_name) {

	$msa_rest_api = "profile/monitoring/import/{$customer_id}/{$profile_name}";
	$curl_cmd = create_msa_operation_request(OP_POST, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "IMPORT MONITORING PROFILE");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

/**
 * Update Monitoring Profile only
 *
 * curl -u ncroot:PWD  -XPUT "http://localhost:10080/ubi-api-rest/profile/monitoring/{customerId}/{profileId}?name={name}&comment={comment}&reference={reference}"
 */
function _profile_monitoring_update ($customer_id, $profile_id, $name = "", $comment = "", $reference = "") {

	$msa_rest_api = "profile/monitoring/{$customer_id}/{$profile_id}";
	if ($name !== "") {
		$msa_rest_api .= "?name={$name}";
	}
	if ($comment !== "") {
		if (strpos($msa_rest_api, "?") === false) {
			$msa_rest_api .= "?";
		}
		else {
			$msa_rest_api .= "&";
		}
		$msa_rest_api .= "comment={$comment}";
	}
	if ($reference !== "") {
		if (strpos($msa_rest_api, "?") === false) {
			$msa_rest_api .= "?";
		}
		else {
			$msa_rest_api .= "&";
		}
		$msa_rest_api .= "reference={$reference}";
	}
	$curl_cmd = create_msa_operation_request(OP_PUT, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "UPDATE MONITORING PROFILE");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

/**
 * Delete Monitoring Profile by Id
 *
 * curl -u ncroot:PWD  -XDELETE "http://localhost:10080/ubi-api-rest/profile/monitoring/{customerId}/{profileId}"
 */
function _profile_monitoring_delete_by_id ($customer_id, $profile_id) {

	$msa_rest_api = "profile/monitoring/{$customer_id}/{$profile_id}";
	$curl_cmd = create_msa_operation_request(OP_DELETE, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "DELETE MONITORING PROFILE BY ID");
	return $response;
}

/**
 * Attach Profile to Device by Reference
 * 
 * curl -u ncroot:PWD  -XPOST "http://localhost:10080/ubi-api-rest/profile/{profileReference}/attach?device={deviceReference}"
 */
function _profile_attach_to_device_by_reference ($profile_reference, $device_reference) {

	$msa_rest_api = "profile/{$profile_reference}/attach?device={$device_reference}";
	$curl_cmd = create_msa_operation_request(OP_PUT, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "ATTACH PROFILE TO DEVICE BY REFERENCE");
	return $response;
}

/**
 * Detach Profile from Device by Reference
 *
 * curl -u ncroot:PWD  -XPOST "http://localhost:10080/ubi-api-rest/profile/{profileReference}/detach?device={deviceReference}"
 */
function _profile_detach_from_device_by_reference ($profile_reference, $device_reference) {

	$msa_rest_api = "profile/{$profile_reference}/detach?device={$device_reference}";
	$curl_cmd = create_msa_operation_request(OP_PUT, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "DETACH PROFILE FROM DEVICE BY REFERENCE");
	return $response;
}

?>
