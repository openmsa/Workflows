<?php

/**
 * This file is necessary to include to use all the in-built libraries of /opt/fmc_repository/Reference/Common
 */
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args() {
	create_var_def('view_name', 'String');
	create_var_def('view_type', 'String');
}

check_mandatory_param('view_name');
check_mandatory_param('view_type');

$view_type = $context["view_type"];

$pos = strpos($view_type, "..");
if($pos === false) {
	require_once '/opt/fmc_repository/Process/Topology/Topology_Types/' . $view_type . '.php';
	echo topology_create_view();
} else {
	echo prepare_json_response(FAILED, "Do not use a file from another folder", $context, false);
}
?>