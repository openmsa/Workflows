<?php

require_once COMMON_DIR . 'curl_performer.php';

/**
 * Create Template Managed Device
 *
 * @param unknown $customer_id
 * @param unknown $device_name
 * @param unknown $manufacturer_id
 * @param unknown $model_id
 * @param unknown $login
 * @param unknown $password
 * @param unknown $password_admin
 * @param unknown $management_address
 * @param string $log_enabled
 * @param string $log_more_enabled
 * @param string $mail_alerting
 * @param string $reporting
 * @return unknown
 */
function _device_create ($customer_id, $device_name, $manufacturer_id,
						$model_id, $login, $password, $password_admin,
						$management_address, $device_external_reference = "",
						$log_enabled = "true", $log_more_enabled = "true", 
						$mail_alerting = "true", $reporting = "false", $snmp_community = "ubiqube") {

	$array = array('name' => $device_name,
			'manufacturerId' => $manufacturer_id,
			'modelId' => $model_id,
			'login' => $login,
			'password' => $password,
			'passwordAdmin' => $password_admin,
			'logEnabled' => $log_enabled,
			'logMoreEnabled' => $log_more_enabled,
			'mailAlerting' => $mail_alerting,
			'reporting' => $reporting,
			'managementAddress' => $management_address,
			'externalReference' => $device_external_reference,
			'snmpCommunity' => $snmp_community
	);
	$json = json_encode($array);
	$msa_rest_api = "device/{$customer_id}";
	$curl_cmd = create_msa_operation_request(OP_PUT, $msa_rest_api, $json);
	$response = perform_curl_operation($curl_cmd, "CREATE TEMPLATE MANAGED DEVICE");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

/**
 * <pre>
 *     curl -u ncroot:ubiqube  -XDELETE http://localhost:10080/ubi-api-rest/device/id/1671
 * </pre>
 *
 */
function _device_delete ($device_id) {

	$msa_rest_api = "device/id/{$device_id}";
	$curl_cmd = create_msa_operation_request(OP_DELETE, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "DELETE DEVICE BY ID");
	return $response;
}

/**
 * <pre>
 *     curl -u ncroot:ubiqube  -XDELETE http://localhost:10080/ubi-api-rest/device/reference/1671
 * </pre>
 *
 */
function _device_delete_by_reference ($device_reference) {

	$msa_rest_api = "device/reference/{$device_reference}";
	$curl_cmd = create_msa_operation_request(OP_DELETE, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "DELETE DEVICE BY REFERENCE");
	return $response;
}

/**
 * REST endpoint available in MSA NB
 * ex:
 * curl -u ncroot:ubiqube  -XPOST http://localhost:10080/ubi-api-rest/device/activate/657
 */
function _device_mark_as_provisioned ($device_id) {

	$msa_rest_api = "device/activate/{$device_id}";
	$curl_cmd = create_msa_operation_request(OP_POST, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "MARK AS PROVISIONED BY DEVICE ID");
	return $response;
}

/**
 * REST endpoint available in MSA NB
 * ex:
 * curl -u ncroot:ubiqube  -XOP_GET http://localhost:10080/ubi-api-rest/DeviceWS/getDeviceStatus/657
 */
function _device_get_status ($device_id) {

	$msa_rest_api = "device/status/{$device_id}";
	$curl_cmd = create_msa_operation_request(OP_GET, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "GET DEVICE STATUS");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

/**
 * curl -u ncroot:Ub1qub3  -XGET http://localhost:80/ubi-api-rest/device/id/104
 * 
 */
function _device_read_by_id ($device_id) {
	
	$msa_rest_api = "device/id/{$device_id}";
	$curl_cmd = create_msa_operation_request(OP_GET, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "READ DEVICE BY ID");
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
 curl -u ncroot:ubiqube  -X GET http://localhost:8080/ubi-api-rest/device/reference/DEVICE_REF1234
 </pre>
 *
 * @param unknown $device_reference
 * @return Ambigous <unknown, mixed>
 */
function _device_read_by_reference ($device_reference) {

	$msa_rest_api = "device/reference/{$device_reference}";
	$curl_cmd = create_msa_operation_request(OP_GET, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "READ BY DEVICE REFERENCE");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

/**
 * reads, from the database, the hostname set for a device
 * @param  $device_id
 */
function _device_get_hostname_by_id ($device_id) { 
	$msa_rest_api = "device/v1/hostname/{$device_id}";
	$curl_cmd = create_msa_operation_request(OP_GET, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "READ DEVICE HOSTNAME BY ID");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

/**
 * REST endpoint available in MSA NB
 * ex:
 * curl -u ncroot:ubiqube  -XPOST http://localhost:10080/ubi-api-rest/device/maintenance/657?enable=true
 */
function _device_set_maintenance_mode ($device_id, $enable = "true") {

	$msa_rest_api = "device/maintenance/{$device_id}?enable={$enable}";
	$curl_cmd = create_msa_operation_request(OP_POST, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "SET DEVICE MAINTENANCE MODE");
	return $response;
}

/**
 * REST endpoint available in MSA NB
 * ex:
 * curl -u ncroot:ubiqube  -XOP_GET http://localhost:10080/ubi-api-rest/configuration/status/id/{deviceId}
 */
function _device_get_update_config_status ($device_id) {

	$msa_rest_api = "device/configuration/status/id/{$device_id}";
	$curl_cmd = create_msa_operation_request(OP_GET, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "GET DEVICE UPDATE CONFIG STATUS");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

/**
 * REST endpoint available in MSA NB
 * ex:
 * curl -u ncroot:ubiqube  -XPOST http://localhost:10080/ubi-api-rest/device/configuration/update/657
 */
function _device_do_update_config ($device_id) {

	$msa_rest_api = "device/configuration/update/{$device_id}";
	$curl_cmd = create_msa_operation_request(OP_POST, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "DO UPDATE CONFIGURATION");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

/**
 * REST endpoint available in MSA NB
 * ex:
 * curl -u ncroot:ubiqube  -X "POST" http://localhost:10080/ubi-api-rest/device/ping/127.0.0.1
 */
function _device_do_ping ($address) {

	$msa_rest_api = "device/ping/{$address}";
	$curl_cmd = create_msa_operation_request(OP_GET, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "DO PING");
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
 curl -u ncroot:ubiqube  -X GET http://localhost:10080/ubi-api-rest/device/provisioning/status/657
 </pre>
 * @return ProvisioningStatus
 */
function _device_get_provisioning_status_by_id ($device_id) {

	$msa_rest_api = "device/provisioning/status/{$device_id}";
	$curl_cmd = create_msa_operation_request(OP_GET, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "GET PROVISIONING STATUS BY DEVICE ID");
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
 curl -u ncroot:ubiqube  -XPOST http://localhost:10080/ubi-api-rest/device/provisioning/657
 </pre>
 */
function _device_do_initial_provisioning_by_id ($device_id) {

	$msa_rest_api = "device/provisioning/{$device_id}";
	$curl_cmd = create_msa_operation_request(OP_POST, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "DO INITIAL PROVISIONING BY DEVICE ID");
	return $response;
}

/**
 * <pre>
 * curl -u ncroot:ubiqube  -X PUT http://localhost:8080/ubi-api-rest/device/push_configuration/2932
 * -d '{"configuration": "config system interface\nedit port1\nset ip 192.168.1.10 255.255.255.0\nend"}'
 * </pre>
 *
 **/
function _device_do_push_configuration_by_id ($device_id, $configuration) {

	$msa_rest_api = "device/push_configuration/{$device_id}";
	$array = array('configuration' => $configuration);
	$json = json_encode($array);
	$curl_cmd = create_msa_operation_request(OP_PUT, $msa_rest_api, $json);
	$response = perform_curl_operation($curl_cmd, "DO PUSH CONFIGURATION BY DEVICE ID");
	return $response;
}

/**
	<pre>
	curl -u ncroot:ubiqube  -X GET http://localhost:8080/ubi-api-rest/device/push_configuration/status/2932
	</pre>
 *
 * @param unknown $device_id
 * @return Ambigous <unknown, mixed>
 */

function _device_get_pushconfig_status_by_id ($device_id) {

	$msa_rest_api = "device/push_configuration/status/{$device_id}";
	$curl_cmd = create_msa_operation_request(OP_GET, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "GET PUSH CONFIGURATION STATUS BY DEVICE ID");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

/**
 * curl -u ncroot:ubiqube  -XPUT 'http://MSA
	IP/ubi-api-rest/device/management_ip/update/{device_id}?ip=10.10.10.10&mask=255.255.255.255'
 */
function _device_update_management_ip_address ($device_id, $ip_address, $netmask = "255.255.255.255") {

	$msa_rest_api = "device/management_ip/update/{$device_id}?ip={$ip_address}&mask={$netmask}";
	$curl_cmd = create_msa_operation_request(OP_PUT, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "UPDATE DEVICE MANAGEMENT IP ADDRESS");
	return $response;
}

/**
 * curl -u ncroot:ubiqube  -H "Content-Type: application/json" -XPUT
 * 'http://localhost:10080/ubi-api-rest/device/conf_profile/switch/3768?old_profile_ref=A&new_profile_ref=C'
 */
function _device_configuration_profile_switch ($device_id, $old_profile_ref, $new_profile_ref) {

	$msa_rest_api = "device/conf_profile/switch/{$device_id}?old_profile_ref={$old_profile_ref}&new_profile_ref={$new_profile_ref}";
	$curl_cmd = create_msa_operation_request(OP_PUT, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "SWITCH DEVICE CONFIGURATION PROFILE");
	return $response;
}

/**
 * curl -u ncroot:ubiqube  -XPUT 'http://localhost:10080/ubi-api-rest/device/credentials/update/14710?login=myLogin&password=myPassword'
 * 
 */
function _device_update_credentials ($device_id, $login, $password) {
	
	$msa_rest_api = "device/credentials/update/{$device_id}?login={$login}&password={$password}";
	$curl_cmd = create_msa_operation_request(OP_PUT, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "UPDATE DEVICE CREDENTIALS IN MSA DATABASE");
	return $response;
}


function _device_do_update_firmware ($device_id) {
	logToFile('[device_rest][do_update_firmware] update firmware on '.$device_id);
	$api_cmd='/opt/ubi-jentreprise/bin/api/device/doFirmwareUpdateByDeviceId.sh '.$device_id;
	logToFile("[device_rest][do_update_firmware]  -> ".$api_cmd);
	$res=shell_exec($api_cmd);
	logToFile("[device_rest][do_update_firmware] ".$res);
	return $res;
}

function _device_check_update_firmware ($device_id) {
	logToFile('[device_rest][check_update_firmware] update firmware on '.$device_id);
	$api_cmd='/opt/ubi-jentreprise/bin/api/device/getFirmwareUpdateStatusByDeviceId.sh '.$device_id;
	logToFile("[device_rest][check_update_firmware]  -> ".$api_cmd);
	$res=shell_exec($api_cmd);
	logToFile("[device_rest][check_update_firmware] ".$res);
	return $res;
}

function _device_create_configure_variable ($device_id, $variablename, $variablevalue) {
	logToFile('[device_rest][create_configure_variable] Add variable '.$variablename.' ('.$variablevalue.') to '.$device_id);
	$api_cmd='/opt/ubi-jentreprise/bin/api/deviceconfigurationvariable/createConfigurationVariable.sh '.$device_id.' '.$variablename.' '.$variablevalue;
	logToFile("[device_rest][create_configure_variable]  -> ".$api_cmd);
	$res=shell_exec($api_cmd);
	logToFile("[device_rest][create_configure_variable] ".$res);
	return $res;
}

function _device_rollback_do_backup ($device_id) {
	logToFile('[device_rest][rollback_do_backup] Backup device '.$device_id);
	$api_cmd='/opt/ubi-jentreprise/bin/api/rollback/doBackup.sh '.$device_id;
	logToFile("[device_rest][rollback_do_backup]  -> ".$api_cmd);
	$res=shell_exec($api_cmd);
	logToFile("[device_rest][rollback_do_backup] ".$res);
	return $res;
}

function _device_rollback_list_revision ($device_id) {
	logToFile('[device_rest][rollback_list_revision] List revision for device '.$device_id);
	$api_cmd='/opt/ubi-jentreprise/bin/api/rollback/doListRevisions.sh '.$device_id;
	logToFile("[device_rest][rollback_list_revision]  -> ".$api_cmd);
	$res=shell_exec($api_cmd);
	logToFile("[device_rest][rollback_list_revision] ".$res);
	return $res;
}

function _device_rollback_do_restore ($device_id, $revision_id) {
	logToFile('[device_rest][rollback_do_restore] Restore device '.$device_id.' using revision '.$revision_id);
	$api_cmd='/opt/ubi-jentreprise/bin/api/rollback/doRestore.sh '.$device_id.' '.$revision_id;
	logToFile("[device_rest][rollback_do_restore]  -> ".$api_cmd);
	$res=shell_exec($api_cmd);
	logToFile("[device_rest][rollback_do_restore] ".$res);
	return $res;
}

?>
