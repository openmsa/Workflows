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
   create_var_def("force", "Boolean");
}

$ec2Client = Ec2Client::factory(array(
    'key'    => $context["key"],
    'secret' => $context["secret"],
    'region' => $context["region"]
));

logToFile("ec2 client successful:" . $context["InstanceId"] . " Region: " . $context["region"]);

$force = true;
if ($context["force"] === "false") {
   $force = false;
}
$array = array("Force" => $force, "InstanceIds" => array($context["InstanceId"]));

$result = $ec2Client->stopInstances($array);

try {
  $res = $result->toArray();
  logToFile(debug_dump($res, "AWS response\n"));
 
}
catch (Exception $e) {
   task_exit(FAILED, "Error : $e");
}

task_exit(ENDED, "VM successfully stopped. Id : " . $context["InstanceId"]);

?>
