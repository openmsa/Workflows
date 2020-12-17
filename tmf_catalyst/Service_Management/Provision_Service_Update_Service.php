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
//  create_var_def('infra_id', 'String');
//  create_var_def('ne_id', 'String');
  create_var_def('interface', 'String');
  create_var_def('vlan', 'String');
  create_var_def('bandwidth', 'String');
}
//Find out if the resources are different, accordingly assign suitable resources set
//$context['status']='confirmed';

task_success('Resources updated for order');
?>