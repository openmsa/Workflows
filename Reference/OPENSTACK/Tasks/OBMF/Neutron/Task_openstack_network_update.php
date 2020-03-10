<?php
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/OPENSTACK/Library/OBMF/openstack_common_obmf.php';

// List all the parameters required by the task
function list_args()
{
  create_var_def('openstack_device_id', 'Device');
  create_var_def('network_name', 'String');
  create_var_def('admin_state_up', 'Boolean');
  create_var_def('router_external', 'Boolean');
  create_var_def('port_security_enabled', 'Boolean');
  create_var_def('shared', 'Boolean');
}

$device_id = substr($context['openstack_device_id'], 3);
$name = $context['network_name'];
$network_id = $context['network_id'];
$admin_state_up = $context['admin_state_up'];
$router_external = $context['router_external'];
$port_security_enabled = $context['port_security_enabled'];
$shared = $context['shared'];

$response = _neutron_network_update($device_id, $network_id, $name, $admin_state_up, $router_external, $port_security_enabled, $shared);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}

$ret = prepare_json_response(ENDED, "Network $network_id Updated Successfully.", $context, true);
echo "$ret\n";
?>