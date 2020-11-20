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
  create_var_def('vms.0.device_id', 'String');
}
$vms=$context['vms'];
foreach($vms as $vm){
  $device_id=$vm['device_id'];
  $device_id=getIdFromUbiId ($device_id);
  $uri = 'Configuration/LINUX/Generic/day0';
  $uris=array();
  $item=array();
  $item['uri']=$uri;
  array_push($uris,$item);
  $uris_array = array();
  $index = 0;
  foreach ($uris as $uri) {
	$uris_array[$index++] = $uri;
  }
  $position = 'PRE_CONFIG';
  $response = _device_configuration_attach_files_to_device($device_id, $uris_array, $position);
}

task_success("Files Attached successfully to the Device : $device_id");
?>