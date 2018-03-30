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
* 2.FUNCTION : pnf.php (Individual method)
*/
require_once dirname(__FILE__). '/../Nal.php';

class pnf extends neccsNal {

    /**
     * GET method (list,refer)
     *
     */
    protected function get() {

        // Get the tenant contract information
        $url  = neccsNal_Config::API_URL;
        $url .= neccsNal_Config::API_URL_LIST;
        $url .= neccsNal_Config::RESOURCE_CONTRACT;
        $request_id = isset( $this->_p['request-id'] ) ? $this->_p['request-id'] : $this->_requestId;
        $url .= '?' . 'request-id=' . $request_id;
        $url .= '&' . 'contract_kind=' . '2';
        $url .= '&' . 'apl_type=' . '2';
        $url .= '&' . 'type=' . $this->_p['type'];
        $url .= '&' . 'device_type=' . $this->_p['device_type'];

        if( $this->_p['device_type'] === neccsNal_Config::PFW_FORTIGATE || $this->_p['device_type'] === neccsNal_Config::PFW_PALOALTO
           || $this->_p['device_type'] === neccsNal_Config::PLB_BIGIP || $this->_p['device_type'] === neccsNal_Config::PLB_THUNDER ){
            $url .= '&' . 'redundant_configuration_flg=' . $this->_p['redundant_configuration_flg'];
        }

        $url_list['tenant_contract_info'] = $url;

        // Get the ten information
        $url  = neccsNal_Config::API_URL;
        $url .= neccsNal_Config::API_URL_LIST;
        $url .= neccsNal_Config::RESOURCE_APLS;
        $request_id = isset( $this->_p['request-id'] ) ? $this->_p['request-id'] : $this->_requestId;
        $url .= '?' . 'request-id=' . $request_id;
        $url .= '&' . 'apl_type=2';
        $url .= '&' . 'type=' . $this->_p['type'];
        $url .= '&' . 'device_type=' . $this->_p['device_type'];

        if( $this->_p['device_type'] === neccsNal_Config::PFW_FORTIGATE || $this->_p['device_type'] === neccsNal_Config::PFW_PALOALTO
           || $this->_p['device_type'] === neccsNal_Config::PLB_BIGIP || $this->_p['device_type'] === neccsNal_Config::PLB_THUNDER ){
            $url .= '&' . 'redundant_configuration_flg=' . $this->_p['redundant_configuration_flg'];
        }

        $url_list['apl_info'] = $url;

        $execList = $this->_execMultiApi( $url_list );
        $result = $this->_getContInfo( $execList );

        $url = neccsNal_Config::NAL_API_URL . str_replace( '/Nal/', '', $_SERVER['REQUEST_URI'] );
        $this->logit( neccsNal_Config::SUCCESS_CODE, "OutPut Data ( $url )", $this->_p, $result );

        $this->success( $result );

    }

    protected function _getContInfo( $execList ){

        $param = array();
        $param = $this->_p;

        $result = array();
        $result['total_info']['quota']           = $this->_getQuotaPnf( $execList, $param );
        $result['total_info']['contract_cnt']    = $this->_getContractCntPnf( $execList, $param );
        $result['total_info']['use_cnt']         = $this->_getUseCntPnf( $execList, $param );
        $result['total_info']['unavailable_cnt'] = $this->_getUnavailableCntPnf( $execList, $param );

        $data = array();
        $apl_info = $execList['apl_info'];
        $result['contract_info'] = array();
        foreach( $apl_info as $value ){
            $task_status = $value['task_status'];
            $data['node_id']            = $value['node_id'];
            $data['device_user_name']   = $value['device_user_name'];
            $data['tenant_name']        = $value['tenant_name'];
            $data['IaaS_tenant_id']     = $value['IaaS_tenant_id'];
            $data['device_name_master'] = $value['device_name_master'];
            $data['ID']                 = $value['ID'];
            $data['task_status']        = $task_status;
            if( $data['task_status'] === '0' || $data['tenant_name'] === '' ){
                $data['use_status']     = 0;
            } else {
                $data['use_status']     = 1;
            }
            $result['contract_info'][] = $data;
        }

        return $result;

    }
}
