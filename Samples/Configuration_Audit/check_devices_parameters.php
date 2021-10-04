<?php
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args()
{
  create_var_def('deviceid.0.ID', 'Device');
  create_var_def('CheckParams.0.ObjectName', 'String');
  create_var_def('CheckParams.0.ParameterName', 'String');
  create_var_def('CheckParams.0.ParameterValue', 'String');
}

$message="";
if (!empty($context['deviceid'])){
  $TaskStatus = true;
  $created_object_ids = array();
  
  /**
   * loop through the parameters to check
   */
  foreach ($context['CheckParams'] as $CheckParamsRow) {

    /**
     * loop through the list of devices
     */
    foreach ($context['deviceid'] as $deviceidRow) {
      $devicelongid = substr($deviceidRow['ID'], 3);

      logToFile("--------------------------------------------------------------------");
      logToFile("-------------------Audit ".$CheckParamsRow['ParameterName'] .$deviceidRow['ID']);

      $array = array($CheckParamsRow['ObjectName']);
      
      /*
       * import the micro-service to audit
       */
      $response = import_objects($devicelongid, $array);

      $response = json_decode($response, true);
      if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
      }

      $objects = $response['wo_newparams'][$CheckParamsRow['ObjectName']];

      $match=false;
      foreach ($objects as $object => $params){
	if ($params[$CheckParamsRow['ParameterName']] == $CheckParamsRow['ParameterValue']) {
    	  $message .= $deviceidRow['ID']." has ".$CheckParamsRow['ParameterName']." set to ".$CheckParamsRow['ParameterValue']."\n";
  	  $match=true;
	  break;
	}
      }

      if (!$match) {
	$message .= $deviceidRow['ID']." does not have ".$CheckParamsRow['ParameterName']." set to ".$CheckParamsRow['ParameterValue']."\n";
	$TaskStatus = false;
      }
      update_asynchronous_task_details($context, $message);
   }
}

if (!$TaskStatus){
	echo prepare_json_response(FAILED, $message, $context, true);
}
else {
	echo prepare_json_response(ENDED, $message, $context, true);
}

} 

else {
echo prepare_json_response(ENDED, 'No device to audit', $context, true);
}
?>
