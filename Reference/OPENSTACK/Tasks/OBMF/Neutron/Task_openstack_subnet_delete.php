<?php
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

// List all the parameters required by the task
function list_args()
{
  create_var_def('openstack_device_id', 'Device');
  create_var_def('subnet_id', 'String');
}

if (empty($context['subnet_id'])) {
	$ret = prepare_json_response(WARNING, "Subnet Id not available to delete the Subnet", $context, true);
	echo "$ret\n";
	exit;
}

$device_id = substr($context['openstack_device_id'], 3);
$subnet_id = $context['subnet_id'];
$response = msa_object_delete($device_id, "subnets", $subnet_id);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}

$ret = prepare_json_response(ENDED, "Subnet $subnet_id deleted successfully", $context, true);
echo "$ret\n";
?>