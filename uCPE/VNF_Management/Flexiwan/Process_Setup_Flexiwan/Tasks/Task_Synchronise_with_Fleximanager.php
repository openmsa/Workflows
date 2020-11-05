<?php

/**
 * This file is necessary to include to use all the in-built libraries of /opt/fmc_repository/Reference/Common
 */
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/Common/Library/msa_common.php';

/**
 * List all the parameters required by the task
 */
function list_args()
{
   create_var_def('device_id', 'Device');
   create_var_def('exec_delay', 'Integer');
}
$exec_delay = $context['exec_delay'];
sleep($exec_delay);

if(isset($parameters) ){
    $context['device_id'] = $parameters['device_id'];
 }
check_mandatory_param("device_id");

$device_id = substr($context['device_id'], 3);


/**
* call to Microservice IMPORT to synchronize the MSA database with the PFsense firewall*/
$arr= array("Devices");
$response = import_objects($device_id, $arr);


//$response = _device_read_by_id($device_id);
$response = json_decode($response, true);


if ($response['wo_status'] !== ENDED) {
  $response = json_encode($response);
  echo $response;
  exit;
}

$temp_flex_id = "";
$temp_flex_org = "";
$context["flex_vnfid"] = "";
$context["flex_vnfid2"] = "";
$context["flex_org"] = "";
$flexiwans = $response["wo_newparams"]["Devices"];
foreach($flexiwans as $row)
{
  

  if($row["fromToken"] =="vnf" && $row["isApproved"] == "false")
  {
    $context["flex_vnfid"] = $row["object_id"];
          $context["flex_org"] = $row["org"];

  }
  elseif($row["fromToken"] =="vnf")
  {
    $temp_flex_id = $row["object_id"];
    $temp_flex_org =  $row["org"];
  }

  if($row["fromToken"] =="msk2")
  {
    $context["flex_vnfid2"] = $row["object_id"];
  }
 
}

if($context["flex_vnfid"] == "")
{
  $context["flex_vnfid"] = $temp_flex_id;
        $context["flex_org"] = $temp_flex_org;
}

if( $context["flex_vnfid"] == "") {
  task_exit(ERROR, "Flexiwan VNF id not found please check VNF is up and running correctly");
  exit;
}

task_exit(ENDED, "Synchronisation to Firewall Successfull");

?>
