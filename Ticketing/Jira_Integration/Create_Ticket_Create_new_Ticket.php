<?php
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args()
{
    create_var_def('jira_device_id', 'Device');
	create_var_def('jira_project', 'String');
	create_var_def('summary', 'String');
	create_var_def('description', 'String');
}
$device_id=$context['jira_device_id'];
$device_id = getIdFromUbiId ($device_id);
$response = _device_read_by_id($device_id);
$response = json_decode($response, true);
logToFile(debug_dump($response,"**************Response**********\n"));
if ($response['wo_status'] !== ENDED) {
  $abc=$response['wo_status'];
  logToFile("nav==$abc==");
  $response = json_encode($response);
  echo $response;
  exit;
}
$device_ip = $response['wo_newparams']['managementAddress'];

$full_url  = "http://$device_ip:80/rest/api/2/issue";
$HTTP_M = "POST";



$project = $context['jira_project'];
$priority = "1";
$issuetype = 10003;
$summary = $context['summary'];
$description = $context['description'];

$body = array(
"fields" => array(
  "project" => array( "id" => $project),
  "summary" => $summary,
  "priority" => array( "id" => $priority),
  "issuetype" => array( "id" => $issuetype ),
  "description" => $description
));

logToFile("Executing the Jira API");
$body = json_encode($body);
$CURL_CMD="/usr/bin/curl";
$curl_cmd = "{$CURL_CMD} -isw '\nHTTP_CODE=%{http_code}' --connect-timeout 60 --max-time 60 -H \"Content-Type: application/json\"  -u demo_user:demo_user  -X {$HTTP_M} -k '{$full_url}' -d '{$body}'";

$response = perform_curl_operation($curl_cmd, "Calling GET HTTP method");
$response = json_decode($response, true);
logToFile("result from Jira");
if ($response['wo_status'] !== ENDED) {
  $response = json_encode($response);
  return $response;
exit;
}

$r_data = json_decode($response["wo_newparams"]["response_body"]);
logToFile(debug_dump($r_data->id,"**************CURL CMD**********\n"));

$context['jira_issue_id'] = $r_data->id; 

task_success('Task OK');
?>