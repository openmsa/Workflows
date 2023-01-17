<?php 

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args()
{
  create_var_def('DeviceId', 'Device');
}

check_mandatory_param('DeviceId');

$device_id = substr($context['DeviceId'], 3);

$response = _device_configuration_list_files_by_id ($device_id);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
    $response = prepare_json_response(FAILED, $response['wo_comment'], $context, true);
    echo $response;
    exit;
}
$context['device_objects_uri'] = $response['wo_newparams'];
$context['device_id'] = $device_id;

$response = prepare_json_response(ENDED, "Files Attached to Device listed Successfully", $context, true);
echo $response;

?>