<?php 

require_once '/opt/fmc_repository/Process/Reference/OPENSTACK/Library/REST/utility.php';

#curl -i http://10.1.144.111:8774/v2/ebd239c789994f3a88d6da7083098851/flavors -X POST 
#-H "X-Auth-Token:fb7317fa0c3c43949ccbe9de55dfba85" -H "Accept: application/json" -H "Content-type: application/json"
# -d '{"flavor" :{ "name":"test-flavor2","ram":1024,"vcpus":2,"disk":10,"os-flavor-access:is_public": false}}'
function _list_stacks_resources ($stacks_endpoint, $auth_token, $stack_name, $stack_id) {
	
	$openstack_rest_api = "{$stacks_endpoint}/stacks/{$stack_name}/{$stack_id}/resources";
	$curl_cmd = create_openstack_operation_request(OP_GET, $openstack_rest_api, $auth_token);
	$response = perform_curl_operation($curl_cmd, "IMPORT STACK RESOURCES");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

?>
