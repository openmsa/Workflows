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
 * 2.FUNCTION : globalip_payout.php (Individual method)
 */
require_once dirname(__FILE__). '/../Nal.php';

class globalip_payout extends neccsNal {

    /**
     * PUT method (It pays out a global IP address)
     *
     */
    protected function put() {

        // IaaS tenant id
        if( isset( $this->_p['IaaS_tenant_id'] ) ) {
            $IaaSTenantId = $this->_p['IaaS_tenant_id'];
        } else {
            $this->error( neccsNal_Config::PARAMETER_ERROR, "IaaS_tenant_id is not set." );
        }

        // Payout number
        if( isset( $this->_p['count'] ) ) {
            $count = $this->_p['count'];
        } else {
            $this->error( neccsNal_Config::PARAMETER_ERROR, "count is not set." );
        }

        // Convert the tenant ID
        $this->_p['tenant_name'] = $this->_getTenant( $IaaSTenantId );

        // Failure to convert the tenant ID
        if( empty( $this->_p['tenant_name'] ) ) {
            $this->error( neccsNal_Config::PARAMETER_ERROR, "Failed to convert the tenant ID." );
        }

        // Create a URL (Referring to the global IP address)
        $baseUrl  = neccsNal_Config::API_URL;
        $baseUrl .= neccsNal_Config::API_URL_LIST;
        $baseUrl .= neccsNal_Config::$setReferResource[neccsNal_Config::GLOBALIP];
        $baseUrl .= '?' . 'delete_flg=' . '0';
        $request_id = isset( $this->_p['request-id'] ) ? $this->_p['request-id'] : $this->_requestId;
        $baseUrl .= '&' . 'request-id=' . $request_id;

        // Add the state to the URL (Use state: unused)
        $url = $baseUrl . '&status=0';

        // Referring to the global IP address (Use state: unused)
        $unUsedGlobalIpInfo = array();
        $unUsedGlobalIpInfo = $this->_execApiHttpMethod( $url, '', '', neccsNal_Config::HTTP_GET );

        // Add the state to the URL (Use state: auto refund
        $url = $baseUrl . '&status=103';

        // Referring to the global IP address (Use state: auto refund)
        $returnGlobalIpAutoInfo = array();
        $returnGlobalIpAutoInfo = $this->_execApiHttpMethod( $url, '', '', neccsNal_Config::HTTP_GET );

        // Add the state to the URL (Use state: manual refund
        $url = $baseUrl . '&status=203';

        // Referring to the global IP address (Use state: manual refund)
        $returnGlobalIpManualInfo = array();
        $returnGlobalIpManualInfo = $this->_execApiHttpMethod( $url, '', '', neccsNal_Config::HTTP_GET );

        // Merge the global IP address information available
        $globalIpInfo = array();
        $globalIpInfo = array_merge( $unUsedGlobalIpInfo, $returnGlobalIpAutoInfo, $returnGlobalIpManualInfo );

        // If it is unable to secure a payout number of items global IP
        if( intval( $count ) > count( $globalIpInfo ) ) {
            $this->error( neccsNal_Config::PARAMETER_ERROR, "There is no global IP inventory ." );
        }

        // Create a URL (Update the global IP address)
        $baseUrl  = neccsNal_Config::API_URL;
        $baseUrl .= neccsNal_Config::API_URL_LIST;
        $baseUrl .= neccsNal_Config::$setReferResource[neccsNal_Config::GLOBALIP] . '/';

        // Update parameters
        $param              = array();
        $param['update_id'] = isset( $this->_p['operation_id'] ) ? $this->_p['operation_id'] : '';
        $param['status']    = '201'; // Payout (Tenant within the unused)
        $param['tenant_name'] = $this->_p['tenant_name'];
        $request_id = isset( $this->_p['request-id'] ) ? $this->_p['request-id'] : $this->_requestId;
        $param['request-id'] = $request_id;

        // The payout number of items loop
        for( $i=0; $i < intval( $count ); $i++ ) {

            // ID addition to be updated key to the URL
            $url = $baseUrl . $globalIpInfo[$i]['ID'];

            // Global IP address update
            $result = $this->_execApi( $url, $param );
        }

        // It outputs the result
        $this->success( $result );
    }
}