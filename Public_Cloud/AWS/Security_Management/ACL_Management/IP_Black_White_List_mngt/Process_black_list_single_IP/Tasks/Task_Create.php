<?php
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args()
{
	create_var_def('device_id', 'Device');
	create_var_def('network_acl_id', 'OBMFRef');
	create_var_def('default', 'Boolean');
	create_var_def('entries.0.rule_number', 'Integer');
	create_var_def('entries.0.egress', 'Boolean');
	create_var_def('entries.0.protocol', 'String');
	create_var_def('entries.0.port_range_from', 'Composite');
	create_var_def('entries.0.port_range_to', 'Composite');
	create_var_def('entries.0.cidr_block', 'String');
	create_var_def('entries.0.rule_action', 'String');
}

check_mandatory_param('device_id');
check_mandatory_param('network_acl_id');
check_mandatory_param('entries');

$device_id = substr($context['device_id'], 3);
$object_id = $context['object_id'];
$micro_service_vars_array = array();
$micro_service_vars_array['network_acl_id'] = $context['network_acl_id'];
$micro_service_vars_array['default'] = $context['default'];
$micro_service_vars_array['entries'] = $context['entries'];

$network_acl_entry = array('network_acl_entry' => array($object_id => $micro_service_vars_array));

$response = execute_command_and_verify_response($device_id, CMD_CREATE, $network_acl_entry, "CREATE network_acl_entry");
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = prepare_json_response($response['wo_status'], $response['wo_comment'], $context, true);
	echo $response;
	exit;
}

$response = prepare_json_response(ENDED, "network_acl_entry $object_id created successfully on the Device $device_id.", $context, true);
echo $response;
?>
