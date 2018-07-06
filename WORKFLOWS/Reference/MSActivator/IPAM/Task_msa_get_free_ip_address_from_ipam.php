<?php 

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args()
{
}

check_mandatory_param('subnet');
check_mandatory_param('netmask');

$subnet = $context['subnet'];
$netmask = $context['netmask'];
$response = _ipam_get_free_address($subnet, $netmask);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}
	
$context['ip_address'] = $response['wo_newparams'];
$response = prepare_json_response(ENDED, "IP address allocated successfully from MSA IPAM.\nIP address : " . $context['ip_address'], $context, true);
echo $response;

?>