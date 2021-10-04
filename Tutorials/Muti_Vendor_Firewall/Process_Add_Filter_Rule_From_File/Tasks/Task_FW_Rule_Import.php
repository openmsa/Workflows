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
  /**
   * You can use var_name convention for your variables
   * They will display automaticaly as "Var Name"
   * The allowed types are:
   *    'String', 'Boolean', 'Integer', 'Password', 'IpAddress',
   *    'IpMask', 'Ipv6Address', 'Composite', 'OBMFRef', 'Device'
   *
   * Add as many variables as needed
   */
  create_var_def('file', 'String');
}

shell_exec('diff /opt/fmc_repository/Datafiles/POLICIES/FIREWALL/FWPOLICIES /opt/fmc_repository/Datafiles/POLICIES/FIREWALL/FWPOLICIES.old | grep "<" | cut -d" " -f2 > /opt/fmc_repository/Datafiles/POLICIES/FIREWALL/FWPOLICIES.diff ');


shell_exec('cp /opt/fmc_repository/Datafiles/POLICIES/FIREWALL/FWPOLICIES /opt/fmc_repository/Datafiles/POLICIES/FIREWALL/FWPOLICIES.old');


/**
 * End of the task do not modify after this point
 */
task_exit ( ENDED, "Diff File Generated" . $context['file'] );
?>