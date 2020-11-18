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
	create_var_def('NetworkInterfaces.0.Id', 'ObjectRef');
}

$ec2Client = Ec2Client::factory(array(
    'key'    => $context["key"],
    'secret' => $context["secret"],
    'region' => $context["region"]
));

logToFile("ec2 client successful");

logToFile(debug_dump($context, "DEBUG CONTEXT:\n"));


if (isset($context["NetworkInterfaces"])) {
$networkInterfaces = $context["NetworkInterfaces"];
$netInterfaceCount = count($networkInterfaces);

logToFile("DEBUG: Network Interfaces count ==> " . $netInterfaceCount . "\n");

for ($i = 0; $i < $netInterfaceCount; $i++) {

	$networkInterfaceId = $context["NetworkInterfaces"][$i]["Id"];
	logToFile("DEBUG: networkInterfaceId --> " . $networkInterfaceId . "\n");

	$instanceId = $context["InstanceId"];
	$deviceIndex = $i + 1;

	$array = array("DeviceIndex" => $deviceIndex,
					"InstanceId" => $instanceId,
					"NetworkInterfaceId" => $networkInterfaceId);
					
	$result = $ec2Client->attachNetworkInterface($array);

	try {
		$res = $result->toArray();
		logToFile(debug_dump($res, "AWS response\n"));
	}
	catch (Exception $e) {
		task_exit(FAILED, "Error : $e");
	}
}


task_exit(ENDED, " Network interfaces are successfully attached to corresponding instance. \n");
} else {
task_exit(ENDED, "No network interface where defined and attached to this instance. \n");
}
?>
