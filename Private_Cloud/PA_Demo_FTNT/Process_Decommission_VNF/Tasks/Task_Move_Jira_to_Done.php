<?php
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args()
{}

$device_id = getIdFromUbiId($context['jira_device_id']);
$response = _device_read_by_id($device_id);
$response = json_decode($response, true);

if ($response['wo_status'] !== ENDED) {
  $response = json_encode($response);
  echo $response;
  exit;
}
$device_ip = $response['wo_newparams']['managementAddress'];
$issue_id = $context['jira_issue_id'] ;

$full_url  = "http://$device_ip:80/rest/api/2/issue/{$issue_id}/transitions";
$HTTP_M = "POST";

$body = array(
"transition" => array("id" => "21"));


$body = json_encode($body);
$CURL_CMD="/usr/bin/curl";
$curl_cmd = "{$CURL_CMD} -isw '\nHTTP_CODE=%{http_code}' --connect-timeout 60 --max-time 60 -H \"Content-Type: application/json\"  -u demo_user:demo_user  -X {$HTTP_M} -k '{$full_url}' -d '{$body}'";

$response = perform_curl_operation($curl_cmd, "Calling GET HTTP method");
$response = json_decode($response, true);

if ($response['wo_status'] !== ENDED) {
  $response = json_encode($response);
  return $response;
exit;
}


task_success('Jira Issue updated to Done');
?>