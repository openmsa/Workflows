<?php

/**
 * This file is necessary to include to use all the in-built libraries of /opt/fmc_repository/Reference/Common
 */
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require '/opt/devops/OpenMSA_Adapters/vendor/autoload.php';

use Aws\Ec2\Ec2Client;

$ec2Client = Ec2Client::factory(array(
    'key'    => $context["key"],
    'secret' => $context["secret"],
    'region' => $context["region"]
));

logToFile("ec2 client successful");

try {
  update_asynchronous_task_details($context, "Starting instance ".$context["instance_id"]);

  $array = array("InstanceIds" => array($context["instance_id"]));
  $result = $ec2Client->startInstances($array);

  $res = $result->toArray();
  logToFile(debug_dump($res, "startInstances: AWS response\n"));
 
}
catch (Exception $e) {
   task_exit(FAILED, "Error : $e");
}

try {
    update_asynchronous_task_details($context, "waiting for instance ".$context["instance_id"]);
	$ec2Client->waitUntilInstanceRunning(array(
		'InstanceIds' => array($context["instance_id"])
	));
}
catch (Exception $e) {
   task_exit(FAILED, "Error : $e");
}

try {
  update_asynchronous_task_details($context, "instance ".$context["instance_id"]." started");

  $array = array("InstanceIds" => array($context["instance_id"]));
  $result = $ec2Client->DescribeInstances($array);
  if (isset($result["Reservations"][0]["Instances"][0]["PublicIpAddress"]) && 
      !empty($result["Reservations"][0]["Instances"][0]["PublicIpAddress"])) {
	  $context["instance_ip"] = $result["Reservations"][0]["Instances"][0]["PublicIpAddress"];
  } else {
	  echo "FAILED: No \"$PublicIpAddress\" is assigned to the created instance from AWS.";
	  exit;
  }
}
catch (Exception $e) {
   task_exit(FAILED, "Error : $e");
}


task_exit(ENDED, "Instance started. Id : " . $context["instance_id"]);

?>
