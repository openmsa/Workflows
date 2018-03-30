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
 * 2.FUNCTION : neccsNal.php
 */
require_once 'Nal/Config.php';
require_once dirname(__FILE__). '/Validate.php';
require_once dirname(__FILE__). '/../lib/OpenStackClient/NovaClient/OscUsageReports.php';
require_once dirname(__FILE__). '/../lib/OpenStackClient/NovaClient/OscFlavors.php';
require_once dirname(__FILE__). '/../lib/OpenStackClient/NovaClient/OsHosts.php';

class neccsNal {

    protected $_tenantList = array();

    /**
     * Constructor
     *
     * @param Input parameters
     */
    function __construct( $param = '' ) {

        // Request method
        $this->_httpMethod = strtoupper( $_SERVER['REQUEST_METHOD'] );

        // Request parameters
        $this->_p          = !empty( $param ) ? $param : $this->getRequestParam();

        // Request ID
        $this->_requestId  = $this->_requestId();

        // NAL Setting file
        $this->_nalConf    = $this->getNalConfFile();

        // Class name
        $this->_className  = $this->_p['function_type'];

        // Gets the tethod by parameters
        $this->getInParam();

    }

    /**
     * Gets the tethod by parameters
     *
     */
    public function getInParam(){

        // In the case of GET
        if( $this->_httpMethod === neccsNal_Config::HTTP_GET ){

            $this->_p['delete_flg'] = '0';
            $this->_p['request-id'] = $this->_requestId;

        // In the case of POST
        } else if( $this->_httpMethod === neccsNal_Config::HTTP_POST ) {

            $this->_p['create_id']  = isset( $this->_p['operation_id'] ) ? $this->_p['operation_id'] : '';
            $this->_p['update_id']  = isset( $this->_p['operation_id'] ) ? $this->_p['operation_id'] : '';

            // In the case of service add their own dc_id the parameter
            if( $this->_p['scenario'] === neccsNal_Config::SERVICE && $this->_nalConf['api_type'] === neccsNal_Config::API_TYPE_NAL ){
                $this->_p['dc_id'] = neccsNal_Config::MY_DC_ID;
            }

        // In the case of PUT
        } else if( $this->_httpMethod === neccsNal_Config::HTTP_PUT ) {

            $this->_p['update_id']  = isset( $this->_p['operation_id'] ) ? $this->_p['operation_id'] : '';

            // In the case of service add their own dc_id the parameter
            if( $this->_p['scenario'] === neccsNal_Config::SERVICE && $this->_nalConf['api_type'] === neccsNal_Config::API_TYPE_NAL ){
                $this->_p['dc_id'] = neccsNal_Config::MY_DC_ID;
            }

        // In the case of DELETE
        } else if( $this->_httpMethod === neccsNal_Config::HTTP_DELETE ){

            $this->_p['update_id']  = isset( $this->_p['operation_id'] ) ? $this->_p['operation_id'] : '';
            $this->_p['delete_flg'] = '1';

            // In the case of service add their own dc_id the parameter
            if( $this->_p['scenario'] === neccsNal_Config::SERVICE && $this->_nalConf['api_type'] === neccsNal_Config::API_TYPE_NAL ){
                $this->_p['dc_id'] = neccsNal_Config::MY_DC_ID;
            }
        }
    }

    /**
     * Get instance
     *
     * @return An instance of the API by class
     */
    public static function getInstance() {

        $method   = strtoupper( $_SERVER['REQUEST_METHOD'] );
        $uri      = explode( '/', $_SERVER['REQUEST_URI'] );
        $scenario = isset( $uri[2] ) ? $uri[2] : '';

        // Get function_type
        if( $method === neccsNal_Config::HTTP_GET ){
            $param = $_GET;
        // If during the PHPUnit test run
        } else if( defined( 'PHPUNIT_RUN' ) ) {
            // Get $_POST
            $param = $_POST;
        }else{
            $param = json_decode( file_get_contents( 'php://input' ), true );
        }
        $param['scenario'] = $scenario;

        $functionType = isset( $param['function_type'] ) ? $param['function_type'] : '';
        $classPath = APP_DIR . "/{$functionType}.php";

        // If the function does not exist, it returns an error
        if( !isset( neccsNal_Config::$tradeMaterialList[$scenario] ) ){
            self::fatalError( neccsNal_Config::PARAMETER_ERROR, "This function can not be used. ({$scenario})" );
        }

        // If the merchandise does not exist, it returns an error
        if( !isset( neccsNal_Config::$tradeMaterialList[$scenario][$functionType] ) ){
            self::fatalError( neccsNal_Config::PARAMETER_ERROR, "This class can not be used. ({$scenario} : {$functionType})" );
        }

        // If not included in the available method name, it returns an error
        if( !in_array( $method, neccsNal_Config::$tradeMaterialList[$scenario][$functionType] ) ){
            self::fatalError( neccsNal_Config::PARAMETER_ERROR, "This class can not be used. ({$scenario} : {$functionType} : {$method})" );
        }

        $nalConf = self::getNalConfFile();

        // Run only if the VALI_DIR is defined
        // Run only when NAL
        if( defined('VALI_DIR') && $nalConf['api_type'] === neccsNal_Config::API_TYPE_NAL ) {

            // Validate check
            $valiModel = new neccsNal_validate();
            $error_message = $valiModel->_execValidate( $param, mb_strtolower( $method ) );

            // If an error message is returned, to output the returned error messages
            if( !empty( $error_message ) ){
                self::fatalError( neccsNal_Config::PARAMETER_ERROR, $error_message, $param );
            }
        }

        // If the class is present, to perform the processing
        if ( file_exists( $classPath ) === true ) {
            require_once $classPath;
            if ( class_exists( $functionType, false ) ) {
                $obj = new $functionType( $param );
            } else {
                self::fatalError( neccsNal_Config::API_INTERNAL_ERROR, "not found class: {$functionType}" );
            }

        // If the class does not exist, call Nal.php
        } else {
            $obj = new neccsNal( $param );
        }

        return $obj; // Return an instance
    }

    /**
     * Error processing (Fatal error)
     *
     * @param Error detail
     */
    public static function fatalError( $errCode='', $message='', $in='' ) {

        // Error message
        $errMsg = !empty( $message ) ? $message : neccsNal_Config::$errorCode[neccsNal_Config::STATUS_ERROR]['message'];

        // Request ID
        $requestId = self::_requestId();

        // Error level
        $errLevel = strtoupper( neccsNal_Config::LEV_ERROR );

        // Operation
        $operation = "undefine_operation";

        $arrTime = explode('.',microtime(true));
        // Log format
        $logInfo = array();
        $logInfo = array(
            '[' . $errLevel . ']',
            date('Y-m-d H:i:s', $arrTime[0]) . '.' .$arrTime[1],
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

        // Error details
        $res = array();
        $res = array(
            'result' => array(
                'status'     => neccsNal_Config::STATUS_ERROR,
                'error-code' => $errCode,
                'message'    => $errMsg,
            ),
            'request-id' => $requestId,
        );

        // If you are running the PHPUnit test, to return only message
        if( defined( 'PHPUNIT_RUN' ) ){
            throw new Exception( $res['result']['message'] );
        }
        header( "HTTP/1.1 200" );
        header( neccsNal_Config::CONTENT_TYPE_JSON );
        print json_encode( $res );
        exit(0);
    }

    /**
     * main
     *
     */
    public function run() {

        $method = $this->_httpMethod;

        try {
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
     * Get request parameters
     *
     * @return $param : Request parameters
     */
    protected function getRequestParam() {

        $param = '';

        // HTTP method
        $httpMethod = isset( $this ) ? $this->_httpMethod : strtoupper( $_SERVER['REQUEST_METHOD'] );

        // Request Parameters
        $param = ( $httpMethod !== neccsNal_Config::HTTP_GET ) ? json_decode( file_get_contents( 'php://input' ), true ) : $_GET;

        // If you are running the PHPUnit test, return value is obtained from $ POST or $ _GET
        if(defined('PHPUNIT_RUN')){
            $param =  ( $httpMethod !== neccsNal_Config::HTTP_GET ) ? $_POST : $_GET;
        }

        return $param;
    }

    /**
     * Load Settings file
     *
     * @param $nalConf : NAL config file
     */
    protected static function getNalConfFile() {

        $filePath = neccsNal_Config::NAL_CONF_PATH;

        // The file does not exist
        if( !file_exists( $filePath ) ) {
            $nalConf = neccsNal_Config::$nalConfDefault;
        }else{
            $nalConf = parse_ini_file( $filePath );

            // Contents of $nalConf is the case of the sky to get from the configuration file
            if( empty( $nalConf ) ) {
                $nalConf = neccsNal_Config::$nalConfDefault;
            }
        }

        return $nalConf;
    }

    /**
     * Creating a Request ID
     *
     * @return : Request ID
     */
    protected static function _requestId() {

        list( $micro, $unixtime ) = explode( " ", microtime() );
        $sec = $micro + date( "s", $unixtime );
        $sec = str_replace( '.', '', $sec );
        return date( "YmdHis", $unixtime ) . sprintf( "%09d", $sec );
    }

    /**
     * GET method (list,refer)
     *
     */
    protected function get() {

        // create a URL
        $url = $this->_setUrl();

        // run the API
        $result = $this->_execApi( $url );

        // return the result
        $this->success( $result );
    }

    /**
     * POST method (post)
     *
     */
    protected function post() {

        // create a file
        $this->makeNalFile();

        // Call the JobCenter or JobScheduler
        $this->execJob();

        // return the result
        $this->success();
    }

    /**
     * PUT method (put)
     *
     */
    protected function put() {

        // create a file
        $this->makeNalFile();

        // Call the JobCenter or JobScheduler
        $this->execJob();

        // return the result
        $this->success();
    }

    /**
     * DELETE method (delete)
     *
     */
    protected function delete() {

        // create a file
        $this->makeNalFile();

        // Call the JobCenter or JobScheduler
        $this->execJob();

        // return the result
        $this->success();
    }

    /**
     * return the result
     *
     * @param $data : Parameters
     */
    protected function success( $data = array() ) {

        $res = array();
        $errorInfo = neccsNal_Config::$errorCode[neccsNal_Config::STATUS_SUCCESS];
        $res = array(
            'result' => array(
                'status'     => neccsNal_Config::STATUS_SUCCESS,
                'error-code' => $errorInfo['code'],
                'message'    => $errorInfo['message'],
            ),
        );

        if( !empty( $data ) || $this->_httpMethod === neccsNal_Config::HTTP_GET ){
            $res['data'] = $data;
        }

        if( isset( $this->_jobId ) ) {
            $res['job-id'] = $this->_jobId;
        }

        if( isset( $this->_callApiType ) ) {
            $res['call-api-type'] = $this->_callApiType;
        }

        $this->_response( $res );
    }

    /**
     * Error processing
     *
     * @param $errCode : Error code
     * @param $message : Error message
     * @param $out     : OUT data
     */
    protected function error( $errCode='', $message, $out='' ) {

        // Error message
        $errMsg = !empty( $message ) ? $message : neccsNal_Config::$errorCode[neccsNal_Config::STATUS_ERROR]['message'];

        // Output Log
        $this->logit( $errCode, $errMsg,'', $out );

        $res = array();
        $res = array(
            'result' => array(
                'status'     => neccsNal_Config::STATUS_ERROR,
                'error-code' => !empty( $errCode ) ? $errCode : neccsNal_Config::$errorCode[neccsNal_Config::STATUS_ERROR]['code'],
                'message'    => $errMsg,
            )
        );
        $this->_response( $res );
    }

    /**
     * Create a response
     *
     * @param $res : Return value
     */
    protected function _response( $res ) {

        // In the case of the child process, the process is terminated without returning a response
        if( isset( $this ) && ( isset( $this->_childProcessFlg ) && $this->_childProcessFlg === '1' ) ) {
            // If during the PHPUnit test run, to return only message
            if( defined( 'PHPUNIT_RUN' ) ){
                throw new Exception( $res['result']['message'] );
            }
            exit(0);
        }

        $res['request-id'] = isset( $this ) ? $this->_requestId : self::_requestId();

        // If you are running the PHPUnit test, to return only message
        if( defined( 'PHPUNIT_RUN' ) ){
            throw new Exception( $res['result']['message'] );
        }

        // Return response
        header( "HTTP/1.1 200" );
        header( neccsNal_Config::CONTENT_TYPE_JSON );
        print json_encode( $res );
        exit(0);
    }

    /**
     * Output a log
     *
     * @param $errCode : Error code
     * @param $message : Log message
     * @param $out     : Input Parameters
     * @param $out     : Out Parameters
     */
    protected function logit( $errCode='', $message='', $in='', $out='' ) {

        // Error level
        $errLevel = strtoupper( neccsNal_Config::$errorLevelCode[$errCode] );

        // Operation
        $logFlg = '1';
        $operation = $this->makeOperation( $logFlg );
        if( empty( $operation ) ) $operation = "undefine_operation";

        if( empty( $in ) ) {
            $in = $this->_p;
        }

        $arrTime = explode('.',microtime(true));
        // Log format
        $logInfo = array();
        $logInfo = array(
            '[' . $errLevel . ']',
            date('Y-m-d H:i:s', $arrTime[0]) . '.' .$arrTime[1],
            '[' . $operation . ']',
            isset( $this ) ? $this->_requestId : self::_requestId(),
            '[CODE]' . $errCode,
            '[IN]' . ( $in !== '' ? json_encode( $in ) : $in ),
            '[OUT]' . ( $out !== '' ? json_encode( $out ) : $out ),
            '[MESSAGE]' . ( is_array( $message ) ? var_export( $message ) : $message ),
        );

        // Log file path
        $logFile = neccsNal_Config::LOG_DIR . neccsNal_Config::$logFileName[$errLevel];

        // Check of the directory
        $dir = dirname( $logFile );
        if( is_dir( $dir ) === false ) {
            @mkdir( $dir, 0755, true );
        }

        // File open
        $fp = @fopen( $logFile, "a" );
        if( $fp === false ) {
            $this->error( neccsNal_Config::API_INTERNAL_ERROR, "file was not opened. ({$logFile})" );
        }

        // Write the log
        if( flock( $fp, LOCK_EX ) ) {
            fputs( $fp, implode( '', $logInfo ) . "\r\n" );
            fflush( $fp );
            flock( $fp, LOCK_UN );
            fclose( $fp );
        }
    }

    /**
     * Make a file
     *
     */
    protected function makeNalFile() {

        // In the case of GET method, the file is not created
        if( $this->_httpMethod === neccsNal_Config::HTTP_GET ) { return; }

        //Oparation
        $operation = $this->makeOperation();

        // Request ID
        if( isset( $this->_p['request-id'] ) ) {
            $this->_requestId = $this->_p['request-id'];
        } else {
            $this->_p['request-id'] = $this->_requestId;
        }

        // Get device_type
        if( isset( $this->_p['device_type'] ) ) {
            $this->_deviceType = $this->_p['device_type'];
            // license
            if( $this->_p['function_type'] === neccsNal_Config::LICENSE ) {
                $this->_deviceType = $this->_p['type'] . $this->_p['device_type'];
            }

            // service
            if( $this->_p['function_type'] === neccsNal_Config::DCCONNECT
             || $this->_p['function_type'] === neccsNal_Config::BANDWIDTH
             || $this->_p['function_type'] === neccsNal_Config::SERVICE_SETTING
             || $this->_p['function_type'] === neccsNal_Config::SERVICEIPV6ADD ) {

                $service_type = '';
                if( isset( $this->_p['service_type'] ) ){
                    $service_type = $this->_p['service_type'];
                } else {
                    $service_type = $this->_p['group_type'];
                }
                $this->_deviceType = $this->_p['device_type']. $service_type;
            }
        } else {
            $this->error( neccsNal_Config::PARAMETER_ERROR, "device_type is not set." );
        }

        // Create a path to the directory
        $trans = array(
            '%ROOT_DIR%' => $this->_nalConf['root_inoutfile'],
            '%UUID%'     => $this->_requestId,
        );
        $this->fileDirPath = strtr( neccsNal_Config::DIR_PATH, $trans );

        // Create a directory
        if( !is_dir( $this->fileDirPath ) ) {
            if( !mkdir( $this->fileDirPath, 0755, true ) ) {
                $this->error( neccsNal_Config::API_INTERNAL_ERROR, "failed in making directory ({$this->fileDirPath})" );
            }
        }

        // Create a IN.json file
        $inFile  = $this->fileDirPath . '/' . neccsNal_Config::IN_FILE;
        if( !empty( $this->_p ) ) {
            foreach( $this->_p as $key => $val ) {
                // The case of an array
                if( is_array( $val ) ){
                    $this->_p[$key] = array();
                    foreach( $val as $key2 => $val2 ){
                        $this->_p[$key][$key2] = $val2;
                    }
                // The case of an string
                }else{
                    $this->_p[$key] = strval( $val );
                }
            }
        }
        $inJson  = json_encode( $this->_p );
        $winFile = @fopen( $inFile, 'w+' );
        if( $winFile === false ) { $this->error( neccsNal_Config::API_INTERNAL_ERROR, "file was not opened. ({$inFile})" ); }
        fwrite( $winFile, $inJson );
        fclose( $winFile );

        // Create a OUT.json file
        $outFile = $this->fileDirPath . '/' . neccsNal_Config::OUT_FILE;
        $woutFile = @fopen( $outFile, 'w+' );

        if( $woutFile === false ) { $this->error( neccsNal_Config::API_INTERNAL_ERROR, "file was not opened. ({$outFile})" ); }

        // If you are running the test, specify a dummy of information
        if( defined('PHPUNIT_RUN')) {
            fwrite( $woutFile, json_encode( array( 'data' => array("test" => "test2") ) ) );
        }

        fclose( $woutFile );

        // This parameter is the parameter JobCenter is available
        $this->jobCenterParam     = "'" . $this->fileDirPath . " " . neccsNal_Config::IN_FILE . " " . neccsNal_Config::OUT_FILE . " " . $this->_deviceType. "'";
        $this->jobCenterOperation = $operation;
    }

    /**
     * Create a operation
     *
     * @param  $logFlg    : 1:Call from the log output method
     * @return $operation : Operating information
     */
    protected function makeOperation( $logFlg='' ) {

        // Class name
        $className = isset( $this->_p['function_type'] ) ? $this->_p['function_type'] : '' ;

        // Function name
        $scenario      = isset( $this->_p['scenario'] ) ? $this->_p['scenario'] : '' ;

        $operation = '';
        switch( $this->_httpMethod ) {
            case neccsNal_Config::HTTP_GET :
                $operation = "get-" . $className . "-info";
                break;
            case neccsNal_Config::HTTP_POST :
                $operation = "create-" . $className;
                break;
            case neccsNal_Config::HTTP_PUT :
                if( $scenario === neccsNal_Config::NODE && $className === neccsNal_Config::LICENSE ) {
                    $operation = "auth-" . $className;
                } else if ( $scenario === neccsNal_Config::NODE && isset( neccsNal_Config::$putOperationList[$className] ) ){
                    $operation = neccsNal_Config::$putOperationList[$className];
                } else{
                    $operation = "update-" . $className;
                }
                break;
            case neccsNal_Config::HTTP_DELETE :
                $operation = "delete-" . $className;
                break;
        }

        if( empty( $operation )  ) {
            if( $logFlg === '1' ) {
                return;
            } else {
                $this->error( neccsNal_Config::API_INTERNAL_ERROR, "operation is unclear" );
            }
        }
        return $operation;
    }

    /**
     * Call JOB Center(post put delete)
     *
     */
    protected function callJobCenter() {

        // Get device_type
        if( isset( $this->_p['device_type'] ) ) {
            $this->_deviceType = $this->_p['device_type'];
            // license
            if( $this->_p['function_type'] === neccsNal_Config::LICENSE ) {
                $this->_deviceType = $this->_p['type'] . $this->_p['device_type'];
            }
        } else {
            $this->error( neccsNal_Config::PARAMETER_ERROR, "device_type is not set." );
        }

        // Call JOB Center
        $jcCmd = neccsNal_Config::CMD_JOB_CENTER;

        // Exec Job
        if( defined('PHPUNIT_RUN')) {
            // If you are running the PHPUnit test,Specify the return value from the parameter
            $out = isset( $this->_p['job_out']) ? $this->_p['job_out']  : '';
        } else {
            // Exec Job
            $out   = shell_exec( "$jcCmd -p $this->jobCenterParam $this->jobCenterOperation" );
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
     * Get Out.json data
     *
     */
    protected function _setOutParam() {

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

        // other than that
        }else{
            // Not made a reference
            return array();
        }

        $filePath .= '/'. neccsNal_Config::OUT_FILE;

        // The file does not exist
        if( !file_exists( $filePath ) ) { return array(); }

        $file = @fopen( $filePath, 'r' );
        if( $file === false ) { $this->error( neccsNal_Config::API_INTERNAL_ERROR, "file was not opened. ({$filePath})" ); }
        $tmp = fgets( $file );
        fclose( $file );

        // Get return value only
        $decodeTmp = json_decode( $tmp, true );
        if( isset( $decodeTmp['data'] ) ){
            $data = $decodeTmp['data'];
            return $data;
        }
        $this->error( neccsNal_Config::API_INTERNAL_ERROR, "file no contents. ({$filePath})" );

    }

    /**
     * Change tenant
     *
     * @return Tenant ID
     */
    protected function _getTenant( $tenant_id ) {

        $url    = neccsNal_Config::API_URL . neccsNal_Config::API_URL_LIST . neccsNal_Config::RESOURCE_TENANTS;
        $param  = '?IaaS_tenant_id=' . $tenant_id;
        $request_id = isset( $this->_p['request-id'] ) ? $this->_p['request-id'] : $this->_requestId;
        $param .= '&request-id=' . $request_id;
        $url   .= $param;
        $result = $this->_execApiHttpMethod( $url, '', '', neccsNal_Config::HTTP_GET );
        if( !empty( $result[0]['tenant_name'] ) ) {
            return $result[0]['tenant_name'];
        } else {
            return "";
        }
    }

    /**
     * Create a URL
     *
     * @return URL
     */
    protected function _setUrl() {

        // Get a URL
        $url = neccsNal_Config::API_URL . neccsNal_Config::API_URL_LIST;
        switch( $this->_httpMethod ) {
            case neccsNal_Config::HTTP_GET :
                // Add the name of the resource
                $url .= neccsNal_Config::$setReferResource[$this->_p['function_type']];
                break;
            default:
                // Add the name of the resource
                $url .= neccsNal_Config::$setReferResource[$this->_p['function_type']]. '/';
                break;
        }

        switch( $this->_httpMethod ) {
            case neccsNal_Config::HTTP_GET :
                $i = 0;
                $param = '';
                // Linking the parameter to the URL
                foreach( $this->_p as $key => $value ){
                    // Specify a value other than the following parameters
                    // function_type | scenario
                    if( $key !== 'function_type' && $key !== 'scenario' ){
                        if( $key === 'IaaS_tenant_id' ){
                            $value = $this->_getTenant( $value );
                            $key = 'tenant_name';

                            // If the tenant_name can not be acquired, return the sky
                            if( $value === '' ){
                                $this->success();
                            }
                        }
                        // Add the "&" to the top
                        if( $i !== 0 ){
                            $param .= '&'. $key. '='. $value;
                            // If the first, "&" is unnecessary
                        }else{
                            $param .= $key . '='. $value;
                        }
                        $i++;
                    }
                }
                // If there is a parameter, add the "?"
                if( $i > 0 ){
                    $url .= '?'. $param;
                }
                break;
            case neccsNal_Config::HTTP_POST :
                break;
            case neccsNal_Config::HTTP_PUT :
            case neccsNal_Config::HTTP_DELETE :
                // Get a unique key
                if( isset( $this->_p['id'] ) && $this->_p['id'] !== '' ){
                    // Bind to the URL
                    $url .= $this->_p['id'];
                }
                break;
        }

        return $url;
    }

    /**
     * Exec API
     *
     * @param URL
     * @param Parameters
     * @param No Proxy flg
     *
     * @return Result of decoding
     */
    protected function _execApi( $url, $param='', $noproxy='' ) {

        // Encode
        if( is_array( $param ) ) $param = http_build_query( $param );

        // Initialization of cURL
        $ch = curl_init( $url );

        // Set of HTTP header
        curl_setopt( $ch, CURLOPT_HTTPHEADER, array( neccsNal_Config::CONTENT_TYPE_URLENCODE ) );

        // Setting of No Proxy
        if( $noproxy ){
            curl_setopt($ch, CURLOPT_PROXY, '');
        }

        // In the case of calls to the WIM API, the BASIC authentication
        if( $this->_nalConf['api_type'] === neccsNal_Config::API_TYPE_NAL ) {
            curl_setopt( $ch, CURLOPT_USERPWD, neccsNal_Config::BASIC_AUTH_ID . ":" . neccsNal_Config::BASIC_AUTH_PW );
        }

        if( $this->_httpMethod === neccsNal_Config::HTTP_GET ) {

            curl_setopt($ch, CURLOPT_HTTPGET, true);
            curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, FALSE);
            curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
            curl_setopt($ch, CURLINFO_HEADER_OUT, true);

        } else if( $this->_httpMethod === neccsNal_Config::HTTP_POST ) {

            curl_setopt($ch, CURLOPT_POST, true);
            curl_setopt($ch, CURLOPT_POSTFIELDS, $param);
            curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, FALSE);
            curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
            curl_setopt($ch, CURLINFO_HEADER_OUT, true);

        } else if( $this->_httpMethod === neccsNal_Config::HTTP_PUT ) {

            curl_setopt($ch, CURLOPT_CUSTOMREQUEST, neccsNal_Config::HTTP_PUT);
            curl_setopt($ch, CURLOPT_FAILONERROR, false);
            curl_setopt($ch, CURLOPT_POSTFIELDS, $param);
            curl_setopt($ch, CURLOPT_POST, true);
            curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, FALSE);
            curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
            curl_setopt($ch, CURLINFO_HEADER_OUT, true);

        } else if( $this->_httpMethod === neccsNal_Config::HTTP_DELETE ) {

            curl_setopt($ch, CURLOPT_CUSTOMREQUEST, neccsNal_Config::HTTP_DELETE);
            curl_setopt($ch, CURLOPT_FAILONERROR, false);
            curl_setopt($ch, CURLOPT_POST, true);
            curl_setopt($ch, CURLOPT_POSTFIELDS, $param);
            curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, FALSE);
            curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
            curl_setopt($ch, CURLINFO_HEADER_OUT, true);
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
            $result = $this->_getIaaSTenantId( $result, $this->_httpMethod );

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
     * Exec API
     *
     * @param URL
     * @param Parameters
     * @param No Proxy flg
     *
     * @return Result of decoding
     */
    protected function _execMultiApi( $url_list, $param=array(), $noproxy='' ) {

        $mh = curl_multi_init();

        $ch = array();
        foreach( $url_list as $key => $url ){

            // Encode
            if( isset( $param[$key] ) && is_array( $param[$key] ) ) $param = http_build_query( $param[$key] );

            // Initialization of cURL
            $ch[$key] = curl_init( $url );

            // Set of HTTP header
            curl_setopt( $ch[$key], CURLOPT_HTTPHEADER, array( neccsNal_Config::CONTENT_TYPE_JSON ) );

            // Setting of No Proxy
            if( $noproxy ){
                curl_setopt($ch[$key], CURLOPT_PROXY, '');
            }

            // In the case of calls to the WIM API, the BASIC authentication
            if( $this->_nalConf['api_type'] === neccsNal_Config::API_TYPE_NAL ) {
                curl_setopt( $ch[$key], CURLOPT_USERPWD, neccsNal_Config::BASIC_AUTH_ID . ":" . neccsNal_Config::BASIC_AUTH_PW );
            }

            if( $this->_httpMethod === neccsNal_Config::HTTP_GET ) {

                curl_setopt($ch[$key], CURLOPT_HTTPGET, true);
                curl_setopt($ch[$key], CURLOPT_SSL_VERIFYPEER, FALSE);
                curl_setopt($ch[$key], CURLOPT_RETURNTRANSFER, true);
                curl_setopt($ch[$key], CURLINFO_HEADER_OUT, true);

            } else if( $this->_httpMethod === neccsNal_Config::HTTP_POST ) {

                curl_setopt($ch[$key], CURLOPT_POST, true);
                curl_setopt($ch[$key], CURLOPT_POSTFIELDS, $param);
                curl_setopt($ch[$key], CURLOPT_SSL_VERIFYPEER, FALSE);
                curl_setopt($ch[$key], CURLOPT_RETURNTRANSFER, true);
                curl_setopt($ch[$key], CURLINFO_HEADER_OUT, true);

            } else if( $this->_httpMethod === neccsNal_Config::HTTP_PUT ) {

                curl_setopt($ch[$key], CURLOPT_CUSTOMREQUEST, neccsNal_Config::HTTP_PUT);
                curl_setopt($ch[$key], CURLOPT_FAILONERROR, false);
                curl_setopt($ch[$key], CURLOPT_POSTFIELDS, $param);
                curl_setopt($ch[$key], CURLOPT_POST, true);
                curl_setopt($ch[$key], CURLOPT_SSL_VERIFYPEER, FALSE);
                curl_setopt($ch[$key], CURLOPT_RETURNTRANSFER, true);
                curl_setopt($ch[$key], CURLINFO_HEADER_OUT, true);

            } else if( $this->_httpMethod === neccsNal_Config::HTTP_DELETE ) {

                curl_setopt($ch[$key], CURLOPT_CUSTOMREQUEST, neccsNal_Config::HTTP_DELETE);
                curl_setopt($ch[$key], CURLOPT_FAILONERROR, false);
                curl_setopt($ch[$key], CURLOPT_POST, true);
                curl_setopt($ch[$key], CURLOPT_POSTFIELDS, $param);
                curl_setopt($ch[$key], CURLOPT_SSL_VERIFYPEER, FALSE);
                curl_setopt($ch[$key], CURLOPT_RETURNTRANSFER, true);
                curl_setopt($ch[$key], CURLINFO_HEADER_OUT, true);
            }
            curl_setopt( $ch[$key], CURLOPT_TIMEOUT, neccsNal_Config::CURL_TIMEOUT );
            curl_multi_add_handle($mh, $ch[$key]);

        }

        $isActive = null;
        while ( CURLM_CALL_MULTI_PERFORM == ($execReturn = curl_multi_exec( $mh, $isActive )) ) {
        }

        while ( $isActive && $execReturn == CURLM_OK ) {
            if ( curl_multi_select( $mh ) != -1 ) {
                while ( CURLM_CALL_MULTI_PERFORM == ($execReturn = curl_multi_exec( $mh, $isActive )) ) {
                }
            }
        }

        if ( $execReturn != CURLM_OK ) {
            return false;
        }

        $execList = array();
        // Execute all URLs in the array
        foreach( $url_list as $key => $url ) {
            // Acquire the last HTTP status information received
            $http_status = curl_getinfo( $ch[$key], CURLINFO_HTTP_CODE );
            $execList[$key]['status'] = $http_status;

            if( in_array( $http_status, neccsNal_Config::$successHttpStatus ) ) {
                $execList[$key]['contents'] = curl_multi_getcontent( $ch[$key] );
            } else if ( in_array( $http_status, neccsNal_Config::$notFoundHttpStatus ) ){
                $execList[$key]['contents'] = array();
            } else {
                $execList[$key]['contents'] = curl_multi_getcontent( $ch[$key] );
            }

            curl_multi_remove_handle( $mh, $ch[$key] );
            curl_close( $ch[$key] );
        }
        curl_multi_close( $mh );

        $results = array();
        foreach( $execList as $key => $exec ){

            // If there is data(HTTP Statsu : 200,201,204)
            if( in_array( $exec['status'], neccsNal_Config::$successHttpStatus ) ) {

                // Output log
                $this->logit( neccsNal_Config::SUCCESS_CODE, "API success ($url_list[$key])", $param, $exec['contents'] );

                // If the "tenant_name" exists in the output, to add to output the results to obtain the tenant ID
                $results[$key] = $this->_getMultiIaaSTenantId( $exec['contents'], $this->_httpMethod );

            // If there is no data(HTTP Status : 500)
            } else if( in_array( $exec['status'], neccsNal_Config::$notFoundHttpStatus ) ){
                // Output log
                $this->logit( neccsNal_Config::SUCCESS_CODE, "data not exists. ($url_list[$key])", $param, $exec['contents'] );
                // Return an empty array
                $results[$key] = $exec['contents'];
            } else {
                $this->error( neccsNal_Config::REST_API_ERROR, "API error ($url_list[$key])", $exec['contents'] );
            }

        }

        return $results;

    }

    /**
     * Brute string to "tenant_name", acquires "IaaS_tenant_id"
     *
     * @param result
     * @return As a result of adding the "IaaS_tenant_id"
     */
    protected function _getIaaSTenantId( $result, $httpMethod ){

        $result = json_decode( $result, true );

        if( $httpMethod === neccsNal_Config::HTTP_POST
         || $httpMethod === neccsNal_Config::HTTP_PUT
         || $httpMethod === neccsNal_Config::HTTP_DELETE ){
            return $result;
        }

        // If the return value of Wim API, does not perform processing
        if( isset( $result['result'] ) ){
            return $result;
        }

        if( !isset( $result[0]['tenant_name'] ) ){
            return $result;
        }

        if( isset( $result[0]['IaaS_tenant_id'] ) ){
            return $result;
        }

        $url = neccsNal_Config::API_URL . neccsNal_Config::API_URL_LIST . neccsNal_Config::RESOURCE_TENANTS;
        $request_id = isset( $this->_p['request-id'] ) ? $this->_p['request-id'] : $this->_requestId;
        $url .= '?request-id='. $request_id;

        // Initialization of cURL
        $ch = curl_init( $url );

        // Set of HTTP header
        curl_setopt( $ch, CURLOPT_HTTPHEADER, array( neccsNal_Config::CONTENT_TYPE_JSON ) );

        // In the case of calls to the WIM API, the BASIC authentication
        if( $this->_nalConf['api_type'] === neccsNal_Config::API_TYPE_NAL ) {
            curl_setopt( $ch, CURLOPT_USERPWD, neccsNal_Config::BASIC_AUTH_ID . ":" . neccsNal_Config::BASIC_AUTH_PW );
        }

        curl_setopt($ch, CURLOPT_HTTPGET, true);
        curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, FALSE);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLINFO_HEADER_OUT, true);
        curl_setopt( $ch, CURLOPT_TIMEOUT, neccsNal_Config::CURL_TIMEOUT );

        $tenantList = curl_exec( $ch );

        $info = curl_getinfo($ch);
        $http_status = $info['http_code'];

        curl_close( $ch );

        // Output log
        $this->logit( neccsNal_Config::SUCCESS_CODE, "API success ($url)", array( 'request_id' => $request_id ), $tenantList );

        $tenantList = json_decode( $tenantList, true );

        if( empty( $tenantList ) ){

            return $result;
        }

        // ( array( tenant_id => tenant_name ) )
        $tenantNameList = array();
        foreach( $tenantList as $tenantInfo){
            $tenantNameList[$tenantInfo['IaaS_tenant_id']] = $tenantInfo['tenant_name'];
        }
        foreach( $result as $key => $value ){
            // If the "tenant_name" exists
            if( !isset( $value['tenant_name'] ) ){
                $result[$key]['IaaS_tenant_id'] = '';
            // If the "tenant_name" does not exist
            }else{
                $tenant_name = $value['tenant_name'];
                // If there is the same "tenant_name" to the tenant list, specified string brute tenant ID
                if( array_search( $tenant_name, $tenantNameList ) ){
                    $num = array_search( $tenant_name, $tenantNameList );
                    $result[$key]['IaaS_tenant_id'] = $num;
                }else{
                    $result[$key]['IaaS_tenant_id'] = '';
                }
            }
        }

        return $result;

    }

    /**
     * Brute string to "tenant_name", acquires "IaaS_tenant_id"
     *
     * @param result
     * @return As a result of adding the "IaaS_tenant_id"
     */
    protected function _getMultiIaaSTenantId( $result, $httpMethod ){

        $result = json_decode( $result, true );

        if( $httpMethod === neccsNal_Config::HTTP_POST
        || $httpMethod === neccsNal_Config::HTTP_PUT
        || $httpMethod === neccsNal_Config::HTTP_DELETE ){
            return $result;
        }

        // If the return value of Wim API, does not perform processing
        if( isset( $result['result'] ) ){
            return $result;
        }

        if( !isset( $result[0]['tenant_name'] ) ){
            return $result;
        }

        if( isset( $result[0]['IaaS_tenant_id'] ) ){
            return $result;
        }

        if( empty( $this->_tenantList ) ){

            $url = neccsNal_Config::API_URL . neccsNal_Config::API_URL_LIST . neccsNal_Config::RESOURCE_TENANTS;
            $request_id = isset( $this->_p['request-id'] ) ? $this->_p['request-id'] : $this->_requestId;
            $url .= '?request-id='. $request_id;

            // Initialization of cURL
            $ch = curl_init( $url );

            // Set of HTTP header
            curl_setopt( $ch, CURLOPT_HTTPHEADER, array( neccsNal_Config::CONTENT_TYPE_JSON ) );

            // In the case of calls to the WIM API, the BASIC authentication
            if( $this->_nalConf['api_type'] === neccsNal_Config::API_TYPE_NAL ) {
                curl_setopt( $ch, CURLOPT_USERPWD, neccsNal_Config::BASIC_AUTH_ID . ":" . neccsNal_Config::BASIC_AUTH_PW );
            }

            curl_setopt($ch, CURLOPT_HTTPGET, true);
            curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, FALSE);
            curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
            curl_setopt($ch, CURLINFO_HEADER_OUT, true);
            curl_setopt( $ch, CURLOPT_TIMEOUT, neccsNal_Config::CURL_TIMEOUT );

            $tenantList = curl_exec( $ch );

            $info = curl_getinfo($ch);
            $http_status = $info['http_code'];

            curl_close( $ch );

            // Output log
            $this->logit( neccsNal_Config::SUCCESS_CODE, "API success ($url)", array( 'request_id' => $request_id ), $tenantList );

            $this->_tenantList = json_decode( $tenantList, true );

            if( empty( $tenantList ) ){

                return $result;
            }

        }

        // ( array( tenant_id => tenant_name ) )
        $tenantNameList = array();
        foreach( $this->_tenantList as $tenantInfo){
            $tenantNameList[$tenantInfo['IaaS_tenant_id']] = $tenantInfo['tenant_name'];
        }
        foreach( $result as $key => $value ){
            // If the "tenant_name" exists
            $tenant_name = $value['tenant_name'];
            // If there is the same "tenant_name" to the tenant list, specified string brute tenant ID
            if( array_search( $tenant_name, $tenantNameList ) ){
                $num = array_search( $tenant_name, $tenantNameList );
                $result[$key]['IaaS_tenant_id'] = $num;
            }else{
                $result[$key]['IaaS_tenant_id'] = '';
            }
        }

        return $result;

    }

    /**
     * Exec API
     *
     * @param URL
     * @param Parameters
     * @param No Proxy flg
     * @param HTTP method
     *
     * @return Result of decoding
     */
    protected function _execApiHttpMethod( $url, $param='', $noproxy='', $httpMethod='' ) {

        // HTTP method
        if( empty( $httpMethod ) ) $httpMethod = $this->_httpMethod;

        // Encode
        if( is_array( $param ) ) $param = http_build_query( $param );

        // Initialization of cURL
        $ch = curl_init( $url );

        //Set of HTTP header
        curl_setopt( $ch, CURLOPT_HTTPHEADER, array( neccsNal_Config::CONTENT_TYPE_URLENCODE ) );

        // Setting of No Proxy
        if( $noproxy ){
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

            curl_setopt($ch, CURLOPT_POST, true);
            curl_setopt($ch, CURLOPT_POSTFIELDS, $param);
            curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, FALSE);
            curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
            curl_setopt($ch, CURLINFO_HEADER_OUT, true);

        } else if( $httpMethod === neccsNal_Config::HTTP_PUT ) {

            curl_setopt($ch, CURLOPT_CUSTOMREQUEST, neccsNal_Config::HTTP_PUT);
            curl_setopt($ch, CURLOPT_FAILONERROR, false);
            curl_setopt($ch, CURLOPT_POSTFIELDS, $param);
            curl_setopt($ch, CURLOPT_POST, true);
            curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, FALSE);
            curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
            curl_setopt($ch, CURLINFO_HEADER_OUT, true);

        } else if( $httpMethod === neccsNal_Config::HTTP_DELETE ) {

            curl_setopt($ch, CURLOPT_CUSTOMREQUEST, neccsNal_Config::HTTP_DELETE);
            curl_setopt($ch, CURLOPT_FAILONERROR, false);
            curl_setopt($ch, CURLOPT_POST, true);
            curl_setopt($ch, CURLOPT_POSTFIELDS, $param);
            curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, FALSE);
            curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
            curl_setopt($ch, CURLINFO_HEADER_OUT, true);
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
     * Call JOB Scheduler(post put delete)
     *
     */
    protected function callJobScheduler() {
        // Call JOB Scheduler
        $file = $this->makeParamterFile(neccsNal_Config::JOB_EXEC_MODE);
        $jcCmd = neccsNal_Config::CMD_JOB_SCHEDULER;
        $jcCmd = strtr($jcCmd,array('%FILE%' => $file ));

        // Exec Job
        if( !defined( 'PHPUNIT_RUN' ) ){
            // Exec Job
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
     * Create a parameter file for Job Scheduler
     * @param $type  1:registration,2:Status check
     * @return xmlfile path
     */
    protected function makeParamterFile( $type ) {

        // Create a path to the directory
        $trans = array(
                        '%ROOT_DIR%' => $this->_nalConf['root_inoutfile'],
                        '%UUID%'         => $this->_requestId,
        );
        $this->fileDirPath = strtr( neccsNal_Config::DIR_PATH, $trans );

        // In the case of registration
        if( $type === neccsNal_Config::JOB_EXEC_MODE ) {

            // Get device_type
            if( isset( $this->_p['device_type'] ) ) {
                $this->_deviceType = $this->_p['device_type'];
                // license
                if( $this->_p['function_type'] === neccsNal_Config::LICENSE ) {
                    $this->_deviceType = $this->_p['type'] . $this->_p['device_type'];
                }
                // service
                if( $this->_p['function_type'] === neccsNal_Config::DCCONNECT
                || $this->_p['function_type'] === neccsNal_Config::BANDWIDTH
                || $this->_p['function_type'] === neccsNal_Config::SERVICE_SETTING
                || $this->_p['function_type'] === neccsNal_Config::SERVICEIPV6ADD ) {

                    $service_type = '';
                    if( isset( $this->_p['service_type'] ) ){
                        $service_type = $this->_p['service_type'];
                    } else {
                        $service_type = $this->_p['group_type'];
                    }
                    $this->_deviceType = $this->_p['device_type']. $service_type;
                }
            } else {
                $this->error( neccsNal_Config::PARAMETER_ERROR, "device_type is not set." );
            }

            $body = neccsNal_Config::FORMAT_JOB_SCHEDULER_IN_BODY;
            $paramlist = '';
            $inParam = array(
                'ROOT_DIR'    => $this->fileDirPath,
                'INPUT_FILE'  => neccsNal_Config::IN_FILE,
                'OUTPUT_FILE' => neccsNal_Config::OUT_FILE,
                'DEVICE_TYPE' => $this->_deviceType
            );
            foreach( $inParam as $key => $value ) {
                $paramlist .= strtr($body , array( '%KEY%' => $key, '%VALUE%' => $value ) );
            }
            // If you call in the WIN server, convert the JOB ID
            if( $this->_nalConf['api_type'] === neccsNal_Config::API_TYPE_WIM ){
                if( $this->_p['function_type'] === neccsNal_Config::DCCONNECT ){
                    $this->jobCenterOperation = str_replace( 'dcconnect', 'wimdcconnect', $this->jobCenterOperation );
                } else if ( $this->_p['function_type'] === neccsNal_Config::BANDWIDTH ){
                    $this->jobCenterOperation = str_replace( 'bandwidth', 'wimbandwidth', $this->jobCenterOperation );
                } else if ( $this->_p['function_type'] === neccsNal_Config::SERVICE_SETTING ){
                    $this->jobCenterOperation = str_replace( 'serviceSetting', 'wimserviceSetting', $this->jobCenterOperation );
                } else {
                    $this->jobCenterOperation = str_replace( 'serviceIPv6Add', 'wimserviceIPv6Add', $this->jobCenterOperation );
                }
            }

            $xml = neccsNal_Config::FORMAT_JOB_SCHEDULER_IN;
            $xml = strtr($xml, array('%PARAMLIST%' => $paramlist, '%JOBNAME%' => $this->jobCenterOperation, '%SCENARIO%' => $this->_p['scenario'] ));

        // In the case of Status check
        } elseif( $type === neccsNal_Config::JOB_CHECK_MODE ) {
            $xml = neccsNal_Config::FORMAT_JOB_SCHEDULER_IN_STATUS;
            $xml = strtr($xml, array('%JOBID%' => $this->_jobId, '%JOBNAME%' => $this->jobCenterOperation, '%SCENARIO%' => $this->_p['scenario'] ));
        }

        if( isset( $this->_p['request-id'] ) ) {
            $this->_requestId = $this->_p['request-id'];
        }

        //  Create a directory
        if( !is_dir( $this->fileDirPath ) ) {
            if( !mkdir( $this->fileDirPath, 0755, true ) ) {
               $this->error( neccsNal_Config::API_INTERNAL_ERROR, "failed in making directory ({$this->fileDirPath})" );
            }
        }

        // Create a in.xml file
        $inFile = $this->fileDirPath . '/' . neccsNal_Config::IN_XMLFILE;
        $fd = @fopen( $inFile, 'w+' );
        fwrite( $fd, $xml );
        if( $fd === false ) { $this->error( neccsNal_Config::API_INTERNAL_ERROR, "file was not opened. ({$inFile})" ); }
        fclose( $fd );
        return $inFile;
    }

    /**
     * Call JobCenter or JobScheduler
     *
     */
    protected function execJob() {
        $job_type = $this->_nalConf['job_type'];
        if( $job_type === neccsNal_Config::JOB_SCHEDULER ){
            $this->callJobScheduler();
        }else{
            $this->callJobCenter();
        }
    }

    /**
     * Call JobCenter or JobScheduler (check)
     *
     * @param The number of retries
     * @param Maximum number of retries
     */
    protected function execCheckJob( $retry, $max ) {
        $job_type = $this->_nalConf['job_type'];
        if( $job_type === neccsNal_Config::JOB_SCHEDULER ){
            $this->checkJobScheduler( $retry, $max );
        }else{
            $this->checkJobCenter( $retry, $max );
        }
    }

    /**
     * Call child process
     *
     */
    protected function childProcessExec(){

        // Create a parameter file for Child process
        $this->makeChildProcessParam();

        // Get the path to the directory where you want to store the file
        $inoutFilePass = $this->_nalConf['root_inoutfile'];

        // Exec command (Asynchronous execution)
        if ( PHP_OS == "WIN32" || PHP_OS == "WINNT" ) {
            // Windows
            $fp= popen( 'start /B cmd /c "php ' . dirname(__FILE__). '/../bin/batch.php -f'. $inoutFilePass .'/'. $this->_requestId. '/ChildProcess"', 'r' );
            pclose($fp);
        } else {
            $execCmd = "php ". dirname(__FILE__). "/../bin/batch.php -f=". $inoutFilePass. "/". $this->_requestId. "/ChildProcess";
            $execCmd .= " > /dev/null &";
            exec( $execCmd );
        }
    }

    /**
     * Create a parameter file for Child process
     *
     */
    protected function makeChildProcessParam(){

        // Create a parameter file for Child process(file)
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

        // Get $this->_p
        $data = $this->_p;
        $data['request_method'] = $this->_httpMethod;
        $data['nal_conf']       = $this->_nalConf;
        $data['job_operation']  = $this->jobCenterOperation;
        $data['scenario']       = $this->_p['scenario'];

        // Serialize the sequence data that was created
        $serializeData = serialize($data);

        // Create a file for the Child Process
        $processFile  = $filePath . '/' . neccsNal_Config::CHILD_PROCESS_FILE;
        $wprocessFile = @fopen( $processFile, 'w+' );
        if( $wprocessFile === false ) {
            $this->error( neccsNal_Config::API_INTERNAL_ERROR, "file was not opened. ({$processFile})" );
        }
        fwrite( $wprocessFile, $serializeData );
        fclose( $wprocessFile );
    }

    /**
     * Create a URL
     * (when referring to the information of the node)
     *
     * @return $url URL list
     */
    protected function _setUrlCustom(){

        $url  = '';
        $urlList = array();

        if( $this->_httpMethod === neccsNal_Config::HTTP_GET ){
            $function_type = $this->_p['function_type'];
            $resourceList = neccsNal_Config::$setReferResourceCustom[$function_type];
        }

        $urlList = array();
        foreach( $resourceList as $keyInfo => $resource ){

            // Get a URL
            $url = neccsNal_Config::API_URL;
            $url .= neccsNal_Config::API_URL_LIST;

            // Add the name of the resource
            $url .= $resource;

            // If the parameter of api_type exists, it resets the value
            if( array_key_exists( 'apl_type', $this->_p ) ){
                unset( $this->_p['apl_type'] );
            }

            // In the case of virtual
            if( $keyInfo === 'vnf_info' ){
                $this->_p['apl_type'] = neccsNal_Config::APL_TYPE_VIRTUAL;
            // In the case of physical
            }else if( $keyInfo === 'pnf_info' ){
                $this->_p['apl_type'] = neccsNal_Config::APL_TYPE_PHYSICS;
            }

            $i = 0;
            $param = '';
           // Linking the parameter to the URL
            foreach( $this->_p as $key => $value ){
                // Specify a value other than the following parameters
                // function_type | scenario
                if( $key !== 'function_type' && $key !== 'scenario' ){
                    // If the acquired key a "IaaS_tenant_id"
                    if( $key === 'IaaS_tenant_id' ){
                        // Converted into information of brute string "tenant_name"
                        $value = $this->_getTenant( $value );
                        $key = 'tenant_name';

                        // If the tenant_name can not be acquired, return the sky
                        if( $value === '' ){
                            $this->success();
                        }
                    }
                    // Add the "&" to the top
                    if( $i !== 0 ){
                        $param .= '&'. $key. '='. $value;
                    // If the first, "&" is unnecessary
                    }else{
                        $param .= $key . '='. $value;
                    }
                    $i++;
                }
            }

            // If there is a parameter, add the "?"
            if( $i > 0 ){
                $url .= '?'. $param;
            }

            $urlList[$keyInfo] = $url;
        }

        return $urlList;

    }

    /**
     * Refer to the usage of OpenStack
     * (There is no specification of the tenant)
     *
     * @param  $tenant_name : tenant_name
     * @param  $endpoint    : Endpoint information
     * @return $resul       : result
     */
    protected function listUsageReport( $tenant_name, $endpoint ){

        $token_id = '';
        $result = array();

        // Refer usage
        $usageReport = new UsageReports();
        list( $endPointArray, $token_id ) = $usageReport->getEndpoints($tenant_name, null, $endpoint);
        try {

            $result = $usageReport->listUsageReport($endPointArray, $token_id, $this->_p['IaaS_region_id']);

            $this->logit( neccsNal_Config::SUCCESS_CODE, "OpenStack API : listUsageReport", $tenant_name, $result );

        } catch (Exception $e) {
            $this->error( neccsNal_Config::OPENSTACK_API_ERROR, "error:" . $e->getMessage(). $e->getTraceAsString() );
        }

        return $result;
    }

    /**
     * Refer to the usage of OpenStack
     * (There is no specification of the tenant)
     *
     * @param  $tenant_name : tenant_name
     * @param  $endpoint    : Endpoint information
     * @return $resul       : result
     */
    protected function listFlavorsDetail( $tenant_name, $endpoint ){

        $token_id = '';
        $result = array();

        // Refer usage
        $flavors = new OscFlavors();
        list( $endPointArray, $token_id ) = $flavors->getEndpoints($tenant_name, null, $endpoint);
        try {
            $result = $flavors->listFlavorsDetail($endPointArray, $token_id, $this->_p['IaaS_region_id']);

            $this->logit( neccsNal_Config::SUCCESS_CODE, "OpenStack API : listFlavorsDetail", $tenant_name, $result );

        } catch (Exception $e) {
            $this->error( neccsNal_Config::OPENSTACK_API_ERROR, "error:" . $e->getMessage(). $e->getTraceAsString() );
        }

        return $result;

    }

    /**
     * Refer to the usage of OpenStack
     * (There is no specification of the tenant)
     *
     * @param  $tenant_name : tenant_name
     * @param  $endpoint    : Endpoint information
     * @return $resul       : result
     */
    protected function listHostDetail( $tenant_name, $endpoint ){

        $token_id = '';
        $result = array();

        // Refer usage
        $hosts = new OsHosts();
        list( $endPointArray, $token_id ) = $hosts->getEndpoints($tenant_name, null, $endpoint);
        try {
            $hostList = $hosts->listHost($endPointArray, $token_id, $this->_p['IaaS_region_id']);

            $this->logit( neccsNal_Config::SUCCESS_CODE, "OpenStack API : listHost", $tenant_name, $hostList );

        } catch (Exception $e) {
            $this->error( neccsNal_Config::OPENSTACK_API_ERROR, "error:" . $e->getMessage(). $e->getTraceAsString() );
        }

        if( empty( $hostList['hosts'] ) ){
            return array();
        }

        list( $endPointArray, $token_id ) = $hosts->getEndpoints($tenant_name, null, $endpoint);
        foreach( $hostList['hosts'] as $host ){

            if( $host['service'] === 'compute' ){
                try {
                    $hostInfo = $hosts->showHostDetail($endPointArray, $host['host_name'], $token_id, $this->_p['IaaS_region_id']);

                    $this->logit( neccsNal_Config::SUCCESS_CODE, "OpenStack API : showHostDetail", $tenant_name, $hostInfo );

                } catch (Exception $e) {
                    $this->error( neccsNal_Config::OPENSTACK_API_ERROR, "error:" . $e->getMessage(). $e->getTraceAsString() );
                }

                if( empty( $hostInfo['host'] ) ){
                    continue;
                }

                foreach( $hostInfo['host'] as $info ){
                    if( $info['resource']['project'] === '(total)' ){
                        $result[] = $info['resource'];
                    }
                }
            }


        }

        return $result;

    }

    /**
     * Get the Endpoint information brute string to tenant
     *
     * @return $result : Endpoint
     */
    protected function getEndpointTenant(){

        // Get a pod_id
        // Get a URL
        $url = neccsNal_Config::API_URL . neccsNal_Config::API_URL_LIST;
        $url .= neccsNal_Config::RESOURCE_APLS. '/';
        $url .= '?tenant_name='. $this->_p['tenant_name'];
        $url .= '&apl_type=1';
        $url .= '&request-id'. $this->_p['request-id'];

        // Get the APL information
        $aplInfo = $this->_execApi( $url );

        // If the APL information is not empty, to get the "pod_id" from the acquired information
        if(!empty( $aplInfo )){
            $pod_id = $aplInfo[0]['pod_id'];
        // If the API information is empty, it returns an empty array
        } else {
            return array();
        }

        // Get the Endpoint information
        // Get a URL
        $url = neccsNal_Config::API_URL . neccsNal_Config::API_URL_LIST;
        $url .= neccsNal_Config::RESOURCE_ENDPOINS. '/';
        $url .= '?type=1';
        $url .= '&pod_id='. $pod_id;
        $url .= '&request-id='. $this->_p['request-id'];

        $result = $this->_execApi( $url );
        $endpoint = json_decode( $result[0]['endpoint_info'], true );

        return $endpoint;

    }

    /**
     * Get the Endpoint information
     *
     * @return $result : Endpoint information
     */
    protected function getEndpoint( $inParam = array() ){
        // Get the Endpoint information
        // Get a URL
        $url = neccsNal_Config::API_URL . neccsNal_Config::API_URL_LIST;

        if( $this->_nalConf['api_type'] === neccsNal_Config::API_TYPE_NAL ){
            $url .= neccsNal_Config::RESOURCE_ENDPOINS. '/';
        }else if( $this->_nalConf['api_type'] === neccsNal_Config::API_TYPE_WIM ){
            $url .= neccsNal_Config::RESOURCE_ENDPOINS_WIM. '/';
        }
        $url .= '?request-id='. $this->_p['request-id'];
        $url .= '&delete_flg=0';

        // Linking the parameter to the URL
        foreach( $inParam as $key => $value ){
            // Specify a value other than the following parameters
            // Add the "&" to the top
            $param = '';
            $param .= $key . '='. $value;
            // If there is a parameter, add the "?"
            $url .= '&'. $param;
        }

        $result = $this->_execApi( $url );

        return $result;

    }

    /**
     * Get the Config information
     *
     * @return $result : Config information
     */
    protected function getConfig( $inParam = array() ){
        // Get the Endpoint information
        // Get a URL
        $url = neccsNal_Config::API_URL . neccsNal_Config::API_URL_LIST;

        if( isset( $inParam['no_wim_flg'] ) && $inParam['no_wim_flg'] === '1' ){
            $url .= neccsNal_Config::RESOURCE_CONFIG. '/';
        }else if( $this->_nalConf['api_type'] === neccsNal_Config::API_TYPE_NAL ){
            $url .= neccsNal_Config::RESOURCE_CONFIG. '/';
        } else {
            $url .= neccsNal_Config::RESOURCE_CONFIG_WIM. '/';
        }
        $url .= '?request-id='. $this->_p['request-id'];
        $url .= '&delete_flg=0';

        // Linking the parameter to the URL
        foreach( $inParam as $key => $value ){
            // Specify a value other than the following parameters
            // Add the "&" to the top
            $param = '';
            $param .= $key . '='. $value;
            // If there is a parameter, add the "?"
            $url .= '&'. $param;
        }

        $result = $this->_execApi( $url );

        return $result;

    }

    /**
     * Get the Config information
     *
     * @return $result : Config information
     */
    protected function getTenantContract( $inParam = array() ){
        // Get the Endpoint information
        // Get a URL
        $url = neccsNal_Config::API_URL . neccsNal_Config::API_URL_LIST;
        $url .= neccsNal_Config::RESOURCE_CONTRACT. '/';
        $url .= '?request-id='. $this->_p['request-id'];
        $url .= '&delete_flg=0';

        // Linking the parameter to the URL
        foreach( $inParam as $key => $value ){
            // Specify a value other than the following parameters
            // Add the "&" to the top
            $param = '';
            $param .= $key . '='. $value;
            // If there is a parameter, add the "?"
            $url .= '&'. $param;
        }

        $result = $this->_execApi( $url );

        return $result;

    }

    /**
     * Delete the directory
     *
     */
    protected function _deleteDirectory() {

        // Specify the path that was created when you created the OUT.json or IN.json( POST,PUT,DELETE )
        if( isset( $this->fileDirPath ) ){

            // Specify the request ID that was paid out in the first
            $dir = $this->fileDirPath;

        // If there is a request ID in IN parameters( GET )
        // $this->_requestId is the UUID to be paid out without fail at the time of API execution
        }else if( isset( $this->_p['request-id'] ) ){

            // Create a path to the directory
            $trans = array(
                            '%ROOT_DIR%' => $this->_nalConf['root_inoutfile'],
                            '%UUID%'     => $this->_p['request-id'],
            );
            $dir = strtr( neccsNal_Config::DIR_PATH, $trans );

        // other than that
        }else{
            // Not made a reference
            return;
        }

        // If the file exists, the s Delete the file
        if( file_exists( $dir ) ){
            // Delete the directory
            if ( $handle = opendir( "$dir" ) ) {
                while ( ( $item = readdir( $handle ) ) !== false ) {
                    if ( $item != "." && $item != ".." ) {
                        // Delete the file
                        if( @unlink( "$dir/$item" ) === false ) {
                            $this->error( neccsNal_Config::API_INTERNAL_ERROR, "failed in delete file. ({$dir}/{$item})" );
                        }
                    }
                }
                closedir( $handle );
                if( @rmdir( $dir ) === false ) {
                    $this->error( neccsNal_Config::API_INTERNAL_ERROR, "failed in delete directory. ({$dir})" );
                }
            }
        }
    }

    /**
     * Get the Pod information
     *
     * @return $result : Pod information
     */
    protected function getPod( $inParam = array() ){
        // Get the Endpoint information
        // Get a URL
        $url = neccsNal_Config::API_URL . neccsNal_Config::API_URL_LIST;
        $url .= neccsNal_Config::RESOURCE_PODS. '/';
        $url .= '?request-id='. $this->_p['request-id'];

        // Linking the parameter to the URL
        foreach( $inParam as $key => $value ){
            // Specify a value other than the following parameters
            // Add the "&" to the top
            $param = '';
            $param .= $key . '='. $value;
            // If there is a parameter, add the "?"
            $url .= '&'. $param;
        }

        $result = $this->_execApi( $url );

        return $result;

    }

    /**
     * Obtain license use_cnt
     *
     * @param license information
     * @param search param(type,device_type)
     *
     * @return $use_cnt
     */
    protected function _getUseCntLicense( $execList, $param ){

        $type        = $param['type'];
        $device_type = $param['device_type'];

        $use_cnt = array();
        $total = 0;

        $nodeIdList = array();
        foreach( $execList['license_info'] as $value ){

            if( $type != $value['type'] || $device_type != $value['device_type']  ){
                continue;
            }

            $tenant_name = $value['tenant_name'];
            // In case of unused license, do not process
            if( $tenant_name === '' ){
                continue;
            }

            // If initial value by tenant is not set, initial value is set
            if( $tenant_name != '' && !isset( $use_cnt[$tenant_name] ) ){
                $use_cnt[$tenant_name]['use_cnt'] = 0;
            }

            if ( $type == neccsNal_Config::TYPE_FW  ){

                if( $device_type == neccsNal_Config::PALOALTO  && !isset( $this->_p['IaaS_tenant_id'] ) ){
                    // For PaloAlto only search data of type_detail
                    $function_type = $param['function_type'];
                    $type_detail = $param['type_detail'];
                    if( $param['type_detail'] == $value['type_detail'] ){
                        if( in_array( $value['status'], neccsNal_Config::$useCntStatusList[$function_type][$type][$device_type] ) ){
                            $use_cnt[$tenant_name]['use_cnt'] += 1;
                            $total += 1;
                        }
                    }
                } else {
                    // For PaloAlto only search data of type_detail
                    $function_type = $param['function_type'];
                    if( in_array( $value['status'], neccsNal_Config::$useCntStatusList[$function_type][$type][$device_type] ) ){
                        if( $value['node_id'] !== '' && !in_array( $value['node_id'], $nodeIdList ) ){
                            $use_cnt[$tenant_name]['use_cnt'] += 1;
                            $total += 1;
                            $nodeIdList[] = $value['node_id'];
                        }
                    }
                }
            }

            if ( $type == neccsNal_Config::TYPE_LB  ){

                $function_type = $param['function_type'];
                if( in_array( $value['status'], neccsNal_Config::$useCntStatusList[$function_type][$type][$device_type] ) ){
                    if( $value['node_id'] !== '' && !in_array( $value['node_id'], $nodeIdList ) ){
                        $use_cnt[$tenant_name]['use_cnt'] += 1;
                        $total += 1;
                        $nodeIdList[] = $value['node_id'];
                    }
                }
            }
        }

        if ( $type == neccsNal_Config::TYPE_ROUTER ){

            $groupIdList = array();
            foreach( $execList['dc_group_info'] as $key1 => $dcGroup ){

                $group_type = intval( $dcGroup['group_type'] );
                if( !in_array( $group_type, neccsNal_Config::$serviceTypeList[$device_type] ) ){
                    continue;
                }

                $tenant_name = $dcGroup['tenant_name'];

                // If initial value by tenant is not set, initial value is set
                if( $tenant_name != '' && !isset( $use_count[$tenant_name] ) ){
                    $use_cnt[$tenant_name]['use_cnt'] = 0;
                }

                if( in_array( $group_type, neccsNal_Config::$serviceTypeList[neccsNal_Config::CISCO] ) && !isset( $this->_p['IaaS_tenant_id'] ) ){

                    foreach( $execList['dc_member_info'] as $key2 => $dcMember ){
                        if( $dcMember['group_id'] === $dcGroup['group_id'] && $param['type_detail'] == $dcMember['bandwidth'] ){
                            // If the same group ID exists in $ groupIdList, it is not counted
                            if( !in_array( $dcMember['group_id'] , $groupIdList ) ){
                                $use_cnt[$tenant_name]['use_cnt'] += 1;
                                $total += 1;
                                $groupIdList[] = $dcMember['group_id'];
                            }
                        }
                    }

                } else {
                    foreach( $execList['dc_member_info'] as $key2 => $dcMember ){
                        if( $dcMember['group_id'] === $dcGroup['group_id'] ){
                            // If the same group ID exists in $ groupIdList, it is not counted
                            if( !in_array( $dcMember['group_id'] , $groupIdList ) ){
                                $use_cnt[$tenant_name]['use_cnt'] += 1;
                                $total += 1;
                                $groupIdList[] = $dcMember['group_id'];
                            }
                        }
                    }
                }
            }
        }

        return array( $total, $use_cnt );
    }

    /**
     * Obtain license unavailable_cnt
     *
     * @param license information
     * @param search param(type,device_type)
     *
     * @return $use_cnt
     */
    protected function _getUnavailableCntLicense( $execList, $param ){

        $licenseInfo = $execList['license_info'];

        $type        = intval( $param['type'] );
        $device_type = intval( $param['device_type'] );

        $use_cnt = array();
        $total = 0;
        foreach( $licenseInfo as $value ){

            if( $type != $value['type'] || $device_type != $value['device_type']  ){
                continue;
            }

            $tenant_name   = $value['tenant_name'];
            $function_type = $param['function_type'];

            if( !empty( neccsNal_Config::$UnavailableCntStatusList[$function_type][$type][$device_type] )
                && in_array( $value['status'], neccsNal_Config::$UnavailableCntStatusList[$function_type][$type][$device_type] ) ){

                if( $type == neccsNal_Config::TYPE_FW  ){

                    if( $device_type == neccsNal_Config::FORTIGATE ){
                        $update_date = $value['update_date'];
                        $now = date('Y-m-d H:i:s');

                        $elapsed_time = ( strtotime($now) - strtotime($update_date) ) / 3600;

                        if( $elapsed_time < neccsNal_Config::FOTIGATE_USABLE_TIME ){
                            $total += 1;
                        }

                    } else if( $device_type == neccsNal_Config::PALOALTO ) {
                        if( $value['type_detail'] == $param['type_detail'] ){
                            $total += 1;
                        }
                    }

                } else {
                    $total += 1;
                }
            }
        }

        return $total;
    }

    /**
     * Obtain license contract_cnt
     *
     * @param license information
     * @param search param(type,device_type)
     *
     * @return $use_cnt
     */
    protected function _getContractCntLicense( $execList, $param ){
        $tenantContCntInfo = $execList['tenant_contract_info'];

        $type        = intval( $param['type'] );
        $device_type = intval( $param['device_type'] );

        $contract_cnt = array();
        $total = 0;
        foreach( $tenantContCntInfo as $value ){

            if( $value['apl_type'] != 1 || $type != $value['type'] || $device_type != $value['device_type']  ){
                continue;
            }

            $tenant_name = $value['tenant_name'];
            // If initial value by tenant is not set, initial value is set
            if( $tenant_name != '' && !isset( $contract_cnt[$tenant_name] ) ){
                $contract_cnt[$tenant_name]['contract_cnt'] = 0;
                $contract_cnt[$tenant_name]['tenant_name']  = $tenant_name;
                $contract_cnt[$tenant_name]['ID']           = $value['ID'];
            }

            if( $type == neccsNal_Config::TYPE_FW ){

                if( $device_type == neccsNal_Config::PALOALTO  && !isset( $this->_p['IaaS_tenant_id'] ) ){

                    $type_detail_info = json_decode( $value['type_detail_info'], true );
                    $type_detail = $param['type_detail'];

                    if( isset( $type_detail_info['type_detail'][$type_detail] ) ){
                        $detail_count = $type_detail_info['type_detail'][$type_detail];
                        $contract_cnt[$tenant_name]['contract_cnt'] += $value['contract'] * $detail_count;
                        $total += $value['contract'] * $detail_count;
                    } else {
                        $contract_cnt[$tenant_name]['contract_cnt'] = 0;
                    }

                } else {
                    $contract_cnt[$tenant_name]['contract_cnt'] += $value['contract'];
                    $total += $value['contract'];
                }

            } else if ( $type == neccsNal_Config::TYPE_LB ){

                $contract_cnt[$tenant_name]['contract_cnt'] += $value['contract'];
                $total += $value['contract'];

            } else if ( $type == neccsNal_Config::TYPE_ROUTER ){

                if( $device_type == neccsNal_Config::CISCO && !isset( $this->_p['IaaS_tenant_id'] ) ){

                    $type_detail_info = json_decode( $value['type_detail_info'], true );
                    $type_detail = $param['type_detail'];

                    if( isset( $type_detail_info['type_detail'][$type_detail] ) ){
                        $detail_count = $type_detail_info['type_detail'][$type_detail];
                        $contract_cnt[$tenant_name]['contract_cnt'] += $value['contract'] * $detail_count;
                        $total += $value['contract'] * $detail_count;
                    } else {
                        $contract_cnt[$tenant_name]['contract_cnt'] = 0;
                    }

                } else {
                    $contract_cnt[$tenant_name]['contract_cnt'] += $value['contract'];
                    $total += $value['contract'];
                }
            }
        }

        return array( $total, $contract_cnt );
    }

    /**
     * Obtain license quota
     *
     * @param license information
     * @param search param(type,device_type)
     *
     * @return $use_cnt
     */
    protected function _getQuotaLisence( $execList, $param ){

        $licenseInfo = $execList['license_info'];

        $type        = intval( $param['type'] );
        $device_type = intval( $param['device_type'] );

        $use_cnt = array();
        $total = 0;
        foreach( $licenseInfo as $value ){

            if( $type != $value['type'] || $device_type != $value['device_type']  ){
                continue;
            }

            if( $type == neccsNal_Config::TYPE_FW && $device_type == neccsNal_Config::PALOALTO ){
                $type_detail = intval( $param['type_detail'] );
                if( !isset( $value['type_detail'] ) || $type_detail != $value['type_detail'] ){
                    continue;
                }
            }

            if( $type == neccsNal_Config::TYPE_ROUTER && $device_type == neccsNal_Config::CISCO ){
                $type_detail = intval( $param['type_detail'] );
                if( !isset( $value['type_detail'] ) || $type_detail != $value['type_detail'] ){
                    continue;
                }
            }

            $total += 1;
        }
        return $total;

    }

    /**
     * Obtain license quota for pnf
     *
     * @param license information
     *
     * @return $use_cnt
     */
    protected function _getQuotaPnf( $execList, $param ){

        $aplInfo = $execList['apl_info'];
        $type        = $param['type'];
        $device_type = $param['device_type'];


        $total = 0;
        foreach( $aplInfo as $value ){

            if( $value['apl_type'] != 2 || $type != $value['type'] || $device_type != $value['device_type'] ){
                continue;
            }

            if( $type == neccsNal_Config::TYPE_FW &&
                ( $device_type == neccsNal_Config::PFW_FORTIGATE || $device_type == neccsNal_Config::PFW_PALOALTO ) ){
                $redundant_configuration_flg = intval( $param['redundant_configuration_flg'] );
                if( !isset( $value['redundant_configuration_flg'] ) || $redundant_configuration_flg != intval( $value['redundant_configuration_flg'] ) ){
                    continue;
                }
            }

            if( $type == neccsNal_Config::TYPE_LB &&
            ( $device_type == neccsNal_Config::PLB_BIGIP || $device_type == neccsNal_Config::PLB_THUNDER ) ){
                $redundant_configuration_flg = intval( $param['redundant_configuration_flg'] );
                if( !isset( $value['redundant_configuration_flg'] ) || $redundant_configuration_flg != $value['redundant_configuration_flg'] ){
                    continue;
                }
            }

            $total++;
        }
        return $total;
    }

    /**
     * Obtain license contract_cnt for pnf
     *
     * @param license information
     * @param search param(type,device_type)
     *
     * @return $use_cnt
     */
    protected function _getContractCntPnf( $execList, $param ){
        $tenantContCntInfo = $execList['tenant_contract_info'];
        $type              = intval( $param['type'] );
        $device_type       = intval( $param['device_type'] );

        $total = 0;
        foreach( $tenantContCntInfo as $value ){

            if( $value['apl_type'] != 2 || $type != $value['type'] || $device_type != $value['device_type']  ){
                continue;
            }

            if( $type == neccsNal_Config::TYPE_FW &&
            ( $device_type == neccsNal_Config::PFW_FORTIGATE || $device_type == neccsNal_Config::PFW_PALOALTO ) ){
                $redundant_configuration_flg = intval( $param['redundant_configuration_flg'] );
                if( !isset( $value['redundant_configuration_flg'] ) || $redundant_configuration_flg != $value['redundant_configuration_flg'] ){
                    continue;
                }
            }

            if( $type == neccsNal_Config::TYPE_LB &&
            ( $device_type == neccsNal_Config::PLB_BIGIP || $device_type == neccsNal_Config::PLB_THUNDER ) ){
                $redundant_configuration_flg = intval( $param['redundant_configuration_flg'] );
                if( !isset( $value['redundant_configuration_flg'] ) || $redundant_configuration_flg != $value['redundant_configuration_flg'] ){
                    continue;
                }
            }

            $total += $value['contract'];
        }

        return $total;
    }

    /**
     * Obtain license use_cnt for pnf
     *
     * @param license information
     *
     * @return $use_cnt
     */
    protected function _getUseCntPnf( $execList, $param ){

        $aplInfo = $execList['apl_info'];

        $type          = intval( $param['type'] );
        $device_type   = intval( $param['device_type'] );
        $function_type = $param['function_type'];

        $total = 0;
        foreach( $aplInfo as $value ){

            if( $value['apl_type'] != 2 || $type != $value['type'] || $device_type != $value['device_type']  ){
                continue;
            }

            if( in_array( $value['task_status'], neccsNal_Config::$useCntStatusList[$function_type][$type][$device_type] ) ){
                // Since the task_status is also registered as 1 for the initial data, also check tenant_name
                if( $value['tenant_name'] !== '' ){
                    $total += 1;
                }
            }
        }

        return $total;
    }

    /**
     * Obtain license unavailable_cnt for pnf
     *
     * @param license information
     *
     * @return $use_cnt
     */
    protected function _getUnavailableCntPnf( $execList, $param ){

        $aplInfo = $execList['apl_info'];

        $type          = intval( $param['type'] );
        $device_type   = intval( $param['device_type'] );
        $function_type = $param['function_type'];

        $total = 0;
        foreach( $aplInfo as $value ){

            if( $value['apl_type'] != 2 || $type != $value['type'] || $device_type != $value['device_type']  ){
                continue;
            }

            if( in_array( $value['task_status'], neccsNal_Config::$UnavailableCntStatusList[$function_type][$type][$device_type] ) ){
                $total += 1;
            }
        }

        return $total;
    }

    /**
     * Obtain globalip unavailable_cnt
     *
     * @param globalip information
     *
     * @return $total_unavailable_cnt
     */
    protected function _getUnavailableCntGlobalip( $execList ){

        $globalipInfo = $execList['global_ip_address_info'];

        $total_unavailable_cnt = 0;
        # TODO check status

        return $total_unavailable_cnt;
    }

    /**
     * Obtain globalip use_cnt
     *
     * @param globalip information
     *
     * @return $total_use_cnt
     */
    protected function _getUseCntGlobalip( $execList, $param ){

        $globalipInfo = $execList['global_ip_address_info'];

        $total_use_cnt = 0;
        foreach( $globalipInfo as $value ){

            $function_type = $param['function_type'];
            if( in_array( $value['status'], neccsNal_Config::$useCntStatusList[$function_type] ) ){
                $total_use_cnt += 1;
            }
        }
        return $total_use_cnt;
    }

    /**
     * Obtain globalip contract_cnt
     *
     * @param tenant contract information
     *
     * @return $total_contract
     */
    protected function _getContractCntGlobalip( $execList, $param ){

        $tenantContCntInfo = $execList['tenant_contract_info'];

        $total_contract = 0;
        foreach( $tenantContCntInfo as $value ){
            $contract_kind = isset( $value['contract_kind'] ) ? $value['contract_kind'] : "";
            if ( $param['nw_resource_kind'] == $contract_kind ) {
                $total_contract += $value['contract'];
            }
        }

        return $total_contract;
    }

    /**
     * Obtain globalip quota
     *
     * @param globalip information
     *
     * @return $quota
     */
    protected function _getQuotaGlobalip( $execList ){

        $globalipInfo = $execList['global_ip_address_info'];
        $total = count($globalipInfo);

        return $total;
    }

    /**
     * Acquire upper limit of MSA
     *
     * @param REST API return value
     *
     * @return $quota
     */
    protected function _getQuotaMsa( $execList ){

        $aplInfo = $execList['msa_info'];

        $total = count( $aplInfo );
        return $total;
    }

    /**
     * Acquire MAS contract number
     *
     * @param REST API return value
     *
     * @return $contract_cnt
     */
    protected function _getContractCntMsa( $execList ){

        $tenantContCntInfo = $execList['tenant_contract_info'];
        $podInfo           = $execList['pod_info'];
        $pod_count         = count( $podInfo );

        $total = 0;
        $tenantNameList = array();
        foreach( $tenantContCntInfo as $value ){
            if( !in_array( $value['tenant_name'] , $tenantNameList ) ){
                $total += 1;
                $tenantNameList[] = $value['tenant_name'];
            }
        }
        $contract_cnt = $total * $pod_count;

        return $contract_cnt;
    }

    /**
     * Acquire the number of MAS usage
     *
     * @param REST API return value
     * @param Input Param
     *
     * @return $use_cnt
     */
    protected function _getUseCntMsa( $execList, $param ){

        $msaInfo = $execList['msa_info'];
        $function_type = $param['function_type'];

        $total = 0;
        foreach( $msaInfo as $value ){
            if( in_array( $value['status'], neccsNal_Config::$useCntStatusList[$function_type] ) ){
                $total += 1;
            }
        }

        return $total;
    }

    /**
     * Acquire unusable number of MSA
     *
     * @param REST API return value
     *
     * @return $unavailable_cnt
     */
    protected function _getUnavailableCntMsa( $execList ){

        $msaInfo = $execList['msa_info'];

        $total_unavailable_cnt = 0;
        // TODO check status

        return $total_unavailable_cnt;

    }

    /**
     * Acquire upper limit of WAN
     *
     * @param REST API return value
     *
     * @return $quota
     */
    protected function _getQuotaWan( $execList ){

        $aplInfo = $execList['wan_info'];

        $total = count( $aplInfo );
        return $total;
    }

    /**
     * Acquire WAN contract number
     *
     * @param REST API return value
     *
     * @return $contract_cnt
     */
    protected function _getContractCntWan( $execList ){

        $tenantContCntInfo = $execList['tenant_contract_info'];
        $podInfo           = $execList['pod_info'];

        $pod_count = 0;
        foreach( $podInfo as $value ){
            // Counting when it is dedicated to WIM or shared
            if( $value['use_type'] == '2' || $value['use_type'] == '3' ){
                $pod_count++;
            }
        }

        $total = 0;
        $tenantNameList = array();
        foreach( $tenantContCntInfo as $value ){
            if( $value['type'] == '3' ){
                if( $value['device_type'] == neccsNal_Config::CISCO ){
                    $type_detail_info = json_decode( $value['type_detail_info'], true );
                    if( !empty( $type_detail_info ) ){
                        foreach( $type_detail_info['type_detail'] as $type_detail ){
                            $total += $value['contract'] * $type_detail;
                        }
                    }
                } else {
                    $total += $value['contract'];
                }
            }
        }
        // ( Number of existing tenants ) * ( Number of pots in WIM )
        $contract_cnt = $total * $pod_count;

        return $contract_cnt;
    }

    /**
     * Acquire the number of WAN usage
     *
     * @param REST API return value
     * @param Input Param
     *
     * @return $use_cnt
     */
    protected function _getUseCntWan( $execList, $param ){

        $msaInfo = $execList['wan_info'];
        $function_type = $param['function_type'];

        $total = 0;
        foreach( $msaInfo as $value ){
            if( in_array( $value['status'], neccsNal_Config::$useCntStatusList[$function_type] ) ){
                $total += 1;
            }
        }

        return $total;
    }

    /**
     * Acquire unusable number of WAN
     *
     * @param REST API return value
     *
     * @return $unavailable_cnt
     */
    protected function _getUnavailableCntWan( $execList ){

        $msaInfo = $execList['wan_info'];

        $total_unavailable_cnt = 0;
        // TODO check status

        return $total_unavailable_cnt;

    }

    /**
     * Acquire the threshold
     *
     * @param REST API return value
     *
     * @return $threshold
     */
    protected function _getThreshold( $execList, $param ){

        $type        = $param['type'];
        $device_type = $param['device_type'];
        $nw_resource_kind = $param['nw_resource_kind'];
        $thresholdInfo    = $execList['threshold_info'];

        foreach( $thresholdInfo as $threshold ){
            if( $param['function_type'] === neccsNal_Config::LICENSE ){
                if( $threshold['nw_resource_kind'] != 2 || $threshold['type'] != $param['type'] || $threshold['device_type'] != $param['device_type'] ){
                    continue;
                }
                if( $threshold['device_type'] == neccsNal_Config::PALOALTO ){
                    if( $threshold['type_detail'] != $param['type_detail'] ){
                        continue;
                    }
                }
                return $threshold['threshold'];
            }

            if ( $param['function_type'] === neccsNal_Config::PNF ) {
                if( $threshold['nw_resource_kind'] != 3 || $threshold['type'] != $type || $threshold['device_type'] != $device_type ){
                    continue;
                }
                if( $threshold['device_type'] == neccsNal_Config::PFW_FORTIGATE || $threshold['device_type'] == neccsNal_Config::PFW_PALOALTO
                || $threshold['device_type'] == neccsNal_Config::PLB_BIGIP || $threshold['device_type'] == neccsNal_Config::PLB_THUNDER ){
                    if( $threshold['redundant_configuration_flg'] != $param['redundant_configuration_flg'] ){
                        continue;
                    }
                }

                if( $threshold['device_type'] == neccsNal_Config::PFW_FORTIGATE_SHARE || $threshold['device_type'] == neccsNal_Config::PFW_PALOALTO_SHARE
                   || $threshold['device_type'] == neccsNal_Config::PLB_BIGIP_SHARE || $threshold['device_type'] == neccsNal_Config::PLB_THUNDER_SHARE ){
                    if( $threshold['redundant_configuration_flg'] != $param['redundant_configuration_flg'] ){
                        continue;
                    }
                }
                return $threshold['threshold'];
            }

            if ( $param['function_type'] === neccsNal_Config::GLOBALIP ) {
                if( $threshold['nw_resource_kind'] == $nw_resource_kind ){
                    return $threshold['threshold'];
                }
            }

            if ( $param['function_type'] === neccsNal_Config::MSA_VLAN ) {
                if( $threshold['nw_resource_kind'] == $nw_resource_kind ){
                    return $threshold['threshold'];
                }

            }

            if ( $param['function_type'] === neccsNal_Config::WAN_VLAN ) {
                if( $threshold['nw_resource_kind'] == $nw_resource_kind ){
                    return $threshold['threshold'];
                }

            }

            if ( $param['function_type'] === neccsNal_Config::CPU_LIST ) {
                if( $threshold['nw_resource_kind'] == $nw_resource_kind ){
                    return $threshold['threshold'];
                }

            }

            if ( $param['function_type'] === neccsNal_Config::MEMORY_LIST ) {
                if( $threshold['nw_resource_kind'] == $nw_resource_kind ){
                    return $threshold['threshold'];
                }

            }

            if ( $param['function_type'] === neccsNal_Config::STORAGE_LIST ) {
                if( $threshold['nw_resource_kind'] == $nw_resource_kind ){
                    return $threshold['threshold'];
                }
            }
        }

        return 0;

    }

    /**
     * Add unit of memory
     *
     * @param Memory Information
     *
     * @return Information on memory with unit
     */
    protected function _setUnitForMemory( $value ){

        if( $value >= 1 || $value === 0 ){
            return $value. 'MB';
        } else if ( $value * 1000 >= 1 ) {
            return ( $value * 1000 ). 'KB';
        } else if ( $value * 1000 * 1000 >= 1 ){
            return ( $value * 1000 * 1000 ). 'B';
        }
    }

    /**
     * Add unit of storage
     *
     * @param Storage Information
     *
     * @return Information on storage with unit
     */
    protected function _setUnitForStorage( $value ){

        if( $value >= 1 || $value === 0 ){
            return $value. 'GB';
        } else if ( $value * 1000 >= 1 ) {
            return ( $value * 1000 ). 'MB';
        } else if ( $value * 1000 * 1000 >= 1 ){
            return ( $value * 1000 * 1000 ). 'KB';
        } else if ( $value * 1000 * 1000 * 1000 >= 1 ){
            return ( $value * 1000 * 1000 * 1000 ). 'B';
        }
    }
}
