<?php
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args()
{
  }
   
/*     
global $CURL_CMD;

$url_IP_provider = $context['url_IP_provider'];
 
$curl_cmd = "{$CURL_CMD} -k -s -XGET ".$url_IP_provider;
logToFile('Curl Request : ' . $curl_cmd);


$response = perform_curl_operation($curl_cmd, "LIST IP");

$response = json_decode($response, true);
$wo_newparams = $response['wo_newparams'];


$ip_list_string = $wo_newparams['response_raw_headers'];
$ip_list = explode("\n", $ip_list_string);
*/

$ip_list = explode(" ", "10.3.4.5 32.9.34.5 98.3.4.5");


$context['ip_list'] = $ip_list;

task_success('Task OK');

?>