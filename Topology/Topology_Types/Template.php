<?php
require_once '/opt/fmc_repository/Process/Topology/Common/Topology_populate.php';
require_once '/opt/fmc_repository/Process/Topology/Common/Topology_common.php';
require_once '/opt/fmc_repository/Process/Reference/Common/Library/topology_rest.php';

function calculateDeviceTopology($deviceId, $name, $device_nature) {
	global $context;

  	logTofile("*** calculateDeviceTopology  deviceId: ".$deviceId." name: ".$name."\n");

	/*
	 * create the managed entity node
	 */
  	$nodePlace = createTopology($deviceId, $name, $device_nature, "router", "style/topology/img/router_OK.svg");
}
?>
