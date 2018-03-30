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
 * 2.FUNCTION : all_dcconnect.php (Individual method)
 */
require_once dirname(__FILE__). '/../Nal.php';

class all_dcconnect extends neccsNal {

    /**
     * GET method (list,refer)
     *
     */
    protected function get() {

        // In NAL server, in the case of the NAL call
        if( $this->_nalConf['api_type'] === neccsNal_Config::API_TYPE_NAL ){

            // Create a URL (Call the WIM API)
            $url = neccsNal_Config::WIM_API_URL . str_replace( '/Nal/', '', $_SERVER['REQUEST_URI'] );
            $url .= '&request-id='. $this->_p['request-id'];

            // Run the API
            $result = $this->_execApi( $url );

            // To add a group information of the flag of that is included in its own DC ID to the information of the DC groups
            if( isset( $result['data']['my_group_list'] ) ){

                $myGroupList = $result['data']['my_group_list'];
                foreach( $result['data'] as $key => $value ){

                    if( $key === 'my_group_list' ) {
                        continue;
                    }

                    $group_id = $value['group_id'];
                    // In the case of group ID that does not exist in the key of DC ID list, processing end
                    if( !isset( $myGroupList[$group_id] ) ) {
                        continue;
                    }

                    // If you are running the PHPUnit test, specify a dummy data
                    if( defined('PHPUNIT_RUN') ){
                        $my_dc_id = $this->_p['my_dc_id'];
                    }else{
                        $my_dc_id = neccsNal_Config::MY_DC_ID;
                    }

                    // If it contains its own DC ID to the list, to add a flag
                    if( in_array( $my_dc_id, $myGroupList[$group_id] ) ){
                        $result['data'][$key]['my_group_flg'] = '1';
                    }
                }

                unset( $result['data']['my_group_list'] );
            }

            $this->_execResult( $result, $url );
        }

        // If the WIN server
        if( $this->_nalConf['api_type'] === neccsNal_Config::API_TYPE_WIM ) {

            // Create a URL
            $url = $this->_setUrl();

            // Run the Rest API
            $result = $this->_execApi( $url );

            // Shaping the acquired data
            $result = $this->_setDataForDc( $result );

            // It outputs the result
            $this->success( $result );
        }

    }

    /**
     * Response return
     *
     * @param Execution result
     * @param URL
     */
    protected function _execResult( $result, $url ) {

        // If the API execution results are included result, the result is output directly
        if ( array_key_exists( 'result', $result ) ) {

            // Acquisition of the error code
            $code = $result['result']['error-code'];
            if( in_array( $code, neccsNal_Config::$successApiCode ) ){
                // Output log
                $this->logit( neccsNal_Config::SUCCESS_CODE, "WIM API success ( $url )", $this->_p, $result );
                // In the case of error
            }else if( in_array( $code, neccsNal_Config::$errorApiCode ) ){
                $errMsg = $result['result']['message'];
                // Output log
                $this->logit($code, $errMsg , '', $result);
            }

            // If you are running the PHPUnit test, return only message
            if( defined( 'PHPUNIT_RUN' ) ){
                throw new Exception( $result['result']['message'] );
            }

            // Response return
            header( "HTTP/1.1 200" );
            header( neccsNal_Config::CONTENT_TYPE_JSON );
            print json_encode( $result );
            exit(0);
        }
    }

    /**
     * Shape the API execution result
     *
     * @param Execution result
     */
    protected function _setDataForDc( $result ){

        // Run only when the tenant administrator
        if( !isset( $this->_p['IaaS_tenant_id'] ) ){
            return  $result;
        }

        // Get the tenant name from the tenant ID
        $this->_p['tenant_name'] = $this->_getTenant( $this->_p['IaaS_tenant_id'] );

        // Create a URL (Referring to the members)
        $url  = neccsNal_Config::API_URL;
        $url .= neccsNal_Config::API_URL_LIST;
        $url .= neccsNal_Config::RESOURCE_DC_CON_MEMBERS;
        $url .= '?' . 'tenant_name=' . $this->_p['tenant_name'];
        $url .= '&' . 'delete_flg=' . 0;
        $request_id = isset( $this->_p['request-id'] ) ? $this->_p['request-id'] : $this->_requestId;
        $url .= '&' . 'request-id=' . $request_id;

        // Referring to the members
        $dcMenberInfo = array();
        $dcMenberInfo = $this->_execApiHttpMethod( $url, '', '', neccsNal_Config::HTTP_GET );

        // To get the DC ID that brute cord to the group ID, group ID as a key
        $result['my_group_list'] = array();
        foreach( $dcMenberInfo as $value ){
            if( !isset( $value['group_id'] ) ) { continue; }
            $group_id = $value['group_id'];
            $result['my_group_list'][$group_id][] = $value['dc_id'];
        }

        return $result;

    }
}
