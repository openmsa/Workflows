<?php
require_once '/opt/fmc_repository/Process/Topology/Common/Topology_populate.php';

// **********SERVICE LAUNCHERS********** //

function topology_create_view() {
	global $context;
	return prepare_json_response(ENDED, "The topology has fully loaded", $context, true);
}

function topology_update_view() {
	global $context;
	return prepare_json_response(ENDED, "The topology has fully loaded", $context, true);
}
?>