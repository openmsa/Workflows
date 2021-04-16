<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

//Define variables
$device_id = $context['device_id'];
$playbook = $context['playbook'];

//Sync out Ansible host to read playbook file content
$response = json_decode(synchronize_objects_and_verify_response($device_id), true);
if ($response['wo_status'] !== ENDED) {
  echo $response;
  exit;
}

$response = json_decode(synchronize_objects_and_verify_response($device_id), true);
if ($response['wo_status'] !== ENDED) {
  echo $response;
  exit;
}

//Read playbook file content
$response = json_decode(import_objects($device_id, array('Read_playbook_file')), True);
$object_ids_array = $response['wo_newparams']['Read_playbook_file'];
$object_params = current($object_ids_array);

//Create array from string
$playbook_array = explode('|', $object_params['text']);

//$vars_array is an array that contains strings with extra-args variables
$vars_array = array();

/*$playbook_variables contains extracted variables like 
array("var_name1" => array("var_name2")
*/
$playbook_variables = array();

//Just bool flag for parser
$is_section = False;

//Extract lines with extra args
foreach ($playbook_array as $line) {
  if ($is_section and preg_match("/$section_end_pattern/", $line) === 1) {
      $is_section = False;    
    }
  if ($is_section) {
      $vars_array[] = trim($line);
    }
  if (preg_match('/(\s+?)vars_prompt.+/', $line, $matches) === 1) {
      $is_section = True;
      $intention = $matches[1];
      $section_end_pattern = '^'.$intention.'\S';
    }
  if (preg_match('/\s*?-\s*?hosts:(.+?)$/', $line, $matches) === 1) {
      $context['ansible_hosts'] = $matches[1];    
    }
}

//Extract variables from var lines
$var_name = '';
foreach ($vars_array as $line) {
  if (strpos($line, '- name') === 0) {
    $temp_array = explode(':', $line);
    $var_name = trim($temp_array[1]);
    $playbook_variables[$var_name] = array();
  } else {
    $temp_array = explode(':', $line);
    $playbook_variables[$var_name][trim($temp_array[0])] = trim(trim($temp_array[1]));
  }
}

$context['playbook_variables'] = $playbook_variables;


task_success('Task OK');
?>