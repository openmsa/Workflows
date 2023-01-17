<?php

require_once '/opt/fmc_repository/Process/Reference/OPENSTACK/Library/REST/utility.php';

#curl -i http://xxxxxxxxx:9696/v2.0/networks.json -X OP_POST -H "X-Auth-Token: ${TEST_TOKEN}" 
#-H "Accept: application/json" -H "Content-Type: application/json" -d 
#'{"network": {"name": "abc", "admin_state_up": true}}'
function _neutron_network_create ($neutron_endpoint, $auth_token, $name, $admin_state_up = true) {
	
	$array = array();
	$array['name'] = $name;
	$array['admin_state_up'] = $admin_state_up;
	$network_array = array('network' => $array);
	$json = json_encode($network_array);
	
	$openstack_rest_api = "{$neutron_endpoint}/v2.0/networks";
	$curl_cmd = create_openstack_operation_request(OP_POST, $openstack_rest_api, $auth_token, $json);
	
	$response = perform_curl_operation($curl_cmd, "NETWORK CREATE");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;	
}

/**
*
* Get Networks
*
**/

function _neutron_subnets_from_name($neutron_endpoint, $auth_token, $networks)
{
	$openstack_rest_api = "{$neutron_endpoint}/v2.0/networks";
	$curl_cmd = create_openstack_operation_request(OP_GET, $openstack_rest_api, $auth_token);

	$response = perform_curl_operation($curl_cmd, "GET NETWORKS");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		return json_encode($response);
	}

	$response = stripslashes($response['wo_newparams']['response_body']);
	$subnets = array();
	if (isset($networks) && ! empty($networks)) {
		foreach ($networks as &$network) {
			$nets = json_decode($response, true);
			foreach ($nets['networks'] as &$net) {
				if ($net['name'] == $network) {
					$subnets[] = $net['subnets'];
				}
			}
		}
	}
	return prepare_json_response(ENDED, ENDED_SUCCESSFULLY, json_encode($subnets));
}

function _neutron_networks_from_name($neutron_endpoint, $auth_token, $networks)
{
	$openstack_rest_api = "{$neutron_endpoint}/v2.0/networks";
	$curl_cmd = create_openstack_operation_request(OP_GET, $openstack_rest_api, $auth_token);

	$response = perform_curl_operation($curl_cmd, "GET NETWORKS");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		return json_encode($response);
	}

	$response = stripslashes($response['wo_newparams']['response_body']);
	$network_list = array();
	if (isset($networks) && ! empty($networks)) {
		foreach ($networks as &$network) {
			$nets = json_decode($response, true);
			foreach ($nets['networks'] as &$net) {
				if ($net['name'] == $network) {
					$network_list[] = $net['id'];
				}
			}
		}
	}
	return prepare_json_response(ENDED, ENDED_SUCCESSFULLY, json_encode($network_list));
}

/***
* GET routers
*
**/
function _neutron_routers_by_routers_name($neutron_endpoint, $auth_token, $routers)
{
	$openstack_rest_api = "{$neutron_endpoint}/v2.0/routers";
	$curl_cmd = create_openstack_operation_request(OP_GET, $openstack_rest_api, $auth_token);

	$response = perform_curl_operation($curl_cmd, "GET ROUTERS");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		return json_encode($response);
	}

	$response = stripslashes($response['wo_newparams']['response_body']);
	$router_list = array();
	if (isset($routers) && ! empty($routers)) {
		foreach ($routers as &$router) {
			$rts = json_decode($response, true);
			foreach ($rts['routers'] as &$rt) {
				if ($rt['name'] == $router) {
					$router_list[] = $rt['id'];
				}
			}
		}
	}
	return prepare_json_response(ENDED, ENDED_SUCCESSFULLY, json_encode($router_list));
}


#curl -i http://xxxxxxxxx:9696/v2.0/subnets.json -X OP_POST -H "X-Auth-Token: ${TEST_TOKEN}" 
#-H "Accept: application/json" -H "Content-Type: application/json" 
#-d '{"subnet": {"network_id": "abc", "ip_version": 4,"cidr": "192.168.100.0/24"}}'
function _neutron_subnet_create($neutron_endpoint, $auth_token, $network_id, $ip_version, $cidr)
{
	$array = array();
	$array['network_id'] = $network_id;
	$array['ip_version'] = $ip_version;
	$array['cidr'] = $cidr;
	$subnet_array = array(
		'subnet' => $array
	);
	$json = json_encode($subnet_array);

	$openstack_rest_api = "{$neutron_endpoint}/v2.0/subnets";
	$curl_cmd = create_openstack_operation_request(OP_POST, $openstack_rest_api, $auth_token, $json);

	$response = perform_curl_operation($curl_cmd, "SUBNET CREATE");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		return json_encode($response);
	}
	return prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
}

#curl -i http://xxxxxxxxx:9696/v2.0/ports.json -X OP_POST -H "X-Auth-Token: ${TEST_TOKEN}" 
#-H "Accept: application/json" -H "Content-Type: application/json" 
#-d '{"port": {"network_id": "abc", "fixed_ips":[{"subnet_id":"abc", 
#"ip_address": "1.2.3.4"}], admin_state_up": true}}'
function _neutron_port_create ($neutron_endpoint, $auth_token, $network_id, $port_name = "", $admin_state_up = true, $fixed_ips = array()) {

	$array = array();
	if ($port_name !== "") {
		$array['name'] = $port_name;
	}
	$array['network_id'] = $network_id;
	$array['admin_state_up'] = $admin_state_up;
	if (!empty($fixed_ips)) {
		$array['fixed_ips'] = $fixed_ips;
	}
	$port_array = array('port' => $array);
	$json = json_encode($port_array);

	$openstack_rest_api = "{$neutron_endpoint}/v2.0/ports";
	$curl_cmd = create_openstack_operation_request(OP_POST, $openstack_rest_api, $auth_token, $json);
	$response = perform_curl_operation($curl_cmd, "PORT CREATE");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

#curl -i -X POST http://xxxxxxxxx:9696/v2.0/ports.json -H "User-Agent: python-neutronclient" 
#-H "Content-Type: application/json" -H "Accept: application/json" -H "X-Auth-Token: 12445" 
#-d '{"ports": [{"name": "temp1", "admin_state_up": false, "network_id": "1233"}, 
#{"name": "temp2", "admin_state_up": false, "network_id": "21345"}]}'
function _neutron_bulk_ports_create ($neutron_endpoint, $auth_token, $ports) {

	$port_array = array('ports' => $ports);
	$json = json_encode($port_array);

	$openstack_rest_api = "{$neutron_endpoint}/v2.0/ports";
	$curl_cmd = create_openstack_operation_request(OP_POST, $openstack_rest_api, $auth_token, $json);

	$response = perform_curl_operation($curl_cmd, "BULK PORTS CREATE");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

#curl -i -X PUT http://xxxxxxxxx:9696/v2.0/ports/ec20daad-4d01-464c-bb1c-242bcc150488.json -H "User-Agent: python-neutronclient" 
#-H "Content-Type: application/json" -H "Accept: application/json" -H "X-Auth-Token: TOKEN_REDACTED" 
#-d '{"port": {"allowed_address_pairs": [{"ip_address": "192.168.1.0/24"}]}}'
function _neutron_port_update_allowed_ipaddress_pairs ($neutron_endpoint, $auth_token, $port_id, $allowed_address_pairs = array()) {

	$array = array();
	$array['allowed_address_pairs'] = $allowed_address_pairs;
	$port_array = array('port' => $array);
	$json = json_encode($port_array);

	$openstack_rest_api = "{$neutron_endpoint}/v2.0/ports/{$port_id}";
	$curl_cmd = create_openstack_operation_request(OP_PUT, $openstack_rest_api, $auth_token, $json);

	$response = perform_curl_operation($curl_cmd, "PORT UPDATE ALLOWED ADDRESS PAIRS");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

#curl -i -X PUT http://xxxxxxxxx:9696/v2.0/ports/ec20daad-4d01-464c-bb1c-242bcc150488.json -H "User-Agent: python-neutronclient" 
#-H "Content-Type: application/json" -H "Accept: application/json" -H "X-Auth-Token: a2e24794f42646218e01c1cb042ecde5" 
#-d '{"port": {"fixed_ips": [{"subnet_id" : "2f30f680-2c26-48c6-b96b-1e429646f949","ip_address":"192.168.1.20"}]}}'
function _neutron_port_update_fixed_ips ($neutron_endpoint, $auth_token, $port_id, $fixed_ips) {

	$array = array();
	$array['fixed_ips'] = $fixed_ips;
	$port_array = array('port' => $array);
	$json = json_encode($port_array);

	$openstack_rest_api = "{$neutron_endpoint}/v2.0/ports/{$port_id}";
	$curl_cmd = create_openstack_operation_request(OP_PUT, $openstack_rest_api, $auth_token, $json);

	$response = perform_curl_operation($curl_cmd, "PORT UPDATE FIXED IPs");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

#curl -i -X PUT http://xxxxxxxxx:9696/v2.0/ports/15f0bd4b-aeef-415a-afaf-1ae8314533f8.json -H "User-Agent: python-neutronclient" 
#-H "Content-Type: application/json" -H "Accept: application/json" -H "X-Auth-Token: TOKEN_REDACTED" -d '{"port": {"name": "mgt_port"}}'
function _neutron_port_update_name ($neutron_endpoint, $auth_token, $port_id, $port_name) {

	$array = array();
	$array['name'] = $port_name;
	$port_array = array('port' => $array);
	$json = json_encode($port_array);
	
	$openstack_rest_api = "{$neutron_endpoint}/v2.0/ports/{$port_id}";
	$curl_cmd = create_openstack_operation_request(OP_PUT, $openstack_rest_api, $auth_token, $json);
	
	$response = perform_curl_operation($curl_cmd, "PORT UPDATE NAME");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

#curl -i http://xxxxxxxxx:9696/v2.0/ports/e9783bb4-6d72-47d5-9d4b-4042806d03ae -X DELETE 
#-H "X-Auth-Token:a116a2fdbe7949e189e4207b95285161" -H "Accept: application/json" 
#-H "Content-Type: application/json"
function _neutron_port_delete ($neutron_endpoint, $auth_token, $port_id) {
	
	$openstack_rest_api = "{$neutron_endpoint}/v2.0/ports/{$port_id}";
	$curl_cmd = create_openstack_operation_request(OP_DELETE, $openstack_rest_api, $auth_token);
	
	$response = perform_curl_operation($curl_cmd, "PORT DELETE");
	return $response;
}

#curl -g -i -X PUT http://xxxxxxxxx:9696/v2.0/ports/6c6e9331-0cdf-4fd0-ac48-7fcad356d800.json 
#-H "User-Agent: python-neutronclient" -H "Content-Type: application/json" -H "Accept: application/json" 
#-H "X-Auth-Token: {SHA1}b691726e88b30f007c535fe18214f82227480e55" 
#-d '{"port": {"port_security_enabled": "False", "security_groups": []}}'
function _neutron_disable_port_security ($neutron_endpoint, $auth_token, $port_id) {

	$array = array();
	$array['port_security_enabled'] = false;
	$array['security_groups'] = array();
	$port_array = array('port' => $array);
	$json = json_encode($port_array);

	$openstack_rest_api = "{$neutron_endpoint}/v2.0/ports/{$port_id}";
	$curl_cmd = create_openstack_operation_request(OP_PUT, $openstack_rest_api, $auth_token, $json);
	$response = perform_curl_operation($curl_cmd, "DISABLE PORT SECURITY");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

#curl -g -i -X POST http://xxxxxxxxx:9696/v2.0/floatingips.json -H "User-Agent: python-neutronclient" 
#-H "Content-Type: application/json" -H "Accept: application/json" -H "X-Auth-Token: 
#{SHA1}1c28f029a9d8e72173b724404c1e04ce1cc5a473" 
#-d '{"floatingip": {"floating_network_id": "fa700a48-724f-470a-a4e4-eaf84ae93af2", 
#"tenant_id": "689b343425824ee3a491a05d01f628e3", "fixed_ip_address": "192.168.2.168", 
#"port_id": "6c6e9331-0cdf-4fd0-ac48-7fcad356d800", "floating_ip_address": "10.30.19.17"}}'
function _neutron_floatingip_create ($neutron_endpoint, $auth_token, $network_id, $tenant_id = "", $floatingip_address = "", $fixed_ip = "", $port_id = "") {

	$array = array();
	$array['floating_network_id'] = $network_id;
	if ($tenant_id !== "") {
		$array['tenant_id'] = $tenant_id;
	}
	if ($fixed_ip !== "") {
		$array['fixed_ip_address'] = $fixed_ip;
	}
	if ($port_id !== "") {
		$array['port_id'] = $port_id;
	}
	if ($floatingip_address !== "") {
		$array['floating_ip_address'] = $floatingip_address;
	}
	$floatingip_array = array('floatingip' => $array);
	$json = json_encode($floatingip_array);

	$openstack_rest_api = "{$neutron_endpoint}/v2.0/floatingips";
	$curl_cmd = create_openstack_operation_request(OP_POST, $openstack_rest_api, $auth_token, $json);
	$response = perform_curl_operation($curl_cmd, "FLOATING IP CREATE");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

#curl -i http://xxxxxxxxx:9696/v2.0/security-group-rules -X OP_POST -H "X-Auth-Token: ${TEST_TOKEN}" 
#-H "Accept: application/json" -H "Content-Type: application/json" 
#-d '{"security_group_rule":{"remote_group_id":null,"direction":"ingress",
#"security_group_id":"d952ec52-2bb9-4c03-9d6e-6185e2acf0e2","ethertype":"IPv4"}}'
function _neutron_security_group_rule_create ($neutron_endpoint, $auth_token, $security_group_id, $remote_group_id, $direction, $ethertype) {
	
	$array = array();
	$array['security_group_id'] = $security_group_id;
	$array['remote_group_id'] = $remote_group_id;
	$array['ethertype'] = $ethertype;
	$array['direction'] = $direction;
	$security_group_rule_array = array('security_group_rule' => $array);
	$json = json_encode($security_group_rule_array);
	
	$openstack_rest_api = "{$neutron_endpoint}/v2.0/security-group-rules";
	$curl_cmd = create_openstack_operation_request(OP_POST, $openstack_rest_api, $auth_token, $json);
	
	$response = perform_curl_operation($curl_cmd, "SECURITY GROUP RULE");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

#curl -g -i -X PUT http://xxxxxxxxx:9696/v2.0/ports/609915ac-1925-414e-98f0-d047a37031dc.json 
#-H "User-Agent: python-neutronclient" -H "Content-Type: application/json" -H "Accept: application/json" 
#-H "X-Auth-Token: {SHA1}391fc66fe5043964a2f862e729aafefc9f01b3e7" -d 
#'{"port": {"security_groups": ["e25e9e23-ac8a-4706-9ee5-d7026b59d7e7"]}}'
function _neutron_attach_security_groups_to_port ($neutron_endpoint, $auth_token, $port_id, $security_groups = array()) {

	$secgrp_array = array('port' => array('security_groups' => $security_groups));
	$json = json_encode($secgrp_array);
	
	$openstack_rest_api = "{$neutron_endpoint}/v2.0/ports/{$port_id}";
	$curl_cmd = create_openstack_operation_request(OP_PUT, $openstack_rest_api, $auth_token, $json);

	$response = perform_curl_operation($curl_cmd, "ATTACH SECURITY GROUP TO PORT");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

#curl -g -i -X PUT http://xxxxxxxxx:9696/v2.0/floatingips/bec23045-e6d4-4530-bbaf-240a270f66e2.json 
#-H "User-Agent: python-neutronclient" -H "Content-Type: application/json" -H "Accept: application/json" 
#-H "X-Auth-Token: {SHA1}96e3f409c10e636c1814ec54afdd1ad144cf7abd" 
#-d '{"floatingip": {"fixed_ip_address": "10.0.0.15", "port_id": "609915ac-1925-414e-98f0-d047a37031dc"}}'
function _neutron_associate_floatingip_to_port ($neutron_endpoint, $auth_token, $floatingip_id, $port_id, $fixed_ip = "") {

	$array = array();
	if (!empty($fixed_ip)) {
		$array['fixed_ip_address'] = $fixed_ip;
	}
	$array['port_id'] = $port_id;
	$floatingip_array = array('floatingip' => $array);
	$json = json_encode($floatingip_array);

	$openstack_rest_api = "{$neutron_endpoint}/v2.0/floatingips/{$floatingip_id}";
	$curl_cmd = create_openstack_operation_request(OP_PUT, $openstack_rest_api, $auth_token, $json);

	$response = perform_curl_operation($curl_cmd, "ASSOCIATE FLOATING IP TO PORT");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

#curl -i -X PUT http://xxxxxxxxx:9696/v2.0/floatingips/b1a2147f-364a-41d5-943c-56e38326b796.json -H "User-Agent: python-neutronclient" 
#-H "Content-Type: application/json" -H "Accept: application/json" -H "X-Auth-Token: TOKEN_REDACTED" -d '{"floatingip": {"port_id": null}}'
function _neutron_disassociate_floatingip_from_port ($neutron_endpoint, $auth_token, $floatingip_id) {

	$array = array();
	$array['port_id'] = null;
	$floatingip_array = array('floatingip' => $array);
	$json = json_encode($floatingip_array);

	$openstack_rest_api = "{$neutron_endpoint}/v2.0/floatingips/{$floatingip_id}";
	$curl_cmd = create_openstack_operation_request(OP_PUT, $openstack_rest_api, $auth_token, $json);

	$response = perform_curl_operation($curl_cmd, "DISASSOCIATE FLOATING IP FROM PORT");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

#curl -g -i -X PUT http://xxxxxxxxx:9696/v2.0/subnets/51328b1e-b2ec-4aa6-a298-fec3d63fc651.json
#-H "User-Agent: python-neutronclient" -H "Content-Type: application/json" -H "Accept: application/json"
#-H "X-Auth-Token: {SHA1}d66bbaa920a056afe96fea6dd6061804d3b7e2cc" -d '{"subnet": {"gateway_ip": "123.0.0.254"}}'
function _neutron_subnet_update_gateway_ip ($neutron_endpoint, $auth_token, $subnet_id, $gateway_ip = "") {

	$array = array();
	$array['gateway_ip'] = $gateway_ip;
	$subnet_array = array('subnet' => $array);
	$json = json_encode($subnet_array);

	$openstack_rest_api = "{$neutron_endpoint}/v2.0/subnets/{$subnet_id}";
	$curl_cmd = create_openstack_operation_request(OP_PUT, $openstack_rest_api, $auth_token, $json);
	$response = perform_curl_operation($curl_cmd, "SUBNET UPDATE GATEWAY IP");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

#curl -g -i -X PUT http://xxxxxxxxx:9696/v2.0/routers/fa477dec-b343-4f60-a13d-0fc250d5055e/add_router_interface.json 
#-H "User-Agent: python-neutronclient" -H "Content-Type: application/json" -H "Accept: application/json" -H "X-Auth-Token: 
#{SHA1}42b7493353205b58cb99edf705e8b9efc0d1d7dd" -d '{"subnet_id": "51328b1e-b2ec-4aa6-a298-fec3d63fc651"}'
function _neutron_router_interface_add ($neutron_endpoint, $auth_token, $router_id, $subnet_id) {	
	$array = array("subnet_id" => $subnet_id);
	$json = json_encode($array);

	$openstack_rest_api = "{$neutron_endpoint}/v2.0/routers/{$router_id}/add_router_interface";
	$curl_cmd = create_openstack_operation_request(OP_PUT, $openstack_rest_api, $auth_token, $json);
	$response = perform_curl_operation($curl_cmd, "ROUTER INTERFACE ADD");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		return json_encode($response);
	}
	return prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
}

#curl -g -i -X PUT http://xxxxxxxxx:9696/v2.0/routers/fa477dec-b343-4f60-a13d-0fc250d5055e/remove_router_interface.json 
#-H "User-Agent: python-neutronclient" -H "Content-Type: application/json" -H "Accept: application/json" 
#-H "X-Auth-Token: {SHA1}2720b29fb37bcd3f1029b641b704c02a16b86abf" -d '{"subnet_id": "51328b1e-b2ec-4aa6-a298-fec3d63fc651"}'
function _neutron_router_interface_delete ($neutron_endpoint, $auth_token, $router_id, $subnet_id) {

	$array = array();
	$array['subnet_id'] = $subnet_id;
	$json = json_encode($array);

	$openstack_rest_api = "{$neutron_endpoint}/v2.0/routers/{$router_id}/remove_router_interface";
	$curl_cmd = create_openstack_operation_request(OP_PUT, $openstack_rest_api, $auth_token, $json);
	$response = perform_curl_operation($curl_cmd, "ROUTER INTERFACE DELETE");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

#curl -g -i -X PUT http://xxxxxxxxx:9696/v2.0/subnets/51328b1e-b2ec-4aa6-a298-fec3d63fc651.json -H "User-Agent: python-neutronclient" 
#-H "Content-Type: application/json" -H "Accept: application/json" -H "X-Auth-Token: {SHA1}7c57e21b97ef05a3fb2e7bc1e4ce6001d2bda97c" 
#-d '{"subnet": {"allocation_pools": [{"start": "123.0.0.10", "end": "123.0.0.20"}, {"start": "123.0.0.21", "end": "123.0.0.25"}]}}'
function _neutron_subnet_update_allocation_pools ($neutron_endpoint, $auth_token, $subnet_id, $allocation_pools) {
	
	$array = array();
	$array['allocation_pools'] = $allocation_pools;
	$subnet_array = array('subnet' => $array);
	$json = json_encode($subnet_array);
	
	$openstack_rest_api = "{$neutron_endpoint}/v2.0/subnets/{$subnet_id}";
	$curl_cmd = create_openstack_operation_request(OP_PUT, $openstack_rest_api, $auth_token, $json);
	$response = perform_curl_operation($curl_cmd, "SUBNET UPDATE ALLOCATION POOLS");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

function _neutron_get_port_info($neutron_endpoint, $auth_token, $port_id) {
	$openstack_rest_api = "{$neutron_endpoint}/v2.0/ports/".$port_id;
	$curl_cmd = create_openstack_operation_request(OP_GET, $openstack_rest_api, $auth_token, "");
	$response = perform_curl_operation($curl_cmd, "PORT LIST");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}


function _neutron_get_public_networks($neutron_endpoint, $auth_token) {
	$openstack_rest_api = "{$neutron_endpoint}/v2.0/networks?router:external=true";
        $curl_cmd = create_openstack_operation_request(OP_GET, $openstack_rest_api, $auth_token, "");
	$response = perform_curl_operation($curl_cmd, "PUBLIC NETWORK LIST");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

