<?php
#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#  
#       http://www.apache.org/licenses/LICENSE-2.0
#  
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.
#  
#  COPYRIGHT  (C)  NEC  CORPORATION  2017
#  
/**
 * 1.SYSTEM   : API Controller
* 2.FUNCTION : ext_globalip.php (Individual method)
*/
require_once dirname(__FILE__). '/../Nal.php';

class ext_globalip extends neccsNal {

    /**
     * GET method (list,refer)
     *
     */
    protected function get() {

        // Get the global ip address information
        $url  = neccsNal_Config::API_URL;
        $url .= neccsNal_Config::API_URL_LIST;
        $url .= neccsNal_Config::RESOURCE_GLOBAL_IP_ADDR;
        $request_id = isset( $this->_p['request-id'] ) ? $this->_p['request-id'] : $this->_requestId;
        $url .= '?' . 'request-id=' . $request_id;
        $url .= '&' . 'delete_flg=0';

        $url_list['global_ip_address_info'] = $url;

        // Get the appliance information
        $url  = neccsNal_Config::API_URL;
        $url .= neccsNal_Config::API_URL_LIST;
        $url .= neccsNal_Config::RESOURCE_APLS;
        $request_id = isset( $this->_p['request-id'] ) ? $this->_p['request-id'] : $this->_requestId;
        $url .= '?' . 'request-id=' . $request_id;
        $url .= '&' . 'delete_flg=0';

        $url_list['appliances_info'] = $url;

        // Get the tenant information
        $url  = neccsNal_Config::API_URL;
        $url .= neccsNal_Config::API_URL_LIST;
        $url .= neccsNal_Config::RESOURCE_TENANTS;
        $request_id = isset( $this->_p['request-id'] ) ? $this->_p['request-id'] : $this->_requestId;
        $url .= '?' . 'request-id=' . $request_id;
        $url .= '&' . 'IaaS_tenant_id=' . $this->_p['IaaS_tenant_id'];
        $url .= '&' . 'delete_flg=0';

        $url_list['tenants_info'] = $url;

        // Get the tenant contract information
        $url  = neccsNal_Config::API_URL;
        $url .= neccsNal_Config::API_URL_LIST;
        $url .= neccsNal_Config::RESOURCE_CONTRACT;
        $request_id = isset( $this->_p['request-id'] ) ? $this->_p['request-id'] : $this->_requestId;
        $url .= '?' . 'request-id=' . $request_id;
        $url .= '&' . 'contract_kind=' . '1';
        $url .= '&' . 'delete_flg=0';

        $url_list['tenant_contract_info'] = $url;

        $execList = $this->_execMultiApi( $url_list );

        // get the use_cnt
        $result = array();
        $result = $this->_getContInfo( $execList );

        $url = neccsNal_Config::NAL_API_URL . str_replace( '/Nal/', '', $_SERVER['REQUEST_URI'] );
        $this->logit( neccsNal_Config::SUCCESS_CODE, "OutPut Data ( $url )", $this->_p, $result );

        $this->success( $result );
    }

    /**
     * PUT method (put)
     *
     */
    protected function put() {

        // IaaS tenant id
        if( isset( $this->_p['IaaS_tenant_id'] ) ) {
            $IaaSTenantId = $this->_p['IaaS_tenant_id'];
        } else {
            $this->error( neccsNal_Config::PARAMETER_ERROR, "IaaS_tenant_id is not set." );
        }

        // global ip address
        if( isset( $this->_p['global_ip'] ) ) {
            $globalIp = $this->_p['global_ip'];
        } else {
            $this->error( neccsNal_Config::PARAMETER_ERROR, "global_ip is not set." );
        }

        // Convert the tenant ID
        $this->_p['tenant_name'] = $this->_getTenant( $IaaSTenantId );

        // Failure to convert the tenant ID
        if( empty( $this->_p['tenant_name'] ) ) {
            $this->error( neccsNal_Config::PARAMETER_ERROR, "Failed to convert the tenant ID." );
        }

        // Create a URL (Referring to the global IP address)
        $url  = neccsNal_Config::API_URL;
        $url .= neccsNal_Config::API_URL_LIST;
        $url .= neccsNal_Config::$setReferResource[neccsNal_Config::EXT_GLOBALIP];
        $url .= '?' . 'tenant_name=' . $this->_p['tenant_name'];
        $url .= '&' . 'global_ip=' . $globalIp;
        $url .= '&' . 'delete_flg=' . '0';
        $request_id = isset( $this->_p['request-id'] ) ? $this->_p['request-id'] : $this->_requestId;
        $url .= '&' . 'request-id=' . $request_id;

        // Referring to the global IP address
        $globalIpInfo = array();
        $globalIpInfo = $this->_execApiHttpMethod( $url, '', '', neccsNal_Config::HTTP_GET );

        // If the global IP address information can not be acquired
        if( empty( $globalIpInfo ) ) {
            $this->error( neccsNal_Config::REST_API_ERROR, "global ip not exists. ($globalIp)" );
        }

        $url  = neccsNal_Config::API_URL;
        $url .= neccsNal_Config::API_URL_LIST;
        $url .= neccsNal_Config::RESOURCE_GLOBAL_IP_ADDR . '/';
        $url .= $globalIpInfo[0]['ID']; // Key to be updated

        $status = $this->_p['status'];
        $request_id = isset( $this->_p['request-id'] ) ? $this->_p['request-id'] : $this->_requestId;
        $node_id = isset( $this->_p['node_id'] ) ? $this->_p['node_id'] : '';

        $param = array();
        $param['status'] = neccsNal_Config::$globalIpUpdateStatus[$status];
        $param['node_id'] = $node_id;
        $param['request-id'] = $request_id;
        $result = $this->_execApi( $url, $param );

        // It outputs the result
        $this->success( $result );
    }

    protected function _getContInfo( $execList ){

        $result = array();

        // Get tenant name
        $tenantInfo = $execList['tenants_info'];
        $tenantName = '';
        if ( !empty($tenantInfo) ){
            $tenantName = $tenantInfo[0]['tenant_name'];
        }

        // Get node name
        $aplInfo = $execList['appliances_info'];
        $node_name_list = array();
        foreach( $aplInfo as $aplData ){
            if( $aplData['node_id'] !== '' && $aplData['apl_type'] === neccsNal_Config::APL_TYPE_VIRTUAL ){
                $node_name_list[$aplData['node_id']] = $aplData['node_name'];
            }else if( $aplData['node_id'] !== '' && $aplData['apl_type'] === neccsNal_Config::APL_TYPE_PHYSICS ){
                $node_name_list[$aplData['node_id']] = $aplData['device_user_name'];
            }
        }

        // Create global IP list
        $globalipInfo = $execList['global_ip_address_info'];
        $result = array();
        $result['contract_info'] = array();
        foreach( $globalipInfo as $globalipData ){
            if( $globalipData['tenant_name'] === $tenantName ){

                $resource_name = neccsNal_Config::EXT_GLOBALIP;
                if( !in_array( $globalipData['status'], neccsNal_Config::$useCntStatusList[$resource_name] ) ){
                    continue;
                }

                $data = array();
                $data['ID']                 = $globalipData['ID'];
                $data['globalip']           = $globalipData['global_ip'];
                $data['node_id']            = $globalipData['node_id'];
                $data['tenant_name']        = $globalipData['tenant_name'];
                if ( array_key_exists( $globalipData['node_id'], $node_name_list ) ) {
                    $data['node_name']      = $node_name_list[$globalipData['node_id']];
                }else{
                    $data['node_name']      = '';
                }
                if ( $globalipData['tenant_name'] === $tenantName ) {
                    $data['IaaS_tenant_id'] = $this->_p['IaaS_tenant_id'];
                }else{
                    $data['IaaS_tenant_id'] = '';
                }
                // When using a tenant
                if( $globalipData['status']  == '202' ){
                    $data['use_status']     = '1';
                }else{
                    $data['use_status']     = '0';

                }

                array_push($result['contract_info'], $data);
            }
        }

        // Get contract num
        $contractInfo = $execList['tenant_contract_info'];
        $contractCnt = 0;
        foreach( $contractInfo as $contractData ){
            if( $contractData['tenant_name'] === $tenantName ){
                $contractCnt += $contractData['contract'];
            }
        }

        // Create unused global IP list
        $unusedCnt = $contractCnt - count($result['contract_info']);
        for ($count = 0; $count < $unusedCnt; $count++){
            $data['ID']             = '';
            $data['globalip']       = '';
            $data['node_id']        = '';
            $data['node_name']      = '';
            $data['tenant_name']    = $tenantName;
            $data['IaaS_tenant_id'] = $this->_p['IaaS_tenant_id'];
            $data['use_status']     = '3';
            array_push($result['contract_info'], $data);
        }

        return $result;

    }

}
