<?php

require_once COMMON_DIR . 'utility.php';

/**
 * Create MSA CURL operation request
 *
 * @param unknown $operation
 * @param unknown $msa_rest_api
 * @param string $json_body
 * @return string
 */
function create_msa_operation_request ($operation, $msa_rest_api, $json_body = "",
										$connection_timeout = 60, $max_time = 60) {

	global $CURL_CMD;
	
	$HTTP_HOST = get_vars_value(WEB_NODE_PRIV_IP);
	$HTTP_PORT = get_vars_value(WEB_NODE_HTTP_PORT);
	$USERNAME = "ncroot";
	$NCROOT_PASSWORD = get_vars_value(NCROOT_PASSWORD_VARIABLE);

	if (strpos($msa_rest_api, "?") !== false) {
		list($uri, $data) = explode("?", $msa_rest_api);
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
		$url = "'http://{$HTTP_HOST}:{$HTTP_PORT}/ubi-api-rest/{$uri_encoded}?{$encoded_data}'";
	}
	else {
		$ait = new ArrayIterator(explode("/", $msa_rest_api));
		$cit = new CachingIterator($ait);
		$uri_encoded = "";
		foreach ($cit as $uri_path) {
			$uri_encoded .= rawurlencode($uri_path);
			if ($cit->hasNext()) {
				$uri_encoded .= "/";
			}
		}
		$url = "'http://{$HTTP_HOST}:{$HTTP_PORT}/ubi-api-rest/{$uri_encoded}'";
	}

	$content_type = "application/json";
	if (strpos($json_body, "@") === 0) {
		$content_type = "*/*";
	}
	$curl_cmd = "{$CURL_CMD} -isw '\nHTTP_CODE=%{http_code}' -u {$USERNAME}:\$p --connect-timeout $connection_timeout --max-time $max_time -H \"Content-Type: {$content_type}\" -X {$operation} {$url}";
	if ($json_body !== "") {
		if (is_json($json_body)) {
			$curl_cmd .= " -d '" . pretty_print_json($json_body) . "'";
		}
		else {
		    $json_body = preg_replace("/'/",'', $json_body ); //remove '
		    $curl_cmd .= ' -d '.escapeshellarg($json_body);
		}
	}
	logToFile("Curl Request : $curl_cmd\n");
	$curl_cmd = "p=$(" . ENCP_SCRIPT .  " '{$NCROOT_PASSWORD}');{$curl_cmd}";
	return $curl_cmd;
}

/**
 * Parse Headers from the CURL Response
 *
 * @param unknown $raw_headers
 * @return multitype:string NULL
 */
function http_parse_headers ($raw_headers) {

	$headers = array();
	$key = '';
	foreach(explode("\n", $raw_headers) as $i => $h) {

		$h = explode(':', $h, 2);
		if (isset($h[1])) {
			if (!isset($headers[$h[0]])) {
				$headers[$h[0]] = trim($h[1]);
			}
			elseif (is_array($headers[$h[0]])) {
				$headers[$h[0]] = array_merge($headers[$h[0]], array(trim($h[1])));
			}
			else {
				$headers[$h[0]] = array_merge(array($headers[$h[0]]), array(trim($h[1])));
			}
			$key = $h[0];
		}
		else {
			if (substr($h[0], 0, 1) == "\t") {
				$headers[$key] .= "\r\n\t".trim($h[0]);
			}
			elseif (!$key) {
				$headers[0] = trim($h[0]);
			}
		}
	}
	return $headers;
}

/**
 * Return HTTP Response Message from HTTP Status Code
 *
 * @param unknown $code
 * @return string
 */
function get_http_status_message ($code) {

	switch ($code) {
		case 000:
			$text = 'The connection/transaction was terminated before the completion of the operation.';
			break;
		case 100:
			$text = 'Continue';
			break;
		case 101:
			$text = 'Switching Protocols';
			break;
		case 102:
			$text = 'Processing';
			break;
		/*case 200:
			$text = 'OK';
			break;
		case 201:
			$text = 'Created';
			break;
		case 202:
			$text = 'Accepted';
			break;
		case 203:
			$text = 'Non-Authoritative Information';
			break;
		case 204:
			$text = 'No Content';
			break;
		case 205:
			$text = 'Reset Content';
			break;
		case 206:
			$text = 'Partial Content';
			break;
		case 207:
			$text = 'Multi-Status';
			break;	*/
		case 300:
			$text = 'Multiple Choices';
			break;
		case 301:
			$text = 'Moved Permanently';
			break;
		case 302:
			$text = 'Moved Temporarily';
			break;
		case 303:
			$text = 'See Other';
			break;
		case 304:
			$text = 'Not Modified';
			break;
		case 305:
			$text = 'Use Proxy';
			break;
		case 400:
			$text = 'Bad Request';
			break;
		case 401:
			$text = 'Authorization Required';
			break;
		case 402:
			$text = 'Payment Required';
			break;
		case 403:
			$text = 'Forbidden';
			break;
		case 404:
			$text = 'Resource Not Found';
			break;
		case 405:
			$text = 'Method Not Allowed';
			break;
		case 406:
			$text = 'Not Acceptable';
			break;
		case 407:
			$text = 'Proxy Authentication Required';
			break;
		case 408:
			$text = 'Request Time-out';
			break;
		case 409:
			$text = 'Conflicting Request';
			break;
		case 410:
			$text = 'Gone';
			break;
		case 411:
			$text = 'Content Length Required';
			break;
		case 412:
			$text = 'Precondition Failed';
			break;
		case 413:
			$text = 'Request Entity Too Large';
			break;
		case 414:
			$text = 'Request-URI Too Long';
			break;
		case 415:
			$text = 'Unsupported Media Type';
			break;
		case 416:
			$text = 'Requested Range Not Satisfiable';
			break;
		case 417:
			$text = 'Expectation Failed';
			break;
		case 418:
			$text = 'I am a teapot';
			break;
		case 419:
			$text = 'Authentication Timeout';
			break;
		case 420:
			$text = 'Enhance Your Calm';
			break;
		case 422:
			$text = 'Unprocessable Entity';
			break;
		case 423:
			$text = 'Locked';
			break;
		case 424:
			$text = 'Method Failure';
			break;
		case 425:
			$text = 'Unordered Collection';
			break;
		case 426:
			$text = 'Upgrade Required';
			break;
		case 428:
			$text = 'Precondition Required';
			break;
		case 429:
			$text = 'Too Many Requests';
			break;
		case 431:
			$text = 'Request Header Fields Too Long';
			break;
		case 444:
			$text = 'No Response';
			break;
		case 449:
			$text = 'Retry With';
			break;
		case 450:
			$text = 'Blocked by Windows Parental Controls';
			break;
		case 451:
			$text = 'Unavailable For Legal Reasons';
			break;
		case 494:
			$text = 'Request Header Too Large';
			break;
		case 495:
			$text = 'Cert Error';
			break;
		case 496:
			$text = 'No Cert';
			break;
		case 497:
			$text = 'HTTP to HTTPS';
			break;
		case 499:
			$text = 'Client Closed Request';
			break;
		case 500:
			$text = 'Internal Server Error';
			break;
		case 501:
			$text = 'Not Implemented';
			break;
		case 502:
			$text = 'Bad Gateway';
			break;
		case 503:
			$text = 'Service Unavailable';
			break;
		case 504:
			$text = 'Gateway Time-out';
			break;
		case 505:
			$text = 'HTTP Version not supported';
			break;
		case 506:
			$text = 'Variant Also Negotiates';
			break;
		case 507:
			$text = 'Insufficient Storage';
			break;
		case 508:
			$text = 'Loop Detected';
			break;
		case 509:
			$text = 'Bandwidth Limit Exceeded';
			break;
		case 510:
			$text = 'Not Extended';
			break;
		case 511:
			$text = 'Network Authentication Required';
			break;
		case 598:
			$text = 'Network read timeout error';
			break;
		case 599:
			$text = 'Network connect timeout error';
			break;
		default:
			$text = 'Unknown HTTP status code ' . $code;
			break;
	}
	return $text;
}

/**
 * Perform CURL operation
 *
 * @param unknown $curl_cmd
 * @return multitype:string
 */
function perform_curl_operation ($curl_cmd, $operation = "") {

	$output_array = array();
	$verbose_details = '';

	if (preg_match("/\s+-v\s+/", $curl_cmd)) {
    		//used -v (verbose mode), we separate the error return (stderr) into the  $verbose_details

    		$descriptorspec = array(
      			0 => array("pipe", "r"),  // stdin  read input
      			1 => array("pipe", "w"),  // stdout write output
      			2 => array("pipe", "w")   // stderr error output
    		);

    		$process = proc_open($curl_cmd, $descriptorspec, $pipes);

    		if (is_resource($process)) {
			fclose($pipes[0]);
      			$out = stream_get_contents($pipes[1]);
      			fclose($pipes[1]);
      			$out = preg_replace("/\r/",'',$out); //remove carriage
      			$output_array = explode("\n",$out);  //reput result into one table
      			$verbose_details = stream_get_contents($pipes[2]);
      			fclose($pipes[2]);
			proc_close($process);
      		}
    	}
	else {
  		exec($curl_cmd, $output_array);
	}

	$result = '';
	$headers_and_response = array();
	$headers_and_response_count = 1;
	$wo_newparams = array();
	foreach ($output_array as $line) {
		if (strpos($line, 'HTTP_CODE') !== 0) {
			$result .= "{$line}\n";
		}
		else {
			if (strpos($line, 'HTTP_CODE=20') !== 0 && strpos($line, 'HTTP_CODE=300') !== 0 && strpos($line, 'HTTP_CODE=100') !== 0) {
				if ($operation !== "") {
					logToFile("$operation FAILED");
				}
				$result = rtrim($result);
				$headers_and_response = explode("\n\n", $result);
				$headers_and_response_count = count($headers_and_response);
				if ($headers_and_response_count > 1) {
					$raw_headers = $headers_and_response[$headers_and_response_count - 2];
					$response_body = $headers_and_response[$headers_and_response_count - 1];
					if (is_json($response_body)) {
						$response_body = pretty_print_json($response_body);
					}
				}
				else {
					$raw_headers = $headers_and_response[$headers_and_response_count - 1];
					$response_body = "";
				}
				if ($verbose_details !== "") {
					logToFile("Curl Response :\n$verbose_details\n$raw_headers\n\n$response_body\n");
				}
				else {
					logToFile("Curl Response :\n$raw_headers\n\n$response_body\n");
				}
				if (strpos($response_body, "<html>") !== false || strpos($line, 'HTTP_CODE=000') !== false) {
					$http_status_code = intval(substr($line, strpos('HTTP_CODE=', $line) + strlen('HTTP_CODE=')));
					$response_body = get_http_status_message($http_status_code);
				}
				$message = "Call to API Failed : $line\nError Message : $response_body";
				$response = prepare_json_response(FAILED, $message, $wo_newparams, true);
				return $response;
			}
		}
	}

	$result = rtrim($result);
	$headers_and_response = explode("\n\n", $result);
	$headers_and_response_count = count($headers_and_response);
	if ($headers_and_response_count > 1) {
		$raw_headers = $headers_and_response[$headers_and_response_count - 2];
		$response_body = $headers_and_response[$headers_and_response_count - 1];
		#$response_headers = http_parse_headers($raw_headers);
		$wo_newparams['response_raw_headers'] = $raw_headers;
		$wo_newparams['response_body'] = $response_body;
		if (is_json($response_body)) {
			$response_body = pretty_print_json($response_body);
		}
		logToFile("Curl Response :\n$raw_headers\n\n$response_body\n");
	}
	else {
		$wo_newparams['response_raw_headers'] = $result;
		logToFile("Curl Response :\n$result\n");
	}
	
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $wo_newparams);
	return $response;
}

?>
