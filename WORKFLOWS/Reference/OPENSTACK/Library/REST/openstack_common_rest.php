<?php 

require_once '/opt/fmc_repository/Process/Reference/OPENSTACK/Library/REST/nova_rest.php';
require_once '/opt/fmc_repository/Process/Reference/OPENSTACK/Library/REST/cinder_rest.php';
require_once '/opt/fmc_repository/Process/Reference/OPENSTACK/Library/REST/neutron_rest.php';
require_once '/opt/fmc_repository/Process/Reference/OPENSTACK/Library/REST/keystone_rest.php';

#curl -i http://ot1-contrail-int-vip:9696/v2.0/subnets.json -X GET -H "X-Auth-Token: ${TEST_TOKEN}"
#-H "Accept: application/json" -H "Content-Type: application/json"
function object_get ($object_name, $auth_token, $openstack_rest_api) {

	$curl_cmd = create_openstack_operation_request(OP_GET, $openstack_rest_api, $auth_token);
	$response = perform_curl_operation($curl_cmd, strtoupper($object_name) . " GET");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

#curl -i http://ot1-contrail-int-vip:9696/v2.0/networks/12345 -X DELETE -H "X-Auth-Token:
#${TEST_TOKEN}" -H "Accept: application/json" -H "Content-Type: application/json"
function object_delete ($object_name, $auth_token, $openstack_rest_api) {

	$curl_cmd = create_openstack_operation_request(OP_DELETE, $openstack_rest_api, $auth_token);
	$response = perform_curl_operation($curl_cmd, strtoupper($object_name) . " DELETE");
	return $response;
}

/**
 * Poll Server Staus and wait for it to be ACTIVE/SHUTOFF/..
 * 
 * @param unknown $nova_endpoint
 * @param unknown $auth_token
 * @param unknown $server_id
 * @param unknown $status_check
 * @param unknown $process_params
 * @return mixed|unknown
 */
function wait_for_server_status ($nova_endpoint, $auth_token, $server_id, $status_check, $process_params, $timeout = SERVER_STATUS_CHANGE_TIMEOUT) {

	$wo_newparams = array();
	$wo_comment = "";
	$server_status = "";
	$total_sleeptime = 0;
	$check_server_status_message = "Checking Server $server_id Status (every " . SERVER_STATUS_CHECK_SLEEP . " seconds";
	$check_server_status_message .= ", timeout = $timeout seconds) :\n";
	while ($server_status !== $status_check) {
		$response = object_get("servers", $auth_token, "{$nova_endpoint}/servers/{$server_id}");
		$response = json_decode($response, true);
		if ($response['wo_status'] !== ENDED) {
			if ($status_check === "DELETE" && strpos($response['wo_comment'], 'Call to API Failed : HTTP_CODE=404') !== false) {
				$response = prepare_json_response(ENDED, "Server $server_id Not Found.\n", $wo_newparams, true);
				return $response;
			}
			$response = json_encode($response);
			return $response;
		}
		$response = $response['wo_newparams']['server'];
		$server_status = $response['status'];
		$server_power_state = $response['OS-EXT-STS:power_state'];
		switch ($server_power_state) {
			case '0':
				$server_power_state = "NOSTATE";
				break;
			case '1':
				$server_power_state = "Running";
				break;
			case '3':
				$server_power_state = "Paused";
				break;
			case '4':
				$server_power_state = "Shutdown";
				break;
			case '6':
				$server_power_state = "Crashed";
				break;
			case '7':
				$server_power_state = "Suspended";
				break;
			case '9':
				$server_power_state = "Building";
				break;
		}
		$server_task_state = "-";
		if ($response['OS-EXT-STS:task_state'] !== null) {
			$server_task_state = $response['OS-EXT-STS:task_state'];
		}
		logToFile("SERVER STATUS : $server_status");
		
		$wo_comment = "Server Status : $server_status \nTask State : $server_task_state\nPower State : $server_power_state\n";
		update_asynchronous_task_details($process_params, $check_server_status_message . $wo_comment);
		if ($server_status === $status_check) {
			break;
		}
		if ($server_status === ERROR) {
			logToFile("SERVER CREATION/ACTION FAILED.");
			$message = $response['fault']['message'];
			$code = $response['fault']['code'];
			$details = $response['fault']['details'];
			$wo_comment = "Server Status : $server_status\nMessage : $message\nCODE : $code\nDetails: $details";
			$response = prepare_json_response(FAILED, $wo_comment, $wo_newparams, true);
			return $response;
		}
		sleep(SERVER_STATUS_CHECK_SLEEP);
		$total_sleeptime += SERVER_STATUS_CHECK_SLEEP;
		if ($total_sleeptime > $timeout) {
			$wo_comment .= "The Server Status could not be changed to $status_check within $timeout seconds.\nHence, Ending the Process as Failure.";
			$response = prepare_json_response(FAILED, $wo_comment, $wo_newparams, true);
			return $response;			
		}
	}
	$response = prepare_json_response(ENDED, $wo_comment, $wo_newparams);
	return $response;
}

/**
 * Poll Server Staus and wait for it to be ACTIVE/SHUTOFF/..
 * Due to issue on Openstack, Retry Server stop/start/.. at specified intervals
 *
 * @param unknown $nova_endpoint
 * @param unknown $auth_token
 * @param unknown $server_id
 * @param unknown $status_check
 * @param unknown $process_params
 * @return mixed|unknown
 */
function wait_for_server_status_with_retry ($nova_endpoint, $auth_token, $server_id, $status_check, $process_params, $timeout = SERVER_STATUS_CHANGE_TIMEOUT, $retry_interval = SERVER_STATUS_CHANGE_RETRY_INTERVAL) {

	$wo_newparams = array();
	$wo_comment = "";
	$server_status = "";
	$total_sleeptime = 0;
	$check_server_status_message = "Checking Server $server_id Status (every " . SERVER_STATUS_CHECK_SLEEP . " seconds";
	$check_server_status_message .= ", timeout = $timeout seconds, retry interval = $retry_interval) :\n";
	while ($server_status !== $status_check) {

		$response = object_get("servers", $auth_token, "{$nova_endpoint}/servers/{$server_id}");
		$response = json_decode($response, true);
		if ($response['wo_status'] !== ENDED) {
			if ($status_check === "DELETE" && strpos($response['wo_comment'], 'Call to API Failed : HTTP_CODE=404') !== false) {
				$response = prepare_json_response(ENDED, "Server $server_id Not Found.\n", $wo_newparams, true);
				return $response;
			}
			$response = json_encode($response);
			return $response;
		}
		$response = $response['wo_newparams']['server'];
		$server_status = $response['status'];
		$server_power_state = $response['OS-EXT-STS:power_state'];
		switch ($server_power_state) {
			case '0':
				$server_power_state = "NOSTATE";
				break;
			case '1':
				$server_power_state = "Running";
				break;
			case '3':
				$server_power_state = "Paused";
				break;
			case '4':
				$server_power_state = "Shutdown";
				break;
			case '6':
				$server_power_state = "Crashed";
				break;
			case '7':
				$server_power_state = "Suspended";
				break;
			case '9':
				$server_power_state = "Building";
				break;
		}
		$server_task_state = "-";
		if ($response['OS-EXT-STS:task_state'] !== null) {
			$server_task_state = $response['OS-EXT-STS:task_state'];
		}
		logToFile("SERVER STATUS : $server_status");

		$wo_comment = "Server Status : " . $server_status .
		"\nTask State : " . $server_task_state .
		"\nPower State : " . $server_power_state . "\n";
		update_asynchronous_task_details($process_params, $check_server_status_message . $wo_comment);
		if ($server_status === $status_check) {
			break;
		}
		if ($server_status === ERROR) {
			logToFile("SERVER CREATION/ACTION FAILED.");
			$message = $response['fault']['message'];
			$code = $response['fault']['code'];
			$details = $response['fault']['details'];
			$wo_comment = "Server Status : $server_status\nMessage : $message\nCODE : $code\nDetails: $details";
			$response = prepare_json_response(FAILED, $wo_comment, $wo_newparams, true);
			return $response;
		}

		if ($total_sleeptime >= $retry_interval) {
			switch ($status_check) {
				case SHUTOFF:
					$wo_comment .= "The Server Status could not be changed to $status_check within $retry_interval seconds.\nHence, retry to Stop.";
					update_asynchronous_task_details($process_params, $check_server_status_message . $wo_comment);
					$response = _nova_server_stop($nova_endpoint, $auth_token, $server_id);
					/**
					 * No need to check the response
					 *
					 * $response = json_decode($response, true);
					 * if ($response['wo_status'] !== ENDED) {
						if (strpos($response['wo_comment'], 'Call to API Failed : HTTP_CODE=409') === false) {
						$response = json_encode($response);
						return $response;
						}
					} */
					break;
				case ACTIVE:
					$wo_comment .= "The Server Status could not be changed to $status_check within $retry_interval seconds.\nHence, retry to Start.";
					update_asynchronous_task_details($process_params, $check_server_status_message . $wo_comment);
					$response = _nova_server_start($nova_endpoint, $auth_token, $server_id);
					/**
					 * No need to check the response
					 *
					 * $response = json_decode($response, true);
					 * if ($response['wo_status'] !== ENDED) {
						if (strpos($response['wo_comment'], 'Call to API Failed : HTTP_CODE=409') === false) {
						$response = json_encode($response);
						return $response;
						}
					} */
					break;
				default:
					break;
			}
			$retry_interval += $retry_interval;
		}

		sleep(SERVER_STATUS_CHECK_SLEEP);
		$total_sleeptime += SERVER_STATUS_CHECK_SLEEP;
		if ($total_sleeptime > $timeout) {
			$wo_comment .= "The Server Status could not be changed to $status_check within $timeout seconds.\nHence, Ending the Process as Failure.";
			$response = prepare_json_response(FAILED, $wo_comment, $wo_newparams, true);
			return $response;
		}
	}
	$response = prepare_json_response(ENDED, $wo_comment, $wo_newparams);
	return $response;
}

/**
 * Poll Port Staus and wait for it to be ACTIVE/DOWN/..
 * 
 * @param unknown $neutron_endpoint
 * @param unknown $auth_token
 * @param unknown $port_id
 * @param unknown $status_check
 * @param unknown $process_params
 * @param string $timeout
 * @return unknown
 */
function wait_for_port_status ($neutron_endpoint, $auth_token, $port_id, $status_to_check, $process_params, $timeout = PORT_STATUS_CHANGE_TIMEOUT) {

	$wo_newparams = array();
	$wo_comment = "";
	$port_status = "";
	$total_sleeptime = 0;
	$check_port_status_message = "Checking Port $port_id Status (every " . PORT_STATUS_CHECK_SLEEP . " seconds";
	$check_port_status_message .= ", timeout = $timeout seconds) :\n";
	if (!is_array($status_to_check)) {
		$status_check = array($status_to_check);
	}
	else {
		$status_check = $status_to_check;
	}
	while (!in_array($port_status, $status_check)) {
		$response = object_get("ports", $auth_token, "{$neutron_endpoint}/v2.0/ports/{$port_id}");
		$response = json_decode($response, true);
		if ($response['wo_status'] !== ENDED) {
			if (in_array("DELETE", $status_check) && strpos($response['wo_comment'], 'Call to API Failed : HTTP_CODE=404') !== false) {
				$response = prepare_json_response(ENDED, "Port $port_id Not Found.\n", $wo_newparams, true);
				return $response;
			}
			$response = json_encode($response);
			return $response;
		}
		$response = $response['wo_newparams']['port'];
		$port_status = $response['status'];
		logToFile("PORT STATUS : $port_status");

		$wo_comment = "Port Status : " . $port_status . "\n";
		update_asynchronous_task_details($process_params, $check_port_status_message . $wo_comment);
		if (in_array($port_status, $status_check)) {
			break;
		}
		if ($port_status === ERROR) {
			logToFile("PORT CREATION/ACTION FAILED.");
			/*$message = $response['fault']['message'];
			$code = $response['fault']['code'];
			$details = $response['fault']['details'];
			$wo_comment = "Port Status : $port_status\nMessage : $message\nCODE : $code\nDetails: $details";*/
			$response = prepare_json_response(FAILED, "Port Creation/Action Failed.\n$wo_comment", $wo_newparams, true);
			return $response;
		}
		sleep(PORT_STATUS_CHECK_SLEEP);
		$total_sleeptime += PORT_STATUS_CHECK_SLEEP;
		if ($total_sleeptime > $timeout) {
			$statuses = "[ ";
			foreach ($status_check as $status) {
				$statuses .= $status . " ";
			}
			$statuses .= "]";
			$wo_comment .= "The Port Status could not be changed to $statuses within $timeout seconds.\nHence, Ending the Process as Failure.";
			$response = prepare_json_response(FAILED, $wo_comment, $wo_newparams, true);
			return $response;
		}
	}
	$response = prepare_json_response(ENDED, $wo_comment, $wo_newparams);
	return $response;
}

/**
 * Poll Volume Staus and wait for it to be AVAILABLE/..
 *
 * @param unknown $neutron_endpoint
 * @param unknown $auth_token
 * @param unknown $port_id
 * @param unknown $status_check
 * @param unknown $process_params
 * @param string $timeout
 * @return unknown
 */
function wait_for_volume_status ($cinder_endpoint, $auth_token, $volume_id, $status_to_check, $process_params, $timeout = VOLUME_STATUS_CHANGE_TIMEOUT) {

	$wo_newparams = array();
	$wo_comment = "";
	$volume_status = "";
	$total_sleeptime = 0;
	$check_volume_status_message = "Checking Volume $volume_id Status (every " . VOLUME_STATUS_CHECK_SLEEP . " seconds";
	$check_volume_status_message .= ", timeout = $timeout seconds) :\n";
	if (!is_array($status_to_check)) {
		$status_check = array($status_to_check);
	}
	else {
		$status_check = $status_to_check;
	}
	while (!in_array($volume_status, $status_check)) {
		$response = object_get("volumes", $auth_token, "{$cinder_endpoint}/volumes/{$volume_id}");
		$response = json_decode($response, true);
		if ($response['wo_status'] !== ENDED) {
			if (in_array("DELETE", $status_check) && strpos($response['wo_comment'], 'Call to API Failed : HTTP_CODE=404') !== false) {
				$response = prepare_json_response(ENDED, "Volume $volume_id Not Found.\n", $wo_newparams, true);
				return $response;
			}
			$response = json_encode($response);
			return $response;
		}
		$response = $response['wo_newparams']['volume'];
		$volume_status = $response['status'];
		logToFile("VOLUME STATUS : $volume_status");

		$wo_comment = "Volume Status : $volume_status\n";
		update_asynchronous_task_details($process_params, $check_volume_status_message . $wo_comment);
		if (in_array($volume_status, $status_check)) {
			break;
		}
		if ($volume_status === VOLUME_ERROR || $volume_status === VOLUME_ERROR_DELETING
				|| $volume_status === VOLUME_ERROR_EXTENDING || $volume_status === VOLUME_ERROR_RESTORING) {

			logToFile("VOLUME CREATION/ACTION FAILED.");
			$response = prepare_json_response(FAILED, "Volume Creation/Action Failed.\n$wo_comment", $wo_newparams, true);
			return $response;
		}
		sleep(VOLUME_STATUS_CHECK_SLEEP);
		$total_sleeptime += VOLUME_STATUS_CHECK_SLEEP;
		if ($total_sleeptime > $timeout) {
			$statuses = "[ ";
			foreach ($status_check as $status) {
				$statuses .= $status . " ";
			}
			$statuses .= "]";
			$wo_comment .= "The Volume Status could not be changed to $statuses within $timeout seconds.\nHence, Ending the Process as Failure.";
			$response = prepare_json_response(FAILED, $wo_comment, $wo_newparams, true);
			return $response;
		}
	}
	$response = prepare_json_response(ENDED, $wo_comment, $wo_newparams);
	return $response;
}

/**
 * Get Private IP addresses from the Server
 *
 * @param unknown $openstack_device_id
 * @param unknown $server
 * @return multitype:NULL
 */
function get_private_ip_addresses ($auth_token, $nova_endpoint, $server_id) {

	$response = object_get("servers", $auth_token, "{$nova_endpoint}/servers/{$server_id}");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$server_addresses = $response['wo_newparams']['addresses'];
	$address_index = 0;
	$ip_addresses = array();
	$wo_newparams = array();
	$wo_comment = "";
	foreach ($server_addresses as $address) {
		foreach($address as $addr) {
			if ($addr['OS-EXT-IPS:type'] === "fixed") {
				$ip_addresses[$address_index]['fixed_ip'] = $addr['addr'];
				$wo_comment .=  "Fixed Ip : " . $ip_addresses[$address_index++]['fixed_ip'] . "\n";
			}
		}
	}
	$wo_newparams['server_fixed_ips'] = $ip_addresses;
	$response = prepare_json_response(ENDED, $wo_comment, $wo_newparams, true);
	return $response;
}

/**
 * Get Server Interfaces details : network, subnet and port details
 * 
 * @param unknown $auth_token
 * @param unknown $nova_endpoint
 * @param unknown $neutron_endpoint
 * @param unknown $server_id
 * @param unknown $server_networks
 * @return unknown
 */
function get_server_interface_details ($auth_token, $nova_endpoint, $neutron_endpoint, $server_id, $server_networks) {

	$response = object_get("servers", $auth_token, "{$nova_endpoint}/servers/{$server_id}/os-interface");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}

	$interface_attachments = $response['wo_newparams']['interfaceAttachments'];

	$wo_comment = "Server Interfaces Details :\n";
	$interface_index = 0;
	$server_interface_details = array();
	foreach ($server_networks as $server_network) {
		$id = "";
		if (!empty($server_network['uuid'])) {
			$id = $server_network['uuid'];
		}
		else if (!empty($server_network['port'])) {
			$id = $server_network['port'];
		}
		foreach ($interface_attachments as $interface) {
			if ($id === $interface['net_id'] || $id === $interface['port_id']) {

				$server_interface_details[$interface_index]['network_id'] = $interface['net_id'];
				$server_interface_details[$interface_index]['port_id'] = $interface['port_id'];
				$server_interface_details[$interface_index]['ip_address'] = $interface['fixed_ips'][0]['ip_address'];
				$server_interface_details[$interface_index]['subnet_id'] = $interface['fixed_ips'][0]['subnet_id'];
				$response = get_subnet_mask_and_gateway_ip_from_subnet($auth_token, $neutron_endpoint, $server_interface_details[$interface_index]['subnet_id']);
				$response = json_decode($response, true);
				if ($response['wo_status'] !== ENDED) {
					$response = json_encode($response);
					return $response;
				}
				$server_interface_details[$interface_index]['subnet_ip'] = $response['wo_newparams']['subnet_ip'];
				$server_interface_details[$interface_index]['subnet_mask'] = $response['wo_newparams']['subnet_mask'];
				$server_interface_details[$interface_index]['subnet_gateway_ip'] = $response['wo_newparams']['subnet_gateway_ip'];

				$wo_comment .= ($interface_index + 1) . "]\n";
				#$wo_comment .=  "Network Id : " . $server_interface_details[$interface_index]['network_id'] . "\n";
				#$wo_comment .=  "Port Id : " . $server_interface_details[$interface_index]['port_id'] . "\n";
				$wo_comment .=  "MAC Address : " . $interface['mac_addr'] . "\n";
				$wo_comment .=  "IP Address : " . $server_interface_details[$interface_index]['ip_address'] . "\n";
				$wo_comment .=  "State : " . $interface['port_state'] . "\n";
				#$wo_comment .=  "Subnet Id : " . $server_interface_details[$interface_index]['subnet_id'] . "\n";
				#$wo_comment .=  "Subnet IP : " . $server_interface_details[$interface_index]['subnet_ip'] . "\n";
				#$wo_comment .=  "Subnet Mask : " . $server_interface_details[$interface_index]['subnet_mask'] . "\n";
				#$wo_comment .=  "Subnet Gateway IP : " . $server_interface_details[$interface_index]['subnet_gateway_ip'] . "\n";

				$interface_index++;
				break;
			}
		}
	}
	$wo_newparams['server_interface_details'] = $server_interface_details;
	$response = prepare_json_response(ENDED, $wo_comment, $wo_newparams, true);
	return $response;
}

#curl -g -i -X GET http://10.31.1.13:9696/v2.0/ports.json?device_id=fa477dec-b343-4f60-a13d-0fc250d5055e
#-H "User-Agent: python-neutronclient" -H "Accept: application/json" -H "X-Auth-Token: {SHA1}74ae9bf825ea9d16061f66518d0b9effa78f0785"
function router_interface_list ($neutron_endpoint, $auth_token, $router_id) {

	$openstack_rest_api = "{$neutron_endpoint}/v2.0/ports/?device_id={$router_id}";
	$response = object_get("routers", $auth_token, $openstack_rest_api);
	return $response;
}

/**
 * Retrieve port_id from network_id and server_id
 *
 * @param unknown $network_id
 * @param unknown $server_id
 * @param unknown $auth_token
 * @param unknown $neutron_endpoint
 * @return string|unknown
 */
function get_port_id_from_network_and_server_id ($auth_token, $neutron_endpoint, $network_id, $server_id) {

	$response = object_get("ports", $auth_token, "{$neutron_endpoint}/v2.0/ports");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$ports = $response['wo_newparams']['ports'];
	$port_id = "";
	$wo_newparams = array();
	foreach ($ports as $port) {

		$device_id = $port['device_id'];
		$net_id = $port['network_id'];
		if ($device_id === $server_id && $network_id === $net_id) {
			$wo_newparams['port_id'] = $port['id'];
			$response = prepare_json_response(ENDED, "Port Id : " . $port['id'], $wo_newparams, true);
			return $response;
		}
	}
	$response = prepare_json_response(FAILED, "Couldn't find the port_id with the given network and device id", $wo_newparams, true);
	return $response;
}

/**
 * Get port_id from subnet and IP address
 *
 * @param unknown $device_id
 * @param unknown $subnet
 * @param unknown $ip_address
 * @param unknown $ports_import
 * @return Ambigous <string, unknown>
 */
function get_port_id_from_subnet_and_ip_address ($auth_token, $neutron_endpoint, $subnet, $ip_address) {

	$response = object_get("ports", $auth_token, "{$neutron_endpoint}/v2.0/ports");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$ports = $response['wo_newparams']['ports'];
	$wo_newparams = array();
	foreach ($ports as $port) {

		$fixed_ips = $port['fixed_ips'];
		foreach ($fixed_ips as $fixed_ip) {
			if (array_key_exists('subnet_id', $fixed_ip) && array_key_exists('ip_address', $fixed_ip)) {
				$subnet_id = $fixed_ip['subnet_id'];
				$ip = $fixed_ip['ip_address'];
				if ($subnet === $subnet_id && $ip_address === $ip) {
					$wo_newparams['port_id'] = $port['id'];
					$response = prepare_json_response(ENDED, "Port Id : " . $port['id'], $wo_newparams, true);
					return $response;
				}
			}
		}
	}
	$response = prepare_json_response(FAILED, "Couldn't find the port_id for given Subnet and IP address.", $wo_newparams, true);
	return $response;
}

/**
 * Get Subnet details from network and IP address
 *
 * @param unknown $openstack_device_id
 * @param unknown $network
 * @param unknown $ip_address
 * @param unknown $subnets_and_networks
 * @return multitype:unknown
 */
function get_subnet_details_from_network ($auth_token, $neutron_endpoint, $network, $ip_address) {

	$response = object_get("networks", $auth_token, "{$neutron_endpoint}/v2.0/networks/{$network}");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$networks = $response['wo_newparams']['networks'];
	$network_subnets = $networks['subnets'];
	#$subnets_count = count($network_subnets);

	$wo_newparams = array();
	$wo_comment = "";
	foreach ($network_subnets as $network_subnet) {
		$response = object_get("subnets", $auth_token, "{$neutron_endpoint}/v2.0/subnets/{$network_subnet}");
		$response = json_decode($response, true);
		if ($response['wo_status'] !== ENDED) {
			$response = json_encode($response);
			return $response;
		}
		$subnet = $response['wo_newparams']['subnet'];
		$cidr = $subnet['cidr'];
		if (cidr_match($ip_address, $cidr)) {
			$response_subnet_and_mask = cidr_to_subnet_and_subnetmask_address($cidr);
			$subnet_gateway_ip = $subnet['gateway_ip'];
			$wo_newparams['subnet'] = $network_subnet;
			$wo_newparams['subnet_ip'] = $response_subnet_and_mask['subnet_ip'];
			$wo_newparams['subnet_mask'] = $response_subnet_and_mask['subnet_mask'];
			$wo_newparams['subnet_gateway_ip'] = $subnet_gateway_ip;
			$wo_comment .= "Subnet Id : " . $wo_newparams['subnet'] . "\n";
			$wo_comment .= "Subnet IP : " . $wo_newparams['subnet_ip'] . "\n";
			$wo_comment .= "Subnet Mask : " . $wo_newparams['subnet_mask'] . "\n";
			$wo_comment .= "Subnet Gateway IP : " . $wo_newparams['subnet_gateway_ip'] . "\n";
			$response = prepare_json_response(ENDED, $wo_comment, $wo_newparams, true);
			return $response;
		}
	}
	$response = prepare_json_response(FAILED, "Couldn't find the Subnet details for given Network and IP address.", $wo_newparams, true);
	return $response;
}

/**
 * Get Subnet Mask and Gateway IP from Subnet
 *
 * @param unknown $openstack_device_id
 * @param unknown $subnet
 * @return multitype:unknown
 */
function get_subnet_mask_and_gateway_ip_from_subnet ($auth_token, $neutron_endpoint, $subnet) {

	$response = object_get("subnets", $auth_token, "{$neutron_endpoint}/v2.0/subnets/{$subnet}");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$wo_newparams = array();
	$wo_comment = "";
	$subnet = $response['wo_newparams']['subnet'];
	$cidr = $subnet['cidr'];
	$response_subnet_and_mask = cidr_to_subnet_and_subnetmask_address($cidr);
	$subnet_gateway_ip = $subnet['gateway_ip'];
	$wo_newparams['subnet_ip'] = $response_subnet_and_mask['subnet_ip'];
	$wo_newparams['subnet_mask'] = $response_subnet_and_mask['subnet_mask'];
	$wo_newparams['subnet_gateway_ip'] = $subnet_gateway_ip;
	$wo_comment .= "Subnet IP : " . $wo_newparams['subnet_ip'] . "\n";
	$wo_comment .= "Subnet Mask : " . $wo_newparams['subnet_mask'] . "\n";
	$wo_comment .= "Subnet Gateway IP : " . $wo_newparams['subnet_gateway_ip'] . "\n";
	$response = prepare_json_response(ENDED, $wo_comment, $wo_newparams, true);
	return $response;
}

/**
 * Get Floating IP address and Network from Id
 *
 * @param unknown $openstack_device_id
 * @param unknown $floating_ip_id
 * @return multitype:unknown
 */
function get_floating_ip_address_and_network_from_id ($auth_token, $neutron_endpoint, $floating_ip_id) {

	$response = object_get("floatingips", $auth_token, "{$neutron_endpoint}/v2.0/floatingips/{$floating_ip_id}");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$wo_newparams = array();
	$wo_comment = "";
	$floatingip = $response['wo_newparams']['floatingip'];
	$wo_newparams['floating_ip_address'] = $floatingip['floating_ip_address'];
	$wo_newparams['floating_ip_network'] = $floatingip['floating_network_id'];
	$wo_comment .= "Floating IP Address : " . $wo_newparams['floating_ip_address'] . "\n";
	$wo_comment .= "Floating IP Network : " . $wo_newparams['floating_ip_network'] . "\n";
	$response = prepare_json_response(ENDED, $wo_comment, $wo_newparams, true);
	return $response;
}

/**
 * Get a Free Floating IP address from the Network
 *
 * @param unknown $openstack_device_id
 * @param unknown $network
 * @param unknown $tenant
 * @return unknown
 */
function get_free_floatingip ($auth_token, $neutron_endpoint, $network, $tenant) {

	$response = object_get("floatingips", $auth_token, "{$neutron_endpoint}/v2.0/floatingips?tenant_id={$tenant}");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$floatingips = $response['wo_newparams']['floatingips'];
	$wo_newparams = array();
	$wo_comment = "";
	foreach ($floatingips as $floatingip) {

		$floatingip_id = $floatingip['id'];
		$floatingip_address = $floatingip['floating_ip_address'];
		$floatingip_network = $floatingip['floating_network_id'];
		if ($floatingip['fixed_ip_address'] === null && $floatingip['port_id'] === null && $floatingip_network === $network) {

			$wo_newparams['floating_ip_address'] = $floatingip_address;
			$wo_newparams['floating_ip_id'] = $floatingip_id;
			$wo_comment .= "Floating IP Id : $floatingip_id\n";
			$wo_comment .= "Floating IP Address : $floatingip_address";
			$response = prepare_json_response(ENDED, $wo_comment, $wo_newparams);
			return $response;
		}
	}
	$response = prepare_json_response(ENDED, "Couldn't find a free Floating IP address in the given Network", $wo_newparams, true);
	return $response;
}

/**
 * Check for a Free Floating IP address in the Network. If not available, create one.
 *
 * @param unknown $openstack_device_id
 * @param unknown $network
 * @param unknown $tenant
 * @return unknown
 */
function allocate_floatingip_address ($auth_token, $neutron_endpoint, $network, $tenant) {

	$response = get_free_floatingip($auth_token, $neutron_endpoint, $network, $tenant);
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}

	if (array_key_exists('floating_ip_id', $response['wo_newparams']) &&
			array_key_exists('floating_ip_address', $response['wo_newparams'])) {
				$response = json_encode($response);
				return $response;
	}
	$response = _neutron_floatingip_create($neutron_endpoint, $auth_token, $network, $tenant);
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$floatingip = $response['wo_newparams']['floatingip'];
	$floatingip_id = $floatingip['id'];
	$floatingip_address = $floatingip['floating_ip_address'];

	$wo_newparams = array();
	$wo_newparams['floating_ip_address'] = $floatingip_address;
	$wo_newparams['floating_ip_id'] = $floatingip_id;
	$wo_comment = "Floating IP Id : $floatingip_id\n";
	$wo_comment .= "Floating IP Address : $floatingip_address";
	$response = prepare_json_response(ENDED, $wo_comment, $wo_newparams);
	return $response;
}

/**
 * Remove all interfaces of the Router
 *
 * @param unknown $openstack_device_id
 * @param unknown $router
 * @return unknown
 */
function remove_all_router_interfaces ($auth_token, $neutron_endpoint, $router) {

	$response = router_interface_list($neutron_endpoint, $auth_token, $router);
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$router_interfaces = $response['wo_newparams']['ports'];

	$wo_comment = "";
	$wo_newparams = array();
	$router_interface_subnets = array();
	$subnet_gateway_ips = array();
	$index = 0;
	foreach ($router_interfaces as $router_interface) {

		$device_owner = $router_interfaces['device_owner'];
		$device_id = $router_interface['device_id'];
		if ($device_owner === "network:router_interface" && $device_id === $router) {
			$response = _neutron_router_interface_delete($neutron_endpoint, $auth_token, $router, $subnet_id);
			$subnet_id = $router_interface['fixed_ips'][0]['subnet_id'];
			$router_interface_subnets[$index]['subnet_id'] = $subnet_id;
			$ip_address = $router_interface['fixed_ips'][0]['ip_address'];
			$subnet_gateway_ips[$index++]['ip_address'] = $ip_address;
			$wo_comment .= "Router Interface Subnet Id : $subnet_id\n";
			$wo_comment .= "Router Interface IP Address : $subnet_gateway_ips";
		}
	}
	$wo_newparams['router_interfaces'] = $router_interface_subnets;
	$wo_newparams['router_interfaces_gateway_ips'] = $subnet_gateway_ips;
	$response = prepare_json_response(ENDED, $wo_comment, $wo_newparams);
	return $response;
}

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

#curl -i http://ct-int-vip:28774/v2/${PJID}/servers/${server_id} -X GET -H "X-Auth-Token:
#${TEST_TOKEN}" -H "Accept: application/json" -H "Content-Type: application/json"
function _nova_get_server_details ($nova_endpoint, $auth_token, $server_id) {

        $openstack_rest_api = "{$nova_endpoint}/servers/{$server_id}";
        $curl_cmd = create_openstack_operation_request(OP_GET, $openstack_rest_api, $auth_token);

        $response = perform_curl_operation($curl_cmd, "SERVER GET DETAILS");
        return $response;
}

?>
