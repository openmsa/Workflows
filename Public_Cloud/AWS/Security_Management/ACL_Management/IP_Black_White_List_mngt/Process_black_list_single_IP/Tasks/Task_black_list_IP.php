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
  create_var_def('single_ip_cidr', 'String');
  create_var_def('single_ip_rule_number', 'String');
}

$device_id = substr ( $context ['aws_region'], 3 );
$single_ip_cidr = $context['single_ip_cidr'];
$single_ip_rule_number = $context['single_ip_rule_number'];
$context['single_ip_last_rule_number'] = $single_ip_rule_number;
$acl_id = $context['acl_id']; 

create_acl_rule($device_id, $acl_id, $single_ip_rule_number, $single_ip_cidr);

task_success('Task OK');


function create_acl_rule ($device_id, $acl_id, $rule_number, $cidr) {

  
	/**
	 * build the Microservice JSON params for the CREATE operation of the microservice
	 */

        $entries_array = array ();     
        $entries_array ['port_range_from'] = "";
        $entries_array ['port_range_to'] = "";
        $entries_array ['protocol'] = -1;
        $entries_array ['rule_action'] = "deny";
        $entries_array ['cidr_block'] = $cidr;
        $entries_array ['rule_number'] = $rule_number;
        $entries_array ['egress'] = false;

	$micro_service_vars_array = array ();
	$micro_service_vars_array ['network_acl_id'] = $acl_id;
	$micro_service_vars_array ['default'] = "false";
	$micro_service_vars_array ['entries'] = $entries_array;
	
	$acl_rule = array (
          'network_acl_entry' => array('0' => $micro_service_vars_array)
	);
	
	/**
	 * call the CREATE for ACL rule MS for each device
	 */
	$response = execute_command_and_verify_response ( $device_id, CMD_CREATE, $acl_rule, "CREATE ACL entry" );

	$response = json_decode ( $response, true );
	if ($response ['wo_status'] === ENDED) {
		
		$response = prepare_json_response ( $response ['wo_status'], $response ['wo_comment'], $context, true );
		echo $response;
	} else {
		task_exit ( FAILED, "Task FAILED" );
	}
}



?>