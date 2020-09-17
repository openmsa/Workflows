<?php
require_once '/opt/fmc_repository/Process/Topology/Common/Topology_populate.php';
require_once '/opt/fmc_repository/Process/Topology/Common/Topology_common.php';
require_once '/opt/fmc_repository/Process/Reference/Common/Library/topology_rest.php';

// **********SERVICE LAUNCHERS********** //
function topology_create_view() {
	global $context;
	
	$context ['Nodes'] = array ();
	$context ['Nodes_MAJ'] = array ();
		  
	$customer_ref = get_customer_ref();
	$list = json_decode(_lookup_list_devices_by_customer_reference($customer_ref), false);

	foreach ($list->wo_newparams as $value) {
		$deviceId = $value->id;
		$name = $value->name;
        $device_info = json_decode(_device_read_by_id ($deviceId));
		$device_nature = $device_info->wo_newparams->sdNature;
		$status = getStatus($deviceId);

		$error = singleVLAN($deviceId, $name, $device_nature);
		
		if ($error != "") {
			logTofile(debug_dump($error, "***TOPOLOGY CREATE ERROR***"));
		}
	}
	
	return prepare_json_response(ENDED, "The topology has fully loaded", $context, false);
}

function topology_update_view() {
	global $context;
	
	if (!isset($context ["Nodes"])) {
		$context ['Nodes'] = array ();
	}
	
	if (!isset($context ["Nodes_MAJ"])) {
		$context ['Nodes_MAJ'] = array ();
	}

	$customer_ref = get_customer_ref();
	$list = json_decode(_lookup_list_devices_by_customer_reference($customer_ref), false);
	
	foreach ($list->wo_newparams as $value) {
		$deviceId = $value->id;
		$name = $value->name;
        $device_info = json_decode(_device_read_by_id ($deviceId));
        $device_nature = $device_info->wo_newparams->sdNature;
		$error = singleVLAN($deviceId, $name, $device_nature, $context ["view_type"]);
		
		if ($error != "") {
			logTofile(debug_dump($error, "***TOPOLOGY CREATE ERROR***"));
		}
	}
	
	return prepare_json_response(ENDED, "Topology  fully loaded", $context, false);
}

// **********SERVICE FUNCTIONS********** //
function singleVLAN($device_id, $name, $device_nature) {
	try {
		$status = getStatus($device_id);
		if($status == "UP") {
			startVLANForDevice($device_id, $name, $device_nature);
		} else {
			if($status == "UNREACHABLE") {
				createTopology($device_id, $name, $device_nature, "router", "style/topology/img/router_ERROR.svg");
			} else if($status == "NEVERREACHED") {
				createTopology($device_id, $name, $device_nature, "router", "style/topology/img/router_NEVERREACHED.svg");
			} else if($status == "CRITICAL") {
				createTopology($device_id, $name, $device_nature, "router", "style/topology/img/router_CRITICAL.svg");
			}
		}
	} catch (Exception $e) {
		logTofile(debug_dump($e, "**************TOPOLOGY ERROR **************"));
		echo prepare_json_response(FAILED, "FAILED", $context, true);
		exit;
	}
}

function startVLANForDevice($deviceId, $name, $device_nature) {

	$nodePlace = createTopology($deviceId, $name, $device_nature, "router", "style/topology/img/router_OK.svg");
	
	$instances_objname = "vlan";
	$array = array (
			$instances_objname
	);
	$vlans = json_decode(import_objects($deviceId, $array))->wo_newparams->vlan;
	foreach ($vlans as $vlan) {
	//	if (!in_array($vlan->object_id, $GLOBALS ["DO_NOT_DESTROY"])) {
	//		array_push($GLOBALS ["DO_NOT_DESTROY"], $vlan->object_id);
	//	}
		
		if ($vlan->object_id == 1) {
			createTopologyNetwork($vlan->object_id, $vlan->name, "vlan", "", "#AA3BF2");
		} else {
			createTopologyNetwork($vlan->object_id, $vlan->name, "vlan", "");
		}
		$context ['Nodes'] [$nodePlace] ["link"] [] ["id"] = $vlan->object_id;
	}

	logTofile(debug_dump($context ["Nodes"], "***TOPOLOGY GLOBALS***"));
	return false;
}
?>
