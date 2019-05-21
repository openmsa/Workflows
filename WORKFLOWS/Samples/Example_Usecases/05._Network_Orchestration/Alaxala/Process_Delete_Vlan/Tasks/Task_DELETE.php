<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/Common/curl_performer.php';

function list_args()
{
  create_var_def('interface', 'String');
  create_var_def('subinterfaced', 'String');

}

function url_encode_ipop($input_string){

$output_string = str_replace(' ','%20',$input_string);
$output_string = str_replace('/','%2F',$output_string);

return $output_string;

}


check_mandatory_param('interface');
check_mandatory_param('subinterfaced');

$ip = $context['device_ip_address'];

/***   We do NOT use urlencode (see SUPFUJ-155)***/
//$interface = urlencode($context['interface']);
$interface = $context['interface'];
$interface_URL=url_encode_ipop($interface);

$subinterfaced = $context['subinterfaced'];

$host = "/restconf/data/ietf-interfaces:interfaces/interface=$interface_URL.$subinterfaced";

$host = 'http://'.$ip.':8080'.$host;

$command = "curl --silent -H 'content-type:application/yang-data+json' -X DELETE '$host'";

logToFile("delete VLAN curl command:\n".$command);

$original_response = perform_curl_operation($command, "Delete VLAN");
$response = json_decode($original_response, true);

if ($response['wo_status'] == ENDED) {

	task_success('Deletion of the VLAN OK ');
}
else{
	task_error('Task FAILED ');
}
?>