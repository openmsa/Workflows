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
* 2.FUNCTION : cpu_detail.php (Individual method)
*/
require_once dirname(__FILE__). '/../Nal.php';

class cpu_detail extends neccsNal {

    protected $_usagesInfo         = array();
    protected $_quotaInfo          = array();

    /**
     * GET method (list,refer)
     *
     */
    protected function get() {

        // pod_id
        if( !isset( $this->_p['pod_id'] ) ) {
            $this->error( neccsNal_Config::PARAMETER_ERROR, "pod_id is not set." );
        }

        $result = array();
        // In NAL server, in the case of the NAL call
        if( $this->_nalConf['api_type'] === neccsNal_Config::API_TYPE_NAL ){

            // Get the tenant contract information
            $url  = neccsNal_Config::API_URL;
            $url .= neccsNal_Config::API_URL_LIST;
            $url .= neccsNal_Config::RESOURCE_PODS;
            $request_id = isset( $this->_p['request-id'] ) ? $this->_p['request-id'] : $this->_requestId;
            $url .= '?' . 'request-id=' . $request_id;
            $url .= '&' . 'pod_id='. $this->_p['pod_id'];
            $url .= '&' . 'delete_flg=0';

            $url_list['pod_info'] = $url;

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

            $wimData = array();
            $use_type = $execList['pod_info'][0]['use_type'];
            if( in_array( $use_type, array( neccsNal_Config::USE_TYPE_WIM, neccsNal_Config::USE_TYPE_SHARE ) ) ){
                // Create a URL (Call of WIM API)
                $url = neccsNal_Config::WIM_API_URL . str_replace( '/Nal/', '', $_SERVER['REQUEST_URI'] );
                $url .= '&dc_id='. neccsNal_Config::MY_DC_ID;
                $url .= '&use_type='. $use_type;
                $url .= '&request-id='. $this->_p['request-id'];

                // API execution
                $result = $this->_execApi( $url );

                $status = isset( $result['result']['status'] ) ? $result['result']['status'] : '';
                $dcChk  = isset( $result['data']['wim_check_flg'] ) ? $result['data']['wim_check_flg'] : '';
                if( $status === neccsNal_Config::STATUS_SUCCESS && $dcChk == '1' ) {
                    $wimData = $result['data'];
                } else {
                    $this->_execResult( $result, $url );
                }
            }
        }

        if( $this->_nalConf['api_type'] === neccsNal_Config::API_TYPE_NAL || $this->_nalConf['api_type'] === neccsNal_Config::API_TYPE_WIM ){

            $inParam['pod_id'] = $this->_p['pod_id'];
            $inParam['dc_id']  = isset( $this->_p['dc_id'] ) ? $this->_p['dc_id'] : 'system';
            $inParam['type']   = neccsNal_Config::ENDPOINT_TYPE_VIM;
            // Acquisition of endpoint information
            $endpointInfo = $this->getEndpoint( $inParam );

            $use_type = isset( $this->_p['use_type'] ) ? $this->_p['use_type'] : $execList['pod_info'][0]['use_type'];
            $data = array();
            if( !empty( $endpointInfo ) ){
                // Reference of OpenStack information
                $endpoint    = json_decode( $endpointInfo[0]['endpoint_info'], true );
                $tenant_name = $endpoint['admin_tenant_name'];

                if( $this->_nalConf['api_type'] === neccsNal_Config::API_TYPE_NAL ){
                    if( in_array( $use_type, array( neccsNal_Config::USE_TYPE_NAL, neccsNal_Config::USE_TYPE_SHARE ) ) ){

                        // Get the information from OpenStack
                        // Memory, CPU, and storage
                        $this->_usagesInfo = $this->listUsageReport( $tenant_name, $endpoint );
                        $this->_quotaInfo  = $this->listHostDetail( $tenant_name, $endpoint );
                        $data = $this->setData();

                        // get number of contracts for flavor by equipment
                        $data['flavor_list_for_cnt'] = $this->_getFlavorListForCnt( $this->_p['pod_id'], $endpointInfo );
                    }

                } else if ( $this->_nalConf['api_type'] === neccsNal_Config::API_TYPE_WIM ) {
                    if( in_array( $use_type, array( neccsNal_Config::USE_TYPE_WIM ) ) ){

                        // Get the information from OpenStack
                        // Memory, CPU, and storage
                        $this->_usagesInfo = $this->listUsageReport( $tenant_name, $endpoint );
                        $this->_quotaInfo  = $this->listHostDetail( $tenant_name, $endpoint );
                        $data = $this->setData();
                    }

                    if( in_array( $use_type, array( neccsNal_Config::USE_TYPE_WIM, neccsNal_Config::USE_TYPE_SHARE ) ) ){
                        // get number of contracts for flavor by equipment
                        $data['flavor_list_for_cnt'] = $this->_getFlavorListForCnt( $this->_p['pod_id'], $endpointInfo );
                    }

                }
            } else {
                $data['flavor_list_for_cnt'] = array();
            }

            // A flag is added because it isn't carried out twice.
            if( $this->_nalConf['api_type'] === neccsNal_Config::API_TYPE_WIM ){
                $data['wim_check_flg'] = '1';
                $this->success( $data );
            }

            // In case of OpenStack information of NAL
            if( $this->_nalConf['api_type'] === neccsNal_Config::API_TYPE_NAL ){
                $nalData = array();
                $nalData = $data;
            }
        }

        if( $this->_nalConf['api_type'] === neccsNal_Config::API_TYPE_NAL ){

            // get Contract Cnt
            $result = $this->_getContInfo( $nalData, $wimData, $execList );
            $result['contract_info'] = array_values( $result['contract_info'] );

            $url = neccsNal_Config::NAL_API_URL . str_replace( '/Nal/', '', $_SERVER['REQUEST_URI'] );
            $this->logit( neccsNal_Config::SUCCESS_CODE, "OutPut Data ( $url )", $this->_p, $result );

            // It outputs the result
            $this->success( $result );
        }
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
                // In the case of error
            }else if( in_array( $code, neccsNal_Config::$errorApiCode ) ){
                $errMsg = $result['result']['message'];
                // Output log
                $this->logit($code, $errMsg , '', $result);
            }

            // If you are running the test, return only message
            if( defined( 'PHPUNIT_RUN' ) ){
                throw new Exception( $result['result']['message'] );
            }

            // Return of the response
            header( "HTTP/1.1 200" );
            header( neccsNal_Config::CONTENT_TYPE_JSON );
            print json_encode( $result );
            exit(0);
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
        $inParam['type']   = neccsNal_Config::CONFIG_TYPE_COMMON;
        $inParam['dc_id']  = isset( $this->_p['dc_id'] ) ? $this->_p['dc_id'] : 'system';
        // get the config
        $confInfo = array();
        $flavorList = array();
        $confInfo = $this->getConfig( $inParam );

        if( empty( $confInfo ) ){
            return array();
        }

        $confInfo = json_decode( $confInfo[0]['config_info'], true );
        $flavorList = $confInfo['os_image_and_flavor_name_list'];

        // Reference of OpenStack information
        $endpoint     = json_decode( $endpointInfo[0]['endpoint_info'], true );
        $tenant_name  = $endpoint['admin_tenant_name'];

        $flavorCntInfo = $this->listFlavorsDetail( $tenant_name, $endpoint );
        $flavorListForCtr = $this->setFlavorData( $flavorList, $flavorCntInfo );

        return $flavorListForCtr;

    }

    /**
     * Format information acquired from REST API
     *
     * @param OpenStack info(NAL)
     * @param OpenStack info(WIM)
     * @param REST API information
     *
     * @return Tenant Information
     */
    protected function _getContInfo( $nalData, $wimData, $execList ){

        $use_type = $execList['pod_info'][0]['use_type'];

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

        $contractCntInfo = array();
        foreach( $execList['tenant_contract_info'] as $contract ){

            if( $contract['apl_type'] != neccsNal_Config::APL_TYPE_VIRTUAL ){
                continue;
            }

            $tenant_name = $contract['tenant_name'];
            if( !isset( $contractCntInfo[$tenant_name] ) ){
                $contractCntInfo[$tenant_name]['contract_cnt']   = 0;
                $contractCntInfo[$tenant_name]['tenant_name']    = $tenant_name;
                $contractCntInfo[$tenant_name]['IaaS_tenant_id'] = $contract['IaaS_tenant_id'];
            }
            $type        = $contract['type'];
            $device_type = $contract['device_type'];

            if( isset( $flavorContCntList[$type][$device_type] ) ){
                if( $contract['type'] == neccsNal_Config::TYPE_ROUTER ){
                    $contractCntInfo[$tenant_name]['contract_cnt'] += $flavorContCntList[$type][$device_type]['count'] * 2;
                } else {
                    $contractCntInfo[$tenant_name]['contract_cnt'] += $flavorContCntList[$type][$device_type]['count'] * $contract['contract'];
                }
            }
        }

        // set Data(tenant info)
        $tenantInfo = array();
        foreach( $execList['apl_info'] as $aplInfo ){
            $node_id = $aplInfo['node_id'];
            $tenantInfo[$node_id]['IaaS_tenant_id'] = $aplInfo['IaaS_tenant_id'];
            $tenantInfo[$node_id]['tenant_name']    = $aplInfo['tenant_name'];
        }

        // set Data(use_cnt)
        $useCntInfo = array();
        $total_use_cnt = 0;
        $useCntList = isset( $data['use_info'] ) ? $data['use_info'] : array();
        foreach( $useCntList as $instance_id => $use_cnt ){
            if( isset( $tenantInfo[$instance_id] ) ){
                $tenant_name = $tenantInfo[$instance_id]['tenant_name'];
                $useCntInfo[$tenant_name]['tenant_name']    = $tenantInfo[$instance_id]['tenant_name'];
                $useCntInfo[$tenant_name]['IaaS_tenant_id'] = $tenantInfo[$instance_id]['IaaS_tenant_id'];

                if( !isset( $useCntInfo[$tenant_name]['use_cnt'] ) ){
                    $useCntInfo[$tenant_name]['use_cnt'] = $use_cnt;
                    $total_use_cnt += $use_cnt;
                } else {
                    $useCntInfo[$tenant_name]['use_cnt'] += $use_cnt;
                    $total_use_cnt += $use_cnt;
                }
            }
        }
        if ( $this->_p['function_type'] === neccsNal_Config::MEMORY_DETAIL ){
            $total_use_cnt = $this->_setUnitForMemory( $total_use_cnt );
        } else if ( $this->_p['function_type'] === neccsNal_Config::STORAGE_DETAIL ){
            $total_use_cnt = $this->_setUnitForStorage( $total_use_cnt );
        }
        $data['total_info']['use_cnt'] = $total_use_cnt;

        $tenant_key = array_merge( array_keys( $useCntInfo ), array_keys( $contractCntInfo ) );
        $tenant_key = array_values( array_unique( $tenant_key ) );

        $data['contract_info'] = array();
        foreach( $tenant_key as $key => $tenant ){
            $data['contract_info'][$key]['ID'] = $key;
            if( isset( $useCntInfo[$tenant] ) ){
                $data['contract_info'][$key]['use_cnt']        = $useCntInfo[$tenant]['use_cnt'];
                $data['contract_info'][$key]['tenant_name']    = $useCntInfo[$tenant]['tenant_name'];
                $data['contract_info'][$key]['IaaS_tenant_id'] = $useCntInfo[$tenant]['IaaS_tenant_id'];
            } else {
                $data['contract_info'][$key]['use_cnt'] = 0;
            }
            if( isset( $contractCntInfo[$tenant] ) ){
                $data['contract_info'][$key]['contract_cnt']   = $contractCntInfo[$tenant]['contract_cnt'];
                $data['contract_info'][$key]['tenant_name']    = $contractCntInfo[$tenant]['tenant_name'];
                $data['contract_info'][$key]['IaaS_tenant_id'] = $contractCntInfo[$tenant]['IaaS_tenant_id'];
            } else {
                $data['contract_info'][$key]['contract_cnt'] = 0;
            }

            if ( $this->_p['function_type'] === neccsNal_Config::MEMORY_DETAIL ){
                $data['contract_info'][$key]['contract_cnt'] = $this->_setUnitForMemory( $data['contract_info'][$key]['contract_cnt'] );
                $data['contract_info'][$key]['use_cnt']      = $this->_setUnitForMemory( $data['contract_info'][$key]['use_cnt'] );
            } else if ( $this->_p['function_type'] === neccsNal_Config::STORAGE_DETAIL ){
                $data['contract_info'][$key]['contract_cnt'] = $this->_setUnitForStorage( $data['contract_info'][$key]['contract_cnt'] );
                $data['contract_info'][$key]['use_cnt']      = $this->_setUnitForStorage( $data['contract_info'][$key]['use_cnt'] );
            }
        }

        if( array_key_exists( 'use_info', $data ) ){
            unset( $data['use_info'] );
        }

        if( array_key_exists( 'flavor_list_for_cnt', $data ) ){
            unset( $data['flavor_list_for_cnt'] );
        }

        if( array_key_exists( 'wim_check_flg', $data ) ){
            unset( $data['wim_check_flg'] );
        }

        return $data;
    }

    /**
     * Return of the response
     *
     * @param tenant infomation
     * @param usage information
     * @param flavor information
     *
     */
    protected function setFlavorData( $flavorList, $flavorCntInfo ) {

        $setFlavorList = array();
        foreach( $flavorList as $type => $info1 ){
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
                        if( $this->_p['function_type'] === neccsNal_Config::CPU_DETAIL ){
                            $setFlavorList[$type][$device_type]['count'] = $floverCnt['vcpus'];
                        } else if ( $this->_p['function_type'] === neccsNal_Config::MEMORY_DETAIL ){
                            $setFlavorList[$type][$device_type]['count'] = $floverCnt['ram'];
                        } else if ( $this->_p['function_type'] === neccsNal_Config::STORAGE_DETAIL ){
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

        $result = array();
        $result['total_info']['quota'] = 0;

        $info = array();
        ///////// In the case usage /////////
        if( !empty( $this->_usagesInfo['tenant_usages'] ) ){

            foreach( $this->_usagesInfo['tenant_usages'] as $serverList ){
                // Get the tenant_name
                $tenant_id = $serverList['tenant_id'];

                // The initialization
                foreach( $serverList['server_usages'] as $value ){
                    $instance_id = $value['instance_id'];

                    // set total_info and contract_info
                    if( $this->_p['function_type'] === neccsNal_Config::CPU_DETAIL ){
                        $info[$instance_id]               = $value['vcpus'];
                    } else if ( $this->_p['function_type'] === neccsNal_Config::MEMORY_DETAIL ){
                        $info[$instance_id]               = $value['memory_mb'];
                    } else if ( $this->_p['function_type'] === neccsNal_Config::STORAGE_DETAIL ){
                        $info[$instance_id]               = $value['local_gb'];
                    }

                }
            }
        } else {
            $info = array();
        }

        // To add to the return value to convert the associative array to normal array
        $result['use_info'] = $info;

        ///////// In the case quota /////////
        foreach( $this->_quotaInfo as $quotaList ){

            // set total_info
            if( $this->_p['function_type'] === neccsNal_Config::CPU_DETAIL ){
                $result['total_info']['quota'] += $quotaList['cpu'];
            } else if ( $this->_p['function_type'] === neccsNal_Config::MEMORY_DETAIL ){
                $result['total_info']['quota'] += $quotaList['memory_mb'];
            } else if ( $this->_p['function_type'] === neccsNal_Config::STORAGE_DETAIL ){
                $result['total_info']['quota'] += $quotaList['disk_gb'];
            }
        }

        if ( $this->_p['function_type'] === neccsNal_Config::MEMORY_DETAIL ){
            $result['total_info']['quota']   = $this->_setUnitForMemory( $result['total_info']['quota'] );
        } else if ( $this->_p['function_type'] === neccsNal_Config::STORAGE_DETAIL ){
            $result['total_info']['quota']   = $this->_setUnitForStorage( $result['total_info']['quota'] );
        }

        return $result;
    }

}
