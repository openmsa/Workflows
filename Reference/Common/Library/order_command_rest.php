<?php

require_once COMMON_DIR . 'curl_performer.php';

/**
 * REST endpoint available in MSA NB
 * ex:
 curl -u ncroot:ubiqube  -XPOST http://localhost:10080/ubi-api-rest/ordercommand/execute/657/UPDATE -d '{
 "deviceId": 657,
 "commandName": "UPDATE",
 "objectParameters": {
 "subnet": "mySubnet"
 }
 }'
 */
function _order_command_execute ($device_id, $command_name, $object_parameters, $connection_timeout = 60, $max_time = 60) {

	$msa_rest_api = "ordercommand/execute/{$device_id}/{$command_name}";
	$curl_cmd = create_msa_operation_request(OP_POST, $msa_rest_api, $object_parameters, $connection_timeout, $max_time);
	$response = perform_curl_operation($curl_cmd, "EXECUTE COMMAND");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

/**
 <pre>
 curl -u ncroot:ubiqube  -XPOST http://localhost:10080/ubi-api-rest/ordercommand/get/configuration/657/UPDATE -d '{
 "syslogd": {
 "Syslog": {
 "syslogd2_status": "disable",
 "object_id": "Syslog",
 "syslogd3_port": "514",
 "syslogd3_server_ip": "192.168.2.3"
 }
 }
 }'
 </pre>
 */
function _order_command_generate_configuration ($device_id, $command_name, $object_parameters) {

	$msa_rest_api = "ordercommand/get/configuration/{$device_id}/{$command_name}";
	$curl_cmd = create_msa_operation_request(OP_POST, $msa_rest_api, $object_parameters);
	$response = perform_curl_operation($curl_cmd, "GENERATE CONFIGURATION");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

/**
<pre>
  curl -u ncroot:ubiqube  -XPOST http://localhost:10080/ubi-api-rest/ordercommand/synchronize/657
</pre>
 * @param unknown $device_id
 * @return unknown
 */
function _order_command_synchronize ($device_id, $connection_timeout = 300, $max_time = 300) {

	$msa_rest_api = "ordercommand/synchronize/{$device_id}";
	$object_parameters= '{"microServiceUris":[]}';
	$curl_cmd = create_msa_operation_request(OP_POST, $msa_rest_api, $object_parameters, $connection_timeout, $max_time);
	$response = perform_curl_operation($curl_cmd, "SYNCHRONIZE OBJETS");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
	 	$response = json_encode($response);
  		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}


function _obmf_create($message,$deviceId){
	return _obmf_exec($message,$deviceId,"CREATE");
}

function _obmf_delete($message,$deviceId){
	return _obmf_exec($message,$deviceId,"DELETE");
}

function _obmf_update($message,$deviceId){
	return _obmf_exec($message,$deviceId,"UPDATE");
}

function _obmf_import($message,$deviceId){
	return _obmf_exec($message,$deviceId,"IMPORT");
}

function _obmf_exec($message,$deviceId,$method){
	$jsonFile='/tmp/'.rand().'.json';
	shell_exec('echo  '.json_encode($message).' > '.$jsonFile);
	$cmd="/opt/ubi-jentreprise/bin/api/ordercommand/executeCommand.sh ".$deviceId." ".$method." ".$jsonFile;
	logToFile("[OBMF_EXEC]".$cmd);
	$res=shell_exec($cmd);
	logToFile("[OBMF_EXEC]".$res);
	shell_exec('rm -f '.$jsonFile);
	return $res;
}

/**
 *
<pre>
foreach ($context['device'] as $dev) {
  $device_id = substr($dev['id'], 3);
  $res = _obmf_list_objects_name($device_id);
  $res = json_decode($res, true);
  $object_names = $res['wo_newparams'];
}
</pre>
 * @param unknown $deviceId
 * @param number $connection_timeout
 * @param number $max_time
 * @return unknown
 */
function _obmf_list_objects_name($deviceId, $connection_timeout = 300, $max_time = 300){
  $msa_rest_api = "ordercommand/objects/{$deviceId}";
  $curl_cmd = create_msa_operation_request(OP_GET, $msa_rest_api, "", $connection_timeout, $max_time);
  $response = perform_curl_operation($curl_cmd, "LIST OBJECTS NAME");
  $response = json_decode($response, true);
  if ($response['wo_status'] !== ENDED) {
    $response = json_encode($response);
    return $response;
  }
  $response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
  return $response;

}

/**
 *
<pre>
foreach ($object_names as $object_name) {
  $res = _obmf_list_object_instances($device_id, $obj_name);
  $res = json_decode($res, true);
  $object_ids = $res['wo_newparams'];
}
</pre>
 * @param unknown $deviceId
 * @param unknown $objectName
 * @param number $connection_timeout
 * @param number $max_time
 * @return unknown
 */
function _obmf_list_object_instances($deviceId, $objectName, $connection_timeout = 300, $max_time = 300){
  $msa_rest_api = "ordercommand/objects/{$deviceId}/{$objectName}";
  $curl_cmd = create_msa_operation_request(OP_GET, $msa_rest_api, "", $connection_timeout, $max_time);
  $response = perform_curl_operation($curl_cmd, "LIST OBJECT INSTANCES");
  $response = json_decode($response, true);
  if ($response['wo_status'] !== ENDED) {
    $response = json_encode($response);
    return $response;
  }
  $response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
  return $response;

}

/**
 *
<pre>
foreach ($object_names as $object_name) {
  $res = _obmf_list_object_instances($device_id, $obj_name);
  $res = json_decode($res, true);
  $object_ids = $res['wo_newparams'];
  foreach ($object_ids as $object_id) {
    $res = _obmf_get_object_variables($device_id, $obj_name, $object_id);
    $res = json_decode($res, true);
    $object = $res['wo_newparams'];
  }
}
</pre>
 * @param unknown $deviceId
 * @param unknown $objectName
 * @param unknown $objectId
 * @param number $connection_timeout
 * @param number $max_time
 * @return unknown
 */
function _obmf_get_object_variables($deviceId, $objectName, $objectId, $connection_timeout = 300, $max_time = 300){
  $msa_rest_api = "ordercommand/objects/{$deviceId}/{$objectName}/object?id={$objectId}";
  $curl_cmd = create_msa_operation_request(OP_GET, $msa_rest_api, "", $connection_timeout, $max_time);
  $response = perform_curl_operation($curl_cmd, "GET OBJECT VARIABLES");
  $response = json_decode($response, true);
  if ($response['wo_status'] !== ENDED) {
    $response = json_encode($response);
    return $response;
  }
  $response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
  return $response;

}

?>
