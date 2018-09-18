<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/RANCHER/CMP/Library/REST/rancher_common_rest.php';

function list_args()
{
  create_var_def('stack_name', 'String');
}

check_mandatory_param('stack_name');

$stack_name = $context['stack_name'];

$response = _rancher_stack_configure($context['rancher_project_id'], $stack_name);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	task_exit(FAILED, "Stack creation failed.\n" . $response['wo_comment']);
}

$stack_id = $response['wo_newparams']['id'];
$context['stack_id'] = $stack_id;

task_exit(ENDED, "Stack created successfully.\nStack Id : $stack_id");

?>
