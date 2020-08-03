<?php

/**
 * This file is necessary to include to use all the in-built libraries of /opt/fmc_repository/Reference/Common
 */
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require '/opt/vendor/autoload.php';

use Aws\Ec2\Ec2Client;

/**
 * List all the parameters required by the task
 */
function list_args()
{
  create_var_def('KeyName', 'String');
}

check_mandatory_param('KeyName');

$ec2Client = Ec2Client::factory(array(
    'key'    => 'AKIAIVVB6I6URUCAGREQ',
    'secret' => 'oMdIyzsAsWk9VyYNHRt6myUqO380InZegnsYtg3D',
    'region' => 'eu-west-1' // (e.g., us-east-1)
));

$context["Key"] = 'SET YOU OWN';
$context["secret"] = 'SET YOU OWN';
$context["region"] = 'SET YOU OWN';

$KeyName = $context["KeyName"];
$array = array("KeyName" => $KeyName);
$result = $ec2Client->createKeyPair($array);

try {
  $res = $result->toArray();
  $context["FingerPrint"] = $res["KeyFingerprint"];
}
catch (Exception $e) {
   task_exit(FAILED, "Error : $e");
}

task_exit(ENDED, "Keypair $KeyName successfully created.");

?>
