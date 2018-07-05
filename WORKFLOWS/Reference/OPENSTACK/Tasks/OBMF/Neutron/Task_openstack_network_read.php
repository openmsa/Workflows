<?php
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

// List all the parameters required by the task
function list_args()
{
  create_var_def('openstack_device_id', 'Device');
  create_var_def('network_id', 'String');
}

if (empty($context['network_id'])) {
	$ret = prepare_json_response(WARNING, "Network Id not available to Import the Network", $context, true);
	echo "$ret\n";
	exit;
}

$device_id = substr($context['openstack_device_id'], 3);
$network_id = $context['network_id'];
$response = import_objects($device_id, array("networks"));
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
   	exit;
}
$network_details = $response['wo_newparams']['networks'][$network_id];
$network_details = json_encode($network_details);

$ret = prepare_json_response(ENDED, "Network details :\n$network_details", $context, true);
echo "$ret\n";
?>