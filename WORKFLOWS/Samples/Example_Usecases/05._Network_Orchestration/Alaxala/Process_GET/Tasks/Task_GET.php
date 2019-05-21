<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/Common/curl_performer.php';

function list_args()
{
 
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

$interface_array = $interfaces['interface'];

unset($context['interfaces']);

foreach ($interface_array as &$itf) {
  //logToFile($itf['name']);
  $name = $itf['name'];
  if (strpos($name, '.') !== false) {
     $context['vlans'][]['name']=$itf['name'];
  } else {
     $context['interfaces'][]['name']=$itf['name'];
  }
}

if ($response_array['wo_status'] == ENDED) {

      
	task_success('Discovery of interfaces OK');
}
else{
	task_error('Task FAILED');
}
exit;
?>