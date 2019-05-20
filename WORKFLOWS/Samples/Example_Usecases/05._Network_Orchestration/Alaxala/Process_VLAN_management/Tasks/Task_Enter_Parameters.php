<?php

/**
 * This file is necessary to include to use all the in-built libraries of /opt/fmc_repository/Reference/Common
 */
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args() {
	create_var_def('customer_id', 'Integer');
	create_var_def('managed_device_name', 'String');
	create_var_def('device_external_reference', 'String');
	create_var_def('manufacturer_id', 'Integer');
	create_var_def('model_id', 'Integer');
	create_var_def('device_ip_address', 'IpAddress');
	create_var_def('login', 'String');
	create_var_def('password', 'Password');
	create_var_def('password_admin', 'Password');
}


/**
 * End of the task (choose one)
 */
task_success('Task OK');

?>