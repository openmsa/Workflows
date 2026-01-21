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

  create_var_def('serialnum', 'String');
  create_var_def('src_ip', 'IpAddress');
}


if(isset($parameters)){
$context['serialnum']=$parameters['serialnum'];
$context['src_ip']=$parameters['src_ip'];	
}


check_mandatory_param('serialnum');
check_mandatory_param('src_ip');

$PROCESSINSTANCEID = $context['PROCESSINSTANCEID'];
$EXECNUMBER = $context['EXECNUMBER'];
$TASKID = $context['TASKID'];
$process_params = array('PROCESSINSTANCEID' => $PROCESSINSTANCEID,
		'EXECNUMBER' => $EXECNUMBER,
		'TASKID' => $TASKID);
$response = _orchestration_update_service_instance_reference($context['UBIQUBEID'], $context['SERVICEINSTANCEID'],$context['serialnum']);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}

task_exit(ENDED, "Task OK");

?>
