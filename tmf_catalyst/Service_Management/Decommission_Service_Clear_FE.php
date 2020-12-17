<?php
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args()
{
}
/*$device_id='UBI1289';
$nw_grp_id="";
$vpn_id="";
$ho_suborder_id=$context['ho_suborder_id'];
$vpn_suborder_id=$context['vpn_suborder_id'];

$device_id = getIdFromUbiId ($device_id);
$response = _device_read_by_id($device_id);
$response = json_decode($response, true);
logToFile(debug_dump($response,"**************Response**********\n"));
if ($response['wo_status'] !== ENDED) {
  $response = json_encode($response);
  echo $response;
  exit;
}
$device_ip = $response['wo_newparams']['managementAddress'];
$fe_order_id=$context['fe_order_id'];

$full_url  = "https://$device_ip/flexibleentry-api/api/v1/orderDetail/TMF_POC_03/BASE/$fe_order_id";
$HTTP_M = "PATCH";

$est=date("yy-m-d");


$body = array(
//   "nw_grp_id" =>"$nw_grp_id",
//   "ho_suborder_id"=>"$ho_suborder_id",
//   "vpn_id" => "$vpn_id",
//   "vpn_suborder_id" => "$vpn_suborder_id",
  "ActualDeliveryDate"=>"",
  "LineId"=>"",
  "NW_Gr_ID"=>"",
  "VPN-ID"=>"",
  "ubiqubeServiceId" => "",
   "completion_date" => ""
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
*/
task_success('Task OK');
?>