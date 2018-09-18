<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/RANCHER/CMP/Library/REST/rancher_common_rest.php';

function list_args()
{
  create_var_def('volume_id', 'String');
}

check_mandatory_param('volume_id');

$response = rancher_object_delete ("projects/" . $context['project_id'] . "/volumes/" . $context['volume_id'], "RANCHER VOLUME");
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	task_exit(FAILED, "Volume deletion failed.\n" . $response['wo_comment']);
}

task_exit(ENDED, "Volume deleted successfully.");

?>