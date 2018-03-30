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
 * 2.FUNCTION : serviceSetting.php (Individual method)
 */
require_once dirname(__FILE__). '/../Nal.php';

class serviceSetting extends neccsNal {

    /**
     * PUT method (put)
     *
     */
    protected function put() {

        // create a file
        $this->makeNalFile();

        // Call the JobCenter or JobScheduler
        $this->execJobNalWim();

        if( $this->_nalConf['api_type'] === neccsNal_Config::API_TYPE_NAL ) {

            // Call child process
            $this->childProcessExec();

            // It outputs the result
            $this->success();

        } else if ( $this->_nalConf['api_type'] === neccsNal_Config::API_TYPE_WIM ) {

            // To specify the number of times retry
            // In the case of the PHPUnit test, specify a 1-second wait to retry once maximum
            $max      = defined( 'PHPUNIT_RUN' ) ? 1 : neccsNal_Config::$retrySettingList[$this->_className][$this->_httpMethod]['retry_max'];
            $interval = defined( 'PHPUNIT_RUN' ) ? 1 : neccsNal_Config::$retrySettingList[$this->_className][$this->_httpMethod]['retry_interval'];

            for( $retry = 1; $retry <= $max; $retry++ ){

                // Call of the API reference job execution result
                $this->checkJobForDbWim( $retry, $max );

                sleep( $interval );

            }

        }

    }

    /**
     * Call the JobCenter or JobScheduler
     *
     */
    protected function execJobNalWim() {

        $job_type = $this->_nalConf['job_type'];
        if( $job_type === neccsNal_Config::JOB_SCHEDULER ){
            $this->callJobScheduler();
        }else{
            $this->callJobCenterNalWim();
        }
    }

    /**
     * Call the JobCenter (post put delete)
     *
     */
    protected function callJobCenterNalWim() {

        // Get a device_type
        if( isset( $this->_p['device_type'] ) ) {
            $this->_deviceType = $this->_p['device_type'];
        } else {
            $this->error( neccsNal_Config::PARAMETER_ERROR, "device_type is not set." );
        }

        // Call the JOB Center
        $jcCmd = neccsNal_Config::CMD_JOB_CENTER;

        // In the case of calling in WIN server, convert the JOB ID
        if( $this->_nalConf['api_type'] === neccsNal_Config::API_TYPE_WIM ){
            $this->jobCenterOperation = str_replace( 'serviceSetting', 'wimserviceSetting', $this->jobCenterOperation );
        }

        // exec JOB
        if( !defined( 'PHPUNIT_RUN' ) ){
            // exec JOB
            $out = shell_exec( "$jcCmd -p $this->jobCenterParam $this->jobCenterOperation" );
        } else {
            // If you are running the PHPUnit test, specify the return value from the parameter
            $out = isset( $this->_p['job_out']) ? $this->_p['job_out']  : '';
        }

        // OUT parameters is not returned
        if( empty( $out ) ) {
            $this->error( neccsNal_Config::JOB_EXEC_ERROR, "Out params was not returned. (job command : $jcCmd -p $this->jobCenterParam $this->jobCenterOperation)" );
        }

        // Output log
        $this->logit( neccsNal_Config::SUCCESS_CODE, "job command : $jcCmd -p $this->jobCenterParam $this->jobCenterOperation", $this->_p, $out );

        // Process the ID
        list( , , $jobkey ) = explode( ":", $out );
        list( $fnc, $dt )   = explode( ".", $jobkey );
        $this->_p['job-id'] = $fnc . '.' . $dt;

        $this->_p['request-id'] = $this->_requestId;

    }

    /**
     * Run WIM API
     *
     * @param URL
     * @param Parameters
     * @param HTTP method
     * @return Execution result of decoding
     */
    protected function _execWimApi( $url, $param='', $httpMethod, $noproxy='' ) {

        if( isset( $this->_p['request-id'] ) ) {
            $param['request-id'] = $this->_p['request-id'];
        }

        // Encode
        if( is_array( $param ) ) $param = json_encode( $param );

        // Initialization of cURL
        $ch = curl_init( $url );

        // Set of HTTP header
        curl_setopt( $ch, CURLOPT_HTTPHEADER, array( neccsNal_Config::CONTENT_TYPE_JSON ) );
        if( $noproxy ) {
            curl_setopt($ch, CURLOPT_PROXY, '');
        }

        // In the case of calls to the WIM API, the BASIC authentication
        if( $this->_nalConf['api_type'] === neccsNal_Config::API_TYPE_NAL ) {
            curl_setopt( $ch, CURLOPT_USERPWD, neccsNal_Config::BASIC_AUTH_ID . ":" . neccsNal_Config::BASIC_AUTH_PW );
        }

        if( $httpMethod === neccsNal_Config::HTTP_GET ) {

            curl_setopt($ch, CURLOPT_HTTPGET, true);
            curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, FALSE);
            curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
            curl_setopt($ch, CURLINFO_HEADER_OUT, true);

        } else if( $httpMethod === neccsNal_Config::HTTP_POST ) {

            curl_setopt( $ch, CURLOPT_POST, true );
            curl_setopt( $ch, CURLOPT_POSTFIELDS, $param );
            curl_setopt( $ch, CURLOPT_SSL_VERIFYPEER, FALSE );
            curl_setopt( $ch, CURLOPT_RETURNTRANSFER, true );
            curl_setopt( $ch, CURLINFO_HEADER_OUT, true );

        } else if( $httpMethod === neccsNal_Config::HTTP_DELETE ) {

            curl_setopt( $ch, CURLOPT_CUSTOMREQUEST, neccsNal_Config::HTTP_DELETE );
            curl_setopt( $ch, CURLOPT_FAILONERROR, false );
            curl_setopt( $ch, CURLOPT_POSTFIELDS, $param );
            curl_setopt( $ch, CURLOPT_POST, true );
            curl_setopt( $ch, CURLOPT_SSL_VERIFYPEER, FALSE );
            curl_setopt( $ch, CURLOPT_RETURNTRANSFER, true );
            curl_setopt( $ch, CURLINFO_HEADER_OUT, true );
        }
        curl_setopt( $ch, CURLOPT_TIMEOUT, neccsNal_Config::CURL_TIMEOUT );
        $result = curl_exec( $ch );

        $info = curl_getinfo($ch);
        $http_status = $info['http_code'];

        curl_close( $ch );

        // If there is data(HTTP Statsu : 200,201,204)
        if( in_array( $http_status, neccsNal_Config::$successHttpStatus ) ) {

            // Output log
            $this->logit( neccsNal_Config::SUCCESS_CODE, "API success ($url)", $param, $result );


            // If the "tenant_name" exists in the output, to add to output the results to obtain the tenant ID
            $result = $this->_getIaaSTenantId( $result, $httpMethod );

            return $result;

        // If there is no data(HTTP Status : 500)
        } else if( in_array( $http_status, neccsNal_Config::$notFoundHttpStatus ) ){
            // Output log
            $this->logit( neccsNal_Config::SUCCESS_CODE, "data not exists. ($url)", $param, $result );
            // Return an empty array
            return array();
        }

        // Otherwise, to error
        $this->error( neccsNal_Config::REST_API_ERROR, "API error ($url)", $result );
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
            if( defined( 'PHPUNIT_RUN' ) ){ throw new Exception( $result['result']['message'] ); }

            // Return of the response
            header( "HTTP/1.1 200" );
            header( neccsNal_Config::CONTENT_TYPE_JSON );
            print json_encode( $result );
            exit(0);
        }
    }

    /**
     * End confirmation of the JobCenter
     *
     */
    protected function checkJobForDbWim( $retry, $max ) {

       // Get a URL
        $url = neccsNal_Config::API_URL . neccsNal_Config::API_URL_LIST;
        $url.= neccsNal_Config::RESOURCE_DC_CON_GROUPS;

        $request_id = isset( $this->_p['request-id'] ) ? $this->_p['request-id'] : $this->_requestId;
        $tenant_name = isset( $this->_p['tenant_name'] ) ? $this->_p['tenant_name'] : '';
        $group_type = isset( $this->_p['group_type'] ) ? $this->_p['group_type'] : '';

        $url .= '?' . 'request-id=' . $request_id;
        $url .= '&' . 'tenant_name=' . $tenant_name;
        $url .= '&' . 'group_type=' . $group_type;
        $url .= '&' . 'delete_flg=' . '0';

        if( $retry === 1 ){
            sleep( neccsNal_Config::DCCONNECT_WIM_STATUS_CHANGE_WAITING );
        }

        // Exec API
        $result = $this->_execWimApi( $url, '', neccsNal_Config::HTTP_GET );

        // Result output
        $status = isset( $result[0]['task_status'] ) ? $result[0]['task_status'] : '';

        // State is [successful]
        if( $status === neccsNal_Config::TASK_STATUS_SUCCESS ) {

            $this->logit( neccsNal_Config::SUCCESS_CODE, "Wim API DB access success ($url)", $this->_p, $status );
            sleep( neccsNal_Config::DCCONNECT_WIM_SUCCESS_WAITING );

            // Get the information of OUT.json(Return empty if there is no data)
            $data = array();
            $data = $this->_setOutParam();

            // Since the check has been successful in Wim, return a success flag
            $data['wim_check_serviceSetting'] = '1';

            // Remove Directory
            $this->_deleteDirectory();

            $this->success( $data );

            // State is [run]
        } else if( $status === neccsNal_Config::TASK_STATUS_RUNNING ) {
            $this->logit( neccsNal_Config::SUCCESS_CODE, "Wim API DB running success ($url)", $this->_p, $status );
            // Re-run if it does not reach the retry limit
            if( $retry !== $max ) {
                return;
            }
            $this->error( neccsNal_Config::JOB_EXEC_ERROR, "Condition error of the retry number of times. retry : $retry" );
        } else {
            // Re-run if it does not reach the retry limit
            if( $retry !== $max ) {
                return;
            }
            $this->error( neccsNal_Config::JOB_EXEC_ERROR, "It is in the unjust status. status : $status" );
        }
    }

}