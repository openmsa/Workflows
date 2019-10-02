<?php 

require_once '/opt/fmc_repository/Process/Reference/OPENSTACK/Library/REST/utility.php';

#curl -i http://10.1.144.111:8774/v2/ebd239c789994f3a88d6da7083098851/flavors -X POST 
#-H "X-Auth-Token:fb7317fa0c3c43949ccbe9de55dfba85" -H "Accept: application/json" -H "Content-type: application/json"
# -d '{"flavor" :{ "name":"test-flavor2","ram":1024,"vcpus":2,"disk":10,"os-flavor-access:is_public": false}}'
function _nova_flavor_create ($nova_endpoint, $auth_token, $tenant_id, $ram, $vcpus, $disk, $name = "", $is_public = false) {
	
	$array = array();
	if ($name !== "") {
		$array['name'] = $name;
	}
	$array['ram'] = $ram;
	$array['vcpus'] = $vcpus;
	$array['disk'] = $disk;
	$array['os-flavor-access:is_public'] = $is_public;
	$flavor_array = array('flavor' => $array);
	$json = json_encode($flavor_array);
	
	$openstack_rest_api = "{$nova_endpoint}/{$tenant_id}/flavors";
	$curl_cmd = create_openstack_operation_request(OP_POST, $openstack_rest_api, $auth_token, $json);
	$response = perform_curl_operation($curl_cmd, "FLAVOR CREATE");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}


#curl -i http://ct-int-vip:28774/v2/${PJID}/servers -X POST -H "X-Auth-Token: ${TEST_TOKEN}" 
#-H "Accept: application/json" -H "Content-Type: application/json" -d 
#'{ "server": { "availability_zone": "ote-lab1","flavorRef": "120","imageRef":"6a0de364-7fef-4e02-9e6e-2b4d3bead6fd",
#"max_count": 1,"min_count": 1,"name": "vyatta_other_tenant_07",
#"networks":[{"uuid":"a4000cdf-835b-4ec0-942d-a456a3b4f495","port_id":"7dceafe1-ef96-4047-b717-dc354eb48ea2"}]}}'
function _nova_server_create ($nova_endpoint, $auth_token, $name, $flavor, $image, 
							$networks, $availability_zone = "", $user_data = "", 
							$security_groups = array(), $min_count = 1, $max_count = 1) {

	$array = array();
	$array['name'] = $name;
	$array['flavorRef'] = $flavor;
	$array['imageRef'] = $image;
	$array['networks'] = $networks;
	if ($availability_zone !== "") {
		$array['availability_zone'] = $availability_zone;
	}
	if ($user_data !== "") {
		$array['user_data'] = $user_data;
	}
	if (!empty($security_groups)) {
		$array['security_groups'] = $security_groups;
	}
	#$array['min_count'] = $min_count;
	#$array['max_count'] = $max_count;
	
	$server_array = array('server' => $array);
	$json = json_encode($server_array);

	$openstack_rest_api = "{$nova_endpoint}/servers";
	$curl_cmd = create_openstack_operation_request(OP_POST, $openstack_rest_api, $auth_token, $json);

	$response = perform_curl_operation($curl_cmd, "SERVER CREATE");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

#curl -g -i -X PUT http://10.31.1.13:8774/v2/5b57e85c3a4e4cc3ae81ea2a503e1d6e/servers/d4e139f8-2cd2-4519-9e3c-32fb6d22fadd 
#-H "User-Agent: python-novaclient" -H "Content-Type: application/json" -H "Accept: application/json" 
#-H "X-Auth-Token: 1dbf7ef4000d44f98348cf828a5f4448" -d '{"server": {"name": "cirros"}}'
function _nova_server_update_name ($nova_endpoint, $auth_token, $server_id, $server_name) {

	$array = array();
	$array['name'] = $server_name;
	$server_array = array('server' => $array);
	$json = json_encode($server_array);
	
	$openstack_rest_api = "{$nova_endpoint}/servers/{$server_id}";
	$curl_cmd = create_openstack_operation_request(OP_PUT, $openstack_rest_api, $auth_token, $json);
	
	$response = perform_curl_operation($curl_cmd, "SERVER NAME UPDATE");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

#curl -g -i -X DELETE http://10.31.1.13:8774/v2/689b343425824ee3a491a05d01f628e3/servers/bc7d8f1e-a479-483b-85a5-a85db9eb60a4 
#-H "User-Agent: python-novaclient" -H "Accept: application/json" -H "X-Auth-Token: {SHA1}30ff76ffd347c2dda6389a46a9206250eeb14422"
function _nova_server_delete ($nova_endpoint, $auth_token, $server_id) {

	$openstack_rest_api = "{$nova_endpoint}/servers/{$server_id}";
	$curl_cmd = create_openstack_operation_request(OP_DELETE, $openstack_rest_api, $auth_token);

	$response = perform_curl_operation($curl_cmd, "SERVER DELETE");
	return $response;
}

#curl -i http://ct-int-vip:28774/v2/${PJID}/servers/1234/action -X POST -H "X-Auth-Token: ${TEST_TOKEN}" 
#-H "Accept: application/json" -H "Content-Type: application/json" -d '{"resize": {"flavorRef": "120"}}'
function _nova_server_resize ($nova_endpoint, $auth_token, $server_id, $resize_flavor_id) {
	
	$array = array();
	$array['flavorRef'] = $resize_flavor_id;
	
	$resize_array = array('resize' => $array);
	$json = json_encode($resize_array);
	
	$openstack_rest_api = "{$nova_endpoint}/servers/{$server_id}/action";
	$curl_cmd = create_openstack_operation_request(OP_POST, $openstack_rest_api, $auth_token, $json);
	
	$response = perform_curl_operation($curl_cmd, "SERVER RESIZE");
	return $response;
}

function _nova_server_resize_confirm ($nova_endpoint, $auth_token, $server_id) {

	$array = array();
	$array['confirmResize'] = null;
	$json = json_encode($array);

	$openstack_rest_api = "{$nova_endpoint}/servers/{$server_id}/action";
	$curl_cmd = create_openstack_operation_request(OP_POST, $openstack_rest_api, $auth_token, $json);

	$response = perform_curl_operation($curl_cmd, "SERVER RESIZE CONFIRM");
	return $response;
}

#curl -g -i -X POST http://10.31.1.13:8774/v2/689b343425824ee3a491a05d01f628e3/servers/
#43ef02a3-d596-4969-9139-09d39f1c95e5/action -H "User-Agent: python-novaclient" 
#-H "Content-Type: application/json" -H "Accept: application/json" 
#-H "X-Auth-Token: {SHA1}8d1fe213446613da45441bd53596c852e00913ef" -d '{"reboot": {"type": "SOFT"}}'
function _nova_server_reboot ($nova_endpoint, $auth_token, $server_id, $type = "SOFT") {

	$array = array();
	$array['type'] = $type;
	$reboot_array = array('reboot' => $array);
	$json = json_encode($reboot_array);
	
	$openstack_rest_api = "{$nova_endpoint}/servers/{$server_id}/action";
	$curl_cmd = create_openstack_operation_request(OP_POST, $openstack_rest_api, $auth_token, $json);
	$response = perform_curl_operation($curl_cmd, "SERVER REBOOT");
	return $response;
}

#curl -i 'http://10.31.1.123:8774/v2/e470fd6ea0834192ab05c17930bee22c/servers/362b95bf-da62-4c52-b39a-547aa79b78ee/action'
# -X POST -H "Accept: application/json" -H "Content-Type: application/json" -H "User-Agent: python-novaclient" 
#-H "X-Auth-Project-Id: ntt" -H "X-Auth-Token: {SHA1}eecb49db110434af8a563c44718e6d1a25e1d613" -d '{"os-start": null}'
function _nova_server_start ($nova_endpoint, $auth_token, $server_id) {

	$array = array();
	$array['os-start'] = null;
	$json = json_encode($array);

	$openstack_rest_api = "{$nova_endpoint}/servers/{$server_id}/action";
	$curl_cmd = create_openstack_operation_request(OP_POST, $openstack_rest_api, $auth_token, $json);
	$response = perform_curl_operation($curl_cmd, "SERVER START");
	return $response;
}

function _nova_server_stop ($nova_endpoint, $auth_token, $server_id) {

	$array = array();
	$array['os-stop'] = null;
	$json = json_encode($array);

	$openstack_rest_api = "{$nova_endpoint}/servers/{$server_id}/action";
	$curl_cmd = create_openstack_operation_request(OP_POST, $openstack_rest_api, $auth_token, $json);
	$response = perform_curl_operation($curl_cmd, "SERVER STOP");
	return $response;
}

#curl -g -i -X POST http://10.31.1.13:8774/v2/fe268fd218aa42868063b7cf34855899/servers/
#46b85ef3-caad-4749-8e72-70939fbfd086/action -H "User-Agent: python-novaclient" -H "Content-Type: application/json" 
#-H "Accept: application/json" -H "X-Auth-Token: {SHA1}6bfc24a82d845208fcf652dd24622f95b5ca532d" 
#-d '{"addSecurityGroup": {"name": "secgrp_vnf_demo"}}'
function _nova_add_security_group ($nova_endpoint, $auth_token, $server_id, $security_group) {

	$array = array();
	$array['name'] = $security_group;
	$server_secgrp_array = array('addSecurityGroup' => $array);
	$json = json_encode($server_secgrp_array);

	$openstack_rest_api = "{$nova_endpoint}/servers/{$server_id}/action";
	$curl_cmd = create_openstack_operation_request(OP_POST, $openstack_rest_api, $auth_token, $json);
	$response = perform_curl_operation($curl_cmd, "SERVER SECURITY GROUP ATTACH");
	return $response;
}

#curl -g -i -X POST http://10.31.1.13:8774/v2/fe268fd218aa42868063b7cf34855899/servers/
#46b85ef3-caad-4749-8e72-70939fbfd086/action -H "User-Agent: python-novaclient" -H "Content-Type: application/json" 
#-H "Accept: application/json" -H "X-Auth-Token: {SHA1}33a8df4a62d6b9e3537d178e8fa43d789f48cc5a" 
#-d '{"addFloatingIp": {"fixed_address": "192.168.2.7", "address": "10.30.19.27"}}'
function _nova_floating_ip_associate ($nova_endpoint, $auth_token, $server_id, $floatingip_address, 
									$fixed_address = "") {

	$array = array();
	$array['address'] = $floatingip_address;
	if ($fixed_address !== "") {
		$array['fixed_address'] = $fixed_address;
	}
	$server_floatingip_array = array('addFloatingIp' => $array);
	$json = json_encode($server_floatingip_array);

	$openstack_rest_api = "{$nova_endpoint}/servers/{$server_id}/action";
	$curl_cmd = create_openstack_operation_request(OP_POST, $openstack_rest_api, $auth_token, $json);
	$response = perform_curl_operation($curl_cmd, "SERVER FLOATING IP ASSOCIATE");
	return $response;
}

#curl -g -i -X POST http://10.31.1.13:8774/v2/fe268fd218aa42868063b7cf34855899/servers/
#46b85ef3-caad-4749-8e72-70939fbfd086/action -H "User-Agent: python-novaclient" -H "Content-Type: application/json" 
#-H "Accept: application/json" -H "X-Auth-Token: {SHA1}df2bf9bb8cd667d0eee6f4e2cd8addbd79446a7c" 
#-d '{"removeFloatingIp": {"address": "10.30.19.27"}}'
function _nova_floating_ip_disassociate ($nova_endpoint, $auth_token, $server_id, $floatingip_address) {

	$array = array();
	$array['address'] = $floatingip_address;
	$server_floatingip_array = array('removeFloatingIp' => $array);
	$json = json_encode($server_floatingip_array);

	$openstack_rest_api = "{$nova_endpoint}/servers/{$server_id}/action";
	$curl_cmd = create_openstack_operation_request(OP_POST, $openstack_rest_api, $auth_token, $json);
	$response = perform_curl_operation($curl_cmd, "SERVER FLOATING IP DISASSOCIATE");
	return $response;
}

#curl -i http://ct-int-vip:28774/v2/${PJID}/servers/${SVID}/os-interface -X POST -H "X-Auth-Token: ${TEST_TOKEN}" 
#-H "Accept: application/json" -H "Content-Type: application/json" -d '{"interfaceAttachment":{"port_id":"1234"}}'
#curl -i http://ct-int-vip:28774/v2/${PJID}/servers/${SVID}/os-interface -X POST -H "X-Auth-Token: ${TEST_TOKEN}" 
#-H "Accept: application/json" -H "Content-Type: application/json" -d 
#'{"interfaceAttachment":{"net_id":"3b49fd97-caab-40ef-9fa6-4073d1639e7c","fixed_ips":[{"ip_address":"192.168.101.2"}]}}'
function _nova_interface_attach ($nova_endpoint, $auth_token, $server_id, $port_id = "",
								$network_id = "", $fixed_ips = array()) {
									
	$array = array();
	if ($port_id !== "") {
		$array['port_id'] = $port_id;
	}
	else {
		$array['net_id'] = $network_id;
		if (!empty($fixed_ips)) {
			$array['fixed_ips'] = $fixed_ips;
		}
	}
	$interface_attachment_array = array('interfaceAttachment' => $array);
	$json = json_encode($interface_attachment_array);
									
	$openstack_rest_api = "{$nova_endpoint}/servers/{$server_id}/os-interface";
	$curl_cmd = create_openstack_operation_request(OP_POST, $openstack_rest_api, $auth_token, $json);
	$response = perform_curl_operation($curl_cmd, "SERVER INTERFACE ATTACH");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

#curl -i http://ct-int-vip:28774/v2/${PJID}/servers/${SVID}/os-interface/12345 -X DELETE -H "X-Auth-Token: 
#${TEST_TOKEN}" -H "Accept: application/json" -H "Content-Type: application/json" 
function _nova_interface_detach ($nova_endpoint, $auth_token, $server_id, $port_id) {
		
	$openstack_rest_api = "{$nova_endpoint}/servers/{$server_id}/os-interface/{$port_id}";
	$curl_cmd = create_openstack_operation_request(OP_DELETE, $openstack_rest_api, $auth_token);
		
	$response = perform_curl_operation($curl_cmd, "SERVER INTERFACE DETACH");
	return $response;
}

#curl -i 'http://10.31.1.125:8774/v2/5fd116d488644b84bd57fca22fb02587/servers/44916e9c-5f3e-4e2b-ae89-48f7b5c2d821/action' -X POST 
#-H "Accept: application/json" -H "Content-Type: application/json" -H "User-Agent: python-novaclient" -H "X-Auth-Project-Id: NTTCom" 
#-H "X-Auth-Token: {SHA1}d4563d73b930b0e7bd37c17ab078887da0a64dd4" -d '{"os-getVNCConsole": {"type": "novnc"}}'
# <console-type>  Type of vnc console ("novnc" or "xvpvnc").
function _nova_get_vnc_console ($nova_endpoint, $auth_token, $server_id, $console_type) {

	$array = array();
	$array['type'] = $console_type;
	$server_vnc_console_array = array('os-getVNCConsole' => $array);
	$json = json_encode($server_vnc_console_array);

	$openstack_rest_api = "{$nova_endpoint}/servers/{$server_id}/action";
	$curl_cmd = create_openstack_operation_request(OP_POST, $openstack_rest_api, $auth_token, $json);
	$response = perform_curl_operation($curl_cmd, "SERVER GET VNC CONSOLE");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

#curl -i -k https://10.1.144.116/v2/abcd/servers/abcd/os-volume_attachments -X POST 
#-H "X-Auth-Token:42946664fc6e41e392bb7ee51a9160b9" -H "Accept: application/json" 
#-H "Content-Type: application/json" 
#-d '{"volumeAttachment":{"volumeId":"b009c52c-97bd-4da4-916c-b2d4c90a85f4"}}'
function _nova_volume_attach ($nova_endpoint, $auth_token, $server_id, $volume_id, $device = null) {
		
	$array = array();
	$array['volumeId'] = $volume_id;
	$array['device'] = $device;
	$volume_attachment_array = array('volumeAttachment' => $array);
	$json = json_encode($volume_attachment_array);
		
	$openstack_rest_api = "{$nova_endpoint}/servers/{$server_id}/os-volume_attachments";
	$curl_cmd = create_openstack_operation_request(OP_POST, $openstack_rest_api, $auth_token, $json);
	$response = perform_curl_operation($curl_cmd, "SERVER VOLUME ATTACH");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

#curl -i -k https://10.1.144.116/v2/abcd/servers/abcd/os-volume_attachments/sdasd -X DELETE 
#-H "X-Auth-Token:f16eb9820b4941879379e166e93e27c7" -H "Accept: application/json" 
#-H "Content-Type: application/json" 
function _nova_volume_detach ($nova_endpoint, $auth_token, $server_id, $volume_id) {

	$openstack_rest_api = "{$nova_endpoint}/servers/{$server_id}/os-volume_attachments/{$volume_id}";
	$curl_cmd = create_openstack_operation_request(OP_DELETE, $openstack_rest_api, $auth_token);

	$response = perform_curl_operation($curl_cmd, "SERVER VOLUME DETACH");
	return $response;
}

?>