<?php

require_once COMMON_DIR . 'curl_performer.php';

/**
 *
 * <pre>
 *        curl -u ncroot:ubiqube  -XPUT http://localhost:10080/ubi-api-rest/device/attach/2355/files/AUTO  -d '
 *         [
 *           { "uri": "Configuration/ABR/ABRA1570/FORTINET/Upload_1" },
 *           { "uri": "Configuration/ABR/ABRA1570/FORTINET/Upload_2" }
 *         ]
 *        '
 * </pre>
 *
 * @param deviceId
 * @param position
 *            on of: POST_CONFIG, PRE_CONFIG, PRE_CUE_CONFIG, POST_CUE_CONFIG, AUTO
 * @param jsonUris
 *            list of repository URIs formated in JSON
*/
function _device_configuration_attach_files_to_device ($device_id, $uris = array(), $position = "AUTO") {

	$msa_rest_api = "device/attach/{$device_id}/files/{$position}";
	$json = json_encode($uris);
	$curl_cmd = create_msa_operation_request(OP_PUT, $msa_rest_api, $json);
	$response = perform_curl_operation($curl_cmd, "ATTACH FILES TO DEVICE");
	return $response;
}

function _device_configuration_attach_file_to_device ($device_id, $uri, $position = "AUTO") {
	$uris_array[0]['uri'] = $uri;
	return _device_configuration_attach_files_to_device($device_id, $uris_array, $position);
}

/**
 *<pre>
 curl -u ncroot:ubiqube  -XPUT http://localhost:10080/ubi-api-rest/device/detach/2355/files  -d '
 [
 { "uri": "Configuration/ABR/ABRA1570/FORTINET/Upload_1" },
 { "uri": "Configuration/ABR/ABRA1570/FORTINET/Upload_2" }
 ]
 '
 *</pre>
 * @param deviceId
 * @param jsonUris
 * @param securityContext
 */
function _device_configuration_detach_files_from_device ($device_id, $uris = array()) {

	$msa_rest_api = "device/detach/{$device_id}/files";
	$json = json_encode($uris);
	$curl_cmd = create_msa_operation_request(OP_PUT, $msa_rest_api, $json);
	$response = perform_curl_operation($curl_cmd, "DETACH FILES FROM DEVICE");
	return $response;
}

function _device_configuration_detach_file_from_device ($device_id, $uri) {
	$uris_array[0]['uri'] = $uri;
	return _device_configuration_detach_files_from_device ($device_id, $uris_array);
}

/**
 * REST endpoint available in MSA NB
 * ex:
 * curl -u ncroot:ubiqube  -XOP_GET http://localhost:10080/ubi-api-rest/device/{deviceId}/files
 */
function _device_configuration_list_files_by_id ($device_id) {

	$msa_rest_api = "device/{$device_id}/files";
	$curl_cmd = create_msa_operation_request(OP_GET, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "LIST FILES BY DEVICE ID");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

?>