<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
/**
 * This file is necessary to include to use all the in-built libraries of /opt/fmc_repository/Reference/Common
 */

function list_args() {
	create_var_def('view_name', 'String');
	create_var_def('view_type', 'String');
}

check_mandatory_param('view_name');
check_mandatory_param('view_type');

$view_type = $context["view_type"];
if (isset($context['ipam_device_id'])) {
  $ipam_device_id = $context['ipam_device_id'];
}

$pos = strpos($view_type, "..");
if($pos === false) {
	$topo_script = '/opt/fmc_repository/Process/Topology/Topology_Types/' . $view_type . '.php';
	logToFile("using topology script: ".$topo_script."\n");
  	require_once $topo_script;
    if ($view_type == 'VRF') {
    	$res = topology_update_service_view($ipam_device_id);
    } else {
		$res =  topology_update_view();
    }
	echo $res;
} else {
	echo prepare_json_response(FAILED, "Do not use a file from another folder", $context, false);
}

?>
