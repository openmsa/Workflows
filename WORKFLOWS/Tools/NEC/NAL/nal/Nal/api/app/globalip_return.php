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
 * 2.FUNCTION : globalip_return.php (Individual method)
 */
require_once dirname(__FILE__). '/../Nal.php';

class globalip_return extends neccsNal {

    /**
     * PUT method (Reimburse the global IP address)
     *
     */
    protected function put() {

        // IaaS_tenant_id
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
        $url .= neccsNal_Config::$setReferResource[neccsNal_Config::GLOBALIP];
        $url .= '?' . 'tenant_name=' . $this->_p['tenant_name'];
        $url .= '&' . 'global_ip=' . $globalIp;
        $url .= '&' . 'status=201';
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

        // Create a URL (Reimburse the global IP address)
        $url  = neccsNal_Config::API_URL;
        $url .= neccsNal_Config::API_URL_LIST;
        $url .= neccsNal_Config::$setReferResource[neccsNal_Config::GLOBALIP] . '/';
        $url .= $globalIpInfo[0]['ID']; // Key to be updated

        // Update parameters
        $param               = array();
        $param['update_id']  = isset( $this->_p['operation_id'] ) ? $this->_p['operation_id'] : '';
        $param['status']     = '203'; // Refunds
        $param['tenant_name']  = '';
        $param['node_id']  = '';
        $request_id = isset( $this->_p['request-id'] ) ? $this->_p['request-id'] : $this->_requestId;
        $param['request-id'] = $request_id;

        // To update the global IP address
        $result = $this->_execApi( $url, $param );

        // It outputs the result
        $this->success( $result );
    }
}