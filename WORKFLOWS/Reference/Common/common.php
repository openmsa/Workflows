<?php

/**
 * define shorthand directory separator constant
 */
if (!defined('DS')) {
  define('DS', DIRECTORY_SEPARATOR);
}

/**
 * set COMMON_DIR to absolute path to common library files.
 * Sets COMMON_DIR only if user application has not already defined it.
 */
if (!defined('COMMON_DIR')) {
  define('COMMON_DIR', dirname(__FILE__) . DS);
}

/**
 * set LIBRARY_DIR to absolute path to common library files.
 * Sets LIBRARY_DIR only if user application has not already defined it.
 */
if (!defined('LIBRARY_DIR')) {
  define('LIBRARY_DIR', dirname(__FILE__) . DS . 'Library' . DS);
}

require_once COMMON_DIR . 'networking_common.php';
require_once COMMON_DIR . 'workflows_common.php';
require_once COMMON_DIR . 'micro_services_common.php';
require_once LIBRARY_DIR . 'msa_common.php';

// Common header for all tasks
$var_defs = array();
function usage($cmd) {
  global $context;

  $usage = <<<EOT
Usage: {$cmd} --<function> {<JSON formatted context>}
Will call the PHP <function> with the given context

{$cmd} --get_vars_definition
       Returns the JSON formated list of variables used by this PHP

{$cmd} --execute {<JSON formatted context>}
       Execute this PHP task with the corresponding context
       Returns the JSON formated context as updated by this task
EOT
;

  $msg = prepare_json_response(FAILED, $usage, $context, true);
  echo $msg;
  exit();
}

if (!isset($argv[1])) {
  usage("php {$argv[0]}");
}

$fct = str_replace("--", "", $argv[1]);
if ($fct !== "execute" && !function_exists($fct)) {
  usage("php {$argv[0]}");
}

// Check all parameters given to the task
if (isset($argv[2])) {
  require_once "$argv[2]";
}
else {
  $context = array();
}

if ($fct !== "execute") {
  call_user_func($fct);
  exit();
}

// End of Common header
function get_vars_definition() {
  global $var_defs;
  if (function_exists('list_args'))
  {
    list_args();
  }
  else
  {
    $var_defs = array();
  }
  $vars = json_encode($var_defs);
  echo "$vars";
}

//
function create_var_def($name, $type = 'String', $values = null, $default_value = '') {
  global $var_defs;
  if (empty($values) || !is_array($values)) {
    $values = array();
  }
  $var_def = array(
      'name' => $name,
      'type' => $type,
      'values' => $values,
      'default_value' => $default_value
  );
  $var_defs[] = $var_def;
}

//
function check_mandatory_param($param_name) {
  global $context;

  if (! isset($context[$param_name])) {
    $response = prepare_json_response(FAILED, "Mandatory parameter $param_name is not present", $context, true);
    echo $response;
    exit();
  }
}

//
function task_exit($status, $message) {
  global $context;
  $response = prepare_json_response($status, $message, $context, true);
  echo $response;
  exit();
}

// when a sub-call success and you want to end the task
function task_success($message) {
  global $context;
  logTofile(debug_dump($message, "Message"));
  $response = prepare_json_response(ENDED, $message, $context, true);
  echo $response;
  exit;
}

// when a sub-call fail and you want to end the task
function task_error($message) {
  global $context;
  logTofile(debug_dump($message, "Error message"));
  $response = prepare_json_response(FAILED, $message, $context, true);
  echo $response;
  exit;
}

?>
