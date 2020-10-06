<?php

require_once COMMON_DIR . 'curl_performer.php';

/**
* Get the device Custom Asset Attribute by device Id
*
* curl -u ncroot:ubiqube -XGET http://MSA_IP/ubi-api-rest/assetManagement/customAssetAttributeValue/id/{deviceId}/attributeName/{attributeName}
*
* @param deviceId
* @param attributeName
* @return Ambigous <unknown, mixed>
*/

function _custom_asset_attribute_value_by_id ($device_id,$attribute_name) {

        $msa_rest_api = "assetManagement/customAssetAttributeValue/id/{$device_id}/attributeName/{$attribute_name}";
        $curl_cmd = create_msa_operation_request(OP_GET, $msa_rest_api);
        $response = perform_curl_operation($curl_cmd, "READ CUSTOM ASSET ATTRIBUTE BY ID AND ATTRIBUTE NAME");
        $response = json_decode($response, true);
        if ($response['wo_status'] !== ENDED) {
                $response = json_encode($response);
                return $response;
        }
        $response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
        return $response;
}

/**
* Get the device Custom Asset Attribute by device Reference
*
* curl -u ncroot:ubiqube http://MSA_IP/ubi-api-rest/assetManagement/customAssetAttributeValue/reference/{deviceReference}/{attributeName}
*
* @param deviceReference
* @param attributeName
*/


function _custom_asset_attribute_value_by_ref ($device_reference,$attribute_name) {

        $msa_rest_api = "assetManagement/customAssetAttributeValue/reference/{$device_reference}/attributeName/{$attribute_name}";
        $curl_cmd = create_msa_operation_request(OP_GET, $msa_rest_api);
        $response = perform_curl_operation($curl_cmd, "READ CUSTOM ASSET ATTRIBUTE BY DEVICE REFERENCE AND ATTRIBUTE NAME");
        $response = json_decode($response, true);
        if ($response['wo_status'] !== ENDED) {
                $response = json_encode($response);
                return $response;
        }
        $response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
        return $response;
}


/**
* Get the device Custom Asset Attributes By Device Id
*
* curl -XGET -u XXX:YYY 'http://MSA_IP/ubi-api-rest/assetManagement/customAssetAttributes/id/{deviceId}'
*
* @param deviceId
*/
function _custom_asset_attributes_by_id ($device_id) {

        $msa_rest_api = "assetManagement/customAssetAttributes/id/{$device_id}";
        $curl_cmd = create_msa_operation_request(OP_GET, $msa_rest_api);
        $response = perform_curl_operation($curl_cmd, "READ CUSTOM ASSET ATTRIBUTES BY ID");
        $response = json_decode($response, true);
        if ($response['wo_status'] !== ENDED) {
                $response = json_encode($response);
                return $response;
        }
        $response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
        return $response;
}

/**
* Get the device Default Assets By Device Id
*
* curl -XGET -u XXX:YYY 'http://MSA_IP/ubi-api-rest/assetManagement/defaultAssets/id/{deviceId}'
*
* @param deviceId
*/
function _default_assets_by_id ($device_id) {

        $msa_rest_api = "assetManagement/defaultAssets/id/{$device_id}";
        $curl_cmd = create_msa_operation_request(OP_GET, $msa_rest_api);
        $response = perform_curl_operation($curl_cmd, "READ DEFAULT ASSETS BY ID");
        $response = json_decode($response, true);
        if ($response['wo_status'] !== ENDED) {
                $response = json_encode($response);
                return $response;
        }
        $response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
        return $response;
}

/**
* Get the device Default Assets by Device Reference
*
* curl -XGET -u XXX:YYY 'http://MSA_IP/ubi-api-rest/assetManagement/defaultAssetsByDeviceReference/reference/{deviceReference...'
*
* @param deviceReference
*/
function _default_assets_by_reference ($device_reference) {

        $msa_rest_api = "assetManagement/defaultAssetsByDeviceReference/reference/{$device_reference}";
        $curl_cmd = create_msa_operation_request(OP_GET, $msa_rest_api);
        $response = perform_curl_operation($curl_cmd, "READ DEFAULT ASSETS BY DEVICE REFERENCE");
        $response = json_decode($response, true);
        if ($response['wo_status'] !== ENDED) {
                $response = json_encode($response);
                return $response;
        }
        $response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
        return $response;
}


/**
* Get the device Default Assets by Device Reference
*
* curl -XGET -u XXX:YYY 'http://MSA_IP/ubi-api-rest/assetManagement/defaultAssetsByDeviceReference/reference/{deviceReference...'
*
* @param deviceReference
*/
function _device_asset_by_id ($device_id) {

        $msa_rest_api = "assetManagement/v1/device-asset/device/id/{$device_id}";
        $curl_cmd = create_msa_operation_request(OP_GET, $msa_rest_api);
        $response = perform_curl_operation($curl_cmd, "READ DEVICE ASSETS BY DEVICE ID");
        $response = json_decode($response, true);
        if ($response['wo_status'] !== ENDED) {
                $response = json_encode($response);
                return $response;
        }
        $response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
        return $response;
}


?>
