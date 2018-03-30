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
* 2.FUNCTION : globalip.php (Individual method)
*/
require_once dirname(__FILE__). '/../Nal.php';

class globalip extends neccsNal {

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

        // Get the tenant contract information
        $url  = neccsNal_Config::API_URL;
        $url .= neccsNal_Config::API_URL_LIST;
        $url .= neccsNal_Config::RESOURCE_CONTRACT;
        $request_id = isset( $this->_p['request-id'] ) ? $this->_p['request-id'] : $this->_requestId;
        $url .= '?' . 'request-id=' . $request_id;
        $url .= '&' . 'contract_kind=' . '1';
        $url .= '&' . 'delete_flg=0';

        $url_list['tenant_contract_info'] = $url;

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
        $url .= '&' . 'delete_flg=0';

        $url_list['tenants_info'] = $url;

        $execList = $this->_execMultiApi( $url_list );

        // get the use_cnt
        $result = array();
        $result = $this->_getContInfo( $execList );

        $url = neccsNal_Config::NAL_API_URL . str_replace( '/Nal/', '', $_SERVER['REQUEST_URI'] );
        $this->logit( neccsNal_Config::SUCCESS_CODE, "OutPut Data ( $url )", $this->_p, $result );

        $this->success( $result );
    }

    protected function _getContInfo( $execList ){

        $param = array();
        $param = $this->_p;
        $param['nw_resource_kind'] = neccsNal_Config::NW_RESOURCE_KIND_GLOBALIP;

        $result = array();
        $result['total_info']['quota']           = $this->_getQuotaGlobalip( $execList );
        $result['total_info']['contract_cnt']    = $this->_getContractCntGlobalip( $execList, $param );
        $result['total_info']['use_cnt']         = $this->_getUseCntGlobalip( $execList, $param );
        $result['total_info']['unavailable_cnt'] = $this->_getUnavailableCntGlobalip( $execList );

        // Get node name
        $aplInfo = $execList['appliances_info'];
        $node_name_list = array();
        foreach( $aplInfo as $aplData ){
            $node_name_list[$aplData['node_id']] = $aplData['node_name'];
        }

        // Get IaaS tenant ID
        $tenantInfo = $execList['tenants_info'];
        $tenant_id_list = array();
        foreach( $tenantInfo as $tenantData ){
            $tenant_id_list[$tenantData['tenant_name']] = $tenantData['IaaS_tenant_id'];
        }

        // Create global IP list
        $globalipInfo = $execList['global_ip_address_info'];
        $result['contract_info'] = array();
        foreach( $globalipInfo as $globalipData ){
            $data = array();
            $data['ID']                 = $globalipData['ID'];
            $data['globalip']           = $globalipData['global_ip'];
            $data['node_id']            = $globalipData['node_id'];
            $data['tenant_name']        = $globalipData['tenant_name'];
            $data['task_status']        = $globalipData['status'];
            if ( $globalipData['node_id'] !== '' && array_key_exists( $globalipData['node_id'], $node_name_list ) ) {
                $data['node_name']      = $node_name_list[$globalipData['node_id']];
            }else{
                $data['node_name']      = '';
            }
            if ( array_key_exists( $globalipData['tenant_name'], $tenant_id_list ) ) {
                $data['IaaS_tenant_id'] = $tenant_id_list[$globalipData['tenant_name']];
            }else{
                $data['IaaS_tenant_id'] = '';
            }
            $resource_name = neccsNal_Config::GLOBALIP;
            if( in_array( $globalipData['status'], neccsNal_Config::$useCntStatusList[$resource_name] ) ){
                $data['use_status']     = '1';
            }else{
                $data['use_status']     = '0';
            }

            array_push($result['contract_info'], $data);
        }

        return $result;

    }
}
