<?php

require_once COMMON_DIR . 'constants.php';
if (file_exists('/opt/fmc_repository/Process/custom_constants.php')) {
	include '/opt/fmc_repository/Process/custom_constants.php';
}

error_reporting(E_ALL | E_STRICT);
$timezone = 'UTC';

// "/etc/localtime" is a symlink to the file with the timezone info
if (is_link('/etc/localtime')) {
	$filename = readlink('/etc/localtime');

	$pos = strpos($filename, 'zoneinfo');
	if ($pos !== false) {
		$timezone = substr($filename, $pos + strlen('zoneinfo/'));
	}
}

date_default_timezone_set($timezone);

/**
 * Log the message
 *
 * @param unknown $msg
 * @param string $filename
 */
function logToFile($msg, $filename = PROCESS_LOGS_FILE) {

	if ($filename === PROCESS_LOGS_FILE) {
		global $context;
		if (isset($context['SERVICEINSTANCEID'])) {
			$filename .= "-" . $context['SERVICEINSTANCEID'];
		}
	}
	
	$date = date('Y-m-d H:i:s');
	$to_log = "$date| $msg";
	file_put_contents($filename, "$to_log\n", FILE_APPEND);
}

/**
 * Obtain a Lock on a file given with file-name : /opt/ubi-jentreprise/<lock_file_name>
 *
 * @param unknown $lock_file
 * @param unknown $mode
 * @param unknown $process_params
 * @param string $sleep_time
 * @param string $timeout
 * @return string
 */
function obtain_file_lock ($lock_file, $mode, $process_params,
							$sleep_time = FILE_LOCK_STATUS_CHECK_SLEEP, $timeout = FILE_LOCK_TIMEOUT) {

	$check_lock_status_message = "Checking Lock Status on the file $lock_file (every $sleep_time seconds";
	$check_lock_status_message .= ", timeout = $timeout seconds) :\n";
	$lock_ok = false;
	$total_sleeptime = 0;
	$wo_newparams = array();
	while (!$lock_ok) {
		$lf = fopen(UBI_JENTREPRISE_DIRECTORY . $lock_file, $mode);
		/**
		 * loop until the lock is free
		*/
		while(!flock($lf, LOCK_EX | LOCK_NB)) {
			update_asynchronous_task_details($process_params, "{$check_lock_status_message}Waiting to obtain Lock");
			sleep($sleep_time);
			$total_sleeptime += $sleep_time;
			if ($total_sleeptime > $timeout) {
				$wo_comment = "Lock couldn't be obtained on the file $lock_file within $timeout seconds.";
				$response = prepare_json_response(FAILED, $wo_comment, $wo_newparams, true);
				return $response;
			}
		}
		// Lock on file aquired. check application lock
		$length = filesize(UBI_JENTREPRISE_DIRECTORY . $lock_file);
		$content = "unlocked";
		if ($length > 0) {
			$content = fread($lf, $length);
		}
		if (strpos($content, "unlock") === 0) {
			// lock at application level
			ftruncate($lf, 0);
			fseek($lf, 0);
			fwrite($lf, "locked");
			$lock_ok = true;
			flock($lf, LOCK_UN);
			fclose($lf);
			$response = prepare_json_response(ENDED, "Lock obtained on the file $lock_file", $wo_newparams, true);
			return $response;
		}
		// application locked
		fclose($lf);
		update_asynchronous_task_details($process_params, "{$check_lock_status_message}Waiting to obtain Lock");
		sleep($sleep_time);
		$total_sleeptime += $sleep_time;
		if ($total_sleeptime > $timeout) {
			$wo_comment = "Lock couldn't be obtained on the file $lock_file within $timeout seconds.";
			$response = prepare_json_response(FAILED, $wo_comment, $wo_newparams, true);
			return $response;
		}
	}
	$response = prepare_json_response(ENDED, "Lock obtained on the file $lock_file", $wo_newparams, true);
	return $response;
}
/**
 * Release obtained file-lock
 * 
 * @param unknown $lock_file
 * @param unknown $mode
 * @param unknown $process_params
 * @param string $sleep_time
 * @param string $timeout
 * @return string
 */
function release_file_lock ($lock_file, $mode, $process_params,
								$sleep_time = FILE_LOCK_STATUS_CHECK_SLEEP, $timeout = FILE_LOCK_TIMEOUT) {

	$wo_newparams = array();
	$check_lock_status_message = "Checking Lock Status on the file $lock_file (every $sleep_time seconds";
	$check_lock_status_message .= ", timeout = $timeout seconds) :\n";
	$total_sleeptime = 0;
	$lf = fopen(UBI_JENTREPRISE_DIRECTORY . $lock_file, $mode);
	while (!flock($lf, LOCK_EX | LOCK_NB))
	{
		update_asynchronous_task_details($process_params, "{$check_lock_status_message}Waiting to release Lock");
		sleep($sleep_time);
		$total_sleeptime += $sleep_time;
		if ($total_sleeptime > $timeout)
		{
			$wo_comment = "Lock couldn't be released on the file $lock_file within $timeout seconds.";
			$response = prepare_json_response(FAILED, $wo_comment, $wo_newparams, true);
			return $response;
		}
	}
	// Lock on file aquired. Unlock application
	fwrite($lf, "unlocked");
	flock($lf, LOCK_UN);
	fclose($lf);
	$response = prepare_json_response(ENDED, "Lock released on the file $lock_file", $wo_newparams, true);
	return $response;
}

/**
 * Get a variable value from vars.ctx file
 *
 * @param unknown $variable
 * @return unknown|boolean
 */
function get_vars_value($variable) {
	$VARS_CTX = VARS_CTX_FILE;
	$vars_content = file_get_contents($VARS_CTX);
	if ($vars_content) {
		$regex = "@$variable=+(.*)@";
		$is_result = preg_match($regex, $vars_content, $result);
		if ($is_result) {
			return $result[1];
		}
	}
	return false;
}

/**
 * Execute a shell command
 * @param unknown $cmd
 * @param string $output_lines
 */
function exec_shell($cmd, &$output_lines = null, &$errors = null) {
  logToFile("Shell exec: $cmd");
  if (isset($output_lines)) {
	  if (isset($errors)) {
	    exec($cmd, $output_lines, $errors);
	  } else {
		exec($cmd, $output_lines);
	  }
  }
  else {
    return shell_exec($cmd);
  }
}

/**
 * Check if given String is in Json format
 *
 * @param unknown $string
 * @return boolean
 */
function is_json($string) {
	return is_string($string) && is_array(json_decode($string, true)) && (json_last_error() == JSON_ERROR_NONE) ? true : false;
}

function create_json_string_from_array ($array) {
	return str_replace("\"", "\\\"", json_encode($array));
}

/**
 * Prepare a Json response
 *
 * @param unknown $wo_status
 * @param unknown $wo_comment
 * @param unknown $wo_newparams
 * @param string $log_response
 * @return string
 */
function prepare_json_response($wo_status, $wo_comment, $wo_newparams, $log_response = false) {

	if (! is_array($wo_newparams) && (substr($wo_newparams,0,1) === "{" || substr($wo_newparams,0,1) === "[")){
		$wo_newparams = json_decode($wo_newparams);
	}

	$response = array('wo_status' => $wo_status,
			'wo_comment' => $wo_comment,
			'wo_newparams' => $wo_newparams
	);
	$response = json_encode($response);

	if ($log_response) {
		logToFile("RESPONSE :\n" . pretty_print_json($response) . "\n");
	}
	return $response;
}

/**
 * Modify Generated configuration to be XML compatible
 *
 * @param unknown $config
 * @return string
 */
function modify_generated_configuration ($config) {

	//$config = str_replace("&", AMPERSAND, $config);
	#$config = str_replace("\\n", NEW_LINE, $config);
	$config = trim(preg_replace('/\s+/', '', $config));
	$config .= NEW_LINE;

	return $config;
}

/**
 * Function to find 2 multi-dimentional Arrays' difference
 * NOTE : The Array order matters in function argument
 *
 * @param unknown $array1
 * @param unknown $array2
 * @return Ambigous <number, unknown>
 */
function array_diff_assoc_recursive($array1, $array2)
{
	foreach($array1 as $key => $value)
	{
		if(is_array($value))
		{
			if(!array_key_exists($key, $array2))
			{
				$difference[$key] = $value;
			}
			elseif(!is_array($array2[$key]))
			{
				$difference[$key] = $value;
			}
			else
			{
				$new_diff = array_diff_assoc_recursive($value, $array2[$key]);
				if($new_diff != FALSE)
				{
					$difference[$key] = $new_diff;
				}
			}
		}
		elseif(!array_key_exists($key, $array2) || $array2[$key] != $value)
		{
			$difference[$key] = $value;
		}
	}
	return !isset($difference) ? 0 : $difference;
}

/**
 * Function to search a value in multi-dimentional array
 *
 * @param unknown $needle
 * @param unknown $haystack
 * @return unknown|boolean
 */
function recursive_array_search($needle, $haystack) {
	foreach($haystack as $key => $value) {
		$current_key = $key;
		if($needle === $value OR (is_array($value) && recursive_array_search($needle, $value) !== false)) {
			return $current_key;
		}
	}
	return false;
}

/**
 * Update Asynchronous Task details : To print task details during Process execution
 *
 * @param unknown $args
 * @param unknown $details
 */
function update_asynchronous_task_details($args, $details) {

	$PROCESSINSTANCEID = $args['PROCESSINSTANCEID'];
	$TASKID = $args['TASKID'];
	$EXECNUMBER = $args['EXECNUMBER'];

	logToFile("UPDATE PROCESS SCRIPT DETAILS : $PROCESSINSTANCEID $TASKID $EXECNUMBER \"{$details}\"\n");
	$response = _orchestration_update_process_script_details($PROCESSINSTANCEID, $TASKID, $EXECNUMBER, $details);
}

/**
 *  Dump a PHP variable to the logs for debugging purpose
 * @param $var
 * @param $comment
 */
function debug_dump($var, $comment = '')
{
  ob_start();
  print_r($var);
  $d = ob_get_contents();
  ob_end_clean();
  return "$comment $d\n";
}

function pretty_print_json ($json) {

	$result = '';
	$level = 0;
	$in_quotes = false;
	$in_escape = false;
	$ends_line_level = NULL;
	$json_length = strlen( $json );

	for( $i = 0; $i < $json_length; $i++ ) {
		$char = $json[$i];
		$new_line_level = NULL;
		$post = "";
		if( $ends_line_level !== NULL ) {
			$new_line_level = $ends_line_level;
			$ends_line_level = NULL;
		}
		if ( $in_escape ) {
			$in_escape = false;
		} else if( $char === '"' ) {
			$in_quotes = !$in_quotes;
		} else if( ! $in_quotes ) {
			switch( $char ) {
				case '}': case ']':
					$level--;
					$ends_line_level = NULL;
					$new_line_level = $level;
					break;

				case '{': case '[':
					$level++;
				case ',':
					$ends_line_level = $level;
					break;

				case ':':
					$post = " ";
					break;

				case " ": case "\t": case "\n": case "\r":
					$char = "";
					$ends_line_level = $new_line_level;
					$new_line_level = NULL;
					break;
			}
		} else if ( $char === '\\' ) {
			$in_escape = true;
		}
		if( $new_line_level !== NULL ) {
			$result .= "\n".str_repeat( "\t", $new_line_level );
		}
		$result .= $char.$post;
	}
	return $result;
}

?>