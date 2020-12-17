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
$process_name="Process/Network_Resources/Free";
$service_id=$context['nw_id'];
$ubiqube_id=$context['UBIQUBEID'];
 _orchestration_launch_process_instance ($ubiqube_id, $service_id, $process_name, "{}");

task_success('Access Resources Freed');
?>