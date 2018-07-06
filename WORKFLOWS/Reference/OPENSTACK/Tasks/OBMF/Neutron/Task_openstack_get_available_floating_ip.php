<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/OPENSTACK/Library/OBMF/openstack_common_obmf.php';

function list_args()
{
	create_var_def('openstack_device_id', 'Device');
	create_var_def('floating_ip_network', 'OBMFRef');
	create_var_def('tenant', 'OBMFRef');
}

check_mandatory_param('openstack_device_id');
check_mandatory_param('floating_ip_network');
check_mandatory_param('tenant');

$openstack_device_id = substr($context['openstack_device_id'], 3);
$floating_ip_network = $context['floating_ip_network'];
$floating_ip_tenant = $context['tenant'];

$response = allocate_floatingip_address($openstack_device_id, $floating_ip_network, $floating_ip_tenant);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}

$context = $response['wo_newparams'];
$response = prepare_json_response(ENDED, $response['wo_comment'], $context, true);
echo $response;

?>