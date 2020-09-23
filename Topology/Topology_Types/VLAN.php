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

		$error = singleVLAN($deviceId, $name, $device_nature, $status);
		
		if ($error != "") {
			logTofile(debug_dump($error, "*** topology_create_view ERROR***"));
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
		$status = getStatus($deviceId);
		$error = singleVLAN($deviceId, $name, $device_nature, $status);
		
		if ($error != "") {
			logTofile(debug_dump($error, "*** topology_update_view  ERROR ***"));
		}
	}
	
	return prepare_json_response(ENDED, "Topology  fully loaded", $context, false);
}

// **********SERVICE FUNCTIONS********** //
function singleVLAN($device_id, $name, $device_nature, $status) {
	try {
		//$status = getStatus($device_id);
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
		logTofile(debug_dump($e, "************** singleVLAN ERROR **************"));
		echo prepare_json_response(FAILED, "FAILED", $context, true);
		exit;
	}
}

function startVLANForDevice($deviceId, $name, $device_nature) {
	global $context;
	logTofile("*** startVLANForDevice  deviceId: ".$deviceId." name: ".$name."\n");

	$nodePlace = createTopology($deviceId, $name, $device_nature, "router", "style/topology/img/router_OK.svg");
	
	$instances_objname = "vlan";
	$array = array (
			$instances_objname
	);

	$import_result = json_decode(import_objects($deviceId, $array));
	if (isset($import_result->wo_newparams->vlan)) {
		$vlans = $import_result->wo_newparams->vlan;
		foreach ($vlans as $vlan) {

			if (!isset($vlan->name)) {
				$vlan->name = "unknown VLAN name. The Microservice VLAN requires a variable \'name\'";
			}
			$vlan_id = $vlan->object_id;
			logTofile("*** startVLANForDevice  vlan_id: ".$vlan_id."\n");

			if ($vlan_id == 1) {
				createTopologyNetwork($vlan_id, $vlan_id, "network", "");
			} else {
				createTopologyNetwork($vlan_id, $vlan_id, "network", "");
			}
			$context ['Nodes'] [$nodePlace] ["link"] [] ["id"] = $vlan_id;
		}
		
		logTofile(debug_dump($context ['Nodes'], "*** startVLANForDevice Nodes ***\n"));
		return false;
	} else {
		logTofile("WARNING: startVLANForDevice: managed entity ".$deviceId." has no vlan microservice attached");
	}
}
?>
