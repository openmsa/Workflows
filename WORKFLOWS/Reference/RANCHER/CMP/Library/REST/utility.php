<?php 

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/RANCHER/CMP/Library/constants.php';

/**
 * Create RANCHER CMP CURL operation request
 *
 * @param unknown $operation
 * @param unknown $rancher_rest_api
 * @param string $auth_token
 * @param string $json_body
 * @return string
 */
function create_rancher_operation_request ($operation, $rancher_rest_api, $json_body = "",
											$connection_timeout = 60, $max_time = 60) {

	global $CURL_CMD;
	global $context;

	$RANCHER_HOST = $context['rancher_ip_address'];
	$RANCHER_PORT = $context['rancher_port'];

	if (strpos($rancher_rest_api, "?") !== false) {
		list($uri, $data) = explode("?", $rancher_rest_api);
		$ait = new ArrayIterator(explode("&", $data));
		$cit = new CachingIterator($ait);
		$encoded_data = "";
		foreach ($cit as $data_value) {
			list($name, $value) = explode("=", $data_value);
			$encoded_data .= "{$name}=" . urlencode($value);
			if ($cit->hasNext()) {
				$encoded_data .= "&";
			}
		}
		$ait = new ArrayIterator(explode("/", $uri));
		$cit = new CachingIterator($ait);
		$uri_encoded = "";
		foreach ($cit as $uri_path) {
			$uri_encoded .= rawurlencode($uri_path);
			if ($cit->hasNext()) {
				$uri_encoded .= "/";
			}
		}
		$url = "'https://{$RANCHER_HOST}:{$RANCHER_PORT}/v2-beta/{$uri_encoded}?{$encoded_data}'";
	}
	else {
		$ait = new ArrayIterator(explode("/", $rancher_rest_api));
		$cit = new CachingIterator($ait);
		$uri_encoded = "";
		foreach ($cit as $uri_path) {
			$uri_encoded .= rawurlencode($uri_path);
			if ($cit->hasNext()) {
				$uri_encoded .= "/";
			}
		}
		$url = "'https://{$RANCHER_HOST}:{$RANCHER_PORT}/v2-beta/{$uri_encoded}'";
	}
	
	$content_type = "application/json";
	$accept = "application/json";
	if (strpos($json_body, "@") === 0) {
		$content_type = "*/*";
	}
	else if (strpos($json_body, "file=") === 0) {
		$content_type = "application/x-www-form-urlencoded";
	}
	$authorization = base64_encode($context['rancher_username'] . ":" . $context['rancher_password']);
	$curl_cmd = "{$CURL_CMD} -iksw '\nHTTP_CODE=%{http_code}' -H \"Content-Type: {$content_type}\" -H \"Accept: {$accept}\" -H 'Authorization: Basic {$authorization}' --connect-timeout $connection_timeout --max-time $max_time -X {$operation} {$url}";
	if ($json_body !== "") {
		$curl_cmd .= " -d '" . pretty_print_json($json_body) . "'";
	}
	logToFile("Curl Request : $curl_cmd\n");
	return $curl_cmd;
}

?>
