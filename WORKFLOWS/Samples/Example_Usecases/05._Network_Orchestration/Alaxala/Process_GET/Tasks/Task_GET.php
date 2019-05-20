<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/Common/curl_performer.php';

function list_args()
{
   create_var_def("interfaces.0.name", "String");
}

$ip = $context['device_ip_address'];
$host = "http://$ip:8080/restconf/data/ietf-interfaces:interfaces";
$command = "curl  --silent  --connect-timeout 60 --max-time 60 -H 'Content-Type:application/json' -XGET $host";

logToFile("CURL:\n".$command);

$response = perform_curl_operation($command, "Get VLAN");
//logToFile("*****".$response);

$response_array = json_decode($response, true);

$wo_newparams = $response_array['wo_newparams'];
$response_raw_headers_array = json_decode($wo_newparams['response_raw_headers'], true);

$interfaces = $response_raw_headers_array['ietf-interfaces:interfaces'];

logToFile(debug_dump($interfaces, "*********** INTERFACES: \n"));

$interface_array = $interfaces['interface'];

unset($context['interfaces']['name']);

foreach ($interface_array as &$itf) {
  logToFile($itf['name']);
  $context['interfaces'][]['name']=$itf['name'];
  
}

if ($response_array['wo_status'] == ENDED) {
	logToFile("\n***** ENDED");
       	//$json_response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, "");
	//echo $json_response;
	//logToFile("\n***** json_response:\n".$json_response);

	task_success('Discovery of interfaces OK');
}
else{
	task_error('Task FAILED');
}
exit;
?>