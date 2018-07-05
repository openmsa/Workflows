<?php 

require_once '/opt/fmc_repository/Process/Reference/OPENSTACK/Library/REST/utility.php';

#curl -i -k https://10.1.144.119/v2/abcde/volumes -X POST 
#-H "X-Auth-Token:42946664fc6e41e392bb7ee51a9160b9" -H "Accept: application/json" 
#-H "Content-Type: application/json" -d '{"volume":{"name":"abc","size":40,
#"availability_zone":"nova","multiattach":"false","bootable":"fales"}}'
function _cinder_volume_create ($cinder_endpoint, $auth_token, $name, $size, 
								$availability_zone = null, $multiattach = false, 
								$bootable = false, $source_volid = null,
								$description = null, $snapshot_id = null, $imageRef = null,
								$volume_type = null, $source_replica = null, $consistencygroup_id = null, 
								$metadata = null, $scheduler_hints = null) {

	$array = array();
	$array['name'] = $name;
	if (!is_int($size)) {
		$size = intval($size);
	}
	$array['size'] = $size;
	$array['availability_zone'] = $availability_zone;
	$array['multiattach'] = $multiattach;
	$array['bootable'] = $bootable;
	$array['source_volid'] = $source_volid;
	$array['description'] = $description;
	$array['snapshot_id'] = $snapshot_id;
	$array['imageRef'] = $imageRef;
	$array['volume_type'] = $volume_type;
	$array['metadata'] = $metadata;
	$array['source_replica'] = $source_replica;
	$array['consistencygroup_id'] = $consistencygroup_id;	
	$array['scheduler_hints'] = $scheduler_hints;
	
	$volume_array = array('volume' => $array);
	$json = json_encode($volume_array);

	$openstack_rest_api = "{$cinder_endpoint}/volumes";
	$curl_cmd = create_openstack_operation_request(OP_POST, $openstack_rest_api, $auth_token, $json);

	$response = perform_curl_operation($curl_cmd, "VOLUME CREATE");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

function _cinder_volume_update ($cinder_endpoint, $auth_token, $volume_id, $name = null,
								$description = null, $metadata = null, $tenant_id = null) {

	$array = array();
	$array['name'] = $name;
	$array['description'] = $description;
	$array['metadata'] = $metadata;
	$array['tenant_id'] = $tenant_id;
	
	$volume_array = array('volume' => $array);
	$json = json_encode($volume_array);

	$openstack_rest_api = "{$cinder_endpoint}/volumes/{$volume_id}";
	$curl_cmd = create_openstack_operation_request(OP_PUT, $openstack_rest_api, $auth_token, $json);

	$response = perform_curl_operation($curl_cmd, "VOLUME UPDATE");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

?>