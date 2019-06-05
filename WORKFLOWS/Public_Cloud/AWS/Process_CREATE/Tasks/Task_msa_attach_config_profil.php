<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
//require_once '/opt/fmc_repository/Process/Reference/Common/Library/profile_rest.php';

function list_args() {
	create_var_def('conf_mon_profiles.0.reference', 'String');
}

check_mandatory_param('conf_mon_profiles');

$PROCESSINSTANCEID = $context['PROCESSINSTANCEID'];
$EXECNUMBER = $context['EXECNUMBER'];
$TASKID = $context['TASKID'];
$process_params = array('PROCESSINSTANCEID' => $PROCESSINSTANCEID,
						'EXECNUMBER' => $EXECNUMBER,
						'TASKID' => $TASKID);

$device_id = substr($context['device_id'], 3);
$device_reference = $context['device_id'];

if (isset($context['conf_mon_profiles'])) {
	for ($i = 0; $i < count($context['conf_mon_profiles']); $i++) 
	{
		$profile_reference = $context['conf_mon_profiles'][$i]['reference'];

		$response = _profile_attach_to_device_by_reference ($profile_reference, $device_reference );
		$response = json_decode($response, true);
		if ($response['wo_status'] !== ENDED) {
			$response = json_encode($response);
			echo $response;
			exit;
		}
	}
		
	$response = wait_for_provisioning_completion($device_id, $process_params);
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		echo $response;
		exit;
	}
	$wo_comment = $response['wo_comment'];
}
$response = prepare_json_response(ENDED, "MSA Device $device_id Provisioned successfully.\n$wo_comment", $context, true);
echo $response;

?>