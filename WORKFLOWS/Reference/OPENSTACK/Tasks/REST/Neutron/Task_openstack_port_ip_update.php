<?php 

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/OPENSTACK/Library/REST/openstack_common_rest.php';

function list_args()
{
}

check_mandatory_param('ip_address');
check_mandatory_param('port_id');
check_mandatory_param('subnet_id');

$ip_address = $context['ip_address'];
$port_id = $context['port_id'];
$subnet_id = $context['subnet_id'];
$token_id = $context['token_id'];
$endpoints = $context['endpoints'];
$neutron_endpoint = $endpoints[NEUTRON]['endpoints'][0][ADMIN_URL];
	
$fixed_ips = array(array('subnet_id' => $subnet_id, 'ip_address' => $ip_address));
$response = _neutron_port_update_fixed_ips($neutron_endpoint, $token_id, $port_id, $fixed_ips);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}
	
$response = prepare_json_response(ENDED, "Port IP $ip_address updated sucessfully on Port $port_id on Openstack.", $context, true);
echo $response;

?>