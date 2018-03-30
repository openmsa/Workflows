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
require_once dirname(__FILE__) . '/../api/Nal.php';

class NalChildProcess extends neccsNal {

    /**
     * Constructor
     *
     */
    function __construct( $param ) {

        // Request method
        $this->_httpMethod = $param['request_method'];

        // Request parameters
        $this->_p          = $param;

        // Request ID
        $this->_requestId  = $param['request-id'];

        // Configuration files of NAL
        $this->_nalConf    = $param['nal_conf'];

        // Class name
        $this->_className  = $param['function_type'];

        // Operation
        $this->jobCenterOperation = $param['job_operation'];

        // Child process flg
        $this->_childProcessFlg = '1';
    }

    /**
     * It gets an instance
     *
     * @param  List of batch argument
     * @return An instance of the API by class
     */
    public static function getBatchInstance( $opts ) {

        // Parameters file
        if( isset( $opts['f'] ) && $opts['f'] !== '' ) {
            $filePath = $opts['f'];
        } else {
            self::fatalBatchError( neccsNal_Config::PARAMETER_ERROR, "A parameter is unjust." );
        }

        // If the file does not exist
        if( !file_exists( $filePath ) ) {
            self::fatalBatchError( neccsNal_Config::PARAMETER_ERROR, "A file doesn't exist. ({$filePath})" );
        }

        $file = @fopen( $filePath, 'r' );
        // File read failure
        if( $file === false ) {
            self::fatalBatchError( neccsNal_Config::PARAMETER_ERROR, "file was not opened. ({$filePath})" );
        }

        // Read the file
        $tmp = fgets( $file );

        // File close
        fclose( $file );

        // Unserialized
        $param = unserialize( $tmp );

        // Required parameter check
        if( !isset( $param['request_method'] ) || !isset( $param['scenario'] ) || !isset( $param['function_type'] ) ) {
            self::fatalBatchError( neccsNal_Config::PARAMETER_ERROR, "A parameter is unjust." );
        }

        $method       = $param['request_method'];
        $scenario     = $param['scenario'];
        $functionType = $param['function_type'];
        $classPath = APP_DIR . "/" . $functionType . neccsNal_Config::CHILD_PROCESS_FILE . ".php";

        // If the function does not exist, an error
        if( !isset( neccsNal_Config::$tradeMaterialList[$scenario] ) ) {
            self::fatalBatchError( neccsNal_Config::PARAMETER_ERROR, "This function can not be used. ({$scenario})" );
        }

        // If the merchandise is not present, the error
        if( !isset( neccsNal_Config::$tradeMaterialList[$scenario][$functionType] ) ) {
            self::fatalBatchError( neccsNal_Config::PARAMETER_ERROR, "This class can not be used. ({$scenario} : {$functionType})" );
        }

        // If not included in the available method name, to error
        if( !in_array( $method, neccsNal_Config::$tradeMaterialList[$scenario][$functionType] ) ){
            self::fatalBatchError( neccsNal_Config::PARAMETER_ERROR, "This class can not be used. ({$scenario} : {$functionType} : {$method})" );
        }


        // If the class is present
        if ( file_exists( $classPath ) === true ) {
            require_once $classPath;
            $className = $functionType . neccsNal_Config::CHILD_PROCESS_FILE;
            if ( class_exists( $className, false ) ) {
                $obj = new $className( $param );
            } else {
                self::fatalBatchError( neccsNal_Config::API_INTERNAL_ERROR, "not found class: {$className}" );
            }

        // If the class does not exist, the call of NalChildProcess.php
        } else {
            $obj = new NalChildProcess( $param );
        }

        return $obj; // Return an instance
    }

    /**
     * error processing (Fatal error)
     *
     * @param Error details
     */
    public static function fatalBatchError( $errCode='', $message='', $param=array() ) {

        // Error message
        $errMsg = !empty( $message ) ? $message : neccsNal_Config::$errorCode[neccsNal_Config::STATUS_ERROR]['message'];

        // Request id
        $requestId = isset( $param['request-id'] ) ? $param['request-id'] : '';

        // Error level
        $errLevel = strtoupper( neccsNal_Config::LEV_ERROR );

        // Operation
        $operation = "undefine_operation_batch"; // Fixed value

        // Request parameters
        $in = !empty( $param ) ? $param : '';

        // Log format
        $logInfo = array();
        $logInfo = array(
            '[' . $errLevel . ']',
            date( 'Y/m/d H:i:s' ),
            '[' . $operation . ']',
            $requestId,
            '[CODE]' . $errCode,
            '[IN]' . ( $in !== '' ? json_encode( $in ) : $in ),
            '[OUT]' . '',
            '[MESSAGE]' . ( is_array( $message ) ? var_export( $message ) : $message ),
        );

        // Log file path
        $logFile = neccsNal_Config::LOG_DIR . neccsNal_Config::$logFileName[$errLevel];

        // Check of the directory
        $dir = dirname( $logFile );
        if( is_dir( $dir ) === false ) {
            mkdir( $dir, 0755, true );
        }

        // File open
        $fp = @fopen( $logFile, "a" );
        if( $fp === false ) {
            return;
        }

        // Write the log
        if( flock( $fp, LOCK_EX ) ) {
            fputs( $fp, implode( '', $logInfo ) . "\r\n" );
            fflush( $fp );
            flock( $fp, LOCK_UN );
            fclose( $fp );
        }

        // If you are running the test, return only message
        if( defined( 'PHPUNIT_RUN' ) ) { throw new Exception( $errMsg ); }
        exit(0);
    }

    /**
     * Main
     *
     */
    public function batchRun() {

        // HTTP method
        $method = $this->_httpMethod;

        try {
            // Call the method
            if( method_exists( $this, $method ) ) {
                $this->$method();
            } else {
                $this->error( neccsNal_Config::API_INTERNAL_ERROR, "not found method: {$method}" );
            }

        } catch( Exception $e ) {
            $this->error( neccsNal_Config::API_INTERNAL_ERROR, $e->getMessage(). $e->getTraceAsString() );
        }
    }

    /**
     * POST method (post)
     *
     */
    protected function post() {
    }

    /**
     * PUT method (put)
     *
     */
    protected function put() {
    }

    /**
     * DELETE method (delete)
     *
     */
    protected function delete() {
    }
}
