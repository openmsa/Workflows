<?php


require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/Common/Library/msa_common.php';


/*
The process recieves server IP and MAC address as parameters
*/
function list_args()
{
  create_var_def('server_ip_address', 'IpAddress');
  create_var_def('server_mac_address', 'String');
  create_var_def('server_bios_profile', 'String');
}

if(isset($parameters) ){
    $context['server_ip_address'] = $parameters['server_ip_address'];
    $context['server_mac_address'] = $parameters['server_mac_address'];
    if (isset($parameters['server_bios_profile'])) {
      $context['BIOS profile'] = $parameters['server_bios_profile'];
    }
}

check_mandatory_param('server_ip_address');
check_mandatory_param('server_mac_address');
if (isset($context['server_bios_profile']) === False) {
  $context['server_bios_profile'] = 'Performance';
}


/*
Initilize additional variables

oui_file contains lines like:
<MAC address OUI>:<Vendor name>:<Default username>:<Default password>:<List of required BIOS parameters>
*/

$server_bios_profile = $context['server_bios_profile'];
$server_profiles_file_path = '/opt/fmc_repository/Process/BIOS_Automation/BIOS_parameters_management/server_profiles.json';
$normalizated_mac = preg_replace('/:|-/', '', $context['server_mac_address']);
$mac_oui = strtoupper(substr($normalizated_mac, 0, 6));
$context['server_vendor'] = $context['username'] = $context['password'] = 'UNKNOWN';

//bios_parameters_array contains BIOS parameters what should be changed, their required values, original values and changing flag
$context['bios_parameters_array'] = array();

//microservice_array contains microservice's description and name
$context['microservices_array'] = array('BIOS parameters manipulation'=> 'redfish_bios_settings',
                                        'BIOS upgrade process'        =>  'redfish_bios_version',
                                        'Redfish account manipulation'=>  'redfish_server_accounts',
                                        'Server power managment'      =>  'redfish_server_actions',
                                        'Server inventory'            =>  'redfish_server_general'
                                        );


//Determine server vendor based on MAC address and fill in bios_parameters_array
$vendor_array = json_decode(file_get_contents($server_profiles_file_path), True);
while ((list($vendor, $properties) = each($vendor_array)) and ($context['server_vendor'] == 'UNKNOWN')) {
  logToFile(debug_dump($properties, "DEBUG: PROPERTIES"));
  if (in_array($mac_oui, $properties['OUI'])) {
    $context['server_vendor'] = $vendor;
    $context['username'] = $properties['Default Credentials']['Username'];
    $context['password'] = $properties['Default Credentials']['Password'];
    foreach ($properties['BIOS profiles'][$server_bios_profile] as $key => $value) {
      $context['bios_parameters_array'][$key] = array("Required Value" => $value,
                                                      "Original Value" => NULL,
                                                      "was_it_changed" => 'false'
                                                    );
    }
  }
}

//If server vendor has been identify correctly then finish the task
if ($context['username'] !== 'UNKNOWN' and $context['password'] !== 'UNKNOWN') {
  $wo_comment = "Server vendor and default credentials were identified correctly";
  task_success('All variables have been defined correctly. Server vendor is '.$context['server_vendor']);
} else {
  task_error("The server hasn't been identivied correctly. The task is failed.");
}
?>
