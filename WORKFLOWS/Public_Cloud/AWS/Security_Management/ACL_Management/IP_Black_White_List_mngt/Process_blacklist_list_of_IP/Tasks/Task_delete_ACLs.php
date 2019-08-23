<?php


require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args()
{
}

$device_id = substr($context['aws_region'], 3);
$vpc_id = $context['vpc_id'];

if (isset($context['acls'])) {

  $acl_array = $context['acls'];
  foreach ($acl_array as $acl_id) {
    delete_network_acl($device_id, $acl_id);
  }
} else {
  logToFile("no Network ACL to delete in VPC ".$vpc_id);
}

task_success('Task OK');


function delete_network_acl($device_id, $acl_id) {
  logToFile("delete Network ACL: ".$acl_id);
}

?>