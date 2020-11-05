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
 
  create_var_def('url_category', 'String');
}

$cat=$context['url_category'];
$device_id=$context['device_id'];
$device_id=getIdFromUbiId ($device_id);
$fqdns = array();

if( $cat === 'Games' || $cat === 'Sports'){
$fqdns[0]['url']='www.espn.com';
$fqdns[0]['name']='sp1';
$fqdns[1]['url']='espn.com';
$fqdns[1]['name']='sp2';
$grp_name="spg";
}
elseif ($cat === 'Social Networking'){

$fqdns[0]['url']='www.facebook.com';
$fqdns[0]['name']='fb1';
$fqdns[1]['url']='www.fb.com';
$fqdns[1]['name']='fb2';
$fqdns[2]['url']='facebook.com';
$fqdns[2]['name']='fb3';
$fqdns[3]['url']='fb.com';
$fqdns[3]['name']='fb4';
$grp_name='sng';
}


$obs=array();
$index=0;

foreach($fqdns as $fqdn){
$objects=array();
$objects['type']='fqdn';
$objects['fqdn']=$fqdn['url'];
$name=$fqdn['name'];
$obs[$index]['member']=$name;
$index++;
$cmd_obj=array("address_object" => array("$name" => $objects));
$response = execute_command_and_verify_response($device_id, CMD_CREATE, $cmd_obj, "ADDRESS CREATE");
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}
}

$mems=array("members" => $obs);


$cmd_obj=array("address_group" => array("$grp_name" => $mems));
$response = execute_command_and_verify_response($device_id, CMD_CREATE, $cmd_obj, "ADDRESS grp CREATE");
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}
$context['grp_name']=$grp_name;

/**
 * End of the task (choose one)
 */
task_success("Address objects created for category: $cat");

?>