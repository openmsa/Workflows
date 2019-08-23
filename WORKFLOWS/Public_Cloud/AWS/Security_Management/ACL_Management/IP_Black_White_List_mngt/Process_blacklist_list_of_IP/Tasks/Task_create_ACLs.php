<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args()
{
 
}

$device_id = substr($context['aws_region'], 3);

$ip_list = $context['ip_list'];
$ip_count = count($ip_list);
logToFile($ip_count. " IP address to blacklist");

$acl_to_create_count = $ip_count / 18;
logToFile($acl_to_create_count. " Network ACL to create");

$vpc_id = $context['vpc_id'];

$acl_array = array();
$acl_count = 0;
for ($acl_count = 0; $acl_count <= $acl_to_create_count; $acl_count++) {
  $acl_id = create_acl($device_id, $vpc_id, $context);
  array_push($acl_array, $acl_id);
} 

logTofile(debug_dump($acl_array, "ACL_ARRAY"));
$context['acls'] = $acl_array;


function create_acl($device_id, $vpc_id, $context) {

  logToFile('create Network ACL for VPC '.$vpc_id);
  $micro_service_vars_array = array();
  $micro_service_vars_array['vpc_id'] = $vpc_id;
  $network_acl = array('network_acl' => array('0' => $micro_service_vars_array));
 
  $response = execute_command_and_verify_response($device_id, CMD_CREATE, $network_acl, "CREATE Network ACL");

  $response = json_decode($response, true);
  
  if ($response['wo_status'] == ENDED) {
        logToFile('*******************************');        
	
        logToFile('extract ACL_ID from response');

	$wo_comment=$response['wo_comment'];
	$resp=json_decode($wo_comment,true);
	$id=$resp['NetworkAcl']['NetworkAclId']; 
        logToFile('ACL_ID : '.$id);
     
        
	logToFile('*******************************');
	return $id;
  } 
}


task_success('Task OK: '.$acl_count.' Network ACL created in VPC '.$vpc_id );

?>