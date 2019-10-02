<?php
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/OPENSTACK/Library/OBMF/openstack_common_obmf.php';

// List all the parameters required by the task
function list_args()
{
  create_var_def('openstack_device_id', 'Device');
  create_var_def('subnet_name', 'String');
  create_var_def('network_id', 'String');
  create_var_def('tenant_id', 'OBMFRef');
  create_var_def('enable_dhcp', 'Boolean');
  create_var_def('cidr', 'String');
  create_var_def('ip_version', 'String');
  create_var_def('gateway_ip', 'IpAddress');
  create_var_def('allocation_pools.0.start', 'String');
  create_var_def('allocation_pools.0.end', 'String');
}

$device_id = substr($context['openstack_device_id'], 3);
$name = $context['subnet_name'];
$network_id = $context['network_id'];
$tenant_id = $context['tenant_id'];
$cidr = $context['cidr'];
$ip_version = $context['ip_version'];
$gateway_ip = $context['gateway_ip'];
$enable_dhcp = $context['enable_dhcp'];
$allocation_pools = array();
if (!empty($context['allocation_pools'])) {
  $allocation_pools = $context['allocation_pools'];
}

$response = _neutron_subnet_create($device_id, $name, $network_id, $tenant_id, $cidr, $ip_version, $gateway_ip, $enable_dhcp, $allocation_pools);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}

$response = get_object_id_from_name($device_id, "subnets", "name", $name);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}
$subnet_id = $response['wo_newparams']['object_id'];
$context['subnet_id'] = $subnet_id;

$ret = prepare_json_response(ENDED, "Subnet Created Successfully.\nSubnet Id : $subnet_id", $context, true);
echo "$ret\n";
?>