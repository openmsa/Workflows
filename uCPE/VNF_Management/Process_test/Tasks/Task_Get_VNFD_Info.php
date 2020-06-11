<?php
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/ENEA/VNF_Management/common.php';

function list_args()
{
      create_var_def('vnf_descriptor', 'OMBFRef');  
}
$HTTP_M = "POST";

$device_ip = $context['device_ip'];
$port      = $context['port'];
$full_url  = "https://$device_ip$port/REST/v2/ServiceMethodExecution/modules/VnfManager/services/Configuration/methods/getVNFDescriptors";
logToFile("**************VNFD***********\n");
$vnfd_list = curl_http_get($context['sessionToken'], $full_url,"", $HTTP_M);

if($vnfd_list['wo_status'] !== ENDED)
{               
    $vnfd_list = prepare_json_response($vnfd_list['wo_status'], "Failed to Import VNFD", $vnfd_list, true);   
    echo $vnfd_list;
    exit;
}

$vnfd_list = json_decode($vnfd_list['wo_newparams']['response_body'],TRUE);
$selected_vnfd = "";


logToFile(debug_dump($context['vnf_descriptor'],"************VNF descriptor*************\n"));

foreach($vnfd_list as $row)
{
  
  //check if any vnfs matc the chosen descriptor.
  if($context['vnf_descriptor'] == $row["id"])
  {
    $selected_vnfd = $row;
    break;
  } 
}

if($selected_vnfd == "")
{
  echo "Your selected VNF Descriptor was not found please check your ucpeManager";
    exit;
}
$context['selected_vnfd'] = "".json_encode($selected_vnfd);

task_exit(ENDED, "Session Token retreived");