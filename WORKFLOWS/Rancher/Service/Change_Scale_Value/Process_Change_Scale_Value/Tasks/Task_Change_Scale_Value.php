<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/RANCHER/CMP/Library/REST/rancher_common_rest.php';

function list_args()
{
  create_var_def('rancher_service_scale', 'Integer');
}

check_mandatory_param('rancher_service_scale');

$response = _rancher_service_configure($context['rancher_project_id'], "", $context['rancher_service_id'], 
					$context['rancher_service_scale']);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	task_exit(FAILED, "Service Scale failed.\n" . $response['wo_comment']);
}

task_exit(ENDED, "Service scaled successfully.");

?>

