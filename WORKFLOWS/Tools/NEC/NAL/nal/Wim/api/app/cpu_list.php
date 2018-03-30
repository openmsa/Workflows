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
* 2.FUNCTION : cpu.php (Individual method)
*/
require_once dirname(__FILE__). '/../Nal.php';

class cpu_list extends neccsNal {

    protected $_usagesInfo         = array();
    protected $_quotaInfo          = array();

    /**
     * GET method (list,refer)
     *
     */
    protected function get() {

        if( $this->_nalConf['api_type'] === neccsNal_Config::API_TYPE_NAL ){

            // Get the apl information
            $url  = neccsNal_Config::API_URL;
            $url .= neccsNal_Config::API_URL_LIST;
            $url .= neccsNal_Config::RESOURCE_APLS;
            $request_id = isset( $this->_p['request-id'] ) ? $this->_p['request-id'] : $this->_requestId;
            $url .= '?' . 'request-id=' . $request_id;
            $url .= '&' . 'delete_flg=0';

            $url_list['apl_info'] = $url;

            // Get the tenant contract information
            $url  = neccsNal_Config::API_URL;
            $url .= neccsNal_Config::API_URL_LIST;
            $url .= neccsNal_Config::RESOURCE_CONTRACT;
            $request_id = isset( $this->_p['request-id'] ) ? $this->_p['request-id'] : $this->_requestId;
            $url .= '?' . 'request-id=' . $request_id;
            $url .= '&' . 'delete_flg=0';

            $url_list['tenant_contract_info'] = $url;

            $execList = $this->_execMultiApi( $url_list );

            $inParam = array();
            $inParam['use_type'] = intval( $this->_p['type_detail'] );
            $podList = $this->getPod( $inParam );

            // If the Pod address information can not be acquired
            if( empty( $podList ) ) {
                $this->error( neccsNal_Config::REST_API_ERROR, "pod not exists." );
            }

            $result = array();
            $total_quota = 0;
            $total_use_cnt = 0;
            $total_contract_cnt = 0;
            foreach( $podList as $key => $pod ){

                $nalData = array();
                $wimData = array();
                $pod_id   = $pod['pod_id'];

                if( in_array( $this->_p['type_detail'], array( neccsNal_Config::USE_TYPE_WIM, neccsNal_Config::USE_TYPE_SHARE ) ) ){
                    // Create a URL (Call of WIM API)
                    $url = neccsNal_Config::WIM_API_URL . str_replace( '/Nal/', '', $_SERVER['REQUEST_URI'] );
                    $url .= '&request-id='. $this->_p['request-id'];
                    $url .= '&pod_id='. $pod_id;
                    $url .= '&dc_id='. neccsNal_Config::MY_DC_ID;

                    // API execution
                    $resultForWim = array();
                    $resultForWim = $this->_execApi( $url );
                    $status = isset( $resultForWim['result']['status'] ) ? $resultForWim['result']['status'] : '';
                    $dcChk  = isset( $resultForWim['data']['wim_check_flg'] ) ? $resultForWim['data']['wim_check_flg'] : '';
                    if( $status === neccsNal_Config::STATUS_SUCCESS && $dcChk === '1') {
                        $wimData = $resultForWim['data'];
                    } else {
                        $this->_execResult( $resultForWim, $url );
                    }
                }

                $nalData = $this->_execProcess( $pod_id );

                list( $quota, $use_cnt, $contract_cnt ) = $this->_getContInfo( $nalData, $wimData, $execList );

                // contract_info
                if( $this->_p['function_type'] === neccsNal_Config::CPU_LIST ){
                    $result['contract_info'][$key]['quota']   = $quota;
                    $result['contract_info'][$key]['use_cnt'] = $use_cnt;
                } else if ( $this->_p['function_type'] === neccsNal_Config::MEMORY_LIST ){
                    $result['contract_info'][$key]['quota']   = $this->_setUnitForMemory( $quota );
                    $result['contract_info'][$key]['use_cnt'] = $this->_setUnitForMemory( $use_cnt );
                } else if ( $this->_p['function_type'] === neccsNal_Config::STORAGE_LIST ){
                    $result['contract_info'][$key]['quota']   = $this->_setUnitForStorage( $quota );
                    $result['contract_info'][$key]['use_cnt'] = $this->_setUnitForStorage( $use_cnt );
                }

                $result['contract_info'][$key]['pod_id'] = $pod_id;

                $total_quota        += $quota;
                $total_use_cnt      += $use_cnt;
                $total_contract_cnt += $contract_cnt;

            }

            // total_info
            if( $this->_p['function_type'] === neccsNal_Config::CPU_LIST ){
                $result['total_info']['quota']        = $total_quota;
                $result['total_info']['use_cnt']      = $total_use_cnt;
                $result['total_info']['contract_cnt'] = $total_contract_cnt;
            } else if ( $this->_p['function_type'] === neccsNal_Config::MEMORY_LIST ){
                $result['total_info']['quota']        = $this->_setUnitForMemory( $total_quota );
                $result['total_info']['use_cnt']      = $this->_setUnitForMemory( $total_use_cnt );
                $result['total_info']['contract_cnt'] = $this->_setUnitForMemory( $total_contract_cnt );
            } else if ( $this->_p['function_type'] === neccsNal_Config::STORAGE_LIST ){
                $result['total_info']['quota']        = $this->_setUnitForStorage( $total_quota );
                $result['total_info']['use_cnt'] = $this->_setUnitForStorage( $total_use_cnt );
                $result['total_info']['contract_cnt'] = $this->_setUnitForStorage( $total_contract_cnt );
            }

            $url = neccsNal_Config::NAL_API_URL . str_replace( '/Nal/', '', $_SERVER['REQUEST_URI'] );
            $this->logit( neccsNal_Config::SUCCESS_CODE, "OutPut Data ( $url )", $this->_p, $result );

            // It outputs the result
            $this->success( $result );

        } else if( $this->_nalConf['api_type'] === neccsNal_Config::API_TYPE_WIM ){
            $result = $this->_execProcess( $this->_p['pod_id'] );
            $result['wim_check_flg'] = '1';
            // It outputs the result
            $this->success( $result );
        }
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
     * Get the tenant_name that brute string to id
     *
     * @return Tenant Information
     */
    protected function _execProcess( $pod_id ){

        $inParam = array();
        $inParam['dc_id']  = isset( $this->_p['dc_id'] ) ? $this->_p['dc_id'] : 'system';
        $inParam['pod_id'] = $pod_id;
        $inParam['type']   = neccsNal_Config::ENDPOINT_TYPE_VIM;
        // Acquisition of endpoint information
        $endpointInfo = $this->getEndpoint( $inParam );

        $info = array();
        if( empty( $endpointInfo ) ){

            $info['quota']   = '0';
            $info['use_info'] = array();
            $info['flavor_list_for_cnt'] = array();

            return $info;
        }

        $use_type = $this->_p['type_detail'];
        // Reference of OpenStack information
        $endpoint    = json_decode( $endpointInfo[0]['endpoint_info'], true );
        $tenant_name = $endpoint['admin_tenant_name'];
        // In the case of NAL, the upper limit number and the usage number are acquired at the time of sharing or VIM, and in the case of WIM at WIM
        if( $this->_nalConf['api_type'] === neccsNal_Config::API_TYPE_NAL ){
            if( in_array( $use_type, array( neccsNal_Config::USE_TYPE_NAL, neccsNal_Config::USE_TYPE_SHARE ) ) ){

                // Get the information from OpenStack
                // Memory, CPU, and storage
                $this->_usagesInfo = $this->listUsageReport( $tenant_name, $endpoint );
                $this->_quotaInfo  = $this->listHostDetail( $tenant_name, $endpoint );
                $info = $this->setData();

                // get number of contracts for flavor by equipment
                $info['flavor_list_for_cnt'] = $this->_getFlavorListForCnt( $pod_id, $endpointInfo );

            }
        } else if ( $this->_nalConf['api_type'] === neccsNal_Config::API_TYPE_WIM ) {
            if( in_array( $use_type, array( neccsNal_Config::USE_TYPE_WIM ) ) ){

                // Get the information from OpenStack
                // Memory, CPU, and storage
                $this->_usagesInfo = $this->listUsageReport( $tenant_name, $endpoint );
                $this->_quotaInfo  = $this->listHostDetail( $tenant_name, $endpoint );
                $info = $this->setData();

            }
            if( in_array( $use_type, array( neccsNal_Config::USE_TYPE_WIM, neccsNal_Config::USE_TYPE_SHARE ) ) ){
                // get number of contracts for flavor by equipment
                $info['flavor_list_for_cnt'] = $this->_getFlavorListForCnt( $pod_id, $endpointInfo );
            }

        }

        return $info;

    }

    /**
     * Format information acquired from REST API
     *
     * @param OpenStack info(NAL)
     * @param OpenStack info(WIM)
     * @param REST API information
     *
     * @return count Information
     */
    protected function _getContInfo( $nalData, $wimData, $execList ){

        $use_type = $this->_p['type_detail'];

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

        $contract_cnt = 0;
        // In case of shared or VIM, acquire the number of subscribers of nodes
        foreach( $execList['tenant_contract_info'] as $contract ){

            if( $contract['apl_type'] != neccsNal_Config::APL_TYPE_VIRTUAL ){
                continue;
            }

            $type        = $contract['type'];
            $device_type = $contract['device_type'];

            if( isset( $flavorContCntList[$type][$device_type] ) ){
                if( $contract['type'] == neccsNal_Config::TYPE_ROUTER ){
                    $contract_cnt += $flavorContCntList[$type][$device_type]['count'] * 2;
                } else {
                    $contract_cnt += $flavorContCntList[$type][$device_type]['count'] * $contract['contract'];
                }
            }
        }

        $quota   = $data['quota'];
        $use_cnt = '0';

        // set Data(tenantInfo)
        $tenantInfo = array();
        foreach( $execList['apl_info'] as $aplInfo ){
            $node_id = $aplInfo['node_id'];
            $tenantInfo[$node_id]['IaaS_tenant_id'] = $aplInfo['IaaS_tenant_id'];
            $tenantInfo[$node_id]['tenant_name']    = $aplInfo['tenant_name'];
        }

        // set Data(use_cnt)
        $useCntInfo = array();
        foreach( $data['use_info'] as $instance_id => $useCnt ){
            if( isset( $tenantInfo[$instance_id] ) ){
                $use_cnt += $useCnt;
            }
        }

        return array( $quota, $use_cnt, $contract_cnt );
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
     * Return of the response
     *
     * @param tenant infomation
     * @param usage information
     * @param flavor information
     *
     */
    protected function setFlavorData( $floverList, $flavorCntInfo ) {

        $setFlavorList = array();
        foreach( $floverList as $type => $info1 ){
            foreach( $info1 as $device_type => $value ){
                $name = $value['flavor_name'];

                foreach( $flavorCntInfo['flavors'] as $key => $floverCnt ){

                    if( $this->_nalConf['api_type'] === neccsNal_Config::API_TYPE_NAL && $type == neccsNal_Config::TYPE_ROUTER ){
                        continue;
                    }

                    if( $this->_nalConf['api_type'] === neccsNal_Config::API_TYPE_WIM
                    && in_array( $type, array( neccsNal_Config::TYPE_FW, neccsNal_Config::TYPE_LB ) )){
                        continue;
                    }

                    if( $floverCnt['name'] === $name ){
                        // set total_info
                        if( $this->_p['function_type'] === neccsNal_Config::CPU_LIST ){
                            $setFlavorList[$type][$device_type]['count'] = $floverCnt['vcpus'];
                        } else if ( $this->_p['function_type'] === neccsNal_Config::MEMORY_LIST ){
                            $setFlavorList[$type][$device_type]['count'] = $floverCnt['ram'];
                        } else if ( $this->_p['function_type'] === neccsNal_Config::STORAGE_LIST ){
                            $setFlavorList[$type][$device_type]['count'] = $floverCnt['disk'];
                        }
                    }
                }
            }
        }

        return $setFlavorList;
    }

    /**
     * Return of the response
     *
     */
    protected function setData() {

        $info = array();
        $info['quota'] = 0;

        $usageList = array();
        ///////// In the case usage /////////
        if( !empty( $this->_usagesInfo['tenant_usages'] ) ){
            foreach( $this->_usagesInfo['tenant_usages'] as $serverList ){

                // Get the tenant_name
                $tenant_id = $serverList['tenant_id'];
                foreach( $serverList['server_usages'] as $value ){
                    $instance_id = $value['instance_id'];

                    // set total_info and contract_info
                    if( $this->_p['function_type'] === neccsNal_Config::CPU_LIST ){
                        $info['use_info'][$instance_id] = $value['vcpus'];
                    } else if ( $this->_p['function_type'] === neccsNal_Config::MEMORY_LIST ){
                        $info['use_info'][$instance_id] = $value['memory_mb'];
                    } else if ( $this->_p['function_type'] === neccsNal_Config::STORAGE_LIST ){
                        $info['use_info'][$instance_id] = $value['local_gb'];
                    }
                }
            }
        }

        ///////// In the case quota /////////
        foreach( $this->_quotaInfo as $quotaList ){
            // set total_info
            if( $this->_p['function_type'] === neccsNal_Config::CPU_LIST ){
                $info['quota'] += $quotaList['cpu'];
            } else if ( $this->_p['function_type'] === neccsNal_Config::MEMORY_LIST ){
                $info['quota'] += $quotaList['memory_mb'];
            } else if ( $this->_p['function_type'] === neccsNal_Config::STORAGE_LIST ){
                $info['quota'] += $quotaList['disk_gb'];
            }
        }

        return $info;
    }
}
