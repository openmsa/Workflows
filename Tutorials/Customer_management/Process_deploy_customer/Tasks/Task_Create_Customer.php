<?php

/**
 * This file is necessary to include to use all the in-built libraries of /opt/fmc_repository/Reference/Common
 */
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

/**
 * List all the parameters required by the task as input parameters.
 * The parameters listed below will be available in the user form
 */
function list_args()
{
  create_var_def('operator_prefix', 'String');
  create_var_def('customer_name', 'String');
}

/** 
 * use this function to check that a value is provided for a set of parameters that are mandatory
 * this is useful when the process is executed by an API call (REST or SOAP). 
 * when the process is executed from the GUI, the user form will be checking for the variables that are configured as 
 * madatory
 */
check_mandatory_param('operator_prefix');
check_mandatory_param('customer_name');

/**
 * read the parameter values passed to the process.
 * these values are stored in the workflow instance context.
 * these parameters are available for read/update at any moment during a process execution.
 */
$operator_prefix = $context['operator_prefix'];
$customer_name = $context['customer_name'];

$customer_reference = $customer_name;
$customer_reference = str_replace(' ', '_', $customer_reference);
$context['customer_reference'] = $customer_reference;

/**
 * call a predefined function to create the customer.
 * this function is a wrapper around the REST API to create a customer.
 * these functions are available in the repository Workflow/Reference/Common/Library
 */
$response = _customer_create($operator_prefix, $customer_name, $customer_reference);
$response = json_decode($response, true);

if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}

$customer_seqnum=$response ['wo_newparams']['id'];
$customer_id = $operator_prefix."A".$customer_seqnum;
$wo_comment = "\nCustomer created with ID : " . $customer_id;

$context['customer_id'] = $customer_id;
$response = prepare_json_response(ENDED, "Customer created successfully.\n$wo_comment", $context, true);
echo $response;

task_exit(ENDED, "Customer Created");

?>
