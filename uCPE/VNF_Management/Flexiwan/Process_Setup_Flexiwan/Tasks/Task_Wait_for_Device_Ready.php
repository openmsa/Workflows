<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args()
{
}


/**
* call to Microservice IMPORT to synchronize the MSA database with the PFsense firewall*/
$device_id = substr($context['device_id'], 3);
$device_ready = false;
$arr= array("Devices");

$x = 0;
while($device_ready != true)
{
   if($x == 20)
   {
	task_error('Flexi-edge device still not in ready state please check in Fleximanager');
	exit;
   }
   $response = import_objects($device_id, $arr);
   $response = json_decode($response, true);

   if ($response['wo_status'] !== ENDED) {
     $response = json_encode($response);
     echo $response;
     exit;
   }

   $flexiwans = $response["wo_newparams"]["Devices"];
   foreach($flexiwans as $row)
   {  
     if($row["object_id"] == $context["flex_vnfid"])
     {
         if(!isset($row["device_state"]))
         {
            //the device is still not ready repeat the 
            sleep(20); //sleep for 20 seconds before runnign check agian
         }
         else
         {
            $device_ready = true;
         }
     } 
   }
   $x++;

}  
   
$response = prepare_json_response(ENDED, "Flexi-edge device is now in a ready state", $context, true);
echo $response;

?>