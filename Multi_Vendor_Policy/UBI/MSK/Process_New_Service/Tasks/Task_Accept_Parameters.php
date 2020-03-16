<?php

/**
 * This file is necessary to include to use all the in-built libraries of /opt/fmc_repository/Reference/Common
 */
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

/**
 * List all the parameters required by the task
 */
function list_args()
{
  	create_var_def('service_subnet_ip', 'String');
	create_var_def('service_subnet_masklen', 'Integer');
	create_var_def('services.0.service_name', 'OBMFRef');
	create_var_def('services.0.service_port', 'Integer');
	create_var_def('services.0.protocol', 'String');
	create_var_def('lan_port', 'OBMFRef');
	//10.1.1.6
	create_var_def('rtr_fw_int_ip', 'IPAddress');
	create_var_def('rtr_sw_int', 'OBMFRef');
	create_var_def('fw_rtr_int', 'OBMFRef');
	create_var_def('fw_wan_int', 'OBMFRef');
	create_var_def('fw_device', 'Device');
	create_var_def('rtr_device', 'Device');
	create_var_def('sw_device', 'Device');
	create_var_def('source_address', 'OBMFRef');
	create_var_def('source_zone', 'OBMFRef');
	create_var_def('destination_zone', 'OBMFRef');
	create_var_def('mode', 'String');
	create_var_def('sw_vlan', 'Composite');
	create_var_def('sw_vlan_name', 'String');
	create_var_def('sw_vlan_description', 'String');

}


/**
 * End of the task (choose one)
 */
task_success('Task OK');
?>