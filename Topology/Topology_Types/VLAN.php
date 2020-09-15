<?php
require_once '/opt/fmc_repository/Process/Reference/Common/Library/Topology/Topology_populate.php';
require_once '/opt/fmc_repository/Process/Reference/Common/Library/topology_rest.php';

// **********SERVICE LAUNCHERS********** //
function topology_create_view() {
	global $context;

	logTofile(debug_dump($context, "***TOPOLOGY VLAN CONTEXT***"));
	$GLOBALS ["Nodes"] = array ();
	$GLOBALS ["DO_NOT_DESTROY"] = array ();
	
	$list = json_decode(_lookup_list_devices_by_customer_reference($context ["UBIQUBEID"]));
	
	foreach ($list->wo_newparams as $value) {
		$deviceId = $value->id;
		$name = $value->name;
		logTofile(debug_dump($deviceId, "***TOPOLOGY VLAN DEVICEID***"));

		$device_info = json_decode(_device_read_by_id ($deviceId));
        $device_nature = $device_info->wo_newparams->sdNature;

		$status = getStatus($deviceId);
		logTofile(debug_dump($status, "***TOPOLOGY VLAN STATUS***"));
		$nodePlace = -1;
		if ($status == "UP") {
			$error = startVLANForDevice($deviceId, $name, $device_nature, $nodePlace);
			if ($error) {
				logTofile(debug_dump($error, "***TOPOLOGY VLAN ERROR***"));
			}
		} else {
			if ($status == "UNREACHABLE") {
				createTopology($deviceId, $name, $device_nature, "router", "style/topology/img/router_ERROR.svg");
			} else if ($status == "NEVERREACHED") {
				createTopology($deviceId, $name, $device_nature, "router", "style/topology/img/router_NEVERREACHED.svg");
			} else if ($status == "CRITICAL") {
				createTopology($deviceId, $name, $device_nature, "router", "style/topology/img/router_CRITICAL.svg");
			}
		}
	}
	
	$context ["Nodes"] = $GLOBALS ["Nodes"];
	$ret = prepare_json_response(ENDED, "The topology has fully loaded", $context, true);
	return $ret;
}

function topology_update_view() {
	global $context;

	logTofile(debug_dump($context, "***TOPOLOGY VLAN CONTEXT***"));
	if (isset($context ["Nodes"])) {
		$GLOBALS ["Nodes"] = $context ["Nodes"];
		unset($context ["Nodes"]);
	} else {
		$GLOBALS ["Nodes"] = array ();
	}
	$GLOBALS ["DO_NOT_DESTROY"] = array ();
	
	$ubiqube_id = $context ['UBIQUBEID'];
	
	$list = json_decode(_lookup_list_devices_by_customer_reference($context ['UBIQUBEID']), false);
	
	foreach ($list->wo_newparams as $value) {
		$deviceId = $value->id;
		$name = $value->name;
		
		array_push($GLOBALS ["DO_NOT_DESTROY"], $deviceId);

		logTofile(debug_dump($deviceId, "***TOPOLOGY VLAN DEVICEID***"));

		$device_info = json_decode(_device_read_by_id ($deviceId));
        $device_nature = $device_info->wo_newparams->sdNature;

		$nodePlace = -1;
		$status = getStatus($deviceId);
		logTofile(debug_dump($status, "***TOPOLOGY VLAN STATUS***"));
		if ($status == "UP") {
			$error = startVLANForDevice($deviceId, $name, $device_nature, $nodePlace);

			if ($error != "") {
				logTofile(debug_dump($error, "***TOPOLOGY VLAN ERROR***"));
			}
		} else {
			if ($status == "UNREACHABLE") {
				$nodePlace = createTopology($deviceId, $name, $device_nature, "router", "style/topology/img/router_ERROR.svg");
			} else if ($status == "NEVERREACHED") {
				$nodePlace = createTopology($deviceId, $name, $device_nature, "router", "style/topology/img/router_NEVERREACHED.svg");
			} else if ($status == "CRITICAL") {
				$nodePlace = createTopology($deviceId, $name, $device_nature, "router", "style/topology/img/router_CRITICAL.svg");
			}
		}
		
		$cluster_id = $GLOBALS ["Nodes"] [$nodePlace] ["cluster_id"];
		if (!in_array($cluster_id, $GLOBALS ["DO_NOT_DESTROY"])) {
			array_push($GLOBALS ["DO_NOT_DESTROY"], $cluster_id);
		}
	}
	
	foreach ($GLOBALS ["Nodes"] as $key => $value_verif) {
		$destroy = true;
		foreach ($GLOBALS ["DO_NOT_DESTROY"] as $value_not_destroy) {
			if ($value_verif ["object_id"] == $value_not_destroy) {
				$destroy = false;
			}
		}
		if ($destroy) {
			unset($GLOBALS ["Nodes"] [$key]);
		}
	}
	
	$context ["Nodes"] = $GLOBALS ["Nodes"];
	logTofile(debug_dump($context, "***TOPOLOGY VLAN CONTEXT***"));
	return prepare_json_response(ENDED, "The topology has fully loaded", $context, true);
}

// **********SERVICE FUNCTIONS********** //
// Don't delete $nodeplace : it's use in Update
function startVLANForDevice($deviceId, $name, $device_nature, &$nodePlace) {

	$nodePlace = createTopology($deviceId, $name, $device_nature, "router", "style/topology/img/router_OK.svg");
	
	$instances_objname = "vlan";
	$array = array (
			$instances_objname
	);
	$vlans = json_decode(import_objects($deviceId, $array))->wo_newparams->vlan;
	foreach ($vlans as $vlan) {
		if (!in_array($vlan->object_id, $GLOBALS ["DO_NOT_DESTROY"])) {
			array_push($GLOBALS ["DO_NOT_DESTROY"], $vlan->object_id);
		}
		
		if ($vlan->object_id == 1) {
			createTopologyNetwork($vlan->object_id, $vlan->name, "vlan", "", "#AA3BF2");
		} else {
			createTopologyNetwork($vlan->object_id, $vlan->name, "vlan", "");
		}
		$GLOBALS ["Nodes"] [$nodePlace] ["link"] [] ["id"] = $vlan->object_id;
	}
	
	logTofile(debug_dump($GLOBALS ["Nodes"], "***TOPOLOGY GLOBALS***"));
	return false;
}

function getStatus($device_id) {
	$info = json_decode(_device_get_status($device_id), true);
	$status = $info ["wo_newparams"];
	
	if (empty($status) || $status == "") {
		return "Site with id " . $device_id . " was not found";
	} else {
		return $status;
	}
}

?>