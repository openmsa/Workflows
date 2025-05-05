<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/PALOALTO/Library/paloalto_generic_obmf.php';

function wait_for_autocom_job_completion ($device_id, $process_params) {

	$wo_newparams = array();
	$status = "";
	$count = 0;
	$sleep = SLEEP_BETWEEN_AUTOCOM_POLLS;
	$wo_comment = "";
	$check_autocom_status_message = "Checking Device $device_id AutoCom Job status (every $sleep seconds";
	$check_autocom_status_message .= ", maximum poll requests = " . MAX_AUTOCOM_POLL_COUNT . ") :\n";
	while ($count !== MAX_AUTOCOM_POLL_COUNT) {
		$response = import_objects($device_id, array('jobs'));
		$response = json_decode($response, true);
		$response_message = $response['wo_newparams'];
		if (array_key_exists('jobs', $response_message) && !empty($response_message['jobs'])) {

			$jobs_detail = $response_message['jobs'];
			$jobs = json_encode($jobs_detail);

			//$autocom_job_type = $jobs_detail['1']['type'];
			$autocom_job_status = $jobs_detail['1']['status'];
			$autocom_job_result = $jobs_detail['1']['result'];
			$autocom_job_progress = $jobs_detail['1']['progress'];

			$wo_comment = "AutoCom Job Status : $autocom_job_status\nResult : $autocom_job_result\nProgress : $autocom_job_progress%\n";
			update_asynchronous_task_details($process_params, $check_autocom_status_message . $wo_comment);
			if ($autocom_job_status === "FIN" && $autocom_job_result === "OK" && $autocom_job_progress === "100") {
				$response = prepare_json_response(ENDED, $wo_comment, $wo_newparams);
				return $response;
			}
			$sleep = SLEEP_BETWEEN_AUTOCOM_POLLS;
		}
		else {
			$wo_comment = "AutoCom Job Status : Not Available yet\n";
			update_asynchronous_task_details($process_params, $check_autocom_status_message . $wo_comment);
			$count++;
		}
		sleep($sleep);
	}
	$response = prepare_json_response(FAILED, "AutoCom Job couldn't be completed within the maximum time.\nHence, Ending the Process as Failure.\n$wo_comment", $wo_newparams, true);
	return $response;
}

?>