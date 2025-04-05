<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/PALOALTO/Library/constants.php';

function _paloalto_generic_antivirus_user_profile ($device_id, $command_name, $profile_name,
									$decoder, $packet_capture = "no", $description = "") {

	$array = array('antivirus_user_profile' =>
				array($profile_name =>
					array('decoder' => $decoder,
							'packet_capture' => $packet_capture,
							'description' => $description
					)
				)
			);
	$response = execute_command_and_verify_response($device_id, $command_name, $array, "CREATE ANTI-VIRUS USER PROFILE", 180, 180);
	return $response;
}
function _paloalto_generic_url_filtering_user_profile ($device_id, $command_name, $profile_name,
										$license_expired = "", $enable_container_page = "no",
										$dynamic_url = "no", $log_container_page_only = "yes",
										$alert = array(), $allow = array(), $block = array(),
										$continue = array(), $override = array(),
										$allow_list = array(), $block_list = array(),
										$action = "block", $description = "") {

	$url_filterting_user_profile_array = array();
	$url_filterting_user_profile_array['licence_expired'] = $license_expired;
	$url_filterting_user_profile_array['enable_container_page'] = $enable_container_page;
	$url_filterting_user_profile_array['log_container_page_only'] = $log_container_page_only;
	$url_filterting_user_profile_array['dynamic_url'] = $dynamic_url;
	$url_filterting_user_profile_array['action'] = $action;
	$url_filterting_user_profile_array['description'] = $description;
	if (!empty($alert)) {
		$url_filterting_user_profile_array['alert'] = $alert;
	}
	if (!empty($allow)) {
		$url_filterting_user_profile_array['allow'] = $allow;
	}
	if (!empty($block)) {
		$url_filterting_user_profile_array['block'] = $block;
	}
	if (!empty($continue)) {
		$url_filterting_user_profile_array['continue'] = $continue;
	}
	if (!empty($override)) {
		$url_filterting_user_profile_array['override'] = $override;
	}
	if (!empty($allow_list)) {
		$url_filterting_user_profile_array['allow_list'] = $allow_list;
	}
	if (!empty($block_list)) {
		$url_filterting_user_profile_array['block_list'] = $block_list;
	}

	$array = array('urlf_user_profile' =>
				array($profile_name => $url_filterting_user_profile_array
				)
			);
	$response = execute_command_and_verify_response($device_id, $command_name, $array, "CREATE URL-FILTERING USER PROFILE", 180, 180);
	return $response;
}
function _paloalto_generic_profile_group ($device_id, $command_name, $profile_group_name, $anti_virus,
						$anti_spyware, $vulnerability, $wildfire_analysis,
						$url_filtering, $file_blocking, $data_filtering) {

	$array = array('profile_group' =>
				array($profile_group_name =>
					array('virus' => $anti_virus,
							'spyware' => $anti_spyware,
							'vulnerability' => $vulnerability,
							'wildfire_analysis' => $wildfire_analysis,
							'url_filtering' => $url_filtering,
							'file_blocking' => $file_blocking,
							'data_filtering' => $data_filtering
					)
				)
			);
	$response = execute_command_and_verify_response($device_id, $command_name, $array, "CREATE PROFILE GROUP", 180, 180);
	return $response;
}
function _paloalto_generic_address_ip_netmask ($device_id, $command_name, $name,
								$address, $masklen) {

	$array = array('address_ip_netmask' =>
				array($name =>
					array('address' => $address,
							'masklen' => $masklen
					)
				)
			);
	$response = execute_command_and_verify_response($device_id, $command_name, $array, "CREATE IP NETMASK", 180, 180);
	return $response;
}
function _paloalto_generic_address_ip_range ($device_id, $command_name, $name,
							$start_address, $end_address) {

	$array = array('address_ip_range' =>
				array($name =>
					array('startaddress' => $start_address,
							'endaddress' => $end_address
					)
				)
			);
	$response = execute_command_and_verify_response($device_id, $command_name, $array, "CREATE IP RANGE", 180, 180);
	return $response;
}
function _paloalto_generic_address_group ($device_id, $command_name, $address_group_name, $address_group_type,
							$filter = "", $addresses = array()) {

	$address_group_array = array();
	$address_group_array['type'] = $address_group_type;
	if ($address_group_type === "dynamic") {
		$address_group_array['filter'] = $filter;
	}
	else if ($address_group_type === "static") {
		$address_group_array['addresses'] = $addresses;
	}

	$array = array('address_group' =>
				array($address_group_name => $address_group_array
					)
				);
	$response = execute_command_and_verify_response($device_id, $command_name, $array, "CREATE ADDRESS GROUP", 180, 180);
	return $response;
}
function _paloalto_generic_security_policy ($device_id, $command_name, $name,
							$zone_from, $src_address, $zone_to, $dst_address,
							$services, $action = "allow", $applications = array(),
							$users = array(), $categories = array(),
							$hip_profiles = array(), $profile_group = "",
							$schedule = "", $log_start = "no", $log_end = "yes") {

	$security_policy_array = array();
	$security_policy_array['zone_from'] = $zone_from;
	$security_policy_array['zone_to'] = $zone_to;
	$security_policy_array['src_address'] = $src_address;
	$security_policy_array['dst_address'] = $dst_address;
	$security_policy_array['services'] = $services;
	$security_policy_array['action'] = $action;

	if ($profile_group !== "") {
		$security_policy_array['profile_group'] = $profile_group;
	}
	if ($schedule !== "") {
		$security_policy_array['schedule'] = $schedule;
	}
	if ($log_start !== "") {
		$security_policy_array['log_start'] = $log_start;
	}
	if ($log_end !== "") {
		$security_policy_array['log_end'] = $log_end;
	}
	if (!empty($applications)) {
		$security_policy_array['application'] = $applications;
	}
	if (!empty($users)) {
		$security_policy_array['users'] = $users;
	}
	if (!empty($categories)) {
		$security_policy_array['categories'] = $categories;
	}
	if (!empty($hip_profiles)) {
		$security_policy_array['hip_profile'] = $hip_profiles;
	}

	$array = array('policy_app' =>
				array($name => $security_policy_array
			)
		);
	$response = execute_command_and_verify_response($device_id, $command_name, $array, "CREATE SECURITY POLICY", 180, 180);
	return $response;
}
function _paloalto_generic_vpn_phase1 ($device_id, $command_name, $name, $lifetime,
						$encryption = array(), $hash = array(), $dhgroup = array(),
						$lifetime_unit = "") {

	$array = array('Phase1' =>
				array($name =>
					array('encryption' => $encryption,
							'hash' => $hash,
							'dhgroup' => $dhgroup,
							'lifetime' => $lifetime,
							'lifetime_unit' => $lifetime_unit
						)
					)
				);
	$response = execute_command_and_verify_response($device_id, $command_name, $array, "CREATE VPN PHASE-1", 180, 180);
	return $response;
}
function _paloalto_generic_antivirus_service ($device_id, $command_name, $av_service_name,
							$av_profile, $policy) {

	$array = array('antivirus_service' =>
				array($av_service_name =>
					array('av_profile' => $av_profile,
							'policy' => $policy
					)
				)
			);
	$response = execute_command_and_verify_response($device_id, $command_name, $array, "CREATE ANTI-VIRUS SERVICE", 180, 180);
	return $response;
}

//{"dns_servers":{"":{"primary":"6.6.6.6","secondary":"4.4.4.4"}}}
function _paloalto_generic_dns_servers ($device_id, $command_name, $primary = "", $secondary = "") {

	$dns_servers_array = array();
	if ($primary !== "") {
		$dns_servers_array['primary'] = $primary;
	}
	if ($secondary !== "") {
		$dns_servers_array['secondary'] = $secondary;
	}

	if ($primary !== "" || $secondary !== "") {
		$array = array('dns_servers' =>
					array("" => $dns_servers_array)
					);
	}
	else {
		$array = array('dns_servers' => "");
	}
	$response = execute_command_and_verify_response($device_id, $command_name, $array, "SET DNS SERVERS", 180, 180);
	return $response;
}
// {"license":{"":{"auth_code":"xyz"}}}
function _paloalto_generic_license ($device_id, $command_name, $auth_code = "") {

	$license_array = array();
	if ($auth_code !== "") {
		$license_array['auth_code'] = $auth_code;
		$array = array('license' =>
					array("" => $license_array)
				);
	}
	else {
		$array = array('license' => "");
	}
	$response = execute_command_and_verify_response($device_id, $command_name, $array, "SET LICENSE", 180, 180);
	return $response;
}

function _paloalto_generic_ethernet ($device_id, $command_name, $ethernet_name, $interface_type) {

	$array = array('ethernet' =>
				array($ethernet_name =>
					array('interface_type' => $interface_type
					)
				)
			);
	$response = execute_command_and_verify_response($device_id, $command_name, $array, "CREATE $interface_type INTERFACE", 180, 180);
	return $response;
}
function _paloalto_generic_eth_tag ($device_id, $command_name, $ethernet_name, $subinterfaces) {

	$array = array('eth_tag' =>
				array($ethernet_name =>
					array('vwireinterface' => $subinterfaces
					)
				)
			);
	$response = execute_command_and_verify_response($device_id, $command_name, $array, "CREATE VIRTUAL-WIRE SUB-INTERFACE", 180, 180);
	return $response;
}
function _paloalto_generic_virtual_wire ($device_id, $command_name, $vwire_name, $interface1, $interface2,
						$tag_allowed = "", $multicast_firewalling = "",
						$link_state_pass_through = "") {

	$array = array('vwire' =>
				array($vwire_name =>
					array('interface1' => $interface1,
							'interface2' => $interface2,
							'tag_allowed' => $tag_allowed,
							'multicast_firewalling' => $multicast_firewalling,
							'link_state_pass_through' => $link_state_pass_through
						)
					)
			);
	$response = execute_command_and_verify_response($device_id, $command_name, $array, "CREATE VIRTUAL-WIRE", 180, 180);
	return $response;
}
function _paloalto_generic_zone ($device_id, $command_name, $zone_name, $zone_type, $zone_members) {

	$array = array('zone' =>
				array($zone_name =>
					array('zone_type' => $zone_type,
							'members' => $zone_members
					)
				)
			);
	$response = execute_command_and_verify_response($device_id, $command_name, $array, "CREATE ZONE", 180, 180);
	return $response;
}

function _paloalto_generic_dhcp_client ($device_id, $command_name, $send_hostname = "no",
										$accept_dhcp_domain = "no", $send_client_id = "no", 
										$accept_dhcp_hostname = "no") {

	$array = array('dhcp_client' =>
				array("" =>
					array('send_hostname' => $send_hostname,
							'accept_dhcp_domain' => $accept_dhcp_domain,
							'send_client_id' => $send_client_id,
							'accept_dhcp_hostname' => $accept_dhcp_hostname
					)
			)
	);
	$response = execute_command_and_verify_response($device_id, $command_name, $array, "CREATE DHCP-CLIENT", 180, 180);
	return $response;
}


?>