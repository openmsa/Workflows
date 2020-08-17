<?php


require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/Common/Library/msa_common.php';

/*
The workflow requires the following variables as input:
 - device_id - Device what software stack will be upgraded on;
 - is_emulation - if True, no real upgrade will be performed. The workflow will check all dependencies and emulate upgrade.
*/
function list_args()
{
  create_var_def('device_id', 'Device');
  create_var_def('device_ip', 'String');
  create_var_def('is_emulation', 'Boolean');
  create_var_def('is_part_of_BPM', 'Boolean');
}

check_mandatory_param('is_emulation');
check_mandatory_param('is_part_of_BPM');
if ($context['is_part_of_BPM']) {
  check_mandatory_param('device_ip');
  $response = json_decode(_lookup_list_device_ids(), True);
  if ($response['wo_status'] !== ENDED) {
    echo $response;
    exit;
  }
  foreach ($response['wo_newparams'] as $device => $properties) {
    if (strpos($properties['name'], $context['device_ip']) !== False) {
    	$context['device_id'] = $properties['id'];
        $context['device_name'] = $properties['name'];
    }
  }
  if (empty($context['device_id'])) {
    echo 'No device id has been found. Exit.';
    exit;
  }
} else {
  check_mandatory_param('device_id');
  preg_match("/\S*?(?<device_id>\d{3})$/", $context['device_id'], $matches);
  $context['device_id'] = $matches['device_id'];
  $response = json_decode(_lookup_list_device_ids(), True);
  if ($response['wo_status'] !== ENDED) {
    echo $response;
    exit;
  }
  foreach ($response['wo_newparams'] as $device => $properties) {
    if ($properties['id'] == $context['device_id']) {
    	$context['device_name'] = $properties['name'];
    }
  }
}

$response = update_asynchronous_task_details($context, "The device is ".$context['device_name']." id is ".$context['device_id']);
sleep(5);

//Define microservice list
$context['microservices_array'] = array('BIOS parameters manipulation'=>  'redfish_bios_settings',
                                        'BIOS upgrade process'        =>  'redfish_bios_version',
                                        'Redfish account manipulation'=>  'redfish_server_accounts',
                                        'Server power managment'      =>  'redfish_server_actions',
                                        'Server inventory'            =>  'redfish_server_general',
                                        'Software inventory links'    =>  'redfish_inventory_sw_links',
                                        'Software inventory'        =>    'redfish_inventory_sw'
                                        );
//Define vars
$context['model_dir_file_path'] = 'UNKNOWN';
$microservices_array = $context['microservices_array'];
$device_id = $context['device_id'];

//The file describes software stacks directories based on server vendor and model
$model_description_file_path = '/opt/fmc_repository/Process/BIOS_Automation/Software_stack_upgrade/model_description.json';

//Identify server's vendor and model
$ms_server_inventory = $microservices_array['Server inventory'];
$response = update_asynchronous_task_details($context, "Getting server vendor and model...");
$response = json_decode(import_objects($device_id, array($ms_server_inventory)), True);
$object_ids_array = $response['wo_newparams'][$ms_server_inventory];
$object_params = current($object_ids_array);
$server_vendor = $object_params['vendor'];
$server_model = $object_params['model'];

//A directory with software stacks (model_dir_file_path) is identified based on device vendor and model 
$model_array = json_decode(file_get_contents($model_description_file_path), True);
while ((list($vendor, $models) = each($model_array)) and ($context['model_dir_file_path'] == 'UNKNOWN')) {
  if (in_array($server_vendor, $models['names'])) {
    while ((list($model, $path) = each($models['models'])) and ($context['model_dir_file_path'] == 'UNKNOWN')) {
      if (strtolower($model) === strtolower($server_model)) {
        $context['model_dir_file_path'] = $path;
      }
    }
  }
}

if (!empty($context['model_dir_file_path'])) {
  task_success("Server model is ".$server_vendor." ".$server_model);
} else {
  task_error("Upgrade directory is not identified");
}

?>
