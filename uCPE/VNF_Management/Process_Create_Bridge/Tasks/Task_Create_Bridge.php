<?php
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/ENEA/VNF_Management/common.php';

function list_args()
{
      create_var_def('bridge_name', 'String');  
      create_var_def('interface_name', 'String');  
      create_var_def('bridge_subType', 'String');  
      create_var_def('ucpe_devices', 'OBMFRef');
}
$HTTP_M = "POST";
//generate UUI for VNF id
$uuid            = uuid(openssl_random_pseudo_bytes(16));
$device_id = substr($context['device_id'], 3);
$device_ip = $context["device_ip_address"];
//$port      = $context['port'];
$nfvacess  = $context['ucpe_devices'];
$bridge_name = $context['bridge_name'];
$bridge_subType= $context['bridge_subType'];
$interface_name= $context['interface_name'];


logToFile("**************Bridge Create***********\n");

//========================================================================================
$body = array(
  "object"=>array(
      "id"            => $uuid,
      "name"        => $bridge_name ,
     "ovsBridgeType"=>array(
    "vnfMgmt" => null,
    "dataPlane" => array(
      "subType" => $bridge_subType,
      "flowRule" =>array(),
      "physicalInterface" => array(array(
        "name" => $interface_name,
        "_internal_objectType" => "VcpeAgent/OvsBridge_ovsBridgeType_dataPlane_physicalInterface"
      )),
      "_internal_objectType" => "VcpeAgent/OvsBridge_ovsBridgeType_dataPlane"
    ),
    "inbandMgmt" => null,
    "_internal_objectType" => "VcpeAgent/OvsBridge_ovsBridgeType"
  ),
  "_internal_objectType"=>"VcpeAgent/OvsBridge"
));
$body = json_encode($body);
//========================================================================================

$full_url ="https://$device_ip:443/REST/v2/ServiceMethodExecution/modules/EMS/services/Config/methods/createObject?elementId=$nfvacess";

$create_bridge = curl_http_get($context['sessionToken'], $full_url,$body, $HTTP_M);

/*if($create_bridge ['wo_status'] !== ENDED)
{               
    $create_bridge = prepare_json_response($create_bridge ['wo_status'], "Failed to create bridge", $create_bridge , true);   
    echo $vnfd_list;
    exit;
}*/

//$response = execute_command_and_verify_response($device_id, CMD_CREATE, $body, "CREATE VNF_bridge");

//$ms_url = "http://localhost/ubi-api-rest/ordercommand/store/configuration/$device_id/CREATE";
//$create_b_ms= curl_http_get("", $ms_url ,$body, "PUT");
logToFile(debug_dump($create_bridge ,"=======================CREATEBR========================"));

/*if($create_b_ms['wo_status'] !== ENDED)
{               
    $create_b_ms= prepare_json_response($create_bridge ['wo_status'], "Failed to create bridge", $create_b_ms, true);   
    echo $create_b_ms;
    exit;
}*/

task_exit(ENDED, "Bridge created successfully");