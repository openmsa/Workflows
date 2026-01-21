<?php 

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/OPENSTACK/Library/constants.php';

/**
 * Create Openstack CURL operation request
 *
 * @param unknown $operation
 * @param unknown $openstack_rest_api
 * @param string $auth_token
 * @param string $json_body
 * @return string
 */
function create_openstack_operation_request ($operation, $openstack_rest_api, $auth_token = "", $json_body = "",
												$connection_timeout = OS_CURL_CONNECTION_TIMEOUT, $max_time = OS_CURL_MAX_TIME) {

	global $CURL_CMD;
	global $CURL_OPENSTACK;
	global $OS_CURL_VERBOSE;
	global $OS_CURL_RETRY_COUNT;
	global $OS_CURL_RETRY_DELAY;
	global $OS_CURL_RETRY_MAX_TIME;
	global $context;

	// curl -i http://xxxxxx:28774/v2/${PJID}/servers -X POST -H "X-Auth-Token: ${TEST_TOKEN}" -H "Accept: application/json" -H "Content-Type: application/json" -d '{ "server": { "availability_zone": "ote-lab1","flavorRef": "120","imageRef":"0f0ba35a-1445-497f-8630-c8a1d0b97a87","max_count": 1,"min_count": 1,"name": "vyatta_other_tenant_03","networks":[{"uuid":"a4000cdf-835b-4ec0-942d-a456a3b4f495","port_id":"7dceafe1-ef96-4047-b717-dc354eb48ea2"},{"uuid":"3b49fd97-caab-40ef-9fa6-4073d1639e7c","port_id":"7dceafe1-ef96-4047-b717-dc354eb48ea2"}]}}'
//  /usr/bin/curl --tlsv1.2 -i -sw '

	$curl_cmd = "{$CURL_CMD} {$CURL_OPENSTACK} -i -sw '\nHTTP_CODE=%{http_code}' {$OS_CURL_VERBOSE} --connect-timeout $connection_timeout --max-time $max_time {$OS_CURL_RETRY_COUNT} {$OS_CURL_RETRY_DELAY} {$OS_CURL_RETRY_MAX_TIME} -k '{$openstack_rest_api}' -X {$operation} -H \"Accept: application/json\" -H \"Content-Type: application/json\"";
	if ($auth_token !== "") {
    //We can check if the Auth-Token(token_id) has expired
    if (isset($context['token_id']) && isset($context['keystone_admin_endpoint']) && isset($context['user_domain_id']) && isset($context['admin_username']) && isset($context['admin_password']) && isset($context['project_domain_id']) && isset($context['admin_tenant_id']) ){
      if (! isset($context['token_id_expire']) || (isset($context['token_id_expire']) && $context['token_id_expire'] < time()) ) {
        //We should get a new token_id
        $response = _keystone_project_scoped_token_get($context['keystone_admin_endpoint'], $context['user_domain_id'], $context['admin_username'],
                           $context['admin_password'], $context['project_domain_id'], $context['admin_tenant_id']);
        $response = json_decode($response, true);
        if ($response['wo_status'] !== ENDED) {
          $response = prepare_json_response(FAILED, $response['wo_comment'], $context, true);
          echo $response;
          exit;
        }

        $response_raw_headers = $response['wo_newparams']['response_raw_headers'];
        $response_headers = http_parse_headers($response_raw_headers);
        $context['token_id'] = $response_headers[X_SUBJECT_TOKEN];
        $context['token_id_expire'] = time() + OPENSTACK_TOKEN_ID_EXPIRE_SEC; // expire in OPENSTACK_TOKEN_ID_EXPIRE_SEC secondes
        $auth_token = $context['token_id'];
	      logToFile(__FILE__ . ' Get new token successfull, expire in '.OPENSTACK_TOKEN_ID_EXPIRE_SEC.' secondes');
      }else{
	      logToFile(__FILE__ . '  Token not expired');
      }
    }else{
	      logToFile(__FILE__ . ' Can not check token_id expire date because missing datas, exist keystone_admin_endpoint='. isset($context['keystone_admin_endpoint']).', exist user_domain_id='.isset($context['user_domain_id']).', exist admin_username='.isset($context['admin_username']).', exist admin_password='.isset($context['admin_password']).', exist project_domain_id='.isset($context['project_domain_id']).', exist admin_tenant_id='.isset($context['admin_tenant_id']));
    }
		$curl_cmd .= " -H \"X-Auth-Token: {$auth_token}\"";
	}
	if ($json_body !== "") {
		$curl_cmd .= " -d '" . pretty_print_json($json_body) . "'";
	}
	logToFile("Curl Request : $curl_cmd\n");
  // Curl Request : /usr/bin/curl --tlsv1.2 -i -sw 'HTTP_CODE=%{http_code}' -v --connect-timeout 120 --max-time 120 --retry 3 --retry-delay 10 --retry-max-time 180 -k 'https://xxxxxx/v2.0/ports/84f29670-e90b-43b7-9051-2d595b71efe8' -X DELETE -H "Accept: application/json" -H "Content-Type: application/json" -H "X-Auth-Token: 9cb83397749145c0b1543e0..."
	return $curl_cmd;
}

/**
 * Seperate keystone v3 endponints by Name
 *
 * @param unknown $endpoints
 * @return Ambigous <multitype:, unknown>
 */
function seperate_endpoints_v3 ($endpoints) {

	$result = array();
	foreach ($endpoints as $endpoint) {
		$result[$endpoint['name']]['type'] = $endpoint['type'];
		foreach ($endpoint['endpoints'] as $endpnt) {
			if ($endpnt['interface'] === "internal") {
				$result[$endpoint['name']][INTERNAL_URL] = $endpnt['url'];
			}
			else if ($endpnt['interface'] === "admin") {
				$result[$endpoint['name']][ADMIN_URL] = $endpnt['url'];
			}
			else if ($endpnt['interface'] === "public") {
				$result[$endpoint['name']][PUBLIC_URL] = $endpnt['url'];
			}
		}
	}
	return $result;
}

/**
 * Seperate keystone v2.0 endponints by Name
 *
 * @param unknown $endpoints
 * @return Ambigous <multitype:, unknown>
 */
function seperate_endpoints_v2 ($endpoints) {

	$result = array();
	foreach ($endpoints as $endpoint) {
		$result[$endpoint['name']]['type'] = $endpoint['type'];
		$result[$endpoint['name']]['endpoints'] = $endpoint['endpoints'];
	}
	return $result;
}

?>