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
* 2.FUNCTION : all_resource.php (Individual method)
*/
require_once dirname(__FILE__). '/../Nal.php';

class all_resource extends neccsNal {

    /**
     * GET method (list,refer)
     *
     */
    protected function get() {

        // If you are an administrator
        if( !isset( $this->_p['IaaS_tenant_id'] )  ){

            if( $this->_nalConf['api_type'] === neccsNal_Config::API_TYPE_NAL ){

                // Get the ten information
                $url  = neccsNal_Config::API_URL;
                $url .= neccsNal_Config::API_URL_LIST;
                $url .= neccsNal_Config::RESOURCE_THRESHOLDS;
                $request_id = isset( $this->_p['request-id'] ) ? $this->_p['request-id'] : $this->_requestId;
                $url .= '?' . 'request-id=' . $request_id;
                $url .= '&' . 'delete_flg=0';

                $url_list['threshold_info'] = $url;

                // Get the tenant contract information
                $url  = neccsNal_Config::API_URL;
                $url .= neccsNal_Config::API_URL_LIST;
                $url .= neccsNal_Config::RESOURCE_CONTRACT;
                $request_id = isset( $this->_p['request-id'] ) ? $this->_p['request-id'] : $this->_requestId;
                $url .= '?' . 'request-id=' . $request_id;
                $url .= '&' . 'delete_flg=0';

                $url_list['tenant_contract_info'] = $url;

                // Get the tenant contract information
                $url  = neccsNal_Config::API_URL;
                $url .= neccsNal_Config::API_URL_LIST;
                $url .= neccsNal_Config::RESOURCE_PODS;
                $request_id = isset( $this->_p['request-id'] ) ? $this->_p['request-id'] : $this->_requestId;
                $url .= '?' . 'request-id=' . $request_id;
                $url .= '&' . 'delete_flg=0';

                $url_list['pod_info'] = $url;

                // Get the msa information
                $url  = neccsNal_Config::API_URL;
                $url .= neccsNal_Config::API_URL_LIST;
                $url .= neccsNal_Config::RESOURCE_MSA;
                $request_id = isset( $this->_p['request-id'] ) ? $this->_p['request-id'] : $this->_requestId;
                $url .= '?' . 'request-id=' . $request_id;
                $url .= '&' . 'delete_flg=0';

                $url_list['msa_info'] = $url;

                // Get the license information
                $url  = neccsNal_Config::API_URL;
                $url .= neccsNal_Config::API_URL_LIST;
                $url .= neccsNal_Config::RESOURCE_LICENSES;
                $request_id = isset( $this->_p['request-id'] ) ? $this->_p['request-id'] : $this->_requestId;
                $url .= '?' . 'request-id=' . $request_id;
                $url .= '&' . 'delete_flg=0';

                $url_list['license_info'] = $url;

                // Get the apl information
                $url  = neccsNal_Config::API_URL;
                $url .= neccsNal_Config::API_URL_LIST;
                $url .= neccsNal_Config::RESOURCE_APLS;
                $request_id = isset( $this->_p['request-id'] ) ? $this->_p['request-id'] : $this->_requestId;
                $url .= '?' . 'request-id=' . $request_id;
                $url .= '&' . 'delete_flg=0';

                $url_list['apl_info'] = $url;

                // Get the apl information
                $url  = neccsNal_Config::API_URL;
                $url .= neccsNal_Config::API_URL_LIST;
                $url .= neccsNal_Config::RESOURCE_GLOBAL_IP_ADDR;
                $request_id = isset( $this->_p['request-id'] ) ? $this->_p['request-id'] : $this->_requestId;
                $url .= '?' . 'request-id=' . $request_id;
                $url .= '&' . 'delete_flg=0';

                $url_list['global_ip_address_info'] = $url;

                $execList = $this->_execMultiApi( $url_list );

                // Get the qupta and use_cnt information
                $execList['oepnstack_info'] = $this->_getOpenStackCnt( $execList );

                $wim_use_flg = 0;
                foreach( $execList['pod_info'] as $pod ){
                    if( in_array( $pod['use_type'], array( neccsNal_Config::USE_TYPE_WIM, neccsNal_Config::USE_TYPE_SHARE ) ) ){
                        $wim_use_flg = '1';
                    }
                }

                $data = array();
                if( $wim_use_flg === '1' ){

                    // Create a URL (Call of WIM API)
                    $url = neccsNal_Config::WIM_API_URL . str_replace( '/Nal/', '', $_SERVER['REQUEST_URI'] );
                    $url .= '&request-id='. $this->_p['request-id'];

                    // API execution
                    $resultForWim = array();
                    $resultForWim = $this->_execApi( $url );

                    $status = isset( $resultForWim['result']['status'] ) ? $resultForWim['result']['status'] : '';
                    $dcChk  = isset( $resultForWim['data']['wim_check_flg'] ) ? $resultForWim['data']['wim_check_flg'] : '';
                    if( $status === neccsNal_Config::STATUS_SUCCESS && $dcChk === '1' ) {
                        $data = $resultForWim['data'];
                    } else {
                        $this->_execResult( $resultForWim, $url );
                    }
                } else {
                    $execList['dc_group_info'] = array();
                    $execList['dc_member_info'] = array();
                    $execList['wan_info'] = array();
                }

                // get the use_cnt
                $result = $this->_getContInfo( array_merge( $execList, $data ) );

                foreach( $result['contract_info'] as $key => $value ){
                    unset( $result['contract_info'][$key]['function_type'] );
                }

                $url = neccsNal_Config::NAL_API_URL . str_replace( '/Nal/', '', $_SERVER['REQUEST_URI'] );
                $this->logit( neccsNal_Config::SUCCESS_CODE, "OutPut Data ( $url )", $this->_p, $result );

                $this->success( $result );
            }
        } else if ( isset( $this->_p['IaaS_tenant_id'] ) ) {

            if( $this->_nalConf['api_type'] === neccsNal_Config::API_TYPE_NAL ){

                $tenant_name = $this->_getTenant( $this->_p['IaaS_tenant_id'] );

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
                $url .= '&' . 'tenant_name=' . $tenant_name;
                $url .= '&' . 'delete_flg=0';

                $url_list['tenant_contract_info'] = $url;

                // Get the license information
                $url  = neccsNal_Config::API_URL;
                $url .= neccsNal_Config::API_URL_LIST;
                $url .= neccsNal_Config::RESOURCE_LICENSES;
                $request_id = isset( $this->_p['request-id'] ) ? $this->_p['request-id'] : $this->_requestId;
                $url .= '?' . 'request-id=' . $request_id;
                $url .= '&' . 'tenant_name=' . $tenant_name;
                $url .= '&' . 'delete_flg=0';

                $url_list['license_info'] = $url;

                // Get the apl information
                $url  = neccsNal_Config::API_URL;
                $url .= neccsNal_Config::API_URL_LIST;
                $url .= neccsNal_Config::RESOURCE_APLS;
                $request_id = isset( $this->_p['request-id'] ) ? $this->_p['request-id'] : $this->_requestId;
                $url .= '?' . 'request-id=' . $request_id;
                $url .= '&' . 'tenant_name=' . $tenant_name;
                $url .= '&' . 'delete_flg=0';

                $url_list['apl_info'] = $url;

                // Get the apl information
                $url  = neccsNal_Config::API_URL;
                $url .= neccsNal_Config::API_URL_LIST;
                $url .= neccsNal_Config::RESOURCE_GLOBAL_IP_ADDR;
                $request_id = isset( $this->_p['request-id'] ) ? $this->_p['request-id'] : $this->_requestId;
                $url .= '?' . 'request-id=' . $request_id;
                $url .= '&' . 'tenant_name=' . $tenant_name;
                $url .= '&' . 'delete_flg=0';

                $url_list['global_ip_address_info'] = $url;

                $execList = $this->_execMultiApi( $url_list );

                $wim_use_flg = 0;
                foreach( $execList['pod_info'] as $pod ){
                    if( in_array( $pod['use_type'], array( neccsNal_Config::USE_TYPE_WIM, neccsNal_Config::USE_TYPE_SHARE ) ) ){
                        $wim_use_flg = '1';
                    }
                }

                $data = array();
                if( $wim_use_flg === '1' ){

                    // Create a URL (Call of WIM API)
                    $url = neccsNal_Config::WIM_API_URL . str_replace( '/Nal/', '', $_SERVER['REQUEST_URI'] );
                    $url .= '&tenant_name='. $tenant_name;
                    $url .= '&request-id='. $this->_p['request-id'];

                    // API execution
                    $resultForWim = array();
                    $resultForWim = $this->_execApi( $url );

                    $status = isset( $resultForWim['result']['status'] ) ? $resultForWim['result']['status'] : '';
                    $dcChk  = isset( $resultForWim['data']['wim_check_flg'] ) ? $resultForWim['data']['wim_check_flg'] : '';
                    if( $status === neccsNal_Config::STATUS_SUCCESS && $dcChk === '1' ) {
                        $data = $resultForWim['data'];
                    } else {
                        $this->_execResult( $resultForWim, $url );
                    }
                } else {
                    $execList['dc_group_info'] = array();
                    $execList['dc_member_info'] = array();
                }

                // get the use_cnt
                $result = $this->_getContInfoTenant( array_merge( $execList, $data ) );

                foreach( $result['contract_info'] as $key => $value ){
                    unset( $result['contract_info'][$key]['function_type'] );
                }

                $url = neccsNal_Config::NAL_API_URL . str_replace( '/Nal/', '', $_SERVER['REQUEST_URI'] );
                $this->logit( neccsNal_Config::SUCCESS_CODE, "OutPut Data ( $url )", $this->_p, $result );

                $this->success( $result );

            }

        }

        if( $this->_nalConf['api_type'] === neccsNal_Config::API_TYPE_WIM ){

            $execList = array();
            if( !isset( $this->_p['IaaS_tenant_id'] )  ){

                if( !isset( $this->_p['pod_id'] ) ){

                    // Get the dc dc group information
                    $url  = neccsNal_Config::API_URL;
                    $url .= neccsNal_Config::API_URL_LIST;
                    $url .= neccsNal_Config::RESOURCE_DC_CON_GROUPS;
                    $request_id = isset( $this->_p['request-id'] ) ? $this->_p['request-id'] : $this->_requestId;
                    $url .= '?' . 'request-id=' . $request_id;
                    $url .= '&' . 'delete_flg=0';

                    $url_list['dc_group_info'] = $url;

                    // Get the dc member information
                    $url  = neccsNal_Config::API_URL;
                    $url .= neccsNal_Config::API_URL_LIST;
                    $url .= neccsNal_Config::RESOURCE_DC_CON_MEMBERS;
                    $request_id = isset( $this->_p['request-id'] ) ? $this->_p['request-id'] : $this->_requestId;
                    $url .= '?' . 'request-id=' . $request_id;
                    $url .= '&' . 'delete_flg=0';

                    $url_list['dc_member_info'] = $url;

                    // Get the Wan information
                    $url  = neccsNal_Config::API_URL;
                    $url .= neccsNal_Config::API_URL_LIST;
                    $url .= neccsNal_Config::RESOURCE_WAN;
                    $request_id = isset( $this->_p['request-id'] ) ? $this->_p['request-id'] : $this->_requestId;
                    $url .= '?' . 'request-id=' . $request_id;

                    $url_list['wan_info'] = $url;

                    $execList = $this->_execMultiApi( $url_list );
                    $execList['wim_check_flg'] = '1';

                } else {
                    $result = $this->_execProcess( $this->_p['pod_id'], $this->_p['use_type'] );
                    $result['wim_check_flg'] = '1';
                    $this->success( $result );
                }

            } else if ( isset( $this->_p['IaaS_tenant_id'] ) ) {

                $tenant_name = $this->_p['tenant_name'];

                // Get the dc dc group information
                $url  = neccsNal_Config::API_URL;
                $url .= neccsNal_Config::API_URL_LIST;
                $url .= neccsNal_Config::RESOURCE_DC_CON_GROUPS;
                $request_id = isset( $this->_p['request-id'] ) ? $this->_p['request-id'] : $this->_requestId;
                $url .= '?' . 'request-id=' . $request_id;
                $url .= '&' . 'tenant_name=' . $tenant_name;
                $url .= '&' . 'delete_flg=0';

                $url_list['dc_group_info'] = $url;

                // Get the dc member information
                $url  = neccsNal_Config::API_URL;
                $url .= neccsNal_Config::API_URL_LIST;
                $url .= neccsNal_Config::RESOURCE_DC_CON_MEMBERS;
                $request_id = isset( $this->_p['request-id'] ) ? $this->_p['request-id'] : $this->_requestId;
                $url .= '?' . 'request-id=' . $request_id;
                $url .= '&' . 'tenant_name=' . $tenant_name;
                $url .= '&' . 'delete_flg=0';

                $url_list['dc_member_info'] = $url;

                $execList = $this->_execMultiApi( $url_list );
                $execList['wim_check_flg'] = '1';

            }

            $this->success( $execList );
        }
    }

    /**
     * Format information acquired from REST API ( tenant user )
     *
     * @param REST API information
     *
     * @return $result
     */
    protected function _getContInfoTenant( $execList ){

        $result['contract_info'] = array();
        $ID = 0;

        ///// Appliance /////
        foreach( neccsNal_Config::$allResourceParam[neccsNal_Config::LICENSE] as $licenseParam ){

            $param = array();
            $param = $licenseParam;

            $data = array();
            $data = $param;
            list( $data['contract_cnt'], )    = $this->_getContractCntLicense( $execList, $param );
            list( $data['use_cnt'], )         = $this->_getUseCntLicense( $execList, $param );
            if( $data['contract_cnt'] > 0 || $data['use_cnt'] > 0 ){

                if( $data['type'] == neccsNal_Config::TYPE_ROUTER ){
                    $data['contract_kind'] = neccsNal_Config::CONTRACT_KIND_SERVICE;
                } else {
                    $data['contract_kind'] = neccsNal_Config::CONTRACT_KIND_NODE;
                }

                unset( $data['type_detail'] );
                unset( $data['nw_resource_kind'] );
                $result['contract_info'][] = $data;
            }
        }

        ///// PNF /////
        foreach( neccsNal_Config::$allResourceParam[neccsNal_Config::PNF] as $pnfParam ){

            if( is_array( $pnfParam['redundant_configuration_flg'] ) ){
                foreach( $pnfParam['redundant_configuration_flg'] as $redundant_configuration_flg ){

                    $param = array();
                    $param = $pnfParam;
                    $param['redundant_configuration_flg'] = $redundant_configuration_flg;

                    $data = array();
                    $data = $param;
                    $data['contract_kind']   = neccsNal_Config::CONTRACT_KIND_NODE;
                    $data['contract_cnt']    = $this->_getContractCntPnf( $execList, $param );
                    $data['use_cnt']         = $this->_getUseCntPnf( $execList, $param );
                    if( $data['contract_cnt'] > 0 || $data['use_cnt'] > 0 ){
                        unset( $data['type_detail'] );
                        unset( $data['nw_resource_kind'] );
                        $result['contract_info'][] = $data;
                    }
                }
            } else {
                $param = array();
                $param = $pnfParam;

                $data = array();
                $data = $param;
                $data['contract_kind']   = neccsNal_Config::CONTRACT_KIND_NODE;
                $data['contract_cnt']    = $this->_getContractCntPnf( $execList, $param );
                $data['use_cnt']         = $this->_getUseCntPnf( $execList, $param );
                if( $data['contract_cnt'] > 0 || $data['use_cnt'] > 0 ){
                    unset( $data['type_detail'] );
                    unset( $data['nw_resource_kind'] );
                    $result['contract_info'][] = $data;
                }
            }
        }
        ///// EXT Globalip /////
        $param = array();
        $param = neccsNal_Config::$allResourceParam[neccsNal_Config::EXT_GLOBALIP];

        $data = array();
        $data = $param;
        $data['contract_kind']   = neccsNal_Config::CONTRACT_KIND_GLOBALIP;
        $data['contract_cnt']    = $this->_getContractCntGlobalip( $execList, $param );
        $data['use_cnt']         = $this->_getUseCntGlobalip( $execList, $param );
        if( $data['contract_cnt'] > 0 || $data['use_cnt'] > 0 ){
            unset( $data['type_detail'] );
            unset( $data['nw_resource_kind'] );
            $result['contract_info'][] = $data;
        }

        return $result;
    }

    /**
     * Format information acquired from REST API
     *
     * @param REST API information
     *
     * @return $result
     */
    protected function _getContInfo( $execList ){

        $result['contract_info'] = array();

        ///// License /////
        foreach( neccsNal_Config::$allResourceParam[neccsNal_Config::LICENSE] as $licenseParam ){

            if( is_array( $licenseParam['type_detail'] ) ){
                foreach( $licenseParam['type_detail'] as $type_detail ){

                    $param = array();
                    $param = $licenseParam;;
                    $param['type_detail'] = $type_detail;

                    $data = array();
                    $data = $param;
                    $data['quota']                    = $this->_getQuotaLisence( $execList, $param );
                    $data['threshold']                = $this->_getThreshold( $execList, $param );
                    list( $data['contract_cnt'], )    = $this->_getContractCntLicense( $execList, $param );
                    list( $data['use_cnt'], )         = $this->_getUseCntLicense( $execList, $param );
                    $data['unavailable_cnt']          = $this->_getUnavailableCntLicense( $execList, $param );
                    $warning_flg = $this->setWarningFlg( $data['quota'], $data['use_cnt'], $data['unavailable_cnt'], $data['threshold'] );
                    if( $warning_flg === 1 ){
                        $data['warning_flg'] = $warning_flg;
                    }
                    if( $data['quota'] > 0  ){
                        $result['contract_info'][] = $data;
                    }
                }
            } else {
                $param = array();
                $param = $licenseParam;

                $data = array();
                $data = $param;
                $data['quota']                    = $this->_getQuotaLisence( $execList, $param );
                $data['threshold']                = $this->_getThreshold( $execList, $param );
                list( $data['contract_cnt'], )    = $this->_getContractCntLicense( $execList, $param );
                list( $data['use_cnt'], )         = $this->_getUseCntLicense( $execList, $param );
                $data['unavailable_cnt'] = $this->_getUnavailableCntLicense( $execList, $param );
                $warning_flg = $this->setWarningFlg( $data['quota'], $data['use_cnt'], $data['unavailable_cnt'], $data['threshold'] );
                if( $warning_flg === 1 ){
                    $data['warning_flg'] = $warning_flg;
                }
                if( $data['quota'] > 0 ){
                    $result['contract_info'][] = $data;
                }

            }
        }

        ///// PNF /////
        foreach( neccsNal_Config::$allResourceParam[neccsNal_Config::PNF] as $pnfParam ){

            if( is_array( $pnfParam['redundant_configuration_flg'] ) ){
                foreach( $pnfParam['redundant_configuration_flg'] as $redundant_configuration_flg ){

                    $param = array();
                    $param = $pnfParam;
                    $param['redundant_configuration_flg'] = $redundant_configuration_flg;

                    $data = array();
                    $data = $param;
                    $data['quota']           = $this->_getQuotaPnf( $execList, $param );
                    $data['threshold']       = $this->_getThreshold( $execList, $param );
                    $data['contract_cnt']    = $this->_getContractCntPnf( $execList, $param );
                    $data['use_cnt']         = $this->_getUseCntPnf( $execList, $param );
                    $data['unavailable_cnt'] = $this->_getUnavailableCntPnf( $execList, $param );
                    $warning_flg = $this->setWarningFlg( $data['quota'], $data['use_cnt'], $data['unavailable_cnt'], $data['threshold'] );
                    if( $warning_flg === 1 ){
                        $data['warning_flg'] = $warning_flg;
                    }
                    if( $data['quota'] > 0 ){
                        $result['contract_info'][] = $data;
                    }
                }
            } else {
                $param = array();
                $param = $pnfParam;

                $data = array();
                $data = $param;
                $data['quota']           = $this->_getQuotaPnf( $execList, $param );
                $data['threshold']       = $this->_getThreshold( $execList, $param );
                $data['contract_cnt']    = $this->_getContractCntPnf( $execList, $param );
                $data['use_cnt']         = $this->_getUseCntPnf( $execList, $param );
                $data['unavailable_cnt'] = $this->_getUnavailableCntPnf( $execList, $param );
                $warning_flg = $this->setWarningFlg( $data['quota'], $data['use_cnt'], $data['unavailable_cnt'], $data['threshold'] );
                if( $warning_flg === 1 ){
                    $data['warning_flg'] = $warning_flg;
                }
                if( $data['quota'] > 0 ){
                    $result['contract_info'][] = $data;
                }
            }
        }
        ///// Globalip /////
        $param = array();
        $param = neccsNal_Config::$allResourceParam[neccsNal_Config::GLOBALIP];

        $data = array();
        $data = $param;
        $data['quota']           = $this->_getQuotaGlobalip( $execList );
        $data['threshold']       = $this->_getThreshold( $execList, $param );
        $data['contract_cnt']    = $this->_getContractCntGlobalip( $execList, $param );
        $data['use_cnt']         = $this->_getUseCntGlobalip( $execList, $param );
        $data['unavailable_cnt'] = $this->_getUnavailableCntGlobalip( $execList );
        $warning_flg = $this->setWarningFlg( $data['quota'], $data['use_cnt'], $data['unavailable_cnt'], $data['threshold'] );
        if( $warning_flg === 1 ){
            $data['warning_flg'] = $warning_flg;
        }
        if( $data['quota'] > 0 ){
            $result['contract_info'][] = $data;
        }

        ///// MSA VLAN /////
        $param = array();
        $param = neccsNal_Config::$allResourceParam[neccsNal_Config::MSA_VLAN];

        $data = array();
        $data = $param;
        $data['quota'] = $this->_getQuotaMsa( $execList );

        $data['threshold']       = $this->_getThreshold( $execList, $param );
        $data['contract_cnt']    = $this->_getContractCntMsa( $execList );
        $data['use_cnt']         = $this->_getUseCntMsa( $execList, $param );
        $data['unavailable_cnt'] = $this->_getUnavailableCntMsa( $execList );
        $warning_flg = $this->setWarningFlg( $data['quota'], $data['use_cnt'], $data['unavailable_cnt'], $data['threshold'] );
        if( $warning_flg === 1 ){
            $data['warning_flg'] = $warning_flg;
        }
        if( $data['quota'] > 0 ){
            $result['contract_info'][] = $data;
        }

        ///// WAN VLAN /////
        $param = array();
        $param = neccsNal_Config::$allResourceParam[neccsNal_Config::WAN_VLAN];

        $data = array();
        $data = $param;
        $data['quota'] = $this->_getQuotaWan( $execList );
        $data['threshold']       = $this->_getThreshold( $execList, $param );
        $data['contract_cnt']    = $this->_getContractCntWan( $execList );
        $data['use_cnt']         = $this->_getUseCntWan( $execList, $param );
        $data['unavailable_cnt'] = $this->_getUnavailableCntWan( $execList );
        $warning_flg = $this->setWarningFlg( $data['quota'], $data['use_cnt'], $data['unavailable_cnt'], $data['threshold'] );
        if( $warning_flg === 1 ){
            $data['warning_flg'] = $warning_flg;
        }
        if( $data['quota'] > 0 ){
            $result['contract_info'][] = $data;
        }


        foreach( $execList['oepnstack_info'] as $key => $value ){

            //// CPU ////
            $param = array();
            $param = neccsNal_Config::$allResourceParam[neccsNal_Config::CPU_LIST];

            $data = array();
            $data = $param;
            $data['type_detail']      = $key;
            $data['contract_cnt']     = $value['vcpus']['contract_cnt'];
            $data['use_cnt']          = $value['vcpus']['use_cnt'];
            $data['quota']            = $value['vcpus']['quota'];
            $data['threshold']        = $this->_getThreshold( $execList, $param );
            $warning_flg = $this->setWarningFlg( $data['quota'], $data['use_cnt'], '', $data['threshold'] );
            if( $warning_flg === 1 ){
                $data['warning_flg'] = $warning_flg;
            }

            if( $data['quota'] > 0 ){
                $result['contract_info'][] = $data;
            }

            //// MEMORY ////
            $param = array();
            $param = neccsNal_Config::$allResourceParam[neccsNal_Config::MEMORY_LIST];

            $data = array();
            $data = $param;
            $data['type_detail']      = $key;
            $data['contract_cnt']     = $this->_setUnitForMemory( $value['ram']['contract_cnt'] );
            $data['use_cnt']          = $this->_setUnitForMemory( $value['ram']['use_cnt'] );
            $data['quota']            = $this->_setUnitForMemory( $value['ram']['quota'] );
            $data['threshold']        = $this->_getThreshold( $execList, $param );
            $warning_flg = $this->setWarningFlg( $data['quota'], $data['use_cnt'], '', $data['threshold'] );
            if( $warning_flg === 1 ){
                $data['warning_flg'] = $warning_flg;
            }

            if( $data['quota'] > 0 ){
                $result['contract_info'][] = $data;
            }

            //// STORAGE ////
            $param = array();
            $param = neccsNal_Config::$allResourceParam[neccsNal_Config::STORAGE_LIST];

            $data = array();
            $data = $param;
            $data['type_detail']      = $key;
            $data['contract_cnt']     = $this->_setUnitForStorage( $value['disk']['contract_cnt'] );
            $data['use_cnt']          = $this->_setUnitForStorage( $value['disk']['use_cnt'] );
            $data['quota']            = $this->_setUnitForStorage( $value['disk']['quota'] );
            $data['threshold']        = $this->_getThreshold( $execList, $param );
            $warning_flg = $this->setWarningFlg( $data['quota'], $data['use_cnt'], '', $data['threshold'] );
            if( $warning_flg === 1 ){
                $data['warning_flg'] = $warning_flg;
            }

            if( $data['quota'] > 0 ){
                $result['contract_info'][] = $data;
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

    /**
     * Set flover data
     *
     * @param flover list
     * @param flover contract list
     *
     * @return flover list
     */
    protected function setFlavorData( $floverList, $flavorCntInfo ) {

        $setFlavorList = array();
        foreach( $floverList as $type => $info1 ){
            foreach( $info1 as $device_type => $value ){

                if( $this->_nalConf['api_type'] === neccsNal_Config::API_TYPE_NAL && $type == neccsNal_Config::TYPE_ROUTER ){
                    continue;
                }

                if( $this->_nalConf['api_type'] === neccsNal_Config::API_TYPE_WIM
                && in_array( $type, array( neccsNal_Config::TYPE_FW, neccsNal_Config::TYPE_LB ) )){
                    continue;
                }

                $name = $value['flavor_name'];
                foreach( $flavorCntInfo['flavors'] as $key => $floverCnt ){
                    if( $floverCnt['name'] === $name ){
                        // set total_info
                        $setFlavorList[$type][$device_type]['vcpus_count'] = $floverCnt['vcpus'];
                        $setFlavorList[$type][$device_type]['ram_count'] = $floverCnt['ram'];
                        $setFlavorList[$type][$device_type]['disk_count'] = $floverCnt['disk'];
                    }
                }
            }
        }

        return $setFlavorList;
    }

    /**
     * get OpenStack count information
     *
     * @param REST API information
     *
     * @return Quota and use_cnt information
     */
    protected function _getOpenStackCnt( $execList ) {

        $result = array();
        $resion_id = $this->_p['IaaS_region_id'];
        foreach( $execList['pod_info'] as $key => $pod ){

            $pod_id   = $pod['pod_id'];
            $use_type = $pod['use_type'];

            $wimData = array();
            if( in_array( $use_type, array( neccsNal_Config::USE_TYPE_WIM, neccsNal_Config::USE_TYPE_SHARE ) ) ){
                // Create a URL (Call of WIM API)
                $url = neccsNal_Config::WIM_API_URL . str_replace( '/Nal/', '', $_SERVER['REQUEST_URI'] );
                $url .= '&request-id='. $this->_p['request-id'];
                $url .= '&dc_id='. neccsNal_Config::MY_DC_ID;
                $url .= '&pod_id='. $pod_id;
                $url .= '&use_type='. $use_type;
                $url .= '&IaaS_region_id='. $resion_id;

                // API execution
                $resultForWim = array();
                $resultForWim = $this->_execApi( $url );
                $status = isset( $resultForWim['result']['status'] ) ? $resultForWim['result']['status'] : '';
                if( $status === neccsNal_Config::STATUS_SUCCESS ) {
                    $wimData = $resultForWim['data'];
                } else {
                    $this->_execResult( $resultForWim, $url );
                }
            }
            $nalData = $this->_execProcess( $pod_id, $use_type );

            $openStackInfo = $this->_getOepnStackInfo( $nalData, $wimData, $execList, $use_type );

            if( !isset( $result[$use_type] ) ){
                $result[$use_type] = $openStackInfo;
            }else {

                $result[$use_type]['vcpus']['quota'] += $openStackInfo['vcpus']['quota'];
                $result[$use_type]['disk']['quota']  += $openStackInfo['disk']['quota'];
                $result[$use_type]['ram']['quota']   += $openStackInfo['ram']['quota'];

                $result[$use_type]['vcpus']['use_cnt'] += $openStackInfo['vcpus']['use_cnt'];
                $result[$use_type]['disk']['use_cnt']  += $openStackInfo['disk']['use_cnt'];
                $result[$use_type]['ram']['use_cnt']   += $openStackInfo['ram']['use_cnt'];

                $result[$use_type]['vcpus']['contract_cnt'] += $openStackInfo['vcpus']['contract_cnt'];
                $result[$use_type]['disk']['contract_cnt']  += $openStackInfo['disk']['contract_cnt'];
                $result[$use_type]['ram']['contract_cnt']   += $openStackInfo['ram']['contract_cnt'];
            }
        }

        return $result;
    }

    /**
     * Format information acquired from REST API
     *
     * @param OpenStack info(NAL)
     * @param OpenStack info(WIM)
     * @param REST API information
     * @param POD use_type
     *
     * @return count Information
     */
    protected function _getOepnStackInfo( $nalData, $wimData, $execList, $use_type ){

        $result = array(
            'vcpus' => array(
                'quota'        => '0',
                'use_cnt'      => '0',
                'contract_cnt' => '0',
            ),
            'ram' => array(
                'quota'        => '0',
                'use_cnt'      => '0',
                'contract_cnt' => '0',
            ),
            'disk' => array(
                'quota'        => '0',
                'use_cnt'      => '0',
                'contract_cnt' => '0',
            ),
        );

        if( $use_type == neccsNal_Config::USE_TYPE_NAL ){
            $data = $nalData;
            $flavorContCntList = $nalData['flavor_list_for_cnt'];

        } else if( $use_type == neccsNal_Config::USE_TYPE_SHARE ) {
            $data = $nalData;
            $flavorContCntList = $nalData['flavor_list_for_cnt'] + $wimData['flavor_list_for_cnt'];

        } else {
            $data = $wimData;
            $flavorContCntList = $wimData['flavor_list_for_cnt'];
        }

        // In case of shared or VIM, acquire the number of subscribers of nodes
        foreach( $execList['tenant_contract_info'] as $contract ){

            if( $contract['apl_type'] != neccsNal_Config::APL_TYPE_VIRTUAL ){
                continue;
            }

            $type        = $contract['type'];
            $device_type = $contract['device_type'];

            if( isset( $flavorContCntList[$type][$device_type] ) ){
                if( $contract['type'] == neccsNal_Config::TYPE_ROUTER ){
                    $result['vcpus']['contract_cnt'] += $flavorContCntList[$type][$device_type]['vcpus_count'] * 2;
                    $result['ram']['contract_cnt']   += $flavorContCntList[$type][$device_type]['ram_count'] * 2;
                    $result['disk']['contract_cnt']  += $flavorContCntList[$type][$device_type]['disk_count'] * 2;
                } else {
                    $result['vcpus']['contract_cnt'] += $flavorContCntList[$type][$device_type]['vcpus_count'] * $contract['contract'];
                    $result['ram']['contract_cnt']   += $flavorContCntList[$type][$device_type]['ram_count'] * $contract['contract'];
                    $result['disk']['contract_cnt']  += $flavorContCntList[$type][$device_type]['disk_count'] * $contract['contract'];
                }
            }
        }

        // set Data(tenantInfo)
        $tenantInfo = array();
        foreach( $execList['apl_info'] as $aplInfo ){
            $node_id = $aplInfo['node_id'];
            $tenantInfo[$node_id]['IaaS_tenant_id'] = $aplInfo['IaaS_tenant_id'];
            $tenantInfo[$node_id]['tenant_name']    = $aplInfo['tenant_name'];
        }

        // set Data(use_cnt)
        foreach( $data['use_info'] as $instance_id => $useCnt ){
            if( isset( $tenantInfo[$instance_id] ) ){
                $result['vcpus']['use_cnt'] += $useCnt['vcpus'];
                $result['ram']['use_cnt']   += $useCnt['ram'];
                $result['disk']['use_cnt']  += $useCnt['disk'];
            }
        }

        // set Data(qupta)
        $result['vcpus']['quota'] = $data['vcpus']['quota'];
        $result['ram']['quota']   = $data['ram']['quota'];
        $result['disk']['quota']  = $data['disk']['quota'];

        return $result;
    }

    /**
     * Acquire upper limit number and usage number]
     *
     * @param pod id
     * @param use_type
     *
     * @return Tenant Information
     */
    protected function _execProcess( $pod_id, $use_type ){

        $inParam = array();
        $inParam['dc_id']  = isset( $this->_p['dc_id'] ) ? $this->_p['dc_id'] : 'system';
        $inParam['pod_id'] = $pod_id;
        $inParam['type']   = neccsNal_Config::ENDPOINT_TYPE_VIM;
        // Acquisition of endpoint information
        $endpointInfo = $this->getEndpoint( $inParam );

        if( empty( $endpointInfo ) ){
            return array();
        }

        // Reference of OpenStack information
        $endpoint     = json_decode( $endpointInfo[0]['endpoint_info'], true );
        $tenant_name  = $endpoint['admin_tenant_name'];

        $info = array();
        // In the case of NAL, the upper limit number and the usage number are acquired at the time of sharing or VIM, and in the case of WIM at WIM
        if( $this->_nalConf['api_type'] === neccsNal_Config::API_TYPE_NAL ){
            if( in_array( $use_type, array( neccsNal_Config::USE_TYPE_NAL, neccsNal_Config::USE_TYPE_SHARE ) ) ){
                // Get the information from OpenStack
                // Memory, CPU, and storage
                $usagesInfo = $this->listUsageReport( $tenant_name, $endpoint );
                $quotaInfo  = $this->listHostDetail( $tenant_name, $endpoint );
                $info = $this->setData( $usagesInfo, $quotaInfo );

                // get number of contracts for flavor by equipment
                $info['flavor_list_for_cnt'] = $this->_getFlavorListForCnt( $pod_id, $endpointInfo );
            }
        } else if ( $this->_nalConf['api_type'] === neccsNal_Config::API_TYPE_WIM ) {
            if( in_array( $use_type, array( neccsNal_Config::USE_TYPE_WIM ) ) ){
                // Get the information from OpenStack
                // Memory, CPU, and storage
                $usagesInfo = $this->listUsageReport( $tenant_name, $endpoint );
                $quotaInfo  = $this->listHostDetail( $tenant_name, $endpoint );
                $info = $this->setData( $usagesInfo, $quotaInfo );
            }

            if( in_array( $use_type, array( neccsNal_Config::USE_TYPE_WIM, neccsNal_Config::USE_TYPE_SHARE ) ) ){
                // get number of contracts for flavor by equipment
                $info['flavor_list_for_cnt'] = $this->_getFlavorListForCnt( $pod_id, $endpointInfo );
            }
        }

        // get number of contracts for flavor by equipment
        $info['flavor_list_for_cnt'] = $this->_getFlavorListForCnt( $pod_id, $endpointInfo );

        return $info;

    }

    /**
     * Formatting data
     *
     * @param usage information
     * @param quota information
     *
     */
    protected function setData( $usagesInfo, $quotaInfo ) {

        $info['vcpus']['quota'] = 0;
        $info['disk']['quota'] = 0;
        $info['ram']['quota'] = 0;

        $usageList = array();
        ///////// In the case usage /////////
        if( !empty( $usagesInfo['tenant_usages'] ) ){
            foreach( $usagesInfo['tenant_usages'] as $serverList ){
                foreach( $serverList['server_usages'] as $value ){
                    $instance_id = $value['instance_id'];

                    // set total_info and contract_info
                    $info['use_info'][$instance_id]['vcpus'] = $value['vcpus'];
                    $info['use_info'][$instance_id]['ram']   = $value['memory_mb'];
                    $info['use_info'][$instance_id]['disk']  = $value['local_gb'];
                }
            }
        }

        ///////// In the case quota /////////
        foreach( $quotaInfo as $quotaList ){
            // set total_info
            $info['vcpus']['quota'] += $quotaList['cpu'];
            $info['ram']['quota']   += $quotaList['memory_mb'];
            $info['disk']['quota']  += $quotaList['disk_gb'];
        }

        return $info;
    }

    /**
     * get Number of contracts for flavor by equipment
     *
     * @param pod_id
     * @param endpointInfo
     *
     * @return Tenant Information
     */
    protected function _getFlavorListForCnt( $pod_id, $endpointInfo ){

        // get the DB information
        $inParam = array();
        $inParam['type']  = neccsNal_Config::CONFIG_TYPE_COMMON;
        $inParam['dc_id'] = isset( $this->_p['dc_id'] ) ? $this->_p['dc_id'] : 'system';
        // get the config
        $confInfo = array();
        $floverList = array();
        $confInfo = $this->getConfig( $inParam );

        if( empty( $confInfo ) ){
            return array();
        }

        $confInfo = json_decode( $confInfo[0]['config_info'], true );
        $floverList = $confInfo['os_image_and_flavor_name_list'];

        // Reference of OpenStack information
        $endpoint     = json_decode( $endpointInfo[0]['endpoint_info'], true );
        $tenant_name  = $endpoint['admin_tenant_name'];

        $flavorCntInfo = $this->listFlavorsDetail( $tenant_name, $endpoint );
        $floverListForCtr = $this->setFlavorData( $floverList, $flavorCntInfo );

        return $floverListForCtr;

    }

    /**
     * If the number of uses exceeds the threshold value, the flag is returned
     *
     * @param $quota
     * @param $use_cnt
     * @param $unavailable_cnt
     * @param $threshold
     *
     * @return Warning flg
     */
    protected function setWarningFlg( $quota, $use_cnt, $unavailable_cnt=0, $threshold ){

        $warning_flg = 0;
        $percent = 0;
        if( $use_cnt == 0 && $unavailable_cnt == 0 ){
            $percent = 0;
        } else if ( $quota == 0 ) {
            $percent = 0;
        } else {
            $percent = round( ( ( $use_cnt + $unavailable_cnt ) / $quota ) * 100 );
        }

        if( $percent > $threshold ){
            $warning_flg = 1;
        }

        return $warning_flg;
    }

}
