<?php 

require_once '/opt/fmc_repository/Process/Reference/OPENSTACK/Library/REST/utility.php';

#curl -i http://xxxxx:8774/v2/ebd239c789994f3a88d6da7083098851/flavors -X POST 
#-H "X-Auth-Token:yyyyy" -H "Accept: application/json" -H "Content-type: application/json"
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


#curl -i http://xxxx:28774/v2/${PJID}/servers -X POST -H "X-Auth-Token: ${TEST_TOKEN}" 
#-H "Accept: application/json" -H "Content-Type: application/json" -d 
#'{ "server": { "availability_zone": "ote-lab1","flavorRef": "120","imageRef":"xxx",
#"max_count": 1,"min_count": 1,"name": "vyatta_other_tenant_07",
#"networks":[{"uuid":"a4000cdf-835b-4ec0-942d-a456a3b4f495","port_id":"xxxx"}]}}'
function _nova_server_create ($nova_endpoint, $auth_token, $name, $flavor, $image, 
							$networks, $availability_zone = "", $user_data = "", $config_drive = "", 
							$security_groups = array(), $min_count = 1, $max_count = 1) {

	$array = array();
	$array['name'] = $name;
	$array['flavorRef'] = $flavor;
	$array['imageRef'] = $image;
	$array['networks'] = $networks;
	if (!empty($availability_zone)) {
		$array['availability_zone'] = $availability_zone;
	}
	if (!empty($user_data)) {
		$array['user_data'] = $user_data;
	}
	if (!empty($config_drive)) {
                $array['config_drive'] = $config_drive;
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

#curl -g -i -X PUT http://xxxx:8774/v2/ c3ae81ea2a503e1d6e/servers/ 2cd2-4519-9e3c-32fb6d22fadd 
#-H "User-Agent: python-novaclient" -H "Content-Type: application/json" -H "Accept: application/json" 
#-H "X-Auth-Token: xxxx" -d '{"server": {"name": "cirros"}}'
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

#curl -g -i -X DELETE http://xxxx:8774/v2/689b343425824ee3a491a05d01f628e3/servers/xxxxxxxxxx0a4 
#-H "User-Agent: python-novaclient" -H "Accept: application/json" -H "X-Auth-Token: {SHA1}xxx"
function _nova_server_delete ($nova_endpoint, $auth_token, $server_id) {

	$openstack_rest_api = "{$nova_endpoint}/servers/{$server_id}";
	$curl_cmd = create_openstack_operation_request(OP_DELETE, $openstack_rest_api, $auth_token);

	$response = perform_curl_operation($curl_cmd, "SERVER DELETE");
	return $response;
}

#curl -i http://xxxxxx:28774/v2/${PJID}/servers/1234/action -X POST -H "X-Auth-Token: ${TEST_TOKEN}" 
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

#curl -g -i -X POST http://xxxxxxxxx:8774/v2/689b343425824ee3a491a05d01f628e3/servers/
# -9139-09d39f1c95e5/action -H "User-Agent: python-novaclient" 
#-H "Content-Type: application/json" -H "Accept: application/json" 
#-H "X-Auth-Token: {SHA1} 45441bd53596c852e00913ef" -d '{"reboot": {"type": "SOFT"}}'
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

#curl -i 'http://xxxxxxxx:8774/v2/e470fd6ea0834192ab05c17930bee22c/servers/-4c52-b39a-547aa79b78ee/action'
# -X POST -H "Accept: application/json" -H "Content-Type: application/json" -H "User-Agent: python-novaclient" 
#-H "X-Auth-Project-Id: " -H "X-Auth-Token: {SHA1}63c44718e6d1a25e1d613" -d '{"os-start": null}'
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

#curl -g -i -X POST http://xxxxxx:8774/v2/868063b7cf34855899/servers/
#46b85ef3-caad-4749-8e72-70939fbfd086/action -H "User-Agent: python-novaclient" -H "Content-Type: application/json" 
#-H "Accept: application/json" -H "X-Auth-Token: {SHA1}5208fcf652dd24622f95b5ca532d" 
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

#curl -g -i -X POST http://xxxxxxx:8774/v2/42868063b7cf34855899/servers/
#46b85ef3-caad-4749-8e72-70939fbfd086/action -H "User-Agent: python-novaclient" -H "Content-Type: application/json" 
#-H "Accept: application/json" -H "X-Auth-Token: {SHA1}9e3537d178e8fa43d789f48cc5a" 
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

#curl -g -i -X POST http://xxxxxxxxx:8774/v2/8aa42868063b7cf34855899/servers/
#46b85ef3-caad-4749-8e72-70939fbfd086/action -H "User-Agent: python-novaclient" -H "Content-Type: application/json" 
#-H "Accept: application/json" -H "X-Auth-Token: {SHA1}667d0eee6f4e2cd8addbd79446a7c" 
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

#curl -i http://xxxxxxxxx:28774/v2/${PJID}/servers/${SVID}/os-interface -X POST -H "X-Auth-Token: ${TEST_TOKEN}" 
#-H "Accept: application/json" -H "Content-Type: application/json" -d '{"interfaceAttachment":{"port_id":"1234"}}'
#curl -i http://xxxxxxxxx:28774/v2/${PJID}/servers/${SVID}/os-interface -X POST -H "X-Auth-Token: ${TEST_TOKEN}" 
#-H "Accept: application/json" -H "Content-Type: application/json" -d 
#'{"interfaceAttachment":{"net_id":"ef-9fa6-4073d1639e7c","fixed_ips":[{"ip_address":"192.168.101.2"}]}}'
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

#curl -i http://xxxxxxxxx:28774/v2/${PJID}/servers/${SVID}/os-interface/12345 -X DELETE -H "X-Auth-Token: 
#${TEST_TOKEN}" -H "Accept: application/json" -H "Content-Type: application/json" 
function _nova_interface_detach ($nova_endpoint, $auth_token, $server_id, $port_id) {
		
	$openstack_rest_api = "{$nova_endpoint}/servers/{$server_id}/os-interface/{$port_id}";
	$curl_cmd = create_openstack_operation_request(OP_DELETE, $openstack_rest_api, $auth_token);
		
	$response = perform_curl_operation($curl_cmd, "SERVER INTERFACE DETACH");
	return $response;
}

#curl -i 'http://xxxxxxxxx:8774/v2/6d488644b84bd57fca22fb02587/servers/f3e-4e2b-ae89-48f7b5c2d821/action' -X POST 
#-H "Accept: application/json" -H "Content-Type: application/json" -H "User-Agent: python-novaclient" -H "X-Auth-Project-Id:  " 
#-H "X-Auth-Token: {SHA1}930b0e7bd37c17ab078887da0a64dd4" -d '{"os-getVNCConsole": {"type": "novnc"}}'
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

#curl -i -k https://xxxxxxxxxv2/abcd/servers/abcd/os-volume_attachments -X POST 
#-H "X-Auth-Token:42946664fc6e41e392bb7ee51a9160b9" -H "Accept: application/json" 
#-H "Content-Type: application/json" 
#-d '{"volumeAttachment":{"volumeId":"d-4da4-916c-b2d4c90a85f4"}}'
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

#curl -i -k https://xxxxxxxxxv2/abcd/servers/abcd/os-volume_attachments/sdasd -X DELETE 
#-H "X-Auth-Token:f16eb9820b4941879379e166e93e27c7" -H "Accept: application/json" 
#-H "Content-Type: application/json" 
function _nova_volume_detach ($nova_endpoint, $auth_token, $server_id, $volume_id) {

	$openstack_rest_api = "{$nova_endpoint}/servers/{$server_id}/os-volume_attachments/{$volume_id}";
	$curl_cmd = create_openstack_operation_request(OP_DELETE, $openstack_rest_api, $auth_token);

	$response = perform_curl_operation($curl_cmd, "SERVER VOLUME DETACH");
	return $response;
}

/**
* VNF Live migration from hostA to hostX of the Openstack VIM.
*
* curl --tlsv1.2 -i -sw 'HTTP_CODE=%{http_code}' --connect-timeout 50 --max-time 50 -X POST -H "X-Auth-Token: gAAAAABdel44SS-FrqBKUdIEthbnsIH-R9cXfO307WcU3bz47fjJw1rxqLdaN4P08uw9U9P1UcB-9Qg-NAk3_FvmXD71tHmyyWYje-m2D1GFxF5WtuGZ3S0n7TsbkeIBLOoJt6bUQ45O0X9qrq9CAJtBWBoDr-SvKMrIup0nAOvlt0e09h_UINo" -H "Content-Type: application/json" -k 'http://xxxxxxxxx:8774/v2.1/df1f081bf2d345099e6bb53f6b9407ff/servers/22b555e1-2fe2-45d6-ace1-e5cad4d34db5/action' -d '{
    "os-migrateLive": {
        "host": "openstack2.ubiqube.com",
        "block_migration": "false",
		"disk_over_commit": false
    }
}'
**/
function _nova_os_migration_live($nova_endpoint, $auth_token, $server_id, $host, $block_migration = "false", $disk_over_commit = "false")
{
	$array = array();
	$array['host'] = $host;
	$array['block_migration'] = $block_migration;
	$array['disk_over_commit'] = $disk_over_commit;
	$os_migrate_live_array = array(
		'os-migrateLive' => $array
	);
	$json = json_encode($os_migrate_live_array);

	$openstack_rest_api = "{$nova_endpoint}/servers/{$server_id}/action";
	$curl_cmd = create_openstack_operation_request(OP_POST, $openstack_rest_api, $auth_token, $json);
	$response = perform_curl_operation($curl_cmd, "SERVER LIVE MIGRATION");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		return json_encode($response);
	}
	return prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response);
}

/*
 * {
 * "evacuate": {
 * "host": "b419863b7d814906a68fb31703c0dbd6",
 * "adminPass": "MySecretPass",
 * "onSharedStorage": "False"
 * }
 * }
 */
function _nova_os_evacuate($nova_endpoint, $auth_token, $server_id, $host)
{
	$array = array();
	$array['onSharedStorage'] = "False";
	$os_evacuate_array = array(
		'evacuate' => $array
	);
	$json = json_encode($os_evacuate_array);

	$openstack_rest_api = "{$nova_endpoint}/servers/{$server_id}/action";
	$curl_cmd = create_openstack_operation_request(OP_POST, $openstack_rest_api, $auth_token, $json);
	$response = perform_curl_operation($curl_cmd, "SERVER EVACUATE");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		return json_encode($response);
	}

	return  prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response);
}


/**
* GET VIM hosts list (hypervisors).
*
* curl --tlsv1.2 -i -sw 'HTTP_CODE=%{http_code}' --connect-timeout 50 --max-time 50 -X GET -H "X-Auth-Token: gAAAAABdel44SS-FrqBKUdIEthbnsIH-R9cXfO307WcU3bz47fjJw1rxqLdaN4P08uw9U9P1UcB-9Qg-NAk3_FvmXD71tHmyyWYje-m2D1GFxF5WtuGZ3S0n7TsbkeIBLOoJt6bUQ45O0X9qrq9CAJtBWBoDr-SvKMrIup0nAOvlt0e09h_UINo" -H "Content-Type: application/json" -k 'http://xxxxxxxxx:8774/v2.1/os-hypervisors'
*
**/
function _nova_os_hypervisors($nova_endpoint, $auth_token)
{
	$openstack_rest_api = "{$nova_endpoint}/os-hypervisors";
	$curl_cmd = create_openstack_operation_request(OP_GET, $openstack_rest_api, $auth_token);
	$response = perform_curl_operation($curl_cmd, "GET OS HYPERVISORS");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		return json_encode($response);
	}
	return prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
}


	/**
* GET VIM hosts list (hypervisors).
*
* curl --tlsv1.2 -i -sw 'HTTP_CODE=%{http_code}' --connect-timeout 50 --max-time 50 -X GET -H "X-Auth-Token: gAAAAABdel44SS-FrqBKUdIEthbnsIH-R9cXfO307WcU3bz47fjJw1rxqLdaN4P08uw9U9P1UcB-9Qg-NAk3_FvmXD71tHmyyWYje-m2D1GFxF5WtuGZ3S0n7TsbkeIBLOoJt6bUQ45O0X9qrq9CAJtBWBoDr-SvKMrIup0nAOvlt0e09h_UINo" -H "Content-Type: application/json" -k 'http://xxxxxxxxx:8774/v2.1/os-hypervisors'
*
**/
function _nova_os_hypervisors_list_detail($nova_endpoint, $auth_token)
{
	$openstack_rest_api = "{$nova_endpoint}/os-hypervisors/detail";
	$curl_cmd = create_openstack_operation_request(OP_GET, $openstack_rest_api, $auth_token);
	$response = perform_curl_operation($curl_cmd, "GET OS HYPERVISORS DETAIL");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		return json_encode($response);
	}
	return prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
}


/**
* GET VIM host details by ID.
*
* curl --tlsv1.2 -i -sw 'HTTP_CODE=%{http_code}' --connect-timeout 50 --max-time 50 -X GET -H "X-Auth-Token: gAAAAABdel44SS-FrqBKUdIEthbnsIH-R9cXfO307WcU3bz47fjJw1rxqLdaN4P08uw9U9P1UcB-9Qg-NAk3_FvmXD71tHmyyWYje-m2D1GFxF5WtuGZ3S0n7TsbkeIBLOoJt6bUQ45O0X9qrq9CAJtBWBoDr-SvKMrIup0nAOvlt0e09h_UINo" -H "Content-Type: application/json" -k 'http://xxxxxxxxx:8774/v2.1/os-hypervisors/8'
*
**/
function _nova_os_hypervisor_details_by_id($nova_endpoint, $auth_token, $hypervisor_id)
{
	$openstack_rest_api = "{$nova_endpoint}/os-hypervisors/{$hypervisor_id}";
	$curl_cmd = create_openstack_operation_request(OP_GET, $openstack_rest_api, $auth_token);
	$response = perform_curl_operation($curl_cmd, "GET OS HYPERVISORS DETAILS");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		return json_encode($response);
	}
	return prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']);
}


