<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args() {
	create_var_def('vro_ip_address', 'String');
	create_var_def('vro_port', 'Integer');
	create_var_def('vcenter_fqdn', 'String');
	create_var_def('vcenter_username', 'String');
	create_var_def('vcenter_password', 'Password');
}

check_mandatory_param('vro_ip_address');
check_mandatory_param('vro_port');
check_mandatory_param('vcenter_fqdn');
check_mandatory_param('vcenter_username');
check_mandatory_param('vcenter_password');

/**
 * TODO : Update vCenter Device details, service ext reference etc..
 * 
 */


$response = prepare_json_response(ENDED, "vCenter Parameters updated successfully.", $context, true);
echo $response;

?>