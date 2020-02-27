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
												$connection_timeout = 60, $max_time = 60) {

	global $CURL_CMD;
	global $CURL_OPENSTACK;
	// curl -i http://ct-int-vip:28774/v2/${PJID}/servers -X POST -H "X-Auth-Token: ${TEST_TOKEN}" -H "Accept: application/json" -H "Content-Type: application/json" -d '{ "server": { "availability_zone": "ote-lab1","flavorRef": "120","imageRef":"0f0ba35a-1445-497f-8630-c8a1d0b97a87","max_count": 1,"min_count": 1,"name": "vyatta_other_tenant_03","networks":[{"uuid":"a4000cdf-835b-4ec0-942d-a456a3b4f495","port_id":"7dceafe1-ef96-4047-b717-dc354eb48ea2"},{"uuid":"3b49fd97-caab-40ef-9fa6-4073d1639e7c","port_id":"7dceafe1-ef96-4047-b717-dc354eb48ea2"}]}}'
	$curl_cmd = "{$CURL_CMD} {$CURL_OPENSTACK} -i -sw '\nHTTP_CODE=%{http_code}' --connect-timeout $connection_timeout --max-time $max_time -k '{$openstack_rest_api}' -X {$operation} -H \"Accept: application/json\" -H \"Content-Type: application/json\"";
	if ($auth_token !== "") {
		$curl_cmd .= " -H \"X-Auth-Token: {$auth_token}\"";
	}
	if ($json_body !== "") {
		$curl_cmd .= " -d '" . pretty_print_json($json_body) . "'";
	}
	logToFile("Curl Request : $curl_cmd\n");
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