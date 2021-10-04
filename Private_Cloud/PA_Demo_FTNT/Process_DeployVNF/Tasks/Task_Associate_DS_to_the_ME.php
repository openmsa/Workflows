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
  create_var_def('conf_profile_reference', 'String');
  create_var_def('dev_ext_reference', 'String');

}
$conf_profile_ref = $context['conf_profile_reference'];
$device_reference = $context['dev_ext_reference'];
$response = _profile_attach_to_device_by_reference ($conf_profile_ref, $device_reference );
 $response = json_decode($response, true);
 if ($response['wo_status'] !== ENDED) {
   $response = json_encode($response);
   echo $response;
 }

task_success('Deployment Settings Associated');
?>