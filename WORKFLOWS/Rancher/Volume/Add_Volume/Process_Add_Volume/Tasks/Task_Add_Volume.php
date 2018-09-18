<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/RANCHER/CMP/Library/REST/rancher_common_rest.php';

function list_args()
{
  create_var_def('volume_name', 'String');
  create_var_def('volume_size_mb', 'Integer');
  create_var_def('volume_driver', 'String');
  create_var_def('volume_host_id', 'String');
  create_var_def('volume_stack_id', 'String');
}

check_mandatory_param('volume_name');

$volume_name = $context['volume_name'];

$volume_size_mb = "";
if (!empty($context['volume_size_mb'])) {
	$volume_size_mb = $context['volume_size_mb'];
}
$volume_driver = "";
if (!empty($context['volume_driver'])) {
	$volume_driver = $context['volume_driver'];
}
$volume_host_id = "";
if (!empty($context['volume_host_id'])) {
	$volume_host_id = $context['volume_host_id'];
}
$volume_stack_id = "";
if (!empty($context['volume_stack_id'])) {
	$volume_stack_id = $context['volume_stack_id'];
}

$response = _rancher_volume_configure ($context['rancher_project_id'], $volume_name, "", $volume_size_mb, $volume_driver, 
					$volume_host_id, $volume_stack_id);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	task_exit(FAILED, "Volume creation failed.\n" . $response['wo_comment']);
}

//$context['volume_id'] = $vm_id; 

task_exit(ENDED, "Volume created successfully.\nVolume Id : $volume_id");

?>
