<?php
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args()
{
}
$nw_grp_id=$context['nw_grp_id'];

$fe_order_id=$context['fe_order_id'];

if($context['isVpnRequest'] === 'No'){
  $tmf_id="TMF_POC12";
}else{
  $tmf_id="TMF_POC13";
}

$full_url  = "https://www.flx-u.com/flexibleentry-api/api/v1/orderDetail/$tmf_id/BASE/$fe_order_id";
$HTTP_M = "PATCH";

$est=date("yy-m-d");
$context['completionDate']=$est;

$body = array(
   "completion_date" => $est
);

$head='corp: p1=TMFPOC01&cnt=1&d=42a9c684be4950b3b0d6c29645641e350457784ef7cfb4804ec31d9a2f4184a2';

$body = json_encode($body);
$CURL_CMD="/usr/bin/curl";
$curl_cmd = "{$CURL_CMD} -isw '\nHTTP_CODE=%{http_code}' --connect-timeout 60 --max-time 60 -H \"Content-Type: application/json\" -H '{$head}' -u POC_API:POC_API  -X {$HTTP_M} -k '{$full_url}' -d '{$body}'";
//logToFile("Naveen-$curl_cmd");
$response = perform_curl_operation($curl_cmd, "Calling GET HTTP method");
$response = json_decode($response, true);

if ($response['wo_status'] !== ENDED) {
  $response = json_encode($response);
  return $response;
exit;
}

$r_data = json_decode($response["wo_newparams"]["response_body"]);
logToFile(debug_dump($r_data,"**************CURL CMD**********\n"));

task_success('Task OK');
?>