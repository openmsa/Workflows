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
* 2.FUNCTION : plb.php (Individual method)
*/
require_once dirname(__FILE__). '/../Nal.php';

class plb extends neccsNal {

    /**
     * GET method (list,refer)
     *
     */
    protected function get() {

        $url  = neccsNal_Config::API_URL;
        $url .= neccsNal_Config::API_URL_LIST;
        $url .= neccsNal_Config::RESOURCE_APLS;
        $url .= '?' . 'ID=' . $this->_p['ID'];
        $url .= '&' . 'delete_flg=' . '0';
        $request_id = isset( $this->_p['request-id'] ) ? $this->_p['request-id'] : $this->_requestId;
        $url .= '&' . 'request-id=' . $request_id;

        // Referring to the global IP address
        $aplIpInfo = array();
        $aplIpInfo = $this->_execApiHttpMethod( $url, '', '', neccsNal_Config::HTTP_GET );

        if( empty( $aplIpInfo ) ){

            $result['pnf_info'] = array();
            $result['port_info'] = array();

        }else{

            $result['pnf_info'] = $aplIpInfo;

            if( !empty( $aplIpInfo[0]['node_id'] ) ){

                unset( $this->_p['ID'] );
                $this->_p['node_id'] = $aplIpInfo[0]['node_id'];

                // Create a URL
                $url = $this->_setUrl();

                // Run the API
                $result['port_info'] = $this->_execApi( $url );

            } else {

                $result['port_info'] = array();

            }

        }

        // It outputs the result
        $this->success( $result );

    }
}
