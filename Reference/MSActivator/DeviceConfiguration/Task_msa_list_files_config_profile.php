<?php 

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

$device_id = $context['device_id'];

$cmd = "bash /opt/ubi-jentreprise/bin/api/device/readDeviceById.sh $device_id |grep configurationProfileId";

logToFile("COMMAND TO GET PROFILE ID:" .$cmd."\n");
$result = shell_exec ("$cmd");

if(!preg_match('/\<configurationProfileId\>(\d+)\<\/configurationProfileId\>/',$result,$match))
{
   $response = prepare_json_response(FAILED, "Listing Files Attached From Config Profile Failed" , $context, true);
    echo $response;
    exit;
}

$config_profile_id = $match[1];

if ($config_profile_id == 0){
   $response = prepare_json_response(ENDED, "No Config Profiles Attached to the device", $context, true);
  echo $response;
  exit;
}

$cmd = "bash /opt/ubi-jentreprise/bin/api/deviceconfiguration/listFilesByConfigurationProfileId.sh $config_profile_id|grep return";

logToFile("COMMAND TO GET PROFILE FILES:" .$cmd."\n");
$result = shell_exec ("$cmd");

if(preg_match_all('/\<return\>(.*)\<\/return\>/',$result,$uris) == 0)
{
   $response = prepare_json_response(FAILED, "Listing Files Attached From Config Profile Failed" , $context, true);
    echo $response;
    exit;
}

if(!isset($context['device_objects_uri']))
{
    $context['device_objects_uri'] = array();
}

foreach($uris[1] as $uri)
{
  array_push($context['device_objects_uri'], $uri);
}

$response = prepare_json_response(ENDED, "Files Attached From Config Profile listed Successfully", $context, true);
echo $response;

?>
