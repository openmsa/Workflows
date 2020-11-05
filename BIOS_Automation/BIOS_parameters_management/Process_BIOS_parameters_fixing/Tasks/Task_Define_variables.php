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
  create_var_def('server_port', 'Integer');
  create_var_def('server_device', 'Device');
  create_var_def('server_vendor', 'String');
  
}

if(isset($parameters)) {
  	if (isset($parameters['server_ip_address'])) {
    	$context['server_ip_address'] = $parameters['server_ip_address'];
    }
    if (isset($parameters['server_mac_address'])) {
    	$context['server_mac_address'] = $parameters['server_mac_address'];
    }
  	if (isset($parameters['server_port'])) {
		$context['server_port'] = $parameters['server_port'];
    }
    if (isset($parameters['server_device'])) {
		$context['server_device'] = $parameters['server_device'];
    }
    if (isset($parameters['server_bios_profile'])) {
      $context['server_bios_profile'] = $parameters['server_bios_profile'];
    }
    if (isset($parameters['server_vendor'])) {
      $context['server_vendor'] = $parameters['server_vendor'];
    }
}


if ($context['server_device'] === 'NULL') {
	check_mandatory_param('server_ip_address');
	check_mandatory_param('server_mac_address');
	check_mandatory_param('server_port');
} else {
    check_mandatory_param('server_device');
    check_mandatory_param('server_vendor');
  
}
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

//bios_parameters_array contains BIOS parameters what should be changed, their required values, original values and changing flag
$context['bios_parameters_array'] = array();

//microservice_array contains microservice's description and name
$context['microservices_array'] = array('BIOS parameters manipulation'=>  'redfish_bios_settings',
                                        'BIOS upgrade process'        =>  'redfish_bios_version',
                                        'Redfish account manipulation'=>  'redfish_server_accounts',
                                        'Server power managment'      =>  'redfish_server_actions',
                                        'Server inventory'            =>  'redfish_server_general',
                                        'Job manager'                 =>  'redfish_job_manager'
                                        );


if ($context['server_device'] === 'NULL') {
	$normalizated_mac = preg_replace('/:|-/', '', $context['server_mac_address']);
	$mac_oui = strtoupper(substr($normalizated_mac, 0, 6));
	$context['server_vendor'] = $context['username'] = $context['password'] = 'UNKNOWN';
	
	//Determine server vendor based on MAC address and fill in bios_parameters_array
	$response = update_asynchronous_task_details($context, "Checking variables and identifying server vendor... ");
	
	$vendor_array = json_decode(file_get_contents($server_profiles_file_path), True);
	while ((list($vendor, $properties) = each($vendor_array)) and ($context['server_vendor'] == 'UNKNOWN')) {
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
	    if (array_key_exists('Miscellaneous parameters', $properties)) {
	      $context['misc_server_params'] = $properties['Miscellaneous parameters'];
	    }
	  }
	}

	//If server vendor has been identify correctly then finish the task
	if ($context['username'] !== 'UNKNOWN' and $context['password'] !== 'UNKNOWN') {
	  $wo_comment = "Server vendor and default credentials were identified correctly";
	  task_success('Checking variables and identifying server vendor... Server vendor is '.$context['server_vendor']);
	} else {
	  task_error("Checking variables and identifying server vendor... the server hasn't been identivied correctly. The task is failed.");
	}
} else {
  	//Determine server vendor based on MAC address and fill in bios_parameters_array
	$response = update_asynchronous_task_details($context, "Identify avaliable profiles for vendor ".$context['server_vendor']."... ");
	
	$vendor_array = json_decode(file_get_contents($server_profiles_file_path), True);
	while ((list($vendor, $properties) = each($vendor_array)) and !$context['bios_parameters_array']) {
	  if ($vendor === $context['server_vendor']) {
	    foreach ($properties['BIOS profiles'][$server_bios_profile] as $key => $value) {
	      $context['bios_parameters_array'][$key] = array("Required Value" => $value,
	                                                      "Original Value" => NULL,
	                                                      "was_it_changed" => 'false'
	                                                    );
	    }
	    if (array_key_exists('Miscellaneous parameters', $properties)) {
	      $context['misc_server_params'] = $properties['Miscellaneous parameters'];
	    }
	  }
	}
  	$response = update_asynchronous_task_details($context, "Identify avaliable profiles for vendor ".$context['server_vendor']."... OK");
    sleep(3);
  	task_success('Server is already provisioned. Activation is not needed');
}
?>
