<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/OPENSTACK/Library/REST/openstack_common_rest.php';

function list_args()
{
  create_var_def('console_type', 'String');
}

check_mandatory_param('server_id');
check_mandatory_param('console_type');

$server_id = $context['server_id'];
$console_type = $context['console_type'];
$token_id = $context['token_id'];
$endpoints = $context['endpoints'];
$nova_endpoint = $endpoints[NOVA]['endpoints'][0][ADMIN_URL];

$response = _nova_get_vnc_console($nova_endpoint, $token_id, $server_id, $console_type);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}

$context['console_url'] = $response['wo_newparams']['console']['url'];

$response = prepare_json_response(ENDED, "VM $console_type console URL :\n" . $context['console_url'], $context, true);
echo $response;

?>