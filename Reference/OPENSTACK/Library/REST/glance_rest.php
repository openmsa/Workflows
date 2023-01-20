<?php

require_once '/opt/fmc_repository/Process/Reference/OPENSTACK/Library/REST/utility.php';

/**
*
* Function allow to list images from the VIM tenant.
* WARNING: Note that the descriptions above discuss read access to images. Only the image owner (or an administrator) has write access to image properties and the image data payload. Further, in order to promise image immutability, the Image service will allow even the owner (or an administrator) only write-once permissions to specific image properties and the image data payload.
*/
function _glance_list_images ($glance_endpoint, $auth_token) {
	
	$openstack_rest_api = "{$glance_endpoint}/v2/images";
	$curl_cmd = create_openstack_operation_request(OP_GET, $openstack_rest_api, $auth_token);
	
	$response = perform_curl_operation($curl_cmd, "LIST IMAGES");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;	
}

/**
* Function allows to update record by patching the JSON representation of the image.
* exemple of $json: 
[
    {
        "op": "replace",
        "path": "/name",
        "value": "Fedora 17"
    },
    {
        "op": "replace",
        "path": "/tags",
        "value": [
            "fedora",
            "beefy"
        ]
    }
]
*/
function _glance_update_image ($glance_endpoint, $auth_token, $image_id, $json) {

	$openstack_rest_api = "{$glance_endpoint}/v2/images/{$image_id}";
	$curl_cmd = create_openstack_operation_request(OP_PATCH, $openstack_rest_api, $auth_token, $json);

	$response = perform_curl_operation($curl_cmd, "UPDATE IMAGE");
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		return $response;
	}
	$response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
	return $response;
}

?>
