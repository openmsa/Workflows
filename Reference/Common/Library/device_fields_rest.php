<?php

require_once COMMON_DIR . 'curl_performer.php';

/**
 * REST endpoint available in MSA NB
 * ex:
 * curl -u ncroot:ubiqube  -XGET http://localhost:10080/ubi-api-rest/deviceFields/1234/serialNumber
 */
function _device_fields_get_serial_number ($device_id) {

    $msa_rest_api = "deviceFields/{$device_id}/serialNumber";
    $curl_cmd = create_msa_operation_request(OP_GET, $msa_rest_api);
    $response = perform_curl_operation($curl_cmd, "GET DEVICE SERIAL NUMBER");
    $response = json_decode($response, true);
    if ($response['wo_status'] !== ENDED) {
        $response = json_encode($response);
        return $response;
    }
    if (array_key_exists('response_body', $response['wo_newparams'])) {
        $response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
    }
    else {
        $response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']);
    }
    return $response;
}

/**
 * curl -u ncroot:ubiqube  -XPUT http://localhost:10080/ubi-api-rest/deviceFields/1234/serialNumber/FGT12345
 */
function _device_fields_set_serial_number ($device_id, $serial_number = "") {

	$msa_rest_api = "deviceFields/{$device_id}/serialNumber/{$serial_number}";
	$curl_cmd = create_msa_operation_request(OP_PUT, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "SET DEVICE SERIAL NUMBER");
	return $response;
}

/**
 * curl -u ncroot:ubiqube  -XPUT http://localhost:10080/ubi-api-rest/deviceFields/1234/emailAlerting?activate=true
 */
function _device_fields_email_alerting ($device_id, $email_alerting_activate) {

	$msa_rest_api = "deviceFields/{$device_id}/emailAlerting?activate={$email_alerting_activate}";
	$curl_cmd = create_msa_operation_request(OP_PUT, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "SET DEVICE EMAIL ALERTING");
	return $response;
}

?>