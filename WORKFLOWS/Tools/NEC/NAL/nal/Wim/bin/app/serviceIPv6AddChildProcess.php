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
* 2.FUNCTION : serviceIPv6AddChildProcess.php
*/
require_once dirname(__FILE__). '/serviceBaseChildProcess.php';

class serviceIPv6AddChildProcess extends serviceBaseChildProcess {

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

        $execCmd = "$jcCmd -p $jobParam ". neccsNal_Config::UPDATE_SERVICE_IPV6_ADD_FINAL;

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

        $this->jobCenterOperation = neccsNal_Config::UPDATE_SERVICE_IPV6_ADD_FINAL;

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

}