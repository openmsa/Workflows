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
 * 2.FUNCTION : service.php (Individual method)
 */
require_once dirname(__FILE__). '/../Nal.php';

class service extends neccsNal {

    /**
     * GET method (list,refer)
     *
     */
    protected function get() {

        // In NAL server, in the case of the NAL call
        if( $this->_nalConf['api_type'] === neccsNal_Config::API_TYPE_NAL ){

            // Get the tenant contract information
            $url  = neccsNal_Config::API_URL;
            $url .= neccsNal_Config::API_URL_LIST;
            $url .= neccsNal_Config::RESOURCE_CONTRACT;
            $request_id = isset( $this->_p['request-id'] ) ? $this->_p['request-id'] : $this->_requestId;
            $url .= '?' . 'request-id=' . $request_id;
            $url .= '&' . 'contract_kind=' . '3';
            $url .= '&' . 'device_type=' . $this->_p['device_type'];
            $url .= '&' . 'delete_flg=0';

            $url_list['tenant_contract_info'] = $url;

            // Get the tenant information
            $url  = neccsNal_Config::API_URL;
            $url .= neccsNal_Config::API_URL_LIST;
            $url .= neccsNal_Config::RESOURCE_TENANTS;
            $request_id = isset( $this->_p['request-id'] ) ? $this->_p['request-id'] : $this->_requestId;
            $url .= '?' . 'request-id=' . $request_id;
            $url .= '&' . 'IaaS_tenant_id=' . $this->_p['IaaS_tenant_id'];
            $url .= '&' . 'delete_flg=0';

            $url_list['tenants_info'] = $url;

            $execList = $this->_execMultiApi( $url_list );

            // Create a URL (Call of WIM API)
            $url = neccsNal_Config::WIM_API_URL . str_replace( '/Nal/', '', $_SERVER['REQUEST_URI'] );
            $url .= '&request-id='. $this->_p['request-id'];

            // API execution
            $resultForWim = $this->_execApi( $url );

            $status = isset( $resultForWim['result']['status'] ) ? $resultForWim['result']['status'] : '';
            if( $status === neccsNal_Config::STATUS_SUCCESS ) {
                $data = $resultForWim['data'];
            } else {
                $this->_execResult( $resultForWim, $url );
            }

            // get the use_cnt
            $result = array();
            $result = $this->_getContInfo( array_merge( $execList, $data ) );

            $url = neccsNal_Config::NAL_API_URL . str_replace( '/Nal/', '', $_SERVER['REQUEST_URI'] );
            $this->logit( neccsNal_Config::SUCCESS_CODE, "OutPut Data ( $url )", $this->_p, $result );

            $this->success( $result );
        }

        // If the WINS server
        if( $this->_nalConf['api_type'] === neccsNal_Config::API_TYPE_WIM ) {

            // Get the tenant contract information
            $url  = neccsNal_Config::API_URL;
            $url .= neccsNal_Config::API_URL_LIST;
            $url .= neccsNal_Config::RESOURCE_DC_CON_GROUPS;
            $request_id = isset( $this->_p['request-id'] ) ? $this->_p['request-id'] : $this->_requestId;
            $url .= '?' . 'request-id=' . $request_id;
            $url .= '&' . 'delete_flg=0';

            $url_list['dc_group_info'] = $url;

            $execList = $this->_execMultiApi( $url_list );

            $this->success( $execList );
        }

    }

    protected function _getContInfo( $execList ){

        $result = array();

        // Get tenant name
        $tenantInfo = $execList['tenants_info'];
        $tenantName = '';
        if ( !empty($tenantInfo) ){
            $tenantName = $tenantInfo[0]['tenant_name'];
        }

        // Create dc group list
        $dcGroupInfo = $execList['dc_group_info'];
        $result = array();
        $result['contract_info'] = array();
        foreach( $dcGroupInfo as $dcGroupData ){

            $device_type = $this->_p['device_type'];
            if( !in_array( $dcGroupData['group_type'], neccsNal_Config::$serviceTypeList[$device_type] ) ){
                continue;
            }

            if( $dcGroupData['tenant_name'] === $tenantName && $tenantName !== '' ){
                $data = array();
                $data['ID']             = $dcGroupData['ID'];
                $data['group_id']       = $dcGroupData['group_id'];
                $data['group_type']     = $dcGroupData['group_type'];
                $data['group_name']     = $dcGroupData['group_name'];
                $data['tenant_name']    = $dcGroupData['tenant_name'];
                $data['task_status']    = $dcGroupData['task_status'];
                $data['IaaS_tenant_id'] = $this->_p['IaaS_tenant_id'];
                $data['use_status']     = '1';
                array_push($result['contract_info'], $data);
            }
        }

        // Get contract num
        $contractInfo = $execList['tenant_contract_info'];
        $contractCnt = 0;
        foreach( $contractInfo as $contractData ){
            if( $contractData['tenant_name'] === $tenantName && $tenantName !== '' ){
                $contractCnt += $contractData['contract'];
            }
        }

        // Create unused global IP list
        $unusedCnt = $contractCnt - count($result['contract_info']);
        for ($count = 0; $count < $unusedCnt; $count++){
            $data['ID']             = '';
            $data['group_id']       = '';
            $data['group_type']     = '';
            $data['group_name']     = '';
            $data['task_status']    = '';
            $data['tenant_name']    = $tenantName;
            $data['IaaS_tenant_id'] = $this->_p['IaaS_tenant_id'];
            $data['use_status']     = '0';
            array_push($result['contract_info'], $data);
        }

        return $result;

    }

    /**
     * Return of the response
     *
     * @param Execution result
     * @param URL
     */
    protected function _execResult( $result, $url ) {

        // If the API execution result contains the "result", the result is output directly
        if ( array_key_exists( 'result', $result ) ) {

            // Get the error code
            $code = $result['result']['error-code'];
            if( in_array( $code, neccsNal_Config::$successApiCode ) ){
                // Output log
                $this->logit( neccsNal_Config::SUCCESS_CODE, "WIM API success ( $url )", $this->_p, $result );

                // If you are running the PHPUnit test, as it is the end
                if( defined( 'PHPUNIT_RUN' ) ){
                    return;
                }

                // In the case of error
            }else if( in_array( $code, neccsNal_Config::$errorApiCode ) ){
                $errMsg = $result['result']['message'];
                // Output log
                $this->logit( neccsNal_Config::REST_API_ERROR, $errMsg, '', $result );
            }

            // If you are running the PHPUnit test, as it is the end
            if( defined( 'PHPUNIT_RUN' ) ){
                throw new Exception( $result['result']['message'] );
            }

            header( "HTTP/1.1 200" );
            header( neccsNal_Config::CONTENT_TYPE_JSON );
            print json_encode( $result );
            exit(0);
        }
    }

}

