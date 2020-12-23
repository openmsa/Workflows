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
$serv_id=$context['sdwan_wf_id'];
$ubiqube_id=$context['UBIQUBEID'];
$process_name="Process/ENEA/VNF_Management/Process_Terminate_VNF";
_orchestration_launch_process_instance ($ubiqube_id, $serv_id, $process_name, "{}");
$process_name="Process/ENEA/VNF_Management/Process_Move_to_Trash";
_orchestration_launch_process_instance ($ubiqube_id, $serv_id, $process_name, "{}");

task_success('Task OK');
?>