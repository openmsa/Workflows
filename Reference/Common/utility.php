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
			$filename = PROCESS_LOGS_DIRECTORY . "process-" . $context['SERVICEINSTANCEID'] . ".log";
		}
	}
	
	$date = date('Y-m-d H:i:s');
	$to_log = "$date|".$context['PROCESSINSTANCEID']."|$msg";
    if(strstr($msg, "\n")) {
        //ending the process specific logs for pretty print json
        $to_log .= "$date|".$context['PROCESSINSTANCEID']."--|";
    }
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
 * Read only one time the full file and fill all values in one global variable $context['vars_ctx_values']
 * @param unknown $variable
 * @return unknown|boolean
 */
function get_vars_value($variable) {
  global $context;
  if (isset($context['vars_ctx_values'][$variable])){
    return $context['vars_ctx_values'][$variable];
  } else {
    $var = _get_variable_by_name($variable);
    $context['vars_ctx_values'][$variable] = $var;
    return $var;
  }
}

function _get_variable_by_name($name) {
        $msa_rest_api = "system-admin/v1/msa_vars?name={$name}";
        $curl_cmd = create_msa_operation_request(OP_GET, $msa_rest_api);
        $response = perform_curl_operation($curl_cmd, "Get variable $name");
        $response = json_decode($response, true);
	if (isset($response['wo_newparams']['response_body'])) {
	        $inner = json_decode($response['wo_newparams']['response_body'], true);
		return $inner[0]['value'];
	}
	return null;
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
 * Generate a list of all IP addresses between $start and $end (inclusive).
 * For Ex. [1.1.1.1, 1.1.1.5] => 1.1.1.1, 1.1.1.2, 1.1.1.3, 1.1.1.4, 1.1.1.5
 * 
 * @param unknown $start
 * @param unknown $end
 */
function get_ip_range ($start, $end) {

	$start = ip2long($start);
	$end = ip2long($end);
	return array_map('long2ip', range($start, $end));
}

/**
 * Get the Start and End Address of the IP range from CIDR
 * For Ex. [10.0.0.0/24] => 10.0.0.0 - 10.0.0.255
 * 
 * @param unknown $cidr
 * @return Array:Start and End IP Address
 */
function cidr_to_range($cidr) {

	$range = array();
	$cidr = explode('/', $cidr);
	$range[0] = long2ip((ip2long($cidr[0])) & ((-1 << (32 - (int)$cidr[1]))));
	$range[1] = long2ip((ip2long($cidr[0])) + pow(2, (32 - (int)$cidr[1])) - 1);
	return $range;
}

/**
 * Check if 2 CIDRs are over-lapping
 * For Ex. : $cidr1 = 100.64.0.0/10 and $cidr2 = 100.0.0.0/9 => true
 *         : $cidr1 = 100.64.0.0/10 and $cidr2 = 100.128.0.0/9 => false
 * 
 * @param unknown $cidr1
 * @param unknown $cidr2
 * @return boolean
 */
function is_overlapping_cidr($cidr1, $cidr2) {

	$range1 = cidr_to_range($cidr1);
	$startIpNum = ip2long($range1[0]);
	$endIpNum = ip2long($range1[1]);

	$range2 = cidr_to_subnet_and_subnetmask_address($cidr2);
	$netnum  = ip2long($range2['subnet_ip']);
	$masknum = ip2long($range2['subnet_mask']);
	for ($i = $startIpNum; $i < $endIpNum; $i++) {
		if (($i & $masknum) === ($netnum & $masknum)) {
			return TRUE;
		}
	}
	return FALSE;
}

/**
 * Match IP address in a CIDR
 *
 * @param unknown $ip
 * @param unknown $cidr
 * @return boolean
 */
function cidr_match ($ip, $cidr) {

	list ($subnet, $mask) = explode ('/', $cidr);
	if ((ip2long($ip) & ~((1 << (32 - $mask)) - 1) ) == ip2long($subnet)) {
		return true;
	}
	return false;
}

/**
 * Check of the given IP in contains in one list of CIDR
 *
 * @param unknown $ip
 * @param  $cidrs_string is a string with all CIDRs  separated with a coma , like '100.65.0.0/16,100.66.0.0/15,100.68.0.0/14'
 * @return false if the IP is OK, else return the list of conflict CIDRs
 */
function cidr_match_list($ip, $cidrs_string) {
  $errors=array();

  if ($cidrs_string){
    $cidrs_string=preg_replace("/\s+/",'',$cidrs_string); //remove blanc space
    if ($cidrs_string){
      $cidrs=explode(",",$cidrs_string);
      foreach($cidrs as $cidr){
        if (cidr_match($ip, $cidr)){
          //The IP $ip is in the CIDR
          $errors[] = $cidr;
        }
      }
    }
  }
  if ($errors){
    //Error, the IP is in one or more specific CIDR
    return implode(", ",$errors);
  }else{
    // The IP is OK
	  return false;
  }
}


/**
 * Convert Netmask to CIDR prefix
 * For ex. 255.255.255.0 -> 24
 *
 * @param unknown $netmask
 * @return number
 */
function netmask_to_cidr ($netmask) {
	$cidr = 0;
	foreach (explode('.', $netmask) as $number) {
		for (;$number > 0; $number = ($number << 1) % 256) {
			$cidr++;
		}
	}
	return $cidr;
}

/**
 * Check if the String is in CIDR format
 * For ex. 101.0.0.100/24
 *
 * @param unknown $string
 */
function is_cidr ($string) {

	$regex = '/^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])(\/([0-9]|[1-2][0-9]|3[0-2]))$/';
	return (preg_match($regex, $string) > 0);
}

/**
 * Convert CIDR to Subnet and Mask address
 * For ex. if CIDR is 10.0.0.0/24 => 10.0.0.0 255.255.255.0
 *
 * @param unknown $cidr
 * @return multitype:string multitype:
 */
function cidr_to_subnet_and_subnetmask_address ($cidr) {

	list ($subnet_ip, $prefix) = explode ('/', $cidr);
	// Take all 1s upto the prefix and rest of the 32-bits as 0s
	$binary_mask = "";
	for ($i = 0; $i < $prefix; $i++) {
		$binary_mask = $binary_mask . "1";
	}
	for ($i = $prefix; $i < 32; $i++) {
		$binary_mask = $binary_mask . "0";
	}

	// Out of 32-bits,convert each 8-bits in integer form
	// Add a "." after first 3 integers
	$binary_octect = "";
	$subnet_mask = "";
	for ($i = 0; $i < 32; $i = $i + 8) {
		$binary_octect = substr($binary_mask, $i, 8);
		$subnet_mask = $subnet_mask . intval($binary_octect, 2);
		if ($i != 24) {
			$subnet_mask = $subnet_mask . ".";
		}
		$binary_octect = "";
	}
	$response = array('subnet_ip' => $subnet_ip, 'subnet_mask' => $subnet_mask);
	return $response;
}

/** check if address is in network
 @note	IPV4 Only
 @param	addr		address to check
 @param	net         network
 @param	mask		network mask
 @return	true if addr is in network
 */
function address_is_in_network($addr, $net, $mask = '255.255.255.255')
{
	// case where IP is with /32 CIDR
	if (strpos($addr, '/')) {
		$tmp = explode('/', $addr);
		$addr = $tmp[0];
	}

	$addrnum = ip2long($addr);
	$netnum  = ip2long($net);
	$masknum = ip2long($mask);

	return (($addrnum & $masknum) === ($netnum & $masknum));
}


/**
 * Function calcul the subnet IP of the given IP and mask ('255.255.255.255')
 *
 * @param  addr    is an IP like '10.12.25.12'
 * @param  netmask  is the mask like '255.255.255.0'
 * @return the subnet IP (the first IP of the subnet) like '10.12.25.0'
 */
function get_subnet_from_IP_and_netmask($addr, $netmask )
{
  $ip_int = ip2long($addr);
  $netmask_int = ip2long($netmask);
  // Network is a logical AND between the address and netmask
  $network_int = $ip_int & $netmask_int;
  $network = long2ip($network_int);
  return $network;
}

/**
* Function to convert a cidr mask (ex: 24) to  netmask (ex: 255.255.255.0)   :
 * @param   cidr_mask  is the mask in CIDR (integer like 24)
 * @return  netmask    is the mask like '255.255.255.0'
*/
function cidrmask_to_netmask($cidr_mask){
  $netmask = str_split (str_pad (str_pad ('', $cidr_mask, '1'), 32, '0'), 8);
  foreach ($netmask as &$element){
    $element = bindec ($element);
  }
  return join ('.', $netmask);
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

	$details = preg_replace ("/\"/",' ',$details);  //remove " to prevent somme error
	$details = preg_replace ("/\'/",' ',$details);  //remove ' to prevent somme error
	$details = preg_replace ("/\(/",' ',$details);  //remove ( to prevent somme error
	$details = preg_replace ("/\)/",' ',$details);  //remove ) to prevent somme error
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

function getIdFromUbiId ($ubi_id){
        $num_id = preg_replace('/[A-Z]+/', '', $ubi_id);
        return $num_id;
}

?>
