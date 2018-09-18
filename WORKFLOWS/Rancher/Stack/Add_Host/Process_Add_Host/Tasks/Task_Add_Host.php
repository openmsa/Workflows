<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/RANCHER/CMP/Library/REST/rancher_common_rest.php';

function list_args()
{
  create_var_def('host_name', 'String');
  create_var_def('name', 'String');
}

check_mandatory_param('host_name');

$host_name = "";
if (!empty($context['host_name'])) {
	$host_name = $context['host_name'];
}
$name = "";
if (!empty($context['name'])) {
	$name = $context['name'];
}

$response = _rancher_host_configure($context['project_id'], $host_name, "", $name);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	task_exit(FAILED, "Host creation failed.\n" . $response['wo_comment']);
}

//$context['host_id'] = $vm_id; 

task_exit(ENDED, "Host created successfully.\nHost Id : $host_id");

?>
