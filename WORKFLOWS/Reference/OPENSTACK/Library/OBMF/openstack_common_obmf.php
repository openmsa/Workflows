<?php 

require_once '/opt/fmc_repository/Process/Reference/OPENSTACK/Library/OBMF/nova_obmf.php';
require_once '/opt/fmc_repository/Process/Reference/OPENSTACK/Library/OBMF/neutron_obmf.php';

/**
 * Get Server Id from the server_name
 * 
 * @param unknown $openstack_device_id
 * @param unknown $server_name
 * @return unknown
 */
function get_server_id ($openstack_device_id, $server_name) {
	
	$instances_objname = "servers";
	$array = array($instances_objname);
	$response = import_objects($openstack_device_id, $array);
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$servers = $response['wo_newparams'][$instances_objname];
	$wo_newparams = array();
	$wo_comment = "";
	foreach ($servers as $server_object_id => $server_params) {
		$name = $server_params['name'];
		if ($name === $server_name) {
			$server_id = $server_params['object_id'];
			$wo_comment .=  "Server Id : $server_id\n";
			$wo_newparams['server_id'] = $server_id;
			$response = prepare_json_response(ENDED, $wo_comment, $wo_newparams, true);
			return $response;
		}
	}
	$response = prepare_json_response(FAILED, "Not able to retrieve the server_id", $wo_newparams, true);
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
function wait_for_server_status ($openstack_device_id, $server_id, $status_check, $process_params, $timeout = SERVER_STATUS_CHANGE_TIMEOUT) {

	$wo_newparams = array();
	$wo_comment = "";
	$server_status = "";
	$total_sleeptime = 0;
	$instances_objname = "servers";
	$array = array($instances_objname);
	$check_server_status_message = "Checking Server $server_id Status (every " . SERVER_STATUS_CHECK_SLEEP . " seconds";
	$check_server_status_message .= ", timeout = $timeout seconds) :\n";
	while ($server_status !== $status_check) {
		$response = import_objects($openstack_device_id, $array);
		$response = json_decode($response, true);
		if ($response['wo_status'] !== ENDED) {
			$response = json_encode($response);
			return $response;
		}
		if (isset($response['wo_newparams'][$instances_objname][$server_id])) {
		$response = $response['wo_newparams'][$instances_objname][$server_id];
		$server_status = $response['status'];
                if (isset($response['power_state'])) {
			$server_power_state = $response['power_state'];
                } else {
                  	$server_power_state = 0;
                }
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
		}
		$server_task_state = "-";
		if (array_key_exists('task_state', $response)) {
			$server_task_state = $response['task_state'];
		}
		logToFile("SERVER STATUS : $server_status");

		$wo_comment = "Server Status : $server_status\nTask State : $server_task_state\nPower State : $server_power_state\n";
		update_asynchronous_task_details($process_params, $check_server_status_message . $wo_comment);
		if ($server_status === $status_check) {
			break;
		}
		if ($server_status === ERROR) {
			logToFile("SERVER CREATION/ACTION FAILED.");
			#$message = $response['fault']['message'];
			#$code = $response['fault']['code'];
			#$details = $response['fault']['details'];
			#$wo_comment = "Server Status : $server_status\nMessage : $message\nCODE : $code\nDetails: $details";
			$response = prepare_json_response(FAILED, "Server Creation/Action Failed.\n$wo_comment", $wo_newparams, true);
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
 * Get Private IP addresses from the Server
 *
 * @param unknown $openstack_device_id
 * @param unknown $server
 * @return multitype:NULL
 */
function get_private_ip_addresses ($openstack_device_id, $server) {

	$instances_objname = "servers";
	$array = array($instances_objname);
	$response = import_objects($openstack_device_id, $array);
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$server_addresses = $response['wo_newparams'][$instances_objname][$server]['addresses'];
	
	$address_index = 0;
	$ip_addresses = array();
	$wo_newparams = array();
	$wo_comment = "";
	foreach ($server_addresses as $address) {
        if ($address['type'] === "fixed") {
			$ip_addresses[$address_index] = $address['addr'];
			$wo_comment .=  "Fixed Ip : " . $ip_addresses[$address_index++] . "\n";
		}
    }
	$wo_newparams['server_fixed_ips'] = $ip_addresses;
	$response = prepare_json_response(ENDED, $wo_comment, $wo_newparams, true);
	return $response;
}

/**
 * Get Private IP addresses from the Server
 *
 * @param unknown $openstack_device_id
 * @param unknown $server
 * @return multitype:NULL
 */
function get_floating_ip_address ($openstack_device_id, $instancename) {

	$instances_objname = "servers";
	$array = array($instances_objname);
	$response = import_objects($openstack_device_id, $array);
		
	//parse $response
	$pos=strpos($response,'"name":"'.$instancename.'"');
	if ($pos === false) {
		 prepare_json_response(FAILED, "Couldn't find the instance name $instancename", $wo_newparams, true);
	} else {
		$response=substr($response,$pos);
		//get the next instance name
		$pos=strpos($response,',"name":"');
		if ($pos === false) {
			//no next
		} else {
			$response=substr($response,0,$pos);
		}
		//parse result
		do {
			$pos=strpos($response,'"addr":"');
			$response=substr($response,$pos+8);
			$lastCharIp=strpos($response,'",');
			$IP=substr($response,0,$lastCharIp);
			$type=strpos($response,'"type":"');
			$response=substr($response,$type+8);
			$lastCharType=strpos($response,'"');
			$Type=substr($response,0,$lastCharType);
			logToFile("INSTANCE -> ".$instancename."  IP -> ".$IP."  Type -> ".$Type);	
			if($Type=="floating"){
				logToFile("**** FOUND **** IP -> ".$IP."  Type -> ".$Type);
				$wo_newparams['server_floating_ip'] = $IP;
				return  prepare_json_response(ENDED, "The instance ".$instancename." is configured with the floating IP ".$wo_newparams['server_floating_ip'], $wo_newparams, true);
			}	
		} while ($pos != false);
	}
	return prepare_json_response(FAILED, "Couldn't find floating IP for instance ".$instancename, null, true);
}

/**
 * Get Server Interfaces details : network, subnet and port details
 * 
 * @param unknown $openstack_device_id
 * @param unknown $server_id
 * @param unknown $networks
 * @return unknown
 */
function get_server_interface_details ($openstack_device_id, $server_id, $networks) {
	
	$response = get_private_ip_addresses($openstack_device_id, $server_id);
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$ip_addresses = $response['wo_newparams']['server_fixed_ips'];
	
	$networks_objname = "networks";
	$subnets_objname = "subnets";
	$array = array($networks_objname, $subnets_objname);
	$response = import_objects($openstack_device_id, $array, true);
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$subnets_and_networks = $response['wo_newparams'];

	$ports_objname = "ports";
	$array = array($ports_objname);
	$response = import_objects($openstack_device_id, $array, true);
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$ports_import = $response['wo_newparams'];

	$wo_comment = "Server Interfaces Details :\n";
	$ip_address_index = 0;
	$server_interfaces_details = array();
	foreach ($networks as $network) {
		$net = $network['network'];
		$ip_address = $ip_addresses[$ip_address_index];
		$response = get_subnet_details_from_network($openstack_device_id, $net, $ip_address, $subnets_and_networks);
		$response = json_decode($response, true);
		if ($response['wo_status'] !== ENDED) {
			$response = json_encode($response);
			return $response;
		}
		$ports = get_port_id_from_subnet_and_ip_address($openstack_device_id, $response['wo_newparams']['subnet_id'], $ip_address, $ports_import);
		$ports = json_decode($ports, true);
		if ($ports['wo_status'] !== ENDED) {
			$ports = json_encode($ports);
			return $ports;
		}
		
		$server_interfaces_details[$ip_address_index]['network'] = $net;
		$server_interfaces_details[$ip_address_index]['ip_address'] = $ip_address;
		$server_interfaces_details[$ip_address_index]['port_id'] = $ports['wo_newparams']['port_id'];
		$server_interfaces_details[$ip_address_index]['subnet_id'] = $response['wo_newparams']['subnet_id'];
		$server_interfaces_details[$ip_address_index]['subnet_ip'] = $response['wo_newparams']['subnet_ip'];
		$server_interfaces_details[$ip_address_index]['subnet_mask'] = $response['wo_newparams']['subnet_mask'];
		$server_interfaces_details[$ip_address_index]['subnet_gateway_ip'] = $response['wo_newparams']['subnet_gateway_ip'];
		
		$wo_comment .= ($ip_address_index + 1) . "]\n";
		#$wo_comment .=  "Network Id : " . $server_interfaces_details[$ip_address_index]['network_id'] . "\n";
		#$wo_comment .=  "Port Id : " . $server_interfaces_details[$ip_address_index]['port_id'] . "\n";
		$wo_comment .=  "MAC Address : " . $ports['wo_newparams']['port_mac_address'] . "\n";
		$wo_comment .=  "IP Address : $ip_address\n";
		$wo_comment .=  "Status : " . $ports['wo_newparams']['port_status'] . "\n";
		#$wo_comment .=  "Subnet Id : " . $server_interfaces_details[$ip_address_index]['subnet_id'] . "\n";
		#$wo_comment .=  "Subnet IP : " . $server_interfaces_details[$ip_address_index]['subnet_ip'] . "\n";
		#$wo_comment .=  "Subnet Mask : " . $server_interfaces_details[$ip_address_index]['subnet_mask'] . "\n";
		#$wo_comment .=  "Subnet Gateway IP : " . $server_interfaces_details[$ip_address_index]['subnet_gateway_ip'] . "\n";

		$ip_address_index++;
	}
	$wo_newparams['server_interface_details'] = $server_interfaces_details;
	$response = prepare_json_response(ENDED, $wo_comment, $wo_newparams, true);
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
function get_port_id_from_subnet_and_ip_address ($device_id, $subnet, $ip_address, $ports_import) {

	$ports = $ports_import['ports'];
	$wo_newparams = array();
	foreach ($ports as $port => $port_params) {
		if (array_key_exists(0, $port_params['fixed_ips'])) {
			$port_subnet = $port_params['fixed_ips'][0]['subnet_id'];
			$port_ip_address = $port_params['fixed_ips'][0]['ip_address'];
			if ($subnet === $port_subnet && $ip_address === $port_ip_address) {
				$port_id = $port_params['object_id'];
				$port_status = $port_params['status'];
				$mac_address = $port_params['mac_address'];
				$wo_newparams['port_id'] = $port_id;
				$wo_newparams['port_ip_address'] = $port_ip_address;
				$wo_newparams['port_status'] = $port_status;
				$wo_newparams['port_mac_address'] = $mac_address;
				$response = prepare_json_response(ENDED, "Port Id : $port_id", $wo_newparams, true);
				return $response;
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
function get_subnet_details_from_network ($openstack_device_id, $network, $ip_address, $subnets_and_networks) {

	$networks_objname = "networks";
	$subnets_objname = "subnets";
	$subnets = $subnets_and_networks[$networks_objname][$network]['subnet_list'];
	$subnets_count = count($subnets);

	$wo_newparams = array();
	$wo_comment = "";
	for ($i = 0; $i < $subnets_count; $i++) {
		$subnet = $subnets[$i]['subnet_id'];
		$cidr = $subnets_and_networks[$subnets_objname][$subnet]['cidr'];
		if (cidr_match($ip_address, $cidr)) {
			$response_subnet_and_mask = cidr_to_subnet_and_subnetmask_address($cidr);
			$subnet_gateway_ip = $subnets_and_networks[$subnets_objname][$subnet]['gateway_ip'];
			$wo_newparams['subnet_id'] = $subnet;
			$wo_newparams['subnet_ip'] = $response_subnet_and_mask['subnet_ip'];
			$wo_newparams['subnet_mask'] = $response_subnet_and_mask['subnet_mask'];
			$wo_newparams['subnet_gateway_ip'] = $subnet_gateway_ip;
			$wo_comment .= "Subnet Id : " . $wo_newparams['subnet_id'] . "\n";
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
 * Get a Free Floating IP address from the Network
 *
 * @param unknown $openstack_device_id
 * @param unknown $network
 * @param unknown $tenant
 * @return unknown
 */
function get_free_floatingip ($openstack_device_id, $network, $tenant) {

	$floatingip_objname = "floatingips";
	$array = array($floatingip_objname);
	$response = import_objects($openstack_device_id, $array);
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$floatingips = $response['wo_newparams'][$floatingip_objname];

	$wo_newparams = array();
	$wo_comment = "";
	foreach ($floatingips as $floatingip_object_id => $floatingip_params) {

		$floatingip_id = $floatingip_params['object_id'];
		$floatingip_address = $floatingip_params['floating_ip_address'];
		$floatingip_network = $floatingip_params['floating_network_id'];
		$floatingip_tenant = $floatingip_params['tenant_id'];
		if ((!array_key_exists('fixed_ip_address', $floatingip_params) ||
				!array_key_exists('port_id', $floatingip_params)) &&
				$floatingip_network === $network && $floatingip_tenant === $tenant) {

					$wo_newparams['floating_ip_address'] = $floatingip_address;
					$wo_newparams['floating_ip_id'] = $floatingip_id;
					$wo_comment .= "Floating IP Id : $floatingip_id\n";
					$wo_comment .= "Floating IP Address : $floatingip_address";
					$response = prepare_json_response(ENDED, $wo_comment, $wo_newparams, true);
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
function allocate_floatingip_address ($openstack_device_id, $network, $tenant) {

	$response = get_free_floatingip($openstack_device_id, $network, $tenant);
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
	$response = _neutron_floatingip_create($openstack_device_id, $network, $tenant);
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = get_free_floatingip($openstack_device_id, $network, $tenant);
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = json_encode($response);
	return $response;
}

function _nova_server_action ($device_id, $server, $action, $arg1 = "", $arg2 = "", $arg3 = "") {

    $array = array();
    $array['action'] = 'Server Action';
    $array['server_action'] = $action;
    if ($arg1 !== "") {
        $array['action_arg1'] = $arg1;
    }
    if ($arg2 !== "") {
        $array['action_arg2'] = $arg2;
    }
    if ($arg3 !== "") {
        $array['action_arg3'] = $arg3;
    }

    $array = array('servers' => array($server => $array));
    $response = execute_command_and_verify_response($device_id, CMD_UPDATE, $array, "SERVER ACTION : $action");
    return $response;
}

?>

