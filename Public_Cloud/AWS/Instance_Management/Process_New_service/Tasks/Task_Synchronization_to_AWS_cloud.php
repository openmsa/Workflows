<?php

/**
 * This file is necessary to include to use all the in-built libraries of /opt/fmc_repository/Reference/Common
 */
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/Common/Library/msa_common.php';
require '/opt/devops/OpenMSA_Adapters/vendor/autoload.php';

use Aws\Ec2\Ec2Client; 

/**
 * List all the parameters required by the task
 */
function list_args()
{
  create_var_def('AwsDeviceId', 'Device');
}

check_mandatory_param("AwsDeviceId");

// set 
$context["wf_instance_id_for_display"] = $context['SERVICEINSTANCEID'];

logToFile(debug_dump($context, "MSA CONTEXT:\n"));

$device_id = substr($context['AwsDeviceId'], 3);
/**
* call to Microservice IMPORT to synchronize the MSA database with the managed AWS VIM
*/
$response = synchronize_objects_and_verify_response($device_id);

logToFile($response);


$response = _device_read_by_id($device_id);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}
$key = $response['wo_newparams']['login'];
$context["key"] = $key;
$secret = $response['wo_newparams']['password'];
$context["secret"] = $secret;


$response = _device_get_hostname_by_id($device_id);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}
$region = $response['wo_newparams']['hostname'];
$context["region"] = $region;


task_exit(ENDED, "Synchronisation to AWS cloud is successful.");

?>
