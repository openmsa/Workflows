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
	create_var_def('id', 'Integer');
	create_var_def('src_ip', 'String');
	create_var_def('dst_port', 'Integer');
}



// read the ID of the selected managed entity  
$devices = $context['devices'];

foreach ($devices as $device) {
  $device_id = $device['id'];
  // extract the database ID
  $devicelongid = substr($device_id, 3);

  logToFile("update device $devicelongid");

  /**
   * build the Microservice JSON params for the CREATE
   */
  $micro_service_vars_array = array();
  $micro_service_vars_array['object_id'] = $context['id'];
  $micro_service_vars_array['src_ip'] = $context['src_ip'];
  $micro_service_vars_array['dst_port'] = $context['dst_port'];

  $object_id = $context['id'];

  $simple_firewall = array('simple_firewall' => array($object_id => $micro_service_vars_array));


  /**
   * call the CREATE for simple_firewall MS for each device
   */
  $response = execute_command_and_verify_response($devicelongid, CMD_CREATE, $simple_firewall, "CREATE simple_firewall");
  $response = json_decode($response, true);
  if ($response['wo_status'] === ENDED) {
    if (isset($context['rules'])) {
      $index = count($context['rules']);
    } else {
      $index = 0;
    }

    $context['rules'][$index]['delete'] = false;
    $context['rules'][$index]['id'] = $context['id'];
    $context['rules'][$index]['src_ip'] = $context['src_ip'];
    $context['rules'][$index]['dst_port'] = $context['dst_port'];

    $response = prepare_json_response($response['wo_status'], $response['wo_comment'], $context, true);
    echo $response;
  } else {
    task_exit(FAILED, "Policy update failed");
  }
}
/**
 * End of the task do not modify after this point
 */
task_exit(ENDED, "".$context['src_ip']." -> ".$context['dst_port'] . " blocked");

?>