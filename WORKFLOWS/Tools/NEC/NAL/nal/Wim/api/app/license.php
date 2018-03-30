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
* 2.FUNCTION : license.php (Individual method)
*/
require_once dirname(__FILE__). '/../Nal.php';

class license extends neccsNal {

    /**
     * GET method (list,refer)
     *
     */
    protected function get() {

        if( $this->_nalConf['api_type'] === neccsNal_Config::API_TYPE_NAL ){

            // Get the tenant contract information
            $url  = neccsNal_Config::API_URL;
            $url .= neccsNal_Config::API_URL_LIST;
            $url .= neccsNal_Config::RESOURCE_TENANTS;
            $request_id = isset( $this->_p['request-id'] ) ? $this->_p['request-id'] : $this->_requestId;
            $url .= '?' . 'request-id=' . $request_id;
            $url .= '&' . 'delete_flg=0';

            $url_list['tenant_info'] = $url;

            // Get the tenant contract information
            $url  = neccsNal_Config::API_URL;
            $url .= neccsNal_Config::API_URL_LIST;
            $url .= neccsNal_Config::RESOURCE_CONTRACT;
            $request_id = isset( $this->_p['request-id'] ) ? $this->_p['request-id'] : $this->_requestId;
            $url .= '?' . 'request-id=' . $request_id;
            $url .= '&' . 'type=' . $this->_p['type'];
            $url .= '&' . 'device_type=' . $this->_p['device_type'];
            $url .= '&' . 'apl_type=1';
            $url .= '&' . 'delete_flg=0';

            $url_list['tenant_contract_info'] = $url;

            // Get the ten information
            $url  = neccsNal_Config::API_URL;
            $url .= neccsNal_Config::API_URL_LIST;
            $url .= neccsNal_Config::RESOURCE_LICENSES;
            $request_id = isset( $this->_p['request-id'] ) ? $this->_p['request-id'] : $this->_requestId;
            $url .= '?' . 'request-id=' . $request_id;
            $url .= '&' . 'type=' . $this->_p['type'];
            $url .= '&' . 'device_type=' . $this->_p['device_type'];
            $url .= '&' . 'delete_flg=0';

            if( ( $this->_p['type'] === neccsNal_Config::TYPE_FW && $this->_p['device_type'] === neccsNal_Config::PALOALTO )
               || $this->_p['type'] === neccsNal_Config::TYPE_ROUTER && $this->_p['device_type'] === neccsNal_Config::CISCO ){
                $url .= '&' . 'type_detail=' . $this->_p['type_detail'];
            }

            $url_list['license_info'] = $url;

            $execList = $this->_execMultiApi( $url_list );

            // Create a URL (Call of WIM API)
            $url = neccsNal_Config::WIM_API_URL . str_replace( '/Nal/', '', $_SERVER['REQUEST_URI'] );
            $url .= '&request-id='. $this->_p['request-id'];

            // API execution
            $resultForWim = array();
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

        if( $this->_nalConf['api_type'] === neccsNal_Config::API_TYPE_WIM ){

            $url  = neccsNal_Config::API_URL;
            $url .= neccsNal_Config::API_URL_LIST;
            $url .= neccsNal_Config::RESOURCE_DC_CON_GROUPS;
            $request_id = isset( $this->_p['request-id'] ) ? $this->_p['request-id'] : $this->_requestId;
            $url .= '?' . 'request-id=' . $request_id;
            $url .= '&' . 'delete_flg=0';

            $url_list['dc_group_info'] = $url;

            $url  = neccsNal_Config::API_URL;
            $url .= neccsNal_Config::API_URL_LIST;
            $url .= neccsNal_Config::RESOURCE_DC_CON_MEMBERS;
            $request_id = isset( $this->_p['request-id'] ) ? $this->_p['request-id'] : $this->_requestId;
            $url .= '?' . 'request-id=' . $request_id;
            $url .= '&' . 'delete_flg=0';

            $url_list['dc_member_info'] = $url;
            $execList = $this->_execMultiApi( $url_list );

            $this->success( $execList );
        }

    }


    /**
     * Format information acquired from REST API
     *
     * @param REST API information
     *
     * @return $result
     */
    protected function _getContInfo( $execList ){
        $param = array();
        $param = $this->_p;

        $result = array();
        $result['total_info']['quota']                               = $this->_getQuotaLisence( $execList, $param );
        $result['total_info']['unavailable_cnt']                     = $this->_getUnavailableCntLicense( $execList, $param );
        list( $result['total_info']['contract_cnt'], $contractList ) = $this->_getContractCntLicense( $execList, $param );
        list( $result['total_info']['use_cnt'], $useList )           = $this->_getUseCntLicense( $execList, $param );

        $data = array();
        foreach( $execList['tenant_info'] as $key => $value ){

            $tenant_name            = $value['tenant_name'];
            $data['tenant_name']    = $tenant_name;
            $data['IaaS_tenant_id'] = $value['IaaS_tenant_id'];
            $data['ID']             = $value['ID'];

            if( isset( $contractList[$tenant_name]['contract_cnt'] ) || isset( $useList[$tenant_name]['use_cnt'] ) ){
                $data['contract_cnt'] = isset( $contractList[$tenant_name]['contract_cnt'] ) ? $contractList[$tenant_name]['contract_cnt'] : 0;
                $data['use_cnt'] = isset( $useList[$tenant_name]['use_cnt'] ) ? $useList[$tenant_name]['use_cnt'] : 0;

                if( $data['contract_cnt'] != 0 || $data['use_cnt'] != 0 ){
                    $result['contract_info'][] = $data;
                }
            }
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
