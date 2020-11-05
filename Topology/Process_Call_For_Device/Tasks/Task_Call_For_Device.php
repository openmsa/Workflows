<?php

/**
 * This file is necessary to include to use all the in-built libraries of /opt/fmc_repository/Reference/Common
 */
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args() {
}

$view_type = $context["view_type"];
$device_id = $context["device_id"];
$name = $context["name"];

if(!isset($context["Nodes"])) {
	$context['Nodes'] = array();
}

if(!isset($context["Nodes_MAJ"])) {
	$context['Nodes_MAJ'] = array();
}

require_once '/opt/fmc_repository/Process/Topology/Topology_Types/' . $view_type . '.php';


try {
    $device_info = json_decode(_device_read_by_id ($deviceId));
    $device_nature = $device_info->wo_newparams->sdNature;
	$status = getStatus($device_id);
	if($status == "UP") {
		startSNMPForDevice($device_id, $name, $device_nature);
	} else {
		if($status == "UNREACHABLE") {
			createTopology($device_id, $name, $device_nature, "router", "style/topology/img/router_ERROR.svg");
		} else if($status == "NEVERREACHED") {
			createTopology($device_id, $name, $device_nature, "router", "style/topology/img/router_NEVERREACHED.svg");
		} else if($status == "CRITICAL") {
			createTopology($device_id, $name, $device_nature, "router", "style/topology/img/router_CRITICAL.svg");
		}
	}
	echo prepare_json_response(ENDED, $device_id, $context, false);
} catch (Exception $e) {
	logTofile(debug_dump($e, "**************TOPOLOGY ERRORT**************"));
	echo prepare_json_response(FAILED, "FAILED", $context, true);
}

?>