<?php
function curl_http_get($SESSION_KEY, $full_url,$body, $HTTP_M)
{
    $CURL_CMD="/usr/bin/curl";
    if($body == "")
    {
    	$body = "{}";
    }
    $curl_cmd = "{$CURL_CMD} -isw '\nHTTP_CODE=%{http_code}' --connect-timeout 600 --max-time 600 -H \"Content-Type: application/json\" -H \"Rest-v2-SessionToken:{$SESSION_KEY}\" -X {$HTTP_M} -k '{$full_url}' -d '{$body}'";
    logToFile( $curl_cmd);

    $response = perform_curl_operation($curl_cmd, "Calling GET HTTP method");
    $response = json_decode($response, true);
    if ($response['wo_status'] !== ENDED) {
    	$response = json_encode($response);
       return $response;
    }
    //$response = json_encode ($final_response,true);
    return $response;
}

function login($USERNAME, $SERVER_PASSWORD, $ip, $port)
{
	$port = ($port != "") ? ":".$port :"";

	$full_url = "https://$ip$port/REST/v2/Authentication/login";	
	$HTTP_M = 'POST';
	$body = array( "username"       => $USERNAME,
                       "password"       => $SERVER_PASSWORD, ); 

	

	$response = curl_http_get("" , $full_url, json_encode($body),$HTTP_M );
	
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		echo $response;
		exit;
	}

	$token = json_decode($response['wo_newparams']['response_body']);
	$token = get_object_vars($token);
        logToFile(debug_dump($token["sessionToken"],"===========TOKEN============="));
	return $token["sessionToken"];
}

function uuid($data){
  assert(strlen($data) == 16);

    $data[6] = chr(ord($data[6]) & 0x0f | 0x40); // set version to 0100
    $data[8] = chr(ord($data[8]) & 0x3f | 0x80); // set bits 6-7 to 10

    return vsprintf('%s%s-%s-%s-%s-%s%s%s', str_split(bin2hex($data), 4));
}


?>
