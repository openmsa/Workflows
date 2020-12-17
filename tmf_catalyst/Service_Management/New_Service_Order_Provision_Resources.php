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
if($context['isVpnRequest'] === 'No'){
  $process_name='Process/Access_Infra_Resources/Confirm_Allocation';
  $ubiqube_id=$context['UBIQUBEID'];
  $service_id=$context['LineId'];
  _orchestration_launch_process_instance ($ubiqube_id, $service_id, $process_name, $json_body = "{}");
  task_success('Access infra resource Provisioned');
}else{
  $process_name="Process/Network_Resources/Confirm_Allocation";
  $ubiqube_id=$context['UBIQUBEID'];
  $service_id=$context['nw_grp_id'];
  _orchestration_launch_process_instance ($ubiqube_id, $service_id, $process_name, $json_body = "{}");
  task_success('Access infra resource Provisioned');
}

?>