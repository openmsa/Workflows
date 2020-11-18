<?php

/**
 * This file is necessary to include to use all the in-built libraries of /opt/fmc_repository/Reference/Common
 */
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require '/opt/devops/OpenMSA_Adapters/vendor/autoload.php';

use Aws\Ec2\Ec2Client;

/**
 * List all the parameters required by the task
 */
function list_args()
{
  create_var_def('AwsDeviceId');
  create_var_def('deviceId');
  create_var_def('ImageId');
  create_var_def('InstanceType');
  create_var_def('security_group');
  create_var_def('SubnetId');
}

check_mandatory_param('ImageId');
check_mandatory_param('InstanceType');
check_mandatory_param('SubnetId');

$PROCESSINSTANCEID = $context['PROCESSINSTANCEID'];
$EXECNUMBER = $context['EXECNUMBER'];
$TASKID = $context['TASKID'];
$process_params = array('PROCESSINSTANCEID' => $PROCESSINSTANCEID,
						'EXECNUMBER' => $EXECNUMBER,
						'TASKID' => $TASKID);
	
$AwsDeviceId = $context["AwsDeviceId"];
$dev_seq_num = substr($AwsDeviceId,3);

$response = _device_read_by_id($dev_seq_num);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}


$region = $context["region"];
$key=$context["key"];
$secret = $context["secret"];

$ec2Client = Ec2Client::factory(array(
    'key'    => $key,
    'secret' => $secret,
    'region' => $region
));

logToFile("ec2 client successful");

$array = array("ImageId" => $context["ImageId"], 
               "MinCount" => 1, 
               "MaxCount" => 1,
               "InstanceType" => $context['InstanceType'], 
               "Placement.AvailabilityZone" => $context["region"], 
               "SubnetId" => $context["SubnetId"], 
               "SecurityGroupIds" => array ("1" => $context["security_group"]));

logToFile(debug_dump($array, "AWS request array\n"));

$result = $ec2Client->runInstances($array);

logToFile("run instances successful : $result");

try {
	$res = $result->toArray();
	logToFile(debug_dump($res, "AWS response\n"));

	$context["InstanceId"] = $res["Instances"][0]["InstanceId"];
	$context["wf_instance_id_for_display"] = $context['InstanceId']." - ".$context["SERVICEINSTANCEID"] ;

	$ec2Client->waitUntilInstanceRunning(array(
		'InstanceIds' => array($context["InstanceId"])
	));

	$result = $ec2Client->describeInstances(array(
			'InstanceIds' => array($context["InstanceId"])
	));

	if (isset($result["Reservations"][0]["Instances"][0]["PublicIpAddress"]) && !empty($result["Reservations"][0]["Instances"][0]["PublicIpAddress"])) {
	  $context["device_ip_address"] = $result["Reservations"][0]["Instances"][0]["PublicIpAddress"];
	} else {
	  echo "FAILED: No \"$PublicIpAddress\" is assigned to the created instance from AWS.";
	  exit;
	}
} catch (Exception $e) {
   task_exit(FAILED, "Error : $e");
}

$array_tag = array(
		'Resources' => array("1" => $context ['InstanceId']),
		'Tags' => array (
				"1" => array('Key' => 'Project', 'Value' => 'AWS demo'),
				"2" => array('Key' => 'Name', 'Value' => 'FGT VNF'),
				),
		);
logToFile ( debug_dump ( $array_tag, "AWS tag instance request array\n" ) );

$result = $ec2Client->createTags ( $array_tag );

logToFile ( "tag instances successful : $result" );

$device_ip_address = $context["device_ip_address"];

task_exit(ENDED, "instance ". $context["InstanceId"] . " / ".$device_ip_address." created");

?>
