<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/RANCHER/CMP/Library/REST/rancher_common_rest.php';

function list_args()
{
  create_var_def('rancher_service_name', 'String');
}

check_mandatory_param('rancher_service_name');

$response = rancher_object_get("projects/" . $context['rancher_project_id'] ."/services?name=" . 	
				$context['rancher_service_name'], "RANCHER SERVICE");
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	task_exit(FAILED, "Service Id retrieval failed.\n" . $response['wo_comment']);
}

$context['rancher_service_id'] = $response['wo_newparams']['data'][0]['id'];

task_exit(ENDED, "Service id retrieved successfully.");

?>
