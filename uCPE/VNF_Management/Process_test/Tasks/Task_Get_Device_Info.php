<?php
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/ENEA/VNF_Management/common.php';

function list_args()
{
	create_var_def('ucpe_devices', 'OMBFRef');
}

$device_id = substr($context['device_id'], 3);
$response = _obmf_get_object_variables($device_id, "devices", $context['ucpe_devices'] );
$response = json_decode($response, true);

if($response['wo_status'] !== ENDED)
{               
    $device_data = prepare_json_response($response['wo_status'], "Failed to get device data", $response, true);   
    echo $device_data;
    exit;
}
$device_data = $response['wo_newparams']['devices'][ $context['ucpe_devices']];

logToFile(debug_dump($device_data,"*********** Device data**************\n"));
$context['device_data'] = $device_data;

task_exit(ENDED, "Device data retreived");
?>