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

logToFile("ec2 client successful:" . $context["InstanceId"] . " Region: " . $context["region"]);

$array = array("InstanceIds" => array($context["InstanceId"]));

$result = $ec2Client->rebootInstances($array);

try {
  $res = $result->toArray();
  logToFile(debug_dump($res, "AWS response\n"));
 
}
catch (Exception $e) {
   task_exit(FAILED, "Error : $e");
}

task_exit(ENDED, "VM successfully rebooted. Id : " . $context["InstanceId"]);

?>
