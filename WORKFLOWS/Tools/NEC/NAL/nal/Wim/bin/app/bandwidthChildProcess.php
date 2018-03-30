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
* 2.FUNCTION : NalChildProcess.php
*/
require_once dirname(__FILE__). '/../NalChildProcess.php';

class bandwidthChildProcess extends NalChildProcess {

    /**
     * POST method (post)
     *
     */
    protected function post() {

        // Call the JobCenter or JobScheduler(Check)
        // To specify the number of times retry
        // In the case of the PHPUnit test, specify a 1-second wait to retry once maximum
        $max      = defined( 'PHPUNIT_RUN' ) ? 1 : neccsNal_Config::$retrySettingList[$this->_className][$this->_httpMethod]['retry_max'];
        $interval = defined( 'PHPUNIT_RUN' ) ? 1 : neccsNal_Config::$retrySettingList[$this->_className][$this->_httpMethod]['retry_interval'];

        // Call the JobCenter or JobScheduler(Check)
        for( $retry = 1; $retry <= $max; $retry++ ) {

            // Completion confirmation job execution
            $this->execCheckNal( $retry, $max );

            // wait
            sleep( $interval );
        }

    }

    /**
     * PUT method (put)
     *
     */
    protected function put() {

        // Call the JobCenter or JobScheduler(Check)
        // To specify the number of times retry
        // In the case of the PHPUnit test, specify a 1-second wait to retry once maximum
        $max      = defined( 'PHPUNIT_RUN' ) ? 1 : neccsNal_Config::$retrySettingList[$this->_className][$this->_httpMethod]['retry_max'];
        $interval = defined( 'PHPUNIT_RUN' ) ? 1 : neccsNal_Config::$retrySettingList[$this->_className][$this->_httpMethod]['retry_interval'];

        // Call the JobCenter or JobScheduler(Check)
        for( $retry = 1; $retry <= $max; $retry++ ) {

            // Completion confirmation job execution
            $this->execCheckNal( $retry, $max );

            // wait
            sleep( $interval );
        }

    }

    /**
     * DELETE method (delete)
     *
     */
    protected function delete() {

        // Call the JobCenter or JobScheduler(Check)
        // To specify the number of times retry
        // In the case of the PHPUnit test, specify a 1-second wait to retry once maximum
        $max      = defined( 'PHPUNIT_RUN' ) ? 1 : neccsNal_Config::$retrySettingList[$this->_className][$this->_httpMethod]['retry_max'];
        $interval = defined( 'PHPUNIT_RUN' ) ? 1 : neccsNal_Config::$retrySettingList[$this->_className][$this->_httpMethod]['retry_interval'];

        // Call the JobCenter or JobScheduler(Check)
        for( $retry = 1; $retry <= $max; $retry++ ) {

            // Completion confirmation job execution
            $this->execCheckNal( $retry, $max );

            // wait
            sleep( $interval );
        }

    }

    /**
     * Call the JobCenter or JobScheduler(Check)
     *
     */
    protected function execCheckNal( $retry, $max ) {
        $job_type = $this->_nalConf['job_type'];
        if( $job_type === neccsNal_Config::JOB_SCHEDULER ){
            $this->checkJobSchedulerNal( $retry, $max );
        }else{
            $this->checkJobCenterNal( $retry, $max );
        }
    }

    /**
     * Call the JobCenter (Job execution completion confirmation)
     *
     */
    protected function checkJobCenterNal( $retry, $max ) {

        // Get the JOB ID
        if( isset( $this->_p['job-id'] ) ) {
            $this->_jobId = $this->_p['job-id'];
        } else {
            return $this->error( neccsNal_Config::PARAMETER_ERROR, "job-id is not set." );
        }

        // Get the request id
        if( isset( $this->_p['request-id'] ) ) {
            $this->_requestId = $this->_p['request-id'];
        } else {
            return $this->error( neccsNal_Config::PARAMETER_ERROR, "request-id is not set." );
        }

        // Replaced by JOB ID
        $param = array( '%JOBID%' => $this->_jobId );
        $jcCmd = strtr( neccsNal_Config::CMD_JOB_CENTER_CHECK, $param );

        // Run the job
        if( !defined( 'PHPUNIT_RUN' ) ){
            // Run the job
            $status = shell_exec( $jcCmd );
        } else {
            // If you are running a PHPUnit test, get the return value from the parameter
            $status = $this->_p['job-status'];
        }

        // status is [done]
        if( $status === neccsNal_Config::JOB_STATUS_DONE ) {

            $this->logit( neccsNal_Config::SUCCESS_CODE, "job command : $jcCmd", $this->_p, $status );

            // Get the information of OUT.json(Return empty if there is no data)
            $data = $this->_setOutParam();
            // Add "function_type" on the parameters passed to the Wim API
            $data['function_type'] = $this->_p['function_type'];
            // Add device_type to the parameter
            $data['device_type'] = $this->_p['device_type'];
            // Add group_type to the parameter
            $data['group_type'] = $this->_p['service_type'];

            // WIM API URL
            $url = neccsNal_Config::WIM_API_URL . $this->_p['scenario'];

            // Run the WIM API
            $result = $this->_execWimApi( $url, $data, $this->_p['request_method']);

            // If successful, DB update process
            $status = isset( $result['result']['status'] ) ? $result['result']['status'] : '';
            $dcChk  = isset( $result['data']['wim_check_bandwidth'] ) ? $result['data']['wim_check_bandwidth'] : '';
            if( $status === neccsNal_Config::STATUS_SUCCESS && $dcChk === '1' ) {

                // It rewrites the IN.json
                $this->_makeInFile( $result, "1" );
                // Access to the DB server
                $this->callJobCenterForDb( $this->_p['request_method'] );

            }

            // It returns the response
            $this->_execResult( $result, $url );

        // status is [run]
        } else if( $status === neccsNal_Config::JOB_STATUS_RUN ) {
            $this->logit( neccsNal_Config::SUCCESS_CODE, "job command : $jcCmd", $this->_p, $status );
            // Re-run if it does not reach the retry limit
            if( $retry !== $max ) {
                return;
            }
            $this->error( neccsNal_Config::JOB_EXEC_ERROR, "Condition error of the retry number of times. retry : $retry" );
        // If the state is empty
        } else if( $status === NULL ) {
            // Re-run if it does not reach the retry limit
            if( $retry !== $max ) {
                return;
            }
            $this->error( neccsNal_Config::JOB_EXEC_ERROR, "Condition error of the retry number of times. retry : $retry" );
        // If the state is illegal
        } else {
            // Re-run if it does not reach the retry limit
            if( $retry !== $max ) {
                return;
            }
            $this->error( neccsNal_Config::JOB_EXEC_ERROR, "It is in the unjust status. status : $status" );
        }
    }

    /**
     * Call the JobCenter or JobScheduler (Job execution completion confirmation)
     *
     */
    protected function checkJobSchedulerNal( $retry, $max ) {

        // Get the JOB ID
        if( isset( $this->_p['job-id'] ) ) {
            $this->_jobId = $this->_p['job-id'];
        } else {
            return $this->error( neccsNal_Config::PARAMETER_ERROR, "job-id is not set." );
        }

        // Get the request id
        if( isset( $this->_p['request-id'] ) ) {
            $this->_requestId = $this->_p['request-id'];
        } else {
            return $this->error( neccsNal_Config::PARAMETER_ERROR, "request-id is not set." );
        }

        // Replaced by JOB ID
        $paramfile = $this->makeParamterFile(2);
        $jcCmd = neccsNal_Config::CMD_JOB_SCHEDULER;
        $jcCmd = strtr($jcCmd,array('%FILE%' => $paramfile ));

        // Run the job
        if( !defined( 'PHPUNIT_RUN' ) ){
            // Run the job
            $out = shell_exec( $jcCmd );
        } else {
            // If you are running the PHPUnit test,Specify the return value from the parameter
            $out = isset( $this->_p['job_out']) ? $this->_p['job_out']  : '';
        }

        if( empty( $out ) ) {
            $this->error( neccsNal_Config::JOB_EXEC_ERROR, "Out params was not returned. (job command : $jcCmd )" );
        }

        $xml = new SimpleXMLElement($out);

        // In the case of normal
        if( (string)$xml->answer->order['state'] === neccsNal_Config::STATUS_SUCCESS ) {
            $this->logit( neccsNal_Config::SUCCESS_CODE, "job command : $jcCmd", $this->_p, $xml->answer->order['state'] );

            // Get the information of OUT.json(Return empty if there is no data)
            $data = $this->_setOutParam();
            // Add "function_type" on the parameters passed to the Wim API
            $data['function_type'] = $this->_p['function_type'];
            // Add device_type to the parameter
            $data['device_type'] = $this->_p['device_type'];
            // Add group_type to the parameter
            $data['group_type'] = $this->_p['service_type'];

            // WIM API URL
            $url = neccsNal_Config::WIM_API_URL . $this->_p['scenario'];

            // Run the WIM API
            $result = $this->_execWimApi( $url, $data, $this->_p['request_method']);

            // If successful, DB update process
            $status = isset( $result['result']['status'] ) ? $result['result']['status'] : '';
            $dcChk  = isset( $result['data']['wim_check_bandwidth'] ) ? $result['data']['wim_check_bandwidth'] : '';
            if( $status === neccsNal_Config::STATUS_SUCCESS && $dcChk === '1' ) {

                // It rewrites the IN.json
                $this->_makeInFile( $result, "1" );
                // Access to the DB server
                $this->callJobSchedulerForDb( $this->_p['request_method'] );

            }

            // It returns the response
            $this->_execResult( $result, $url );


        // In the case of error
        }else if( (string)$xml->answer->order['state'] === neccsNal_Config::STATUS_ERROR  ) {
                // Re-run if it does not reach the retry limit
                if( $retry !== $max ) {
                    return;
                }
                $this->error( neccsNal_Config::JOB_EXEC_ERROR, "It is in the unjust status. status : " . $xml->answer->ERROR['code'] );

        // If you are running
        }else {
            $this->logit( neccsNal_Config::SUCCESS_CODE, "job command : $jcCmd", $this->_p, neccsNal_Config::JOB_STATUS_RUN );
            // Re-run if it does not reach the retry limit
            if( $retry !== $max ) {
                return;
            }
            $this->error( neccsNal_Config::JOB_EXEC_ERROR, "Condition error of the retry number of times. retry : $retry" );
        }
    }

    /**
     * Run the JOB(For DB server access)
     *
     * @return The execution result of the API for the DB server access
     */
    protected function callJobCenterForDb( $method = '' ){

        // Specify the path that was created when you created the OUT.json or IN.json( POST,PUT,DELETE )
        if( isset( $this->fileDirPath ) ){

            // Specify the request ID that was paid out in the first
            $filePath = $this->fileDirPath;

        // If there is a request ID in IN parameters( GET )
        // $this->_requestId is the UUID to be paid out without fail at the time of API execution
        }else if( isset( $this->_p['request-id'] ) ){

            // Create a path to the directory
            $trans = array(
                            '%ROOT_DIR%' => $this->_nalConf['root_inoutfile'],
                            '%UUID%'     => $this->_p['request-id'],
            );
            $filePath = strtr( neccsNal_Config::DIR_PATH, $trans );

        }

        // Get a device_type
        if( isset( $this->_p['device_type'] ) ) {
            $this->_deviceType = $this->_p['device_type']. $this->_p['service_type'];
        } else {
            $this->error( neccsNal_Config::PARAMETER_ERROR, "device_type is not set." );
        }

        // Call the JOB Center
        $jcCmd = neccsNal_Config::CMD_JOB_CENTER;

        // Add the parameter
        $jobParam = "'" . $filePath . " " . neccsNal_Config::IN_FILE . " " . neccsNal_Config::OUT_FILE . " ". $this->_deviceType.  "'";

        $execCmd = "$jcCmd -p $jobParam ". neccsNal_Config::UPDATE_BANDWIDTH_FINAL;

        // Run the job
        if( !defined( 'PHPUNIT_RUN' ) ){
            // Run the job
            $out = shell_exec( $execCmd );
        } else {
            // If you are running the PHPUnit test,Specify the return value from the parameter
            $out = isset( $this->_p['job_out']) ? $this->_p['job_out']  : '';
        }

        // OUT parameters is not returned
        if( empty( $out ) ) {
            $this->error( neccsNal_Config::JOB_EXEC_ERROR, "Out params was not returned. (job command : $execCmd)" );
        }

        // Output log
        $this->logit( neccsNal_Config::SUCCESS_CODE, "job command : $execCmd", $this->_p, $out );

        // Process the ID
        list( , , $jobkey ) = explode( ":", $out );
        list( $fnc, $dt )   = explode( ".", $jobkey );
        $this->_p['job-id'] = $fnc . '.' . $dt;

        $this->_p['request-id'] = $this->_requestId;

    }

    /**
     * Call JobScheduler (post put delete)
     *
     */
    protected function callJobSchedulerForDb() {

        $this->jobCenterOperation = neccsNal_Config::UPDATE_BANDWIDTH_FINAL;

        $file = $this->makeParamterFile(neccsNal_Config::JOB_EXEC_MODE);
        $jcCmd = neccsNal_Config::CMD_JOB_SCHEDULER;
        $jcCmd = strtr($jcCmd,array('%FILE%' => $file ));

        // Run the JOB
        if( !defined( 'PHPUNIT_RUN' ) ){
            // Run the JOB
            $out = shell_exec( $jcCmd );
        } else {
            // If you are running the PHPUnit test,Specify the return value from the parameter
            $out = isset( $this->_p['job_out']) ? $this->_p['job_out']  : '';
        }

        // OUT parameters is not returned
        if( empty( $out ) ) {
            $this->error( neccsNal_Config::JOB_EXEC_ERROR, "Out params was not returned. (job command : $jcCmd )" );
        }

        // Output log
        $this->logit( neccsNal_Config::SUCCESS_CODE, "job command : $jcCmd", $this->_p, $out );

        $xml = new SimpleXMLElement($out);
        $this->_p['job-id'] = (string)$xml->answer->ok->order['order'];

        $this->_p['request-id'] = $this->_requestId;

    }

    /**
     * Run the WIM API
     * ※ Used to pass parameters from arguments when calling WIM.
     *
     * @param URL
     * @param Parameters
     * @param HTTP method
     * @return Execution result of decoding
     */
    protected function _execWimApi( $url, $param='', $httpMethod, $noproxy='' ) {

        // requet id
        if( isset( $this->_p['request-id'] ) ) {
            $param['request-id'] = $this->_p['request-id'];
        }

        // encode
        if( is_array( $param ) ) $param = json_encode( $param );

        // Initialization of cURL
        $ch = curl_init( $url );

        // Set of HTTP header
        curl_setopt( $ch, CURLOPT_HTTPHEADER, array( neccsNal_Config::CONTENT_TYPE_JSON ) );
        if( $noproxy ){
            curl_setopt($ch, CURLOPT_PROXY, '');
        }

        // In the case of calls to the WIM API, the BASIC authentication
        if( $this->_nalConf['api_type'] === neccsNal_Config::API_TYPE_NAL ) {
            curl_setopt( $ch, CURLOPT_USERPWD, neccsNal_Config::BASIC_AUTH_ID . ":" . neccsNal_Config::BASIC_AUTH_PW );
        }

        if( $httpMethod === neccsNal_Config::HTTP_POST ) {

            curl_setopt( $ch, CURLOPT_POST, true );
            curl_setopt( $ch, CURLOPT_POSTFIELDS, $param );
            curl_setopt( $ch, CURLOPT_SSL_VERIFYPEER, FALSE );
            curl_setopt( $ch, CURLOPT_RETURNTRANSFER, true );
            curl_setopt( $ch, CURLINFO_HEADER_OUT, true );

        } else if( $this->_httpMethod === neccsNal_Config::HTTP_PUT ) {

            curl_setopt($ch, CURLOPT_CUSTOMREQUEST, neccsNal_Config::HTTP_PUT);
            curl_setopt($ch, CURLOPT_FAILONERROR, false);
            curl_setopt($ch, CURLOPT_POSTFIELDS, $param);
            curl_setopt($ch, CURLOPT_POST, true);
            curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, FALSE);
            curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
            curl_setopt($ch, CURLINFO_HEADER_OUT, true);

        } else if( $httpMethod === neccsNal_Config::HTTP_DELETE ) {

            curl_setopt( $ch, CURLOPT_CUSTOMREQUEST, neccsNal_Config::HTTP_DELETE );
            curl_setopt( $ch, CURLOPT_FAILONERROR, false );
            curl_setopt( $ch, CURLOPT_POST, true );
            curl_setopt( $ch, CURLOPT_POSTFIELDS, $param );
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
     * It rewrites the IN.json
     *
     * @param The execution result of the WIM API
     * @param Content to be written to the IN.json 0 : $result['data']
     *                                             2 : $result
     */
    protected function _makeInFile( $result, $all_flg = "0" ){

        // Specify the path that was created when you created the OUT.json or IN.json( POST,PUT,DELETE )
        if( isset( $this->fileDirPath ) ){

            // Specify the request ID that was paid out in the first
            $filePath = $this->fileDirPath;

            // Create a path from the request ID if there is a request ID
        }else if( isset( $this->_p['request-id'] ) ){

           // Create a path to the directory
            $trans = array(
                            '%ROOT_DIR%' => $this->_nalConf['root_inoutfile'],
                            '%UUID%'     => $this->_p['request-id'],
            );
            // Specify the specified request ID in the input Parameters
            $filePath = strtr( neccsNal_Config::DIR_PATH, $trans );

        }

        // If all acquisition flag is 1
        if( $all_flg === "1" ){
            // $result
            $data = $result;
        }else{
            // $result['data']
            $data = $result['data'];
        }

        // Create a file input Parameters
        $inFile  = $filePath . '/' . neccsNal_Config::IN_FILE;
        $inJson  = json_encode( $data );
        $winFile = @fopen( $inFile, 'w+' );
        if( $winFile === false ) {
            $this->error( neccsNal_Config::API_INTERNAL_ERROR, "file was not opened. ({$inFile})" );
        }
        fwrite( $winFile, $inJson );
        fclose( $winFile );

    }
}