<?php 

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/OPENSTACK/Library/constants.php';

function _nova_server_create ($device_id, $server_name, $networks,
							$availability_zone = "", $flavor, $image,
							$security_groups = array(), $key = "",
							$user_data = "", $personality = array(), $config_drive="false") {

	$server_array = array();
	$server_array['name'] = $server_name;
	$server_array['networks'] = $networks;
	$server_array['flavor_id'] = $flavor;
	$server_array['image_id'] = $image;
	$server_array['key'] = $key;
	$server_array['config_drive'] = $config_drive;
	$server_array['user_data'] = $user_data;
	if ($availability_zone !== "") {
		$array['availability_zone'] = $availability_zone;
	}
	if (!empty($security_groups)) {
		$server_array['security_groups'] = $security_groups;
	}
	if (!empty($personality)) {
		$server_array['personality'] = $personality;
	}

	$array = array("servers" => array("" => $server_array));
	$response = execute_command_and_verify_response($device_id, CMD_CREATE, $array, "SERVER CREATE");
	return $response;
}

function _nova_server_delete ($device_id, $server) {

        $server_array = array();
        $array = array("servers" => array($server => $server_array));
	$response = execute_command_and_verify_response($device_id, CMD_DELETE, $array, "SERVER DELETE");
	return $response;
}

function _nova_floating_ip_associate ($device_id, $server, $floating_ip_id, $fixed_address = "", $image_id ="", $flavor_id ="") {

	$floatingip_array = array();
	$floatingip_array['action_arg1'] = $floating_ip_id;
	$floatingip_array['action'] = 'Server Action';
	$floatingip_array['server_action'] = 'Add Floating IP Address';
	if ($fixed_address !== "") {
		$floatingip_array['action_arg2'] = $fixed_address;
	}
	$floatingip_array['image_id'] = $image_id;
	$floatingip_array['flavor_id'] = $flavor_id;

	$array = array('servers' => array($server => $floatingip_array));

	$response = execute_command_and_verify_response($device_id, CMD_UPDATE, $array, "SERVER FLOATING-IP ASSOCIATE");
	return $response;
}

?>
