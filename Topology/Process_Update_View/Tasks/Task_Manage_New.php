<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
/**
 * This file is necessary to include to use all the in-built libraries of /opt/fmc_repository/Reference/Common
 */

unset($context["device_id"]);
unset($context["name"]);

$TO_DELETE = array();
if (!isset($context["Nodes"])) {
	echo prepare_json_response(ENDED, "No device.", $context, false);
	return;
}

foreach ($context["Nodes"] as $key => $value) {
	$contains = false;
	
	if($value["subtype"] == "cluster") {
		foreach ($context["Nodes_MAJ"] as $value2) {
			if($value2["cluster_id"] == $value["object_id"]) {
				$contains = true;
				break;
			}
		}
	} else {
		foreach ($context["Nodes_MAJ"] as $value2) {
			if($value2["object_id"] == $value["object_id"]) {
				$contains = true;
				break;
			}
		}
	}
	if(!$contains) {
		$TO_DELETE[] = $key;
	}
}

foreach ($TO_DELETE as $value) {
	unset($context["Nodes"][$value]);
}

unset($context["Nodes_MAJ"]);

echo prepare_json_response(ENDED, "The new devices are managed", $context, false);

?>
