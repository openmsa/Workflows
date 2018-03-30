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
 * 2.FUNCTION : msa_vlan.php (Individual method)
 */
require_once dirname(__FILE__). '/../Nal.php';

class msa_vlan extends neccsNal {

    /**
     * GET method (list,refer)
     *
     */
    protected function get() {

        // Get the tenant contract information
        $url  = neccsNal_Config::API_URL;
        $url .= neccsNal_Config::API_URL_LIST;
        $url .= neccsNal_Config::RESOURCE_PODS;
        $request_id = isset( $this->_p['request-id'] ) ? $this->_p['request-id'] : $this->_requestId;
        $url .= '?' . 'request-id=' . $request_id;
        $url .= '&' . 'delete_flg=0';

        $url_list['pod_info'] = $url;

        // Get the tenant contract information
        $url  = neccsNal_Config::API_URL;
        $url .= neccsNal_Config::API_URL_LIST;
        $url .= neccsNal_Config::RESOURCE_CONTRACT;
        $request_id = isset( $this->_p['request-id'] ) ? $this->_p['request-id'] : $this->_requestId;
        $url .= '?' . 'request-id=' . $request_id;
        $url .= '&' . 'delete_flg=0';

        $url_list['tenant_contract_info'] = $url;

        // Get the ten information
        $url  = neccsNal_Config::API_URL;
        $url .= neccsNal_Config::API_URL_LIST;
        $url .= neccsNal_Config::RESOURCE_MSA;
        $request_id = isset( $this->_p['request-id'] ) ? $this->_p['request-id'] : $this->_requestId;
        $url .= '?' . 'request-id=' . $request_id;
        $url .= '&' . 'delete_flg=0';

        $url_list['msa_info'] = $url;

        $execList = $this->_execMultiApi( $url_list );
        $result = $this->_getContInfo( $execList );

        $url = neccsNal_Config::NAL_API_URL . str_replace( '/Nal/', '', $_SERVER['REQUEST_URI'] );
        $this->logit( neccsNal_Config::SUCCESS_CODE, "OutPut Data ( $url )", $this->_p, $result );

        $this->success( $result );
    }

    protected function _getContInfo( $execList ){

        $param = $this->_p;

        $result = array();
        $result['total_info']['quota']           = $this->_getQuotaMsa( $execList );
        $result['total_info']['contract_cnt']    = $this->_getContractCntMsa( $execList );
        $result['total_info']['use_cnt']         = $this->_getUseCntMsa( $execList, $param );
        $result['total_info']['unavailable_cnt'] = $this->_getUnavailableCntMsa( $execList );

        $data = array();
        $function_type = $this->_p['function_type'];
        $msaInfo = $execList['msa_info'];
        $result['contract_info'] = array();
        foreach( $msaInfo as $value ){
            $data['vlan_id']            = $value['vlan_id'];
            $data['tenant_name']        = $value['tenant_name'];
            $data['IaaS_tenant_id']     = $value['IaaS_tenant_id'];
            $data['ID']                 = $value['ID'];
            $data['task_status']        = $value['status'];
            if( in_array( $data['task_status'], neccsNal_Config::$useCntStatusList[$function_type] ) ){
                $data['use_status']     = "1";
            } else {
                $data['use_status']     = "0";
            }
            $result['contract_info'][] = $data;
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

