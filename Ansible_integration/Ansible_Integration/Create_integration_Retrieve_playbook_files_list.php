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
  create_var_def('var_name', 'String');
  create_var_def('var_name2', 'Integer');
}

/**
 * A function to check whether all the mandatory parameters are present in user-input
 *
 * The function needs to be called for each mandatory parameter.
 * This function call prevents the Task execution whenever there is a mandatory parameter missing,
 * and gives error at the beginning itself preventing any issues in-between/end of the Task due to a missing mandatory parameter.
 *
 *
 * NOTE : There might be cases where conditions are required.
 * For ex. if (empty($context['var_name']) || (empty($context['var_name2']) && empty($context['var_name3']))) => FAIL [Don't proceed]
 * Such cases need to be handled as per the Task logic
 */
check_mandatory_param('var_name');

/**
 * $context => Service Context variable per Service Instance
 * All the user-inputs of Tasks are automatically stored in $context
 * Also, any new variables should be stored in $context which are used across Service Instance
 * The variables stored in $context can be used across all the Tasks and Processes of a particular Service
 * Update $context array [add/update/delete variables] as per requirement
 *
 * ENTER YOUR CODE HERE
 */
$context['var_name2'] = $context['var_name2'] + 1;

/**
 * Format of the Task response :
 * JSON format : {"wo_status":"status","wo_comment":"comment","wo_newparams":{json_body}}
 * wo_status : ENDED [Green color] or FAILED [Red color] or WARNING [Orange color]
 * 			-> While the Task is Running [means no response returned yet], task status is RUNNING [Blue color]
 *          -> When status is returned as FAILED, the Orchestration Engine stops the Process Execution from this Task
 * wo_comment : Appropriate Comment to display as per the success/failure of the Task
 * wo_newparams : json_body parameters returned from this Task
 *
 * Function prepare_json_response() takes care of Creating a Json response from inputs
 * This function definiton can be found at : /opt/fmc_repository/Process/Reference/Common/utility.php
 * NOTE : For 'wo_newparams', always pass "$context" [whether wo_status is ENDED/FAILED/WARNING to preserve it across Service Instance]
 *     -> Last argument "true" mentions whether the json_response to be Logged in the logfile : /opt/jboss/latest/logs/process.log
 *     -> If not passed, it's "false"
 *
 * The response "$ret" should be echoed from the Task "echo $ret" which is read by Orchestration Engine
 * In case of FAILURE/WARNING, the Task can be Terminated by calling "exit" as per Logic
 */
if ($context['var_name2'] % 2 === 0) {
	$ret = prepare_json_response(FAILED, 'Task Failed', $context, true);
	echo "$ret\n";
	exit;
}

/**
 * End of the task (choose one)
 */
task_success('Task OK');
task_error('Task FAILED');
?>