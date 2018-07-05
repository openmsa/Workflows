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

?>