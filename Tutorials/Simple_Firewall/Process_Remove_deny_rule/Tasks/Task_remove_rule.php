<?php

/**
 * This file is necessary to include to use all the in-built libraries of /opt/fmc_repository/Reference/Common
 */
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

/**
 * List all the parameters required by the task
 */
function list_args() {
	create_var_def ( 'rules.0.delete', 'String' );
	create_var_def ( 'rules.0.id', 'String' );
	create_var_def ( 'rules.0.src_ip', 'String' );
	create_var_def ( 'rules.0.src_mask', 'String' );
	create_var_def ( 'rules.0.dst_ip', 'String' );
	create_var_def ( 'rules.0.dst_mask', 'String' );
	create_var_def ( 'rules.0.service', 'String' );
	create_var_def ( 'rules.0.action', 'String' );
}

/**
 * loop through each rule stored in the array "rules" and call the microservice DELETE when the flag "delete" is set to true
 */
logToFile ( "* * * * " );
logToFile($context['rules']);
logToFile(debug_dump($context ['rules']), "RULES");
$index = 0;
foreach ( $context ['rules'] as $rulesRow ) {
	logToFile(debug_dump($rulesRow), "RULE ROW");
	$delete = $rulesRow ['delete'];
	$rule_id = $rulesRow ['id'];
	$rule_src_ip = $rulesRow ['src_ip'];
	$rule_dst_ip = $rulesRow ['dst_ip'];
	$rule_service = $rulesRow ['service'];
	logToFile ( "************************************************" );
	logToFile ( "$index ) delete:$delete : $rule_id - $rule_src_ip -> $rule_dst_ip:$rule_service" );
	
	if ($delete === "true") {
		
		$object_id = $rule_id;
		$simple_firewall = array (
				'simple_firewall' => $object_id 
		);

		/**
		 * iterate through the array of devices in order to remove the policy for each device
		 */
		foreach ( $context ['devices'] as $deviceidRow ) {
			/**
			 * extract the device database identifier from the device ID
			 */
			$device_id = substr ( $deviceidRow ['id'], 3 );
		
			$response = execute_command_and_verify_response ( $device_id, CMD_DELETE, $simple_firewall, "DELETE simple_firewall" );
			$response = json_decode ( $response, true );
			if ($response ['wo_status'] === ENDED) {
				$response = prepare_json_response ( $response ['wo_status'], $response ['wo_comment'], $context, true );
				echo $response;
			} else {
				logToFile("WARNING: call to DELETE failed for $device_id");
 			}
		}
		unset ( $context ['rules'] [$index] );
	}
	$index ++;
}

/**
 * End of the task do not modify after this point
 */
task_exit ( ENDED, "Task OK" );

?>