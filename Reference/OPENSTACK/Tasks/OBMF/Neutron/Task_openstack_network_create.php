<?php
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/OPENSTACK/Library/OBMF/openstack_common_obmf.php';

// List all the parameters required by the task
function list_args()
{
  create_var_def('openstack_device_id', 'Device');
  create_var_def('network_name', 'String');
  create_var_def('network_type', 'String');
  create_var_def('tenant_id', 'OBMFRef');
  create_var_def('admin_state_up', 'Boolean');
  create_var_def('router_external', 'Boolean');
  create_var_def('port_security_enabled', 'Boolean');
  create_var_def('shared', 'Boolean');
  create_var_def('segmentation_id', 'String');
  create_var_def('physical_network', 'String');
}

$device_id = substr($context['openstack_device_id'], 3);
$name = $context['network_name'];
$network_type = $context['network_type'];
$tenant_id = $context['tenant_id'];
$admin_state_up = $context['admin_state_up'];
$router_external = $context['router_external'];
$port_security_enabled = $context['port_security_enabled'];
$shared = $context['shared'];
$segmentation_id = $context['segmentation_id'];
$physical_network = $context['physical_network'];

$response = _neutron_network_create($device_id, $name, $tenant_id, $admin_state_up, $router_external, $port_security_enabled, $shared, $network_type, $segmentation_id, $physical_network);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}

$response = get_object_id_from_name($device_id, "networks", "name", $name);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}
$network_id = $response['wo_newparams']['object_id'];
$context['network_id'] = $network_id;

$ret = prepare_json_response(ENDED, "Network Created Successfully.\nNetwork Id : $network_id", $context, true);
echo "$ret\n";
?>