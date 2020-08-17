<?php
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

//Grab variable from context
$device_id = $context['device_id'];


$announce = update_asynchronous_task_details($context, "Modyfing microservice to read playbook list... ");
/*
$microservice_file is path to microservice that dynamically updated based on
directory where Ansible playbooks located are. The microservice is proposed to extract
avaliable playbooks.
*/
$microservice_file = $context['retrieve_playbook_files'];

//Define playbook dir inside microservice.
$rewrite_string = '<operation>for file in '.$context["playbook_path"].'/*.yml; do md5sum \$file; done</operation>';

//Modify microservice with new playbook directory.
$sed_command = 'sed -i "s|<operation.*|'.$rewrite_string.'|" '.$microservice_file;
$result = shell_exec($sed_command);

$announce = update_asynchronous_task_details($context, "Modyfing microservice to read playbook list... OK");

$announce = update_asynchronous_task_details($context, "Syncing Ansible host... ");
//Sync out ansible ME to grab avaliable playbooks.
$response = json_decode(synchronize_objects_and_verify_response($device_id), true);
if ($response['wo_status'] !== ENDED) {
  echo $response;
  exit;
}

$announce = update_asynchronous_task_details($context, "Syncing Ansible host... OK");

//Finish the task
task_success('Success. The microservice to gather avaliable playbooks has been modified.');
?>