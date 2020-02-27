<?php

require_once COMMON_DIR . 'curl_performer.php';

/**
 * curl -u ncroot:ubiqube  -XGET
 * 'http://localhost:10080/ubi-api-rest/ipam/ip?subnet=192.168.10.1&mask=255.255.255.0'
 */
function _ipam_get_free_address ($subnet, $netmask) {

	$msa_rest_api = "ipam/ip?subnet={$subnet}&mask={$netmask}";
	$curl_cmd = create_msa_operation_request(OP_GET, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "GET FREE IP ADDRESS FROM IPAM");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

?>