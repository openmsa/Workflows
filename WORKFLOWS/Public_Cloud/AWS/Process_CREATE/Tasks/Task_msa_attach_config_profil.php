<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args() {
	create_var_def('conf_profile_reference', 'String');
	create_var_def('mon_profile_reference', 'String');
}


$PROCESSINSTANCEID = $context['PROCESSINSTANCEID'];
$EXECNUMBER = $context['EXECNUMBER'];
$TASKID = $context['TASKID'];
$process_params = array('PROCESSINSTANCEID' => $PROCESSINSTANCEID,
						'EXECNUMBER' => $EXECNUMBER,
						'TASKID' => $TASKID);

$device_id = substr($context['device_id'], 3);
$device_reference = $context['device_id'];

if (isset($context['conf_profile_reference'])) {
  $conf_profile_ref = $context['conf_profile_reference'];
  $response = _profile_attach_to_device_by_reference ($conf_profile_ref, $device_reference );
  $response = json_decode($response, true);
  if ($response['wo_status'] !== ENDED) {
    $response = json_encode($response);
    echo $response;
  }
}

if (isset($context['mon_profile_reference'])) {
  $mon_profile_reference = $context['mon_profile_reference'];
  $response = _profile_attach_to_device_by_reference ($mon_profile_reference, $device_reference );
  $response = json_decode($response, true);
  if ($response['wo_status'] !== ENDED) {
    $response = json_encode($response);
    echo $response;
  }

}
$response = prepare_json_response(ENDED, "Configuration and Monitoring profile attached.\n", $context, true);
echo $response;

?>