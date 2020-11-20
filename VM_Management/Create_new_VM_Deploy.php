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
  create_var_def('name', 'String');
  create_var_def('template', 'String');
  create_var_def('cpu', 'String');
  create_var_def('memory', 'String');
  create_var_def('host', 'String');
  create_var_def('datastore', 'String');
  create_var_def('folder', 'String');
  create_var_def('network1', 'String');
  create_var_def('network2', 'String');
}

$name = $context['name'];
$template = $context['template'];
$cpu = $context['cpu'];
$memory = $context['memory'];
$host = $context['host'];
$datastore = $context['datastore'];
$folder = $context['folder'];
$netowrk1 = $context['network1'];
$netowrk2 = $context['network2'];

task_success('Task OK');
?>