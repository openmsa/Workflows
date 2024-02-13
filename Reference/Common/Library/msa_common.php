<?php

require_once LIBRARY_DIR . 'device_rest.php';
require_once LIBRARY_DIR . 'device_fields_rest.php';
require_once LIBRARY_DIR . 'device_configuration_rest.php';
require_once LIBRARY_DIR . 'ipam_rest.php';
require_once LIBRARY_DIR . 'lookup_rest.php';
require_once LIBRARY_DIR . 'secengine_rest.php';
require_once LIBRARY_DIR . 'orchestration_rest.php';
require_once LIBRARY_DIR . 'order_command_rest.php';
require_once LIBRARY_DIR . 'configuration_variable_rest.php';
require_once LIBRARY_DIR . 'smarty.php';
require_once LIBRARY_DIR . 'repository_rest.php';
require_once LIBRARY_DIR . 'user_rest.php';
require_once LIBRARY_DIR . 'email_rest.php';
require_once LIBRARY_DIR . 'profile_rest.php';
require_once LIBRARY_DIR . 'delegation_rest.php';
require_once LIBRARY_DIR . 'topology_rest.php';
require_once LIBRARY_DIR . 'openstack_function.php';
require_once LIBRARY_DIR . 'customer_rest.php';
require_once LIBRARY_DIR . 'operator_rest.php';
require_once LIBRARY_DIR . 'widget_portal_rest.php';

/**
 * Import objects for a device
 *
 * @param unknown $device_id
 * @param unknown $objects_array
 * @param string $assoc
 * @return unknown
 */
function import_objects ($device_id, $objects_array) {

	$array = array();
	$import_string = "Import [";
	foreach ($objects_array as $obj) {
		$array[$obj] = "0";
		$import_string .= " $obj";
	}
	$import_string .= " ]";

	$response = execute_command_and_verify_response($device_id, CMD_IMPORT, $array, $import_string);
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, $response['wo_comment'], $response['wo_newparams']);
	return $response;
}

/** 
 * To delete an MSA Object of a device
 */
function msa_object_delete ($device_id, $object_name, $object_id) {

	$object_params = array($object_name => $object_id);
	$response = execute_command_and_verify_response($device_id, CMD_DELETE, $object_params, "DELETE $object_name => $object_id");
	return $response;
}

/**
 * Execute Command Response verifier
 *
 * @param unknown $operation
 * @param unknown $response
 * @return unknown
 */
function execute_command_and_verify_response ($device_id, $command_name, $object_parameters, $comment, $connection_timeout = 60, $max_time = 60) {

	$object_parameters = json_encode($object_parameters);
	$response = _order_command_execute($device_id, $command_name, $object_parameters, $connection_timeout, $max_time);
	return verify_response($response, $device_id, $command_name, $comment);
}

function synchronize_objects_and_verify_response ($device_id, $connection_timeout = 300, $max_time = 300) {

	$response = _order_command_synchronize($device_id, $connection_timeout, $max_time);
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$message = "";
	foreach ($response['wo_newparams'] as $object) {
		$object_newparam['wo_newparams'] = $object;
		$response = verify_response($object_newparam, $device_id, CMD_SYNCHRONIZE);
		$response = json_decode($response, true);
		if ($response['wo_status'] !== ENDED) {
			if ($message !== "") {
				$message = "Objects Synchronized :\n$message\n";
			}
			$message .= $response['wo_comment'];
			$response = prepare_json_response(FAILED, $message, array(), true);
			return $response;
		}
		if (!empty($response['wo_comment'])) {
			$message .= $response['wo_comment'] . "\n";
		}
	}
	$response = prepare_json_response(ENDED, "Objects Synchronization successful for the device $device_id", array(), true);
	return $response;
}

function synchronize_objects_and_verify_response_v2($device_id, $connection_timeout = 300, $max_time = 300) {

	$response = _order_command_synchronize($device_id, $connection_timeout, $max_time);
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$message = "";
	$result = array();
	foreach ($response['wo_newparams'] as $object) {
		$object_newparam['wo_newparams'] = $object;
		$response = verify_response_v2($object_newparam, $device_id, CMD_SYNCHRONIZE);
		$response = json_decode($response, true);
		if ($response['wo_status'] !== ENDED) {
			if ($message !== "") {
				$message = "Objects Synchronized :\n$message\n";
			}
			$message .= $response['wo_comment'];
			$response = prepare_json_response(FAILED, $message, array(), true);
			return $response;
		}
		if (!empty($response['wo_comment'])) {
			$message .= $response['wo_comment'] . "\n";
		}
		$result = array_merge($result, $response['wo_newparams']);
	}
	$response = prepare_json_response(ENDED, "Objects Synchronization successful for the device $device_id", $result, true);
	return $response;
}

function verify_response($response, $device_id, $command_name, $comment = '') {

	if ($command_name !== CMD_SYNCHRONIZE) {
		$response = json_decode($response, true);
		if ($response['wo_status'] !== ENDED) {
			$response = json_encode($response);
			return $response;
		}
	}
	$status = $response['wo_newparams']['status'];
	logToFile("RESPONSE STATUS : $status");
	$message = $response['wo_newparams']['message'];

	$wo_newparams = array();
	if ($status !== STATUS_OK || $message === null) {
		if ($comment !== "") {
			logToFile("$comment FAILED.");
		}
		$fail_message = "OBMF Operation $command_name Failed.";
		if ($message === null) {
			$fail_message .= "\nPlease ensure all of the following conditions are met before running the Process again :";
			$fail_message .= "\n1] The Device $device_id is UP and able to perform OBMF operations from MSA";
			$fail_message .= "\n2] The Object is attached to the Device $device_id";
			if ($command_name !==  CMD_SYNCHRONIZE) {
				$fail_message .= "\n3] The attached Object definition has $command_name operation defined";
			}
		}
		/*
		 * else if (strpos($message, 'Local command failed') !== false
					|| strpos($message, 'device unreachable') !== false
					|| strpos($message, 'Connection refused') !== false
					|| strpos($message, 'Command failed on the device') !== false) {
		*/
		else {			
			$fail_message = $message . "\n" . $fail_message;
		}	
		$response = prepare_json_response(FAILED, $fail_message, $wo_newparams, true);
		return $response;
	}
	if ($command_name === CMD_IMPORT) {
		$response = prepare_json_response(ENDED, "$comment completed successfully", $message, true);
	}
	else {
		if ($command_name === CMD_SYNCHRONIZE) {
			$obj_name = substr($message, 2);
			$obj_name = substr($obj_name, 0, strpos($obj_name, "\""));
			$message = $obj_name;
		}
		$response = prepare_json_response(ENDED, $message, $wo_newparams, true);
	}
	return $response;
}

function verify_response_v2($response, $device_id, $command_name, $comment = '') {

	if ($command_name !== CMD_SYNCHRONIZE) {
		$response = json_decode($response, true);
		if ($response['wo_status'] !== ENDED) {
			$response = json_encode($response);
			return $response;
		}
	}
	$status = $response['wo_newparams']['status'];
	logToFile("RESPONSE STATUS : $status");
	$message = $response['wo_newparams']['message'];

	$wo_newparams = array();
	if ($status !== STATUS_OK || $message === null) {
		if ($comment !== "") {
			logToFile("$comment FAILED.");
		}
		$fail_message = "OBMF Operation $command_name Failed.";
		if ($message === null) {
			$fail_message .= "\nPlease ensure all of the following conditions are met before running the Process again :";
			$fail_message .= "\n1] The Device $device_id is UP and able to perform OBMF operations from MSA";
			$fail_message .= "\n2] The Object is attached to the Device $device_id";
			if ($command_name !==  CMD_SYNCHRONIZE) {
				$fail_message .= "\n3] The attached Object definition has $command_name operation defined";
			}
		}
		/*
		 * else if (strpos($message, 'Local command failed') !== false
					|| strpos($message, 'device unreachable') !== false
					|| strpos($message, 'Connection refused') !== false
					|| strpos($message, 'Command failed on the device') !== false) {
		*/
		else {
			$fail_message = $message . "\n" . $fail_message;
		}
		$response = prepare_json_response(FAILED, $fail_message, $wo_newparams, true);
		return $response;
	}

	$response = prepare_json_response(ENDED, "$comment completed successfully", $message, true);

	return $response;
}


/**
 * Generate Configuration and Verify Response
 *
 * @param unknown $device_id
 * @param unknown $command_name
 * @param unknown $object_parameters
 * @param unknown $comment
 */
function generate_configuration_and_verify_response ($device_id, $command_name, $object_parameters, $comment) {

	$object_parameters = json_encode($object_parameters);
	$response = _order_command_generate_configuration($device_id, $command_name, $object_parameters);
	return verify_response($response, $device_id, $command_name, $comment);
}

/**
 * Function to compare 2 configurations : config_1 and config_2
 * The Result is an array containing differences in CREATE, UPDATE and DELETE operations
 *
 * @param unknown $config_1
 * @param unknown $config_2
 * @return multitype:Ambigous <multitype:, unknown> unknown
 */
function compare_config ($config_1, $config_2) {

	$create_diff_array = array();
	$update_diff_array = array();
	$delete_diff_array = $config_2;

	/**
	 * Outer loop => [Each object_name => objects]
	 * For ex. : {"route": {"object_id":{"a":123,"b":"abc",...}, {"object_id":{"a":456,"b":"xyz",...}}},
	 * 				{"firewall": {"object_id":{"a":123,"b":"abc",...}, {"object_id":{"a":456,"b":"xyz",...}}}},
	 * 				....}
	 */
	foreach ($config_1 as $object_name => $objects) {

		/**
		 * Inner loop => [Each object_id => object_params]
		 * For ex. : {"object_id":{"a":123,"b":"abc",...}}
		 */
		foreach ($objects as $object_id => $object_params) {

			/**
			 * If 'object_id' of 'config_1' exists in 'config_2' => UPDATE operation
			 */
			if (array_key_exists($object_id, $config_2[$object_name])) {

				/**
				 * If 'object_params' of 'config_1' and 'config_2' are different
				 * => Means something was UPDATED for this Object
				 * => Hence, Store the config_1's object_params in update_diff_array
				 */
				if (array_diff_assoc_recursive($object_params, $config_2[$object_name][$object_id]) !== 0) {
					$update_diff_array[$object_name][$object_id] = $object_params;
				}
			}
			/**
			 * If 'object_id' of 'config_1' does not exist in 'config_2'
			 * => Means the object with object_id was DELETED
			 * => Hence, Store the config_1's object_params in create_diff_array
			 */
			else {
				$create_diff_array[$object_name][$object_id] = $object_params;
			}
			/**
			 * delete_difff_array was initialized with 'config_2'
			 * => Remove all the entries of 'config_2' that are available in 'config_1'
			 * => Hence, the delete_diff_array will be left with entries that are only in 'config_2' with CREATE operation
			 */
			unset($delete_diff_array[$object_name][$object_id]);
		}
	}

	/**
	 * Remove 'object_name' entries for which there is no Object to DELETE
	 */
	foreach ($delete_diff_array as $object_name => $objects) {

		if (empty($objects)) {
			unset($delete_diff_array[$object_name]);
		}
	}

	logToFile(debug_dump($create_diff_array, "CREATE DIFFERENCE ARRAY\n"));
	logToFile(debug_dump($update_diff_array, "UPDATE DIFFERENCE ARRAY\n"));
	logToFile(debug_dump($delete_diff_array, "DELETE DIFFERENCE ARRAY\n"));

	return array(CMD_CREATE => $create_diff_array,
					CMD_UPDATE => $update_diff_array,
					CMD_DELETE => $delete_diff_array);
}

/**
 * Get object_id from object name
 *
 * @param unknown $device_id
 * @param unknown $object
 * @param unknown $object_name_key
 * @param unknown $object_name_value
 * @return unknown
 */
function get_object_id_from_name ($device_id, $object, $object_name_key, $object_name_value) {

	$instances_objname = $object;
	$array = array($instances_objname);
	$response = import_objects($device_id, $array);
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$objects = $response['wo_newparams'][$instances_objname];
	$wo_newparams = array();
	$wo_comment = "";
	foreach ($objects as $id => $object_params) {
	   if (array_key_exists($object_name_key, $object_params)) {
		$name = $object_params[$object_name_key];
		if ($name === $object_name_value) {
			$object_id = $object_params['object_id'];
			$wo_comment .= "Object Id : $object_id\n";
			$wo_newparams['object_id'] = $object_id;
			$response = prepare_json_response(ENDED, $wo_comment, $wo_newparams, true);
			return $response;
		}
	  }
	}
	$response = prepare_json_response(FAILED, "Not able to retrieve the object_id.", $wo_newparams, true);
	return $response;
}

/**
 * Rollback an OBMF operation
 * 1] If Create Fails, Delete the the Created object
 * 2] If Delete/Update Fails, push the last good configuration
 *
 * @param unknown $device_id
 * @param unknown $process_params
 * @param unknown $object_parameters
 * @param string $configuration
 * @param string $timeout_ignore_message
 * @param string $timeout
 * @return unknown
 */
function rollback_obmf ($device_id, $process_params, $object_parameters = array(), $configuration = "",
							$timeout_ignore_message = "", $timeout = PUSH_CONFIG_TIMEOUT) {

	logToFile("\nOBMF ROLLBACK STARTS HERE...\n");
	$wo_newparams = array();
	if ($configuration === "") {
		$response = execute_command_and_verify_response($device_id, CMD_DELETE, $object_parameters, "DELETE");
		$response = json_decode($response, true);
		if ($response['wo_status'] !== ENDED) {
			$wo_comment = "ROLLBACK FAILED : OBMF operation DELETE Failed.\n" . $response['wo_comment'];
			logToFile("\n$wo_comment\n");
			$response = prepare_json_response(FAILED, $wo_comment, $wo_newparams, true);
			return $response;
		}
		$response = prepare_json_response(ENDED, "ROLLBACK ENDED : Object Deleted successfully on the device $device_id.\n",
											$wo_newparams, true);
	}
	else {
		$response = _device_do_push_configuration_by_id($device_id, $configuration);
		$response = json_decode($response, true);
		if ($response['wo_status'] !== ENDED) {
			$wo_comment = "ROLLBACK FAILED : Do Push Configuration Failed.\n" . $response['wo_comment'];
			logToFile("\n$wo_comment\n");
			$response = prepare_json_response(FAILED, $wo_comment, $wo_newparams, true);
			return $response;
		}

		$response = wait_for_pushconfig_completion($device_id, $process_params, $timeout_ignore_message, $timeout);
		$response = json_decode($response, true);
		if ($response['wo_status'] !== ENDED) {
			$wo_comment = "ROLLBACK FAILED : Push Configuration Failed/Timed Out.\n" . $response['wo_comment'];
			logToFile("\n$wo_comment\n");
			$response = prepare_json_response(FAILED, $wo_comment, $wo_newparams, true);
			return $response;
		}
		$pushconfig_status_message = $response['wo_comment'];
		$response = prepare_json_response(ENDED, "ROLLBACK ENDED : Last good configuration updated successfully on the device $device_id.\n" . $pushconfig_status_message,
											$wo_newparams, true);
	}
	logToFile("\nOBMF ROLLBACK ENDS HERE...\n");
	return $response;
}

/**
 * Wait for Device reachability from MSA
 *
 * @param unknown $device_id
 * @return unknown
 */
function wait_for_device_reachability ($device_id, $process_params, $timeout = DEVICE_STATUS_CHANGE_TIMEOUT) {

	$wo_newparams = array();
	$device_status = "";
	$wo_comment = "";
	$total_sleeptime = 0;
	$check_device_status_message = "Checking Device $device_id Status (every " . DEVICE_STATUS_CHECK_SLEEP . " seconds";
	$check_device_status_message .= ", timeout = $timeout seconds) :\n";
	while (strpos($device_status, UP) === false) {
		$response = _device_get_status($device_id);
		$response = json_decode($response, true);
		if ($response['wo_status'] !== ENDED) {
			$response = json_encode($response);
			return $response;
		}
		$device_status = $response['wo_newparams'];
		logToFile("DEVICE STATUS : $device_status");
		$wo_comment = "Device Status : {$device_status}\n";
		update_asynchronous_task_details($process_params, $check_device_status_message . $wo_comment);
		if ($device_status === UP) {
			break;
		}
		sleep(DEVICE_STATUS_CHECK_SLEEP);
		$total_sleeptime += DEVICE_STATUS_CHECK_SLEEP;
		if ($total_sleeptime > $timeout) {
			$wo_comment .= "The Device could not be reachable from MSA within $timeout seconds.\nHence, Ending the Process as Failure.";
			$response = prepare_json_response(FAILED, $wo_comment, $wo_newparams, true);
			return $response;
		}
	}
	$response = prepare_json_response(ENDED, $wo_comment, $wo_newparams);
	return $response;
}

/**
 * Poll Provisioning Status and wait for it's completion
 *
 * @param unknown $device_id
 * @param unknown $process_params
 * @return string|unknown
 */
function wait_for_provisioning_completion ($device_id, $process_params, $sleep_time = PROVISIONING_STATUS_CHECK_SLEEP, $wo_comment = "") {

	$wo_newparams = array();
	$provisioning_process = RUNNING;
	while ($provisioning_process === RUNNING || $provisioning_process === NOTRUN) {
		$response = _device_get_provisioning_status_by_id($device_id);
    	$response = json_decode($response, true);
		if ($response['wo_status'] !== ENDED) {
			$response = json_encode($response);
			return $response;
    	}
		$rawJSONResult = $response['wo_newparams']['rawJSONResult'];
    	$smsJsonResult = json_decode($rawJSONResult, true);
    	$sms_result = $smsJsonResult['sms_result'];
    	$provisioning_process = $smsJsonResult['PROVISIONING_PROCESS'];

    	$update_async_task_details = "$wo_comment\n";
    	if ($provisioning_process === RUNNING) {
			$update_async_task_details .= "Checking device $device_id provisioning status (every $sleep_time seconds) :\n";
    	}

    	$sms_stage = "";
		if ($provisioning_process !== NOTRUN){
			foreach ($sms_result as $result) {
				$sms_stage = $result['sms_stage'];
				$sms_status = $result['sms_status'];
				$sms_message = $result['sms_message'];
				if ($sms_status === RUNNING) {
					$update_async_task_details .= "$sms_stage: $sms_status\n";
					logToFile("PROVISIONING STAGE : $sms_stage => STATUS : $sms_status => MESSAGE : $sms_message");
					update_asynchronous_task_details($process_params, $update_async_task_details);
					break;
				} 
				else if ($sms_status !== NOTRUN) {
					$update_async_task_details .= "$sms_stage: $sms_message\n";
				}
			}
		}
		if (($provisioning_process === ENDED || $provisioning_process === FAILED)){
			break;
		}
		sleep($sleep_time);
	}
	if ($provisioning_process === FAILED) {
		$error_message = "Error Message at $sms_stage : \n" . $smsJsonResult['errorMsg'];
		$response = prepare_json_response(FAILED, $error_message, $wo_newparams, true);
		return $response;
	}
	$response = prepare_json_response(ENDED, $update_async_task_details, $wo_newparams);
	return $response;
}

/**
 * Poll Push-config Status and wait for it's completion
 *
 * @param unknown $device_id
 * @param string $timeout_ignore_message
 * @param unknown $process_params
 * @return mixed|unknown
 */
function wait_for_pushconfig_completion ($device_id, $process_params, $ignore_messages = array(), $timeout = PUSH_CONFIG_TIMEOUT) {

	$wo_newparams = array();
	$status = '';
	$message = '';
	$wo_comment = "";
	$total_sleeptime = 0;
	$check_pushconfig_status_message = "Checking Device $device_id Push Config Status (every " . PUSH_CONFIG_CHECK_SLEEP . " seconds";
	$check_pushconfig_status_message .= ", timeout = $timeout seconds) :\n";
	while ($status !== ENDED) {

		$response = _device_get_pushconfig_status_by_id($device_id);
		$response = json_decode($response, true);
		if ($response['wo_status'] !== ENDED) {
			$response = json_encode($response);
			return $response;
		}
		$status = $response['wo_newparams']['status'];
		$message = $response['wo_newparams']['message'];
		logToFile("PUSH CONFIG STATUS : $status");
		logToFile("PUSH CONFIG MESSAGE : $message");

		$wo_comment = "Push Config Status : " . $status;
		$wo_comment_print = $wo_comment;
		$wo_comment .= "\nPush Config Message : $message\n";
		if (strlen($message) > 3800) {
			$message = substr($message, 0, 3800);
			$wo_comment_print .= "\nPush Config Message (truncated) : $message\n";
		}
		else {
			$wo_comment_print = $wo_comment;
		}
		update_asynchronous_task_details($process_params, $check_pushconfig_status_message . $wo_comment_print);
		if ($status === ENDED) {
			break;
		}
		else if ($status === FAILED) {
			logToFile(debug_dump($ignore_messages, "PUSH CONFIG IGNORE MESSAGES\n"));
			$ignore_message_found = false;
			if (!empty($ignore_messages)) {
				foreach ($ignore_messages as $ignore_message) {
					if (strpos($message, $ignore_message) !== false) {
						$ignore_message_found = true;
						break;
					}
				}
			}
			if ($ignore_message_found) {
				break;
			}
			$response = prepare_json_response(FAILED, $message, $wo_newparams, true);
			return $response;
		}
		sleep(PUSH_CONFIG_CHECK_SLEEP);
		$total_sleeptime += PUSH_CONFIG_CHECK_SLEEP;
		if ($total_sleeptime > $timeout) {
			$wo_comment .= "The Device $device_id Push Configuration could not be completed within $timeout seconds.\nHence, Ending the Process as Failure.";
			$response = prepare_json_response(FAILED, $wo_comment, $wo_newparams, true);
			return $response;
		}
	}
	$response = prepare_json_response(ENDED, $wo_comment, $wo_newparams);
	return $response;
}

/**
 * Poll Ping Status and wait for it's success/failure
 *
 * @param unknown $ip_address
 * @param unknown $process_params
 * @return mixed|unknown
 */
function wait_for_ping_status ($ip_address, $process_params, $status_check = STATUS_OK, $max_ping_counts = MAX_PING_COUNT) {

	$wo_newparams = array();
	$ping_status = '';
	$count = 0;
	$wo_comment = "";
	$check_ping_status_message = "Checking IP Address $ip_address PING Status (every " . SLEEP_BETWEEN_PINGS . " seconds";
	$check_ping_status_message .= ", maximum ping requests = " . $max_ping_counts . ") :\n";
	while ($ping_status !== $status_check) {

		$response = _device_do_ping($ip_address);
		$response = json_decode($response, true);
		if ($response['wo_status'] !== ENDED) {
			$response = json_encode($response);
			return $response;
		}
		$ping_status = $response['wo_newparams']['status'];
		logToFile("PING STATUS : $ping_status");

		if ($ping_status === FAILED) {
			$ping_message = $response['wo_newparams']['message'];
			logToFile("PING MESSAGE : $ping_message");
			if (strpos($ping_message, 'Bad parameters on command') !== false) {
				$response = prepare_json_response(FAILED, "{$ping_message} :\n{$ip_address}", $wo_newparams, true);
				return $response;
			}
			$wo_comment = "PING Status : Destination Host Unreachable\n";
		}
		else {
			$wo_comment = "PING Status : $ping_status\n";
		}
		update_asynchronous_task_details($process_params, $check_ping_status_message . $wo_comment);
		if ($ping_status === $status_check) {
			break;
		}
		sleep(SLEEP_BETWEEN_PINGS);
		$count++;
		if ($count === $max_ping_counts) {
			if ($status_check === STATUS_OK) {
				$wo_comment = "IP Address $ip_address is not reachable within maximum time limit. Hence Ending the Process as a Failure.";
			}
			else {
				$wo_comment = "IP Address $ip_address is reachable beyond maximum time limit. Hence Ending the Process as a Failure.";
			}
			$response = prepare_json_response(FAILED, $wo_comment, $wo_newparams, true);
			return $response;
		}
	}
	$response = prepare_json_response(ENDED, $wo_comment, $wo_newparams);
	return $response;
}

/**
 * Poll SSH Connection and wait for it's success/failure
 *
 * @param unknown $ip_address
 * @param unknown $process_params
 * @return mixed|unknown
 */
function wait_for_ssh_status($ip_address, $port_no = SSH_DEFAULT_PORT_NO, $process_params = null,
		$status_check = STATUS_OK, $max_ssh_counts = MAX_SSH_COUNT) {

	$wo_newparams = array();
	$ssh_status = '';
	$count = 0;
	$wo_comment = "";
	$params = "{$ip_address}\r\n{$port_no}";
	$check_ssh_status_message = "Checking IP Address $ip_address SSH connectivity (every " . SLEEP_BETWEEN_SSH_RETRY . " seconds";
	$check_ssh_status_message .= ", maximum SSH retry requests = $max_ssh_counts) :\n";
	while ($ssh_status !== $status_check) {

		$response = _secengine_perform_command_on_device(0, SMS_CMD_SSH_STATUS, $params);
		$response = json_decode($response, true);
		if ($response['wo_status'] !== ENDED) {
			if (strpos($response['wo_comment'], "'$ip_address' Failed") !== false) {
				$wo_comment = "SSH Status : No route to host\n";
				$ssh_status = FAILED;
				logToFile("SSH STATUS : $ssh_status");
			}
			else {
				$response = json_encode($response);
				return $response;
			}
		}
		if (array_key_exists('status', $response['wo_newparams'])) {
			$ssh_status = $response['wo_newparams']['status'];
			logToFile("SSH STATUS : $ssh_status");

			if ($ssh_status === FAILED) {
				$ssh_message = $response['wo_newparams']['message'];
				logToFile("SSH MESSAGE : $ssh_message");
				if (strpos($ssh_message, 'Bad parameters on command') !== false) {
					$response = prepare_json_response(FAILED, "{$ssh_message} :\n{$params}", $wo_newparams, true);
					return $response;
				}
				$wo_comment = "SSH Status : No route to host\n";
			}
			else {
				$wo_comment = "SSH Status : $ssh_status\n";
			}
		}
		update_asynchronous_task_details($process_params, $check_ssh_status_message . $wo_comment);
		if ($ssh_status === $status_check) {
			break;
		}
		sleep(SLEEP_BETWEEN_SSH_RETRY);
		$count++;
		if ($count === $max_ssh_counts) {
			if ($status_check === STATUS_OK) {
				$wo_comment = "IP Address $ip_address is not reachable within maximum time limit. Hence Ending the Process as a Failure.";
			}
			else {
				$wo_comment = "IP Address $ip_address is reachable beyond maximum time limit. Hence Ending the Process as a Failure.";
			}
			$response = prepare_json_response(FAILED, $wo_comment, $wo_newparams, true);
			return $response;
		}
	}
	$response = prepare_json_response(ENDED, $wo_comment, $wo_newparams);
	return $response;
}

/**
 * Execute a shell cmd and wait for a particular output string
 *
 * @param unknown $cmd
 * @param unknown $expected_output_string
 * @param unknown $process_params
 * @param string $output_flag
 * @param string $timeout
 * @return string
 */
function execute_linux_command_and_wait_for_output ($cmd, $expected_output_string, $process_params, $timeout = LINUX_CMD_OUTPUT_CHECK_TIMEOUT) {

	$output = NULL;
	$wo_newparams = array();
	$wo_comment = "";
	$total_sleeptime = 0;
	$check_cmd_output_message = "Checking command output (every " . LINUX_CMD_OUTPUT_CHECK_SLEEP . " seconds";
	$check_cmd_output_message .= ", timeout = $timeout seconds) :\n";
	while ((!empty($expected_output_string) && strpos($output, $expected_output_string) === false) || (empty($expected_output_string) && $output !== "")) {
		$output_array = array();
		exec($cmd, $output_array);
		$output = "";
		foreach ($output_array as $line) {
			$output .= "$line\n";
		}
		logToFile("Command : $cmd");
		logToFile("Output : $output");
		sleep(LINUX_CMD_OUTPUT_CHECK_SLEEP);
		$total_sleeptime += LINUX_CMD_OUTPUT_CHECK_SLEEP;
		$wo_comment = "Command : $cmd\nOutput : $output\n";
		update_asynchronous_task_details($process_params, $check_cmd_output_message . $wo_comment);
		if ($total_sleeptime > $timeout) {
			$wo_comment .= "The expected output string was not available in the command output within $timeout seconds.\nHence, Ending the Process as Failure.";
			$response = prepare_json_response(FAILED, $wo_comment, $wo_newparams, true);
			return $response;
		}
	}
	$response = prepare_json_response(ENDED, $wo_comment, $wo_newparams);
	return $response;
}

/**
 * Poll Process Status and wait for it's completion
 *
 * @param unknown $process_id
 * @param unknown $process_params
 * @return string|unknown
 */
function wait_for_process_completion ($process_id, $process_params, $sleep_time = PROCESS_STATUS_CHECK_SLEEP) {

  $wo_newparams = array();
  $response = _orchestration_get_process_instance($process_id);
  $response = json_decode($response, true);
  if ($response['wo_status'] !== ENDED) {
    $response = json_encode($response);
    return $response;
  }
  $process_task_status = $response['wo_newparams']['status']['processTaskStatus'];
  $process_task_count = count($process_task_status);

  $service_id = $response['wo_newparams']['serviceId']['id'];
  $service_name = $response['wo_newparams']['serviceId']['name'];
  $process_id = $response['wo_newparams']['processId']['id'];
  $process_name = $response['wo_newparams']['processId']['name'];

  $update_async_task_details = array();
  $update_async_task_details[0] = "Checking Process $process_id Status (every $sleep_time seconds) :\n";
  $update_async_task_details[0] .= "Service Id : $service_id\nService Name : $service_name\n";
  $update_async_task_details[0] .= "Process Id : $process_id\nProcess Name : $process_name\n\n";

  $wo_comment = "";
  $total_sleeptime = 0;
  $tasks_already_displayed = array();
  $process_status = $response['wo_newparams']['status']['status']; //get the status of the whole tasks
  
  //In processTaskStatus we don't see all available tasks before all tasks are finished, there are filled one after one when they are finished individually.
  //We want write into logs the running task and each task already ended. 
  
  while ($process_status === RUNNING) { //status of the whole tasks, it will be ended when all tasks are ended.
    $response = _orchestration_get_process_instance($process_id);
    $response = json_decode($response, true);
    if ($response['wo_status'] !== ENDED) {
      $response = json_encode($response);
      return $response;
    }

    $process_task_status = $response['wo_newparams']['status']['processTaskStatus'];
    $process_status = $response['wo_newparams']['status']['status'];
 

    if ($process_status === FAILED) {
      $response = prepare_json_response(FAILED, $response['wo_newparams']['status']['details'], $wo_newparams, true);
      return $response;
    }
  
    //Log in 'live times' all tasks not already logged (we display each task only 1 time : status RUNNING (if the task is running) or  status ENDED when the task is ended)
    foreach ($process_task_status as $process_1task_status) {
      $order_status = $process_1task_status['status'];
      $order        = $process_1task_status['order'];
      if ($order_status === FAILED) {
        $response = prepare_json_response(FAILED, $details, $wo_newparams, true);
        return $response;
      }elseif( ! isset($tasks_already_displayed[$order][$order_status])){
        //to display        
        $script_name = $process_1task_status['scriptName'];
        $details     = $process_1task_status['details'];
        logToFile("SCRIPT NAME : $script_name => STATUS : $order_status");
        $update_async_task_details[$order] = "$order] $script_name\n";
        $update_async_task_details[$order] .= "Details : $details\n";
        $update_async_task_details[$order] .= "Status : $order_status\n";
        $tasks_already_displayed[$order][$order_status]=1;
      }  
    } 
    $update_async_task_details_string='';
    foreach ($update_async_task_details as $detail){
      $update_async_task_details_string .= $detail;
    }       
    update_asynchronous_task_details($process_params, $update_async_task_details_string);
    
    if ($process_status!== ENDED){
      sleep($sleep_time);
    }    
  }
    
  //$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $wo_newparams);
  $response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']);
  return $response;
}

/**
 * Add an array service variable into current context
 * For ex. : if service_variable name = device.0.id, value = MSA123
 * Then, it will add $context['device'][0]['id'] = "MSA123" 
 * 
 * @param unknown $name
 * @param unknown $value
 */
function add_service_variable_string_to_context ($name, $value) {

	global $context;
	$pos = &$context;
	foreach(explode(".", $name) as $split)
	{
		if(!isset($pos[$split]))
		{
			$pos[$split] = array();
		}
		$pos = &$pos[$split];
	}
	$pos = $value;
}

function convert_to_msa_var () {

	global $context;
	global $workflow_internal_params;

        $context_params = array();
        foreach ($context as $key => $value) {
		if (!in_array($key, $workflow_internal_params)) {
	                build_msa_param($context_params, null, $key, $value);
		}
        }
        return $context_params;
}

function build_msa_param (&$context_params, $current_key, $sub_key, $sub_value) {

        $full_key = $current_key;
        if (empty($full_key)) {
                $full_key = $sub_key;
        }
        else {
                $full_key .= ".{$sub_key}";
        }
        if (is_array($sub_value)) {
                if (array_values($sub_value) === $sub_value) {
                        for ($index = 0; $index < count($sub_value); $index++) {
                                build_msa_param($context_params, $full_key, $index, $sub_value[$index]);
                        }
                }
                else {
                        foreach ($sub_value as $key => $value) {
                                build_msa_param($context_params, $full_key, $key, $value);
                        }
                }
        }
        else {
                $context_params[$full_key] = $sub_value;
        }
}

/**
 * Poll Device Update Config Status and wait for it's completion
 *
 * @param unknown $device_id
 * @param unknown $process_params
 * @return mixed|unknown
 */
function wait_for_update_config_completion ($device_id, $process_params, $timeout = UPDATE_CONFIG_TIMEOUT) {

	$wo_newparams = array();
	$status = '';
	$wo_comment = "";
	$total_sleeptime = 0;
	$check_update_config_status_message = "Checking Device $device_id Update Config Status (every " . UPDATE_CONFIG_CHECK_SLEEP . " seconds";
	$check_update_config_status_message .= ", timeout = $timeout seconds) :\n";
	while ($status !== ENDED) {

		$response = _device_get_update_config_status($device_id);
		$response = json_decode($response, true);
		if ($response['wo_status'] !== ENDED) {
			$response = json_encode($response);
			return $response;
		}
		$status = $response['wo_newparams']['status'];
		$message = $response['wo_newparams']['message'];
		logToFile("UPDATE CONFIG STATUS : $status");
		logToFile("UPDATE CONFIG MESSAGE : $message");

		$wo_comment = "Update Config Status : " . $status;
		$wo_comment .= "\nUpdate Config Message : $message\n";
		update_asynchronous_task_details($process_params, $check_update_config_status_message . $wo_comment);
		if ($status === ENDED) {
			break;
		}
		else if ($status === FAILED) {
			$response = prepare_json_response(FAILED, $message, $wo_newparams, true);
			return $response;
		}
		sleep(UPDATE_CONFIG_CHECK_SLEEP);
		$total_sleeptime += UPDATE_CONFIG_CHECK_SLEEP;
		if ($total_sleeptime > $timeout) {
			$wo_comment .= "The Device $device_id Update Config could not be completed within $timeout seconds.\nHence, Ending the Process as Failure.";
			$response = prepare_json_response(FAILED, $wo_comment, $wo_newparams, true);
			return $response;
		}
	}
	$response = prepare_json_response(ENDED, $wo_comment, $wo_newparams);
	return $response;
}

function msa_execute_service_by_reference_and_wait_for_completion ($external_ref, $service_name, $process_name, $json_body = "{}", $store_service_vars_in_context = true, $service_reference = "") {

        global $context;

        $response = _orchestration_execute_service_by_reference($external_ref, $service_reference, $service_name, $process_name, $json_body);
        $response = json_decode($response, true);
        if ($response['wo_status'] !== ENDED) {
		task_error($response['wo_comment']);
        }

        $process_id = $response['wo_newparams']['processId']['id'];
        $service_id = $response['wo_newparams']['serviceId']['id'];
	$response = wait_for_process_completion($process_id, $context);
  	$response = json_decode($response, true);
  	if ($response['wo_status'] !== ENDED) {
		task_error($response['wo_comment']);
  	}

    	//Get the context from the WF
	if ($store_service_vars_in_context) {
	  	$response =  _orchestration_get_service_variables_by_service_id($service_id);
	  	$response = json_decode($response, true);
  		if ($response['wo_status'] !== ENDED) {
			task_error($response['wo_comment']);
  		}
  		$context['executed_service_id'] = $service_id;
  		$context[$service_name][$service_id]['context'] = $response['wo_newparams'];
	}
}



?>
