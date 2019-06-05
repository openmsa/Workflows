<?php

/**
 * This file is necessary to include to use all the in-built libraries of /opt/fmc_repository/Reference/Common
 */
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require '/opt/sms/bin/php/vendor/autoload.php';

use Aws\Ec2\Ec2Client;

/**
 * List all the parameters required by the task
 */
function list_args()
{
  create_var_def('AwsDeviceId', 'Device');
  create_var_def('deviceId', 'Device');
  create_var_def('ImageId', 'String');
  create_var_def('MaxCount', 'Integer');
  create_var_def('MinCount', 'Integer');
  create_var_def('InstanceType', 'String');
  create_var_def('SubnetId', 'OBMFref');
}

check_mandatory_param('ImageId');
check_mandatory_param('InstanceType');
check_mandatory_param('MaxCount');
check_mandatory_param('MinCount');
check_mandatory_param('SubnetId');

logToFile("check params successful");
$key = "AKIAI67XKTXU32R5IEAQ";
$secret= "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";
$region = "eu-west-1";

$context["key"] = $key;
$context["secret"] = $secret;
$context["region"] = $region;

$ec2Client = Ec2Client::factory(array(
    'key'    => $key,
    'secret' => $secret,
    'region' => $region
));

logToFile("ec2 client successful");

$array = array("ImageId" => $context["ImageId"], "MinCount" => $context["MinCount"], "MaxCount" => $context["MaxCount"],
"InstanceType" => $context['InstanceType'], "Placement.AvailabilityZone" => $context["region"], 'SubnetId' => $context["SubnetId"],);
logToFile(debug_dump($array, "AWS request array\n"));
$result = $ec2Client->runInstances($array);

logToFile("run instances successful : $result");

try {
	$res = $result->toArray();
	logToFile(debug_dump($res, "AWS response\n"));

	$context["InstanceId"] = $res["Instances"][0]["InstanceId"];

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

task_exit(ENDED, "VM successfully created. Id : " . $context["InstanceId"]);

?>
