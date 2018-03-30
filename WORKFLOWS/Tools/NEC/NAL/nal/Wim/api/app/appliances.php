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
 * 2.FUNCTION : appliances.php (Individual method)
 */
require_once dirname(__FILE__). '/../Nal.php';

class appliances extends neccsNal {

    /**
     * GET method (list,refer)
     *
     */
    protected function get() {

        // Get the appliance information
        $url  = neccsNal_Config::API_URL;
        $url .= neccsNal_Config::API_URL_LIST;
        $url .= neccsNal_Config::RESOURCE_APLS;
        $request_id = isset( $this->_p['request-id'] ) ? $this->_p['request-id'] : $this->_requestId;
        $url .= '?' . 'request-id=' . $request_id;
        $url .= '&' . 'apl_type=' . $this->_p['apl_type'];
        $url .= '&' . 'type=' . $this->_p['type'];
        $url .= '&' . 'device_type=' . $this->_p['device_type'];
        $url .= '&' . 'delete_flg=0';
        if( $this->_p['apl_type'] === neccsNal_Config::APL_TYPE_PHYSICS ){
            if( $this->_p['device_type'] === neccsNal_Config::PFW_FORTIGATE || $this->_p['device_type'] === neccsNal_Config::PFW_PALOALTO
               || $this->_p['device_type'] === neccsNal_Config::PLB_BIGIP || $this->_p['device_type'] === neccsNal_Config::PLB_THUNDER ){
                $url .= '&' . 'redundant_configuration_flg=' . $this->_p['redundant_configuration_flg'];
            }
        }

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
        $url .= '&' . 'contract_kind=' . '2';
        $url .= '&' . 'apl_type=' . $this->_p['apl_type'];
        $url .= '&' . 'type=' . $this->_p['type'];
        $url .= '&' . 'device_type=' . $this->_p['device_type'];
        $url .= '&' . 'delete_flg=0';
        if( $this->_p['apl_type'] === neccsNal_Config::APL_TYPE_PHYSICS ){
            if( $this->_p['device_type'] === neccsNal_Config::PFW_FORTIGATE || $this->_p['device_type'] === neccsNal_Config::PFW_PALOALTO
               || $this->_p['device_type'] === neccsNal_Config::PLB_BIGIP || $this->_p['device_type'] === neccsNal_Config::PLB_THUNDER ){
                $url .= '&' . 'redundant_configuration_flg=' . $this->_p['redundant_configuration_flg'];
            }
        }

        $url_list['tenant_contract_info'] = $url;

        $execList = $this->_execMultiApi( $url_list );

        // get the use_cnt
        $result = array();
        $result = $this->_getContInfo( $execList );

        $url = neccsNal_Config::NAL_API_URL . str_replace( '/Nal/', '', $_SERVER['REQUEST_URI'] );
        $this->logit( neccsNal_Config::SUCCESS_CODE, "OutPut Data ( $url )", $this->_p, $result );

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

        // Create appliances list
        $apl_type    = $this->_p['apl_type'];
        $type        = $this->_p['type'];
        $device_type = $this->_p['device_type'];

        $aplInfo = $execList['appliances_info'];
        $result = array();
        $result['contract_info'] = array();
        foreach( $aplInfo as $aplData ){
            if( $aplData['tenant_name'] === $tenantName && $tenantName !== '' ){
                $data = array();
                $data['ID']             = $aplData['ID'];
                $data['node_id']        = $aplData['node_id'];
                $data['task_status']    = $aplData['task_status'];
                $data['tenant_name']    = $aplData['tenant_name'];
                $data['IaaS_tenant_id'] = $this->_p['IaaS_tenant_id'];
                $data['use_status'] = '1';
                if( $this->_p['apl_type'] === neccsNal_Config::APL_TYPE_VIRTUAL ){
                    $data['node_name']  = $aplData['node_name'];
                }else{
                    $data['node_name']  = $aplData['device_user_name'];
                }

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

        // Create unused appliances list
        $unusedCnt = $contractCnt - count($result['contract_info']);
        for ($count = 0; $count < $unusedCnt; $count++){
            $data['ID']             = '';
            $data['node_id']        = '';
            $data['node_name']      = '';
            $data['task_status']    = '';
            $data['tenant_name']    = $tenantName;
            $data['IaaS_tenant_id'] = $this->_p['IaaS_tenant_id'];
            $data['use_status']     = '0';
            array_push($result['contract_info'], $data);
        }

        return $result;

    }

}

