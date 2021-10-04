<?php

/**
* This file is necessary to include to use all the in-built libraries of /opt/fmc_repository/Reference/Common
*/
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args() {
}

logToFile(debug_dump($context, "******CONTEXT******"));

$external_ref = $context["customer_id"];
$service_reference = $context["SERVICEINSTANCEREFERENCE"];
$service_name = "Process/ENEA/VNF_Management/VNF_Master";
$process_name = "Process/ENEA/VNF_Management/Process_Deploy_VNFs";

_orchestration_execute_service_by_reference_using_parameters($external_ref, $service_reference, $service_name, $process_name, json_encode($context));

echo prepare_json_response(ENDED, "CALL SERVICE OK", $context, true);

?>