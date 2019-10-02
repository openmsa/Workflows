<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args()
{
}

$workflow_name = $context['workflow_name'];
$workflow_customers = $context['workflow_customers'];

$wo_comment = "";
foreach ($workflow_customers as $workflow_customer) {
	$customer_ubiqube_id = $workflow_customer['ubiqube_id'];
	$response = _orchestration_service_detach($customer_ubiqube_id, "Process/MSA_MD_Template_Workflows/{$workflow_name}/{$workflow_name}.xml");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$wo_comment .= "Workflow detachment from the customer $customer_ubiqube_id : FAIL\n";
	}
	else {
		$wo_comment .= "Workflow detachment from the customer $customer_ubiqube_id : PASS\n";
	}
}

if (!empty($workflow_name)) {
	shell_exec('rm -rf ' . WORKFLOWS_HOME_DIR . "MSA_MD_Template_Workflows/{$workflow_name}");
}
	
$response = prepare_json_response(ENDED, "Workflow $workflow_name deleted from the repository with below details : \n\n{$wo_comment}", $context, true);
echo $response;

?>