<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/RANCHER/CMP/Library/REST/rancher_common_rest.php';

function list_args()
{
  #create_var_def('token_name', 'String');
}

/**
$token_name = "";
if (!empty($context['token_name'])) {
	$token_name = $context['token_name'];
}
*/

$response = _rancher_registration_token_create($context['rancher_project_id']);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	task_exit(FAILED, "Token creation failed.\n" . $response['wo_comment']);
}

$context['registration_token'] = $response['wo_newparams']['id'];

task_exit(ENDED, "Token created successfully.");

?>
