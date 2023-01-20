<?php

require_once '/opt/fmc_repository/Process/Reference/OPENSTACK/Library/REST/utility.php';

#export TEST_TOKEN=`curl -si 'http://xxxxxx/v3/auth/tokens' -X OP_POST -H 'Accept: application/json' 
#-H 'Content-type: application/json' 
#-d '{'auth': {'identity': {'methods': ['password'], 'password': {'user': {'domain': {'name': 'Default'}, 
#'name': 'abc', 'password': 'abc'}}},  'scope': {'project': {'domain': {'name': 'Default'}, 
#'name': 'xyz'}}}}' | grep X-Subject-Token | awk '{print $2}' | sed 's/\r//'`; echo $TEST_TOKEN
function _keystone_project_scoped_token_get ($keystone_endpoint, $userdomain, $username, $password, 
									$scopedomain, $projectname) {
	
	$array = array();
	$array['domain'] = array('id' => $userdomain);
	//$array['domain'] = array('name' => $userdomain);
	$array['user'] = array('domain' => $array['domain'], 'name' => $username, 'password' => $password);
	$array['password'] = array('user' => $array['user']);

	$array['domain'] = array('id' => $scopedomain);
	//$array['domain'] = array('name' => $scopedomain);
	$array['project'] = array('domain' => $array['domain'], 'id' => $projectname);
	$array['scope'] = array('project' => $array['project']);
	
	$array['identity'] = array('methods' => array('password'), 'password' => $array['password']);
	$array['auth'] = array('identity' => $array['identity'], 'scope' => $array['scope']); 
	
	$token_array = array('auth' => $array['auth']);
	$json = json_encode($token_array);
	$openstack_rest_api = "{$keystone_endpoint}/auth/tokens";
	$curl_cmd = create_openstack_operation_request(OP_POST, $openstack_rest_api, "", $json);
	$response = perform_curl_operation($curl_cmd, "PROJECT TOKEN GET");
	return $response;
}

#export ADMIN_TOKEN=`curl -si -X OP_POST http://xxxxxxxxxx/v3/auth/tokens -H "Accept: application/json" 
#-H "Content-type: application/json" -d '{"auth": {"identity": {"methods": ["password"], 
#"password": {"user": {"domain": {"name": "dmnAdmin"}, "name": "usrDmnAdmin", "password": "xxxxxxxx"}}},  
#"scope": {"domain":  {"name": "Default"}}}}' | grep X-Subject-Token | awk '{print $2}' | sed 's/\r//'`;echo $ADMIN_TOKEN
function _keystone_domain_scoped_token_get ($keystone_endpoint, $userdomain, $username, $password, $scopedomain) {

	$array = array();
	$array['domain'] = array('name' => $userdomain);
	$array['user'] = array('domain' => $array['domain'], 'name' => $username, 'password' => $password);
	$array['password'] = array('user' => $array['user']);

	$array['domain'] = array('name' => $scopedomain);
	$array['scope'] = array('domain' => $array['domain']);

	$array['identity'] = array('methods' => array('password'), 'password' => $array['password']);
	$array['auth'] = array('identity' => $array['identity'], 'scope' => $array['scope']);

	$token_array = array('auth' => $array['auth']);
	$json = json_encode($token_array);
	$openstack_rest_api = "{$keystone_endpoint}/auth/tokens";
	$curl_cmd = create_openstack_operation_request(OP_POST, $openstack_rest_api, "", $json);
	$response = perform_curl_operation ($curl_cmd, "ADMIN TOKEN GET");
	return $response;
}

#curl -si 'http://xxxxxxxxxxxxxxx/v2.0/tokens' -H "Content-type: application/json" 
#-d '{ "auth": {"tenantId": "1234", "passwordCredentials" : {"username": "admin", "password": "admin123"}}}'
function _keystone_v2_token_get ($keystone_endpoint, $username, $password, $tenant_id) {

	$array = array();
	$array['passwordCredentials'] = array('username' => $username, 'password' => $password);
	$array['auth'] = array('tenantId' => $tenant_id, 'passwordCredentials' => $array['passwordCredentials']);
	$token_array = array('auth' => $array['auth']);	
	
	$json = json_encode($token_array);
	$openstack_rest_api = "{$keystone_endpoint}/tokens";
	$curl_cmd = create_openstack_operation_request(OP_POST, $openstack_rest_api, "", $json);
	$response = perform_curl_operation($curl_cmd, "KEYSTONE V2.0 TOKEN GET");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

#curl -i -X OP_POST http://xxxxxxxxxxx/v3/users -H "X-Auth-Token: ${ADMIN_TOKEN}" -H "Accept: application/json" 
#-H "Content-type: application/json" -d 
#'{"user": {"domain_id": "v2AccessDomain", "enabled": true,"name": "abc"}}'
function _keystone_user_create ($keystone_endpoint, $auth_token, $domain_id, $name, $enabled = "true") {
	
	$array = array();
	$array['domain_id'] = $domain_id;
	$array['name'] = $name;
	$array['enabled'] = $enabled;
	$user_array = array('user' => $array);
	$json = json_encode($user_array);
	
	$openstack_rest_api = "{$keystone_endpoint}/users";
	$curl_cmd = create_openstack_operation_request(OP_POST, $openstack_rest_api, $auth_token, $json);
	
	$response = perform_curl_operation ($curl_cmd, "USER CREATE");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

#url -i -X PATCH http://xxxxxxxx/v3/users/c02b1913b277410784c6956e24360141 -H "X-Auth-Token: ${ADMIN_TOKEN}" 
#-H "Accept: application/json" -H "Content-type: application/json" -d '{"user": {"password": "abc"}}'
function _keystone_user_password_update ($keystone_endpoint, $auth_token, $user_id, $password) {
	
	$array = array();
	$array['password'] = $password;
	$user_array = array('user' => $array);
	$json = json_encode($user_array);
	
	$openstack_rest_api = "{$keystone_endpoint}/users/{$user_id}";
	$curl_cmd = create_openstack_operation_request(OP_PATCH, $openstack_rest_api, $auth_token, $json);	
	$response = perform_curl_operation ($curl_cmd, "USER PASSWORD UPDATE");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

#curl -i -X OP_POST http://xxxxxxxxx/v3/projects -H "X-Auth-Token: ${ADMIN_TOKEN}" -H "Accept: application/json" 
#-H "Content-type: application/json" -d 
#'{"project": {"enabled": true, "domain_id": "v2AccessDomain", "description": null,"name": "abc"}}'
function _keystone_project_create ($keystone_endpoint, $auth_token, $domain_id, $name, $enabled = "true", $description = "") {

	$array = array();
	$array['domain_id'] = $domain_id;
	$array['name'] = $name;
	$array['enabled'] = $enabled;
	$array['description'] = $description;
	$project_array = array('project' => $array);
	
	$json = json_encode($project_array);
	$openstack_rest_api = "{$keystone_endpoint}/projects";
	$curl_cmd = create_openstack_operation_request(OP_POST, $openstack_rest_api, $auth_token, $json);
	$response = perform_curl_operation ($curl_cmd, "PROJECT CREATE");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

#curl -i -X OP_PUT http://xxxxxxxxxxx/v3/projects/${PJID}/users/$USERID/roles/$ROLEID -H "X-Auth-Token: ${ADMIN_TOKEN}" 
#-H "Accept: application/json" -H "Content-type: application/json"
function _keystone_user_role_add ($keystone_endpoint, $auth_token, $tenant_id, $user_id, $role_id) {

	$openstack_rest_api = "{$keystone_endpoint}/projects/{$tenant_id}/users/{$user_id}/roles/{$role_id}";
	$curl_cmd = create_openstack_operation_request(OP_PUT, $openstack_rest_api, $auth_token);
	$response = perform_curl_operation ($curl_cmd, "USER ROLE ADD");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

?>
