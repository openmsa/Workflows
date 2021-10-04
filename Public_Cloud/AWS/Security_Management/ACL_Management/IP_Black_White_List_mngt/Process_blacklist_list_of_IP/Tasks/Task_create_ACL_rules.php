<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args()
{
 
}


$ip_list = $context['ip_list'];

$counter=100;
foreach ($ip_list as $ip){
    logToFile('ip :' . $ip);


$device_id = substr($context['aws_region'], 3);

$entries = array("rule_number" => $counter,
                 "egress" => "false",
		 "protocol" => "-1",
                 "port_range_from" => "",
 		 "port_range_to" => "",
		 "cidr_block" => $ip."/32",
		 "rule_action" => "deny");


$micro_service_vars_array = array();
$micro_service_vars_array['network_acl_id'] = $context['network_acl_id'];
$micro_service_vars_array['default'] = $context['default'];
$micro_service_vars_array['entries'] = array('0' => $entries);

$network_acl_entry = array('network_acl_entry' => array('0' => $micro_service_vars_array));

$response = execute_command_and_verify_response($device_id, CMD_CREATE, $network_acl_entry, "CREATE network_acl_entry");
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = prepare_json_response($response['wo_status'], $response['wo_comment'], $context, true);
	echo $response;
	exit;
}

$response = prepare_json_response(ENDED, "network_acl_entry created successfully on the Device $device_id.", $context, true);

$counter++;
}



task_success('Task OK');

?>