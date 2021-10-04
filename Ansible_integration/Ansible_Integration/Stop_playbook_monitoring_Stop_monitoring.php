<?php

//This is not good way to finish process, but since we are in a loop, lets do it.
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

$service_id = $context['service_id'];

//Create bash string
$kill_command = '/bin/kill -s TERM $(ps aux | grep -v awk | awk \'/^jboss.+?[Aa]nsible.+?'.$service_id.'/ {print $2}\')';

$result = exec($kill_command);
task_success('Task OK');

?>