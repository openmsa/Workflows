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
}

$ec2Client = Ec2Client::factory(array(
    'key'    => $context["key"],
    'secret' => $context["secret"],
    'region' => $context["region"]
));

logToFile("ec2 client successful:" . $context["instance_id"] . " Region: " . $context["region"]);
try {
  update_asynchronous_task_details($context, "stopping instance ".$context["instance_id"]);

  $force = true;
  $array = array("Force" => $force, "InstanceIds" => array($context["instance_id"]));
  $result = $ec2Client->stopInstances($array);

  $res = $result->toArray();
  logToFile(debug_dump($res, "AWS response\n"));
}
catch (Exception $e) {
   task_exit(FAILED, "Error : $e");
}

try {
    update_asynchronous_task_details($context, "waiting for instance to stop ".$context["instance_id"]);
	$ec2Client->waitUntilInstanceStopped(array(
		'InstanceIds' => array($context["instance_id"])
	));
}
catch (Exception $e) {
   task_exit(FAILED, "Error : $e");
}


task_exit(ENDED, "Instance stopped. Id : " . $context["instance_id"]);

?>
