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

$ip_list = array('23.0.0.1', '23.0.0.2', '23.0.0.3', '23.0.0.4', '23.0.0.5', '23.0.0.6', '23.0.0.7', '23.0.0.8', '23.0.0.9', '23.0.0.10', '23.0.0.11', '23.0.0.12', '23.0.0.13', '23.0.0.14', '23.0.0.15', '23.0.0.16', '23.0.0.17', '23.0.0.18');


$context['ip_list'] = $ip_list;

task_success('Task OK');

?>