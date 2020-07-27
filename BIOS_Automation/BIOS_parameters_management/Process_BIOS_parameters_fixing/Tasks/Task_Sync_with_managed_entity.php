<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/Common/Library/msa_common.php';

//Retrive variables from $context and define the new ones
$device_id = $context['device_id'];
$microservices_array = $context['microservices_array'];

//Sync microservices
$response = json_decode(synchronize_objects_and_verify_response($device_id), true);
if ($response['wo_status'] !== ENDED) {
        $response = json_encode($response);
        echo $response;
        exit;
}

$response = json_decode(_device_read_by_id($device_id), True);
if ($response['wo_status'] !== ENDED) {
        $response = json_encode($response);
        echo $response;
        exit;
}

task_success('Managed entity has been synced sucessfully.');

?>