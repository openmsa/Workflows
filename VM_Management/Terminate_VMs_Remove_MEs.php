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
$vms=$context['vms'];
foreach($vms as $vm){
  $ms_params=array();
  $dev=$vm['device_id'];
  $response = _device_delete($dev);
  $response = json_decode($response, true);
  if ($response['wo_status'] !== ENDED) {
	$response['wo_status'] = WARNING;
	$response = json_encode($response);
	echo $response;
	exit;
  }
}

task_success('MEs Deleted');
?>