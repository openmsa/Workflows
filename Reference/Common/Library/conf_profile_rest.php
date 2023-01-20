<?php

require_once COMMON_DIR . 'curl_performer.php';

function _conf_profile_create22 ($customer_id, $conf_profile_name ) {
  $response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, 'TEST OK');
  return $response;        
}              
        
/**
 * Create configuration profile / Deployment setting
 *   curl -u   -XPOST http://localhost:80/ubi-api-rest/conf-profile/v2/{$customer_id}
 * @param unknown $customer_id
         
 */
function _conf_profile_create ($customer_id, $conf_profile_name, $manufacturer_id,
            $model_id, $conf_profile_external_reference, $comment='', $microserviceUris, $templateUris='', $attachedManagedEntities='' ) {
  # Create configuration profile / Deployment setting

  $array = array('name' => $conf_profile_name,
      'externalReference'       => $conf_profile_external_reference,
      'vendor'                  => array( "id" => $manufacturer_id),
      'modelId'                 => array( "id" => $model_id  ),
      'comment'                 => $comment,
      'microserviceUris'        => $microserviceUris,
      'templateUris'            => $templateUris,
      'attachedManagedEntities' => $attachedManagedEntities
      );
 
  $response = prepare_json_response(FAILED, ENDED_SUCCESSFULLY, json_encode($array));
  return $response;
 
  $json = json_encode($array);
  $msa_rest_api = "conf-profile/v2/{$customer_id}";
  $curl_cmd = create_msa_operation_request(OP_POST, $msa_rest_api, $json);
  $response = perform_curl_operation($curl_cmd, "Create configuration profile   Deployment setting");
  $response = json_decode($response, true);
  if ($response['wo_status'] !== ENDED) {
    $response = json_encode($response);
    return $response;
  }
  $response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
  return $response;
}



/**
 * curl -u   -XGET http://localhost:80/ubi-api-rest/conf-profile/v2/list/customer/{customerId} 
 *    Find configuration profiles by customer 
 * 
 */
function _conf_profile_read_by_id ($customer_id) {
	
	$msa_rest_api = "/conf-profile/v2/list/customer/{$customer_id}";
	$curl_cmd = create_msa_operation_request(OP_GET, $msa_rest_api);
	$response = perform_curl_operation($curl_cmd, "READ CONF Profile/ deployment Setting by Customer ID");
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
 *     curl -u ncroot:ubiqube  -XDELETE http://localhost:10080/ubi-api-rest/conf-profile/id/1671
 * </pre>
 *
 */
function _conf_profile_delete ($conf_profile_id) {

  $msa_rest_api = "conf-profile/v2/{$conf_profile_id}";
  $curl_cmd = create_msa_operation_request(OP_DELETE, $msa_rest_api);
  $response = perform_curl_operation($curl_cmd, "Delete configuration profile by id");
  return $response;
}
