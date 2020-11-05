<?php

/**
 * This file is necessary to include to use all the in-built libraries of /opt/fmc_repository/Reference/Common
 */
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

$vendor = $context['vendor'];
$microservice_path = $context['microservice_path'];
$microservice_file_array = $context['microservice_file_array'];
$profile_id = $context['profile_id'];

$files = array();
foreach ($microservice_file_array as $number => &$file) {
  $files[] = array("uri"=>$microservice_path.$vendor.'/'.$file);
}

$response = json_decode(_profile_configuration_attach_files($profile_id, $files), True);

if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	exit;
}


task_success('Microservices have been attached sucessfully');
?>