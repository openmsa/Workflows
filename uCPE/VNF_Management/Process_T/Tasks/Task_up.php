<?php

/**
 * This file is necessary to include to use all the in-built libraries of /opt/fmc_repository/Reference/Common
 */
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

/**
 * List all the parameters required by the task
 */
function list_args()
{
  
}

//$context["SERVICEINSTANCEREFERENCE"] = $context["vnf_name"];
$response = _orchestration_update_service_instance_reference ($context['UBIQUBEID'], $context['service_id'], $context['vnf_name']);

logToFile(debug_dump($response,"===============service instance ref update================"));
task_success('Task OK');
?>