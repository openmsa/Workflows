<?php
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/ENEA/VNF_Management/common.php';

function list_args()
{}

$HTTP_M = "POST";

$device_ip = $context['device_ip'];
$port      = $context['port'];
$ucep_device_id = $context['device_data']["object_id"];
$body = array(
		"parentKey"=>null,
		"query"=>null,
		"store"=>null,
		"type"=>"VcpeAgent/OvsBridge",
		  "parentType"=>null
);

$body = json_encode($body);
//logToFile(debug_dump($ucep_device_id ,"*********** UCPE D DATA**************\n"));

$full_url  = "https://$device_ip$port/REST/v2/ServiceMethodExecution/modules/EMS/services/Config/methods/getObjectList?elementId=$ucep_device_id";
logToFile("**************Connection Info***********\n");

$connection_info = curl_http_get($context['sessionToken'], $full_url,$body, $HTTP_M);

/*
$x = $connection_info['wo_newparams']['response_body'];
$y = json_decode($x,TRUE);
logToFile(debug_dump($y['results'],"*********** UCPE D DATA**************\n"));

echo "test fin";
exit;
*/
if($connection_info['wo_status'] !== ENDED)
{               
    $connection_info = prepare_json_response($connection_info['wo_status'], "Failed to Import VNFD", $connection_info, true);   
    echo $connection_info;
    exit;
}

$context['connection_info'] = json_decode($connection_info['wo_newparams']['response_body'],TRUE);


task_exit(ENDED, "Bridge details retreived");	
?>