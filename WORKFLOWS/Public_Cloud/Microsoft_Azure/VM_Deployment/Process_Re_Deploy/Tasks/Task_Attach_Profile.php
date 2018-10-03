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
  /** 
   * You can use var_name convention for your variables
   * They will display automaticaly as "Var Name"
   * The allowed types are:
   *    'String', 'Boolean', 'Integer', 'Password', 'IpAddress',
   *    'IpMask', 'Ipv6Address', 'Composite', 'OBMFRef', 'Device'
   *
   * Add as many variables as needed
   */ 
 
   
}
$device_ref=$context['device_id'];
$profile_ref=$context['profile_ref'];
sleep(10);

$response =_profile_attach_to_device_by_reference ($profile_ref, $device_ref);

$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}
	

$wo_comment = $response['wo_comment'];
$response = prepare_json_response(ENDED, "Profile $profile_ref attached to Device $device_ref.\n$wo_comment", $context, true);
echo $response;


sleep(15);
?>
