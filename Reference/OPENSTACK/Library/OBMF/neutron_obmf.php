<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/OPENSTACK/Library/constants.php';

function _neutron_disable_port_security ($device_id, $port_id) {

	$array = array("ports" =>
				array($port_id =>
					array('port_security_enabled' => "false",
							'security_groups' => array()
					)
				)
			);
	$response = execute_command_and_verify_response($device_id, CMD_UPDATE, $array, "DISABLE PORT SECURITY");
	return $response;
}

function _neutron_floatingip_create ($device_id, $floatingip_network, $tenant = "", $floatingip_address = "", 
							$fixed_ip_address = "", $port_id = "") {

	$floatingip_array = array();
	$floatingip_array['floating_network_id'] = $floatingip_network;
	if ($floatingip_address !== "") {
		$floatingip_array['floating_ip_address'] = $floatingip_address;
	}
	if ($fixed_ip_address !== "") {
		$floatingip_array['fixed_ip_address'] = $fixed_ip_address;
	}
	if ($port_id !== "") {
		$floatingip_array['port_id'] = $port_id;
	}
	if ($tenant !== "") {
		$floatingip_array['tenant_id'] = $tenant;
	}

	$array = array("floatingips" => array("" => $floatingip_array));
	$response = execute_command_and_verify_response($device_id, CMD_CREATE, $array, "FLOATING-IP CREATE");
	return $response;
}

function _neutron_router_create ($device_id, $name, $admin_state_up, $external_network) {

        $floatingip_array = array();
        $floatingip_array['name'] = $name;
        $floatingip_array['admin_state_up'] = $admin_state_up;
        $floatingip_array['network_id'] = $external_network;
        //$floatingip_array['destination'] = false;
        //$floatingip_array['ha'] = false;

        $array = array("routers" =>
                                array("" => $floatingip_array));
        $response = execute_command_and_verify_response($device_id, CMD_CREATE, $array, "ROUTER CREATE");
        return $response;
}

function _neutron_router_interface_update ($device_id, $router_id, $subnet_id, $router_interface_action = "Add Router Interface", $router_action = "Router Action") {

        $router_array = array();
        $router_array['router_action'] = $router_action;
        $router_array['router_interface_action'] = $router_interface_action;
        $router_array['subnet'] = $subnet_id;

        $array = array("routers" =>
                                array($router_id => $router_array));
        $response = execute_command_and_verify_response($device_id, CMD_UPDATE, $array, "ROUTER UPDATE");
        return $response;
}


/*
{"networks":{{"mtu":"","shared":"false","port_security_enabled":"false","network_type":"vxlan","status":"","object_id":"","segmentation_id":"","tenant_id":"5b57e85c3a4e4cc3ae81ea2a503e1d6e","physical_network":"","admin_state_up":"true","name":"test_network","router_external":"false"}}}
*/
function _neutron_network_create ($device_id, $name, $tenant_id, $admin_state_up = "true", $router_external = "false", $port_security_enabled = "false", $shared = "false", $network_type = "", $segmentation_id = "", $physical_network = "") {

 $network_array = array();
 $network_array['name'] = $name;
 $network_array['tenant_id'] = $tenant_id;
 $network_array['admin_state_up'] = $admin_state_up;
 $network_array['router_external'] = $router_external;
 $network_array['port_security_enabled'] = $port_security_enabled;
 $network_array['shared'] = $shared;
 if ($network_type !== "") {
    $network_array['network_type'] = $network_type;
 }
 if ($segmentation_id !== "") {
    $network_array['segmentation_id'] = $segmentation_id;
 }
 if ($physical_network !== "") {
    $network_array['physical_network'] = $physical_network;
 }

$array = array("networks" => array("" => $network_array));
$response = execute_command_and_verify_response($device_id, CMD_CREATE, $array, "NETWORK CREATE");
return $response;
}

function _neutron_network_update ($device_id, $network_id, $name, $admin_state_up = "true", $router_external = "false", $port_security_enabled = "false", $shared = "false") {

 $network_array = array();
 $network_array['name'] = $name;
 $network_array['admin_state_up'] = $admin_state_up;
 $network_array['router_external'] = $router_external;
 $network_array['port_security_enabled'] = $port_security_enabled;
 $network_array['shared'] = $shared;

$array = array("networks" => array($network_id => $network_array));
$response = execute_command_and_verify_response($device_id, CMD_UPDATE, $array, "NETWORK UPDATE");
return $response;
}

function _neutron_subnet_create ($device_id, $name, $network_id, $tenant_id, $cidr, $ip_version = 4, $gateway_ip = "", $enable_dhcp = "true", $allocation_pools = array()) {

 $subnet_array = array();
 $subnet_array['name'] = $name;
 $subnet_array['network_id'] = $network_id;
 $subnet_array['tenant_id'] = $tenant_id;
 $subnet_array['cidr'] = $cidr;
 $subnet_array['ip_version'] = $ip_version;
 $subnet_array['enable_dhcp'] = $enable_dhcp;
 if ($gateway_ip !== "") {
   $subnet_array['gateway_ip'] = $gateway_ip;
 }
 if (!empty($allocation_pools)) {
   $subnet_array['allocation_pools'] = $allocation_pools;
 }
 $array = array("subnets" => array("" => $subnet_array));
 $response = execute_command_and_verify_response($device_id, CMD_CREATE, $array, "SUBNET CREATE");
 return $response;
}

function _neutron_subnet_update ($device_id, $subnet_id, $name, $gateway_ip = "", $enable_dhcp = "true", $allocation_pools = array()) {

 $subnet_array = array();
 $subnet_array['name'] = $name;
 $subnet_array['enable_dhcp'] = $enable_dhcp;
 if ($gateway_ip !== "") {
   $subnet_array['gateway_ip'] = $gateway_ip;
 }
 else {
   $subnet_array['gateway_ip'] = null;
 }
 if (!empty($allocation_pools)) {
   $subnet_array['allocation_pools'] = $allocation_pools;
 }
 $array = array("subnets" => array($subnet_id => $subnet_array));
 $response = execute_command_and_verify_response($device_id, CMD_UPDATE, $array, "SUBNET UPDATE");
 return $response;
}

/**
* Create subnetwork port
**/
function _neutron_port_create ($device_id, $name, $tenant_id, $network_id, $subnet_id, $fixed_ip, $admin_state_up = "true", $port_security_enabled = "false") {

	$port = array();
	$port['name'] = $name;
	$port['tenant_id'] = $tenant_id;
	$port['network_id'] = $network_id;
	$port['admin_state_up'] = $admin_state_up;
	$port['port_security_enabled'] = $port_security_enabled;
	$port['fixed_ips'][] = array("subnet_id" => $subnet_id, "ip_address" => $fixed_ip);

	$array = array("ports" => array("" => $port));
	$response = execute_command_and_verify_response($device_id, CMD_CREATE, $array, "PORT CREATE");
	return $response;
}


?>
