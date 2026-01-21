<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/PALOALTO/Library/paloalto_generic_common.php';

function list_args() {
	create_var_def('device_id', 'Device');
	create_var_def('address_group_name', 'String');
	create_var_def('address_group_type', 'String');
	create_var_def('filter', 'String');
	create_var_def('addresses.0.address', 'OBMFRef');
}

check_mandatory_param('device_id');
check_mandatory_param('address_group_name');
check_mandatory_param('address_group_type');
check_mandatory_param('filter');
check_mandatory_param('addresses');

$device_id = substr($context['device_id'], 3);

$address_group_name = $context['address_group_name'];
$address_group_type = $context['address_group_type'];
$addresses = array();
if (array_key_exists('addresses', $context)) {
	$addresses = $context['addresses'];
}
$filter = "";
if (!empty($context['filter'])) {
	$filter = $context['filter'];
}

$response = _paloalto_generic_address_group($device_id, CMD_CREATE, $address_group_name, $address_group_type, 
							$filter, $addresses);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}

$response = prepare_json_response(ENDED, "Address Group $address_group_name created successfully on the PA Device $device_id", $context, true);
echo $response;

?>
