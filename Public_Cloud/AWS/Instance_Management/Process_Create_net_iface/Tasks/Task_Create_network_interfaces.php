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
	create_var_def('SubnetId', 'String');
	create_var_def('netInterfaceCount', 'Integer');
}

check_mandatory_param('SubnetId');
check_mandatory_param('netInterfaceCount');

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

// By default 2 ports will be created in the same subnet
$netInterfaceCount = $context["netInterfaceCount"];

for ($i = 0; $i < $netInterfaceCount; $i++) 
{
	logToFile("loop no. : " . $i . "\n" );

	$array = array("SubnetId" => $context["SubnetId"]);
	$result = $ec2Client->createNetworkInterface($array);

	try {
		$res = $result->toArray();
		logToFile(debug_dump($res, "AWS response\n"));

		${"networkInterface" . $i} = $res["NetworkInterface"]["NetworkInterfaceId"];
		logToFile("** VARIABLE: " . ${"networkInterface" . $i} . "\n");
	}
	catch (Exception $e) {
		task_exit(FAILED, "Error : $e");
	}

	$context["networkInterface" . $i] = ${"networkInterface" . $i};
	
}

task_exit(ENDED, " Network interface is successfully created. \n");
logToFile(debug_dump($context, "DUMP of CONTEXT\n"));

?>
