<?php

/**
 * This file is necessary to include to use all the in-built libraries of /opt/fmc_repository/Reference/Common
 */
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

/**
 * list all the parameters required by the task
 */
function list_args() {
	create_var_def ( 'id', 'String' );
	create_var_def ( 'src_ip', 'String' );
	create_var_def ( 'src_mask', 'String' );

	create_var_def ( 'dst_ip', 'String' );
	create_var_def ( 'dst_mask', 'String' );

	create_var_def ( 'service', 'String' );
	create_var_def ( 'action', 'String' );
}
/**
 * iterate through the array of devices in order to apply the policy for each device
 */
$response;
foreach ( $context ['devices'] as $deviceidRow ) {
	/**
	 * extract the device database identifier from the device ID
	 */
	$devicelongid = substr ( $deviceidRow ['id'], 3 );
	logToFile ( "***************************" );
	logToFile ( "update device $devicelongid" );
	
	/**
	 * build the Microservice JSON params for the CREATE operation of the microservice
	 */
	$micro_service_vars_array = array ();
	$micro_service_vars_array ['object_id'] = $context ['id'];

	$micro_service_vars_array ['src_ip'] = $context ['src_ip'];
	$micro_service_vars_array ['src_mask'] = $context ['src_mask'];

	$micro_service_vars_array ['dst_ip'] = $context ['dst_ip'];
	$micro_service_vars_array ['dst_mask'] = $context ['dst_mask'];

	$micro_service_vars_array ['service'] = $context ['service'];
	$micro_service_vars_array ['action'] = $context ['action'];
	
	$object_id = $context ['id'];
	
	$simple_firewall = array (
			'simple_firewall' => array (
					$object_id => $micro_service_vars_array 
			) 
	);
	
	/**
	 * call the CREATE for simple_firewall MS for each device
	 */
	$response = execute_command_and_verify_response ( $devicelongid, CMD_CREATE, $simple_firewall, "CREATE simple_firewall" );
	$response = json_decode ( $response, true );
	if ($response ['wo_status'] != ENDED) {
		task_exit ( FAILED, "Task FAILED: call to CREATE failes" );
	}
	
	$response = synchronize_objects_and_verify_response($devicelongid);
	$response = json_decode ( $response, true );
	if ($response ['wo_status'] != ENDED) {
		task_exit ( FAILED, "Task FAILED: IMPORT failed" );
	}

}
if (isset ( $context ['rules'] )) {
	$index = count ( $context ['rules'] );
} else {
	$index = 0;
}
logToFile("index: $index");
/**
 * add the firewall policy rule to the array of rules applied on the devices
 */
$context ['rules'] [$index] ['delete'] = false;
$context ['rules'] [$index] ['id'] = $context ['id'];

$context ['rules'] [$index] ['src_ip'] = $context ['src_ip'];
$context ['rules'] [$index] ['src_mask'] = $context ['src_mask'];

$context ['rules'] [$index] ['dst_ip'] = $context ['dst_ip'];
$context ['rules'] [$index] ['dst_mask'] = $context ['dst_mask'];

$context ['rules'] [$index] ['service'] = $context ['service'];
$context ['rules'] [$index] ['action'] = $context ['action'];	


$context ['backend_rules'] [$index] ['delete'] = false;
$context ['backend_rules'] [$index] ['id'] = $context ['id'];

$context ['backend_rules'] [$index] ['src_ip'] = $context ['src_ip'];
$context ['backend_rules'] [$index] ['src_mask'] = $context ['src_mask'];

$context ['backend_rules'] [$index] ['dst_ip'] = $context ['dst_ip'];
$context ['backend_rules'] [$index] ['dst_mask'] = $context ['dst_mask'];

$context ['backend_rules'] [$index] ['service'] = $context ['service'];
$context ['backend_rules'] [$index] ['action'] = $context ['action'];	


$response = prepare_json_response ( $response ['wo_status'], $response ['wo_comment'], $context, true );
echo $response;

/**
 * End of the task do not modify after this point
 */
task_exit ( ENDED, "Task OK" );

?>