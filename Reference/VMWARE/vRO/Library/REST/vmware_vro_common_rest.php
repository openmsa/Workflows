<?php 

require_once '/opt/fmc_repository/Process/Reference/VMWARE/vRO/Library/REST/execution_rest.php';
require_once '/opt/fmc_repository/Process/Reference/VMWARE/vRO/Library/REST/presentation_rest.php';
require_once '/opt/fmc_repository/Process/Reference/VMWARE/vRO/Library/REST/interaction_presentation_rest.php';

// curl -X GET --header 'Accept: text/html' 'https://10.31.1.19:8281/vco/api/workflows?maxResult=2147483647&startIndex=0&queryCount=false'
function vro_object_get ($vro_rest_api, $object_name) {

	$curl_cmd = create_vro_operation_request(OP_GET, $vro_rest_api);
	$response = perform_curl_operation($curl_cmd, strtoupper($object_name) . " GET");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

// curl -X DELETE --header 'Accept: text/html' 'https://10.31.1.19:8281/vco/api/workflows/123?force=false&forceDeleteLocked=false'
function vro_object_delete ($vro_rest_api, $object_name) {

	$curl_cmd = create_vro_operation_request(OP_DELETE, $vro_rest_api);
	$response = perform_curl_operation($curl_cmd, strtoupper($object_name) . " DELETE");
	return $response;
}

function vro_get_execution_id ($response_headers) {

	$response_headers = http_parse_headers($response_headers);
	$location_array = explode("/", $response_headers['Location']);
	return $location_array[count($location_array) - 2];	
}

function vro_wait_for_workflow_completion ($workflow_id, $execution_id, $timeout = VRO_WORKFLOW_EXECUTION_TIMEOUT) {

	global $context;
	
	$wo_newparams = array();
	$state = '';
	$wo_comment = "";
	$total_sleeptime = 0;
	$check_workflow_status_message = "Checking Workflow Status (every " . VRO_WORKFLOW_EXECUTION_STATUS_CHECK_SLEEP . " seconds";
	$check_workflow_status_message .= ", timeout = $timeout seconds) :\n";
	while ($state !== VRO_WORKFLOW_COMPLETED) {

		$response = vro_object_get("workflows/{$workflow_id}/executions/{$execution_id}", "VRO WORKFLOW EXECUTIONS");
		$response = json_decode($response, true);
		if ($response['wo_status'] !== ENDED) {
			$response = json_encode($response);
			return $response;
		}
		$state = $response['wo_newparams']['state'];
		logToFile("VRO WORKFLOW EXECUTION STATE : $state");
		
		$wo_comment = "Workflow execution state : $state";
		update_asynchronous_task_details($context, $check_workflow_status_message . $wo_comment);
		if ($state === VRO_WORKFLOW_COMPLETED) {
			$wo_newparams = $response['wo_newparams']['output-parameters'];
			break;
		}
		else if ($state === VRO_WORKFLOW_FAILED) {
			$content_exception = $response['wo_newparams']['content-exception'];
			$wo_comment .= "\nWorkfow execution content exception : $content_exception";
			$response = prepare_json_response(FAILED, $wo_comment, $wo_newparams, true);
			return $response;
		}
		sleep(VRO_WORKFLOW_EXECUTION_STATUS_CHECK_SLEEP);
		$total_sleeptime += VRO_WORKFLOW_EXECUTION_STATUS_CHECK_SLEEP;
		if ($total_sleeptime > $timeout) {
			$wo_comment .= "Workflow execution could not be completed within $timeout seconds.\nHence, Ending the Process as Failure.";
			$response = prepare_json_response(FAILED, $wo_comment, $wo_newparams, true);
			return $response;
		}
	}
	$response = prepare_json_response(ENDED, $wo_comment, $wo_newparams);
	return $response;
}

function vro_execute_workflow_and_wait_for_completion ($workflow_id, $parameters_array) {

	global $context;
	
	$response = _execution_start_workflow($workflow_id, $parameters_array);
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = prepare_json_response(FAILED, $response['wo_comment'], $context, true);
		echo $response;
		exit;
	}
	
	$execution_id = vro_get_execution_id($response['wo_newparams']['response_raw_headers']);
	$context['execution_id'] = $execution_id;
	
	$response = vro_wait_for_workflow_completion($workflow_id, $execution_id);
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = prepare_json_response(FAILED, $response['wo_comment'], $context, true);
		echo $response;
		exit;
	}
	$context['output_parameters'] = $response['wo_newparams'];
}

?>