<?php 

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/VMWARE/vRO/Library/constants.php';

/**
 * Create VMware vRO CURL operation request
 *
 * @param unknown $operation
 * @param unknown $vro_rest_api
 * @param string $auth_token
 * @param string $json_body
 * @return string
 */
function create_vro_operation_request ($operation, $vro_rest_api, $json_body = "",
												$connection_timeout = 60, $max_time = 60) {

	global $CURL_CMD;
	global $context;

	$VRO_HOST = $context['vro_ip_address'];
	$VRO_PORT = $context['vro_port'];

	if (strpos($vro_rest_api, "?") !== false) {
		list($uri, $data) = explode("?", $vro_rest_api);
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
		$url = "'https://{$VRO_HOST}:{$VRO_PORT}/vco/api/{$uri_encoded}?{$encoded_data}'";
	}
	else {
		$ait = new ArrayIterator(explode("/", $vro_rest_api));
		$cit = new CachingIterator($ait);
		$uri_encoded = "";
		foreach ($cit as $uri_path) {
			$uri_encoded .= rawurlencode($uri_path);
			if ($cit->hasNext()) {
				$uri_encoded .= "/";
			}
		}
		$url = "'https://{$VRO_HOST}:{$VRO_PORT}/vco/api/{$uri_encoded}'";
	}
	
	$content_type = "application/json";
	$accept = "application/json";
	if (strpos($json_body, "@") === 0) {
		$content_type = "*/*";
	}
	else if (strpos($json_body, "file=") === 0) {
		$content_type = "application/x-www-form-urlencoded";
	}
	$authorization = base64_encode($context['vcenter_username'] . ":" . $context['vcenter_password']);
	$curl_cmd = "{$CURL_CMD} -iksw '\nHTTP_CODE=%{http_code}' -H \"Content-Type: {$content_type}\" -H \"Accept: {$accept}\" -H 'Authorization: Basic {$authorization}' --connect-timeout $connection_timeout --max-time $max_time -X {$operation} {$url}";
	if ($json_body !== "") {
		$curl_cmd .= " -d '" . pretty_print_json($json_body) . "'";
	}
	logToFile("Curl Request : $curl_cmd\n");
	return $curl_cmd;
}

function vro_add_parameter_in_request (&$parameters, $name, $type, $value, $scope = "local", $description = "") {

	$index = count($parameters);
	$parameters[$index]['name'] = $name;
	$parameters[$index]['type'] = $type;
	$parameters[$index]['value'] = $value;
	$parameters[$index]['scope'] = $scope;
	$parameters[$index]['description'] = $description;
}

?>