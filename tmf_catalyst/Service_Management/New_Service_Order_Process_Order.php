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
  create_var_def('service_order_id', 'String');
  create_var_def('service_type', 'String');
  create_var_def('fe_order_id', 'String');
  create_var_def('suborder_id', 'String');
  create_var_def('SiteGeographicalLocation', 'String');
  create_var_def('TargetDeliveryDate', 'String');
  create_var_def('LineId', 'String');
  create_var_def('BudgetCap', 'String');
  create_var_def('SiteGeographicalLocation1', 'String');
  create_var_def('SiteGeographicalLocation2', 'String');
}

$context['status']='ordered';

task_success('Order Processed');
//task_error('Task FAILED');
?>