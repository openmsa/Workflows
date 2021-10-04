<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args()
{
  create_var_def('rawlog', 'String');
}

task_success('Event:'.$context['rawlog']);

?>