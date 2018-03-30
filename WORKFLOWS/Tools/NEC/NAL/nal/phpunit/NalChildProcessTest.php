<?php
/**
 * Generated by PHPUnit_SkeletonGenerator on 2016-07-08 at 09:26:45.
 */
require_once dirname(__FILE__) . '/../Nal/bin/NalChildProcess.php';
require_once dirname(__FILE__) . '/Stub/NalChildProcessStb.php';
class NalChildProcessTest extends PHPUnit_Framework_TestCase
{
    /**
     * @var NalChildProcess
     */
    protected $object;

    /**
     * Sets up the fixture, for example, opens a network connection.
     * This method is called before a test is executed.
     */
    protected function setUp()
    {
        if( !defined( 'PHPUNIT_RUN' ) ) {
            define( "PHPUNIT_RUN", "phpunit_run" );
        }

        $this->homeDir = realpath( dirname(__FILE__) ) ;
        if( !defined('HOME_DIR')) {
            define( 'HOME_DIR', $this->homeDir );
        }
        if( !defined('API_DIR')) {
            define( 'API_DIR' , HOME_DIR . '' );
        }
        if( !defined('APP_DIR')) {
            define( 'APP_DIR' , API_DIR . '/Stub' );
        }
    }

    /**
     * Tears down the fixture, for example, closes a network connection.
     * This method is called after a test is executed.
     */
    protected function tearDown()
    {
    }

    /**
     * @covers NalChildProcess::__construct
     * @todo   Implement __construct().
     */
    public function testConstruct() {
        // case 1
        $param['request_method'] = 'POST';
        $param['request-id'] = '20160708120000';
        $param['nal_conf'] = array( 'root_inoutfile' => '/var/log/nal/job', 'api_type' => 'nal', 'job_type' => '1', );
        $param['function_type'] = "vfw";
        $param['job_operation'] = 'create-vfw';
        $obj = new NalChildProcess( $param );
        $this->assertTrue( $obj instanceof  NalChildProcess );
    }

    /**
     * @covers NalChildProcess::getBatchInstance
     * @todo   Implement testGetBatchInstance().
     * @runInSeparateProcess
     * @preserveGlobalState disabled
     */
    public function testGetBatchInstance() {

        $filePath = '/var/log/nal/job/20160708120000000000000';

        $this->removeDir( $filePath );

        // case1
        $opts = array();
        try {
            NalChildProcess::getBatchInstance( $opts );
        } catch ( Exception $e ) {
            $this->assertEquals( $e->getMessage(), "A parameter is unjust." );
        }

        // case 2
        $opts = array( 'f' => $filePath . '/' . neccsNal_Config::CHILD_PROCESS_FILE );
        try {
            NalChildProcess::getBatchInstance( $opts );
        } catch ( Exception $e ) {
            $this->assertEquals( $e->getMessage(), "A file doesn't exist. (" . $filePath . '/' . neccsNal_Config::CHILD_PROCESS_FILE .")" );
        }

        // case3
        if( !is_dir( $filePath ) ) {
            mkdir( $filePath, 0755, true );
        }
        $pFile = $filePath . '/' . neccsNal_Config::CHILD_PROCESS_FILE;
        $wFile = fopen( $pFile, 'w+' );
        fwrite( $wFile, serialize( array( 'test' ) ) );
        fclose( $wFile );

        $opts = array( 'f' => $filePath . '/' . neccsNal_Config::CHILD_PROCESS_FILE );
        try {
            NalChildProcess::getBatchInstance( $opts );
        } catch ( Exception $e ) {
            $this->assertEquals( $e->getMessage(), "A parameter is unjust." );
        }

        // case4
        $data = array(
            'request_method' => 'POST',
            'scenario'       => 'test',
            'function_type'  => 'vfw',
            'nal_conf'       => neccsNal_Config::$nalConfDefault,
        );
        $pFile = $filePath . '/' . neccsNal_Config::CHILD_PROCESS_FILE;
        $wFile = fopen( $pFile, 'w+' );
        fwrite( $wFile, serialize( $data ) );
        fclose( $wFile );

        $opts = array( 'f' => $filePath . '/' . neccsNal_Config::CHILD_PROCESS_FILE );
        try {
            NalChildProcess::getBatchInstance( $opts );
        } catch ( Exception $e ) {
            $this->assertEquals( $e->getMessage(), "This function can not be used. (test)" );
        }

        // case5
        $data = array(
            'request_method' => 'POST',
            'scenario'       => 'node',
            'function_type'  => 'dcconnect',
            'nal_conf'       => neccsNal_Config::$nalConfDefault,
        );
        $pFile = $filePath . '/' . neccsNal_Config::CHILD_PROCESS_FILE;
        $wFile = fopen( $pFile, 'w+' );
        fwrite( $wFile, serialize( $data ) );
        fclose( $wFile );

        $opts = array( 'f' => $filePath . '/' . neccsNal_Config::CHILD_PROCESS_FILE );
        try {
            NalChildProcess::getBatchInstance( $opts );
        } catch ( Exception $e ) {
            $this->assertEquals( $e->getMessage(), "This class can not be used. (node : dcconnect)" );
        }

        // case6
        $data = array(
            'request_method' => 'PUT',
            'scenario'       => 'node',
            'function_type'  => 'vport',
            'nal_conf'       => neccsNal_Config::$nalConfDefault,
            'job_operation'  => 'create-vfw',
        );
        $pFile = $filePath . '/' . neccsNal_Config::CHILD_PROCESS_FILE;
        $wFile = fopen( $pFile, 'w+' );
        fwrite( $wFile, serialize( $data ) );
        fclose( $wFile );

        $opts = array( 'f' => $filePath . '/' . neccsNal_Config::CHILD_PROCESS_FILE );
        try {
            NalChildProcess::getBatchInstance( $opts );
        } catch ( Exception $e ) {
            $this->assertEquals( $e->getMessage(), "This class can not be used. (node : vport : PUT)" );
        }

        // case7
        $data = array(
            'request_method' => 'POST',
            'scenario'       => 'service',
            'function_type'  => 'dcconnect',
            'nal_conf'       => neccsNal_Config::$nalConfDefault,
            'request-id'     => '20160708120000000000000',
            'job_operation'  => 'create-vfw',
        );
        $pFile = $filePath . '/' . neccsNal_Config::CHILD_PROCESS_FILE;
        $wFile = fopen( $pFile, 'w+' );
        fwrite( $wFile, serialize( $data ) );
        fclose( $wFile );

        $opts = array( 'f' => $filePath . '/' . neccsNal_Config::CHILD_PROCESS_FILE );
        $obj = NalChildProcess::getBatchInstance( $opts );
        $this->assertTrue( $obj instanceof dcconnectChildProcess );

        // case8
        $data = array(
            'request_method' => 'POST',
            'scenario'       => 'node',
            'function_type'  => 'vport',
            'nal_conf'       => neccsNal_Config::$nalConfDefault,
            'request-id'     => '20160708120000000000000',
            'job_operation'  => 'create-vfw',
        );
        $pFile = $filePath . '/' . neccsNal_Config::CHILD_PROCESS_FILE;
        $wFile = fopen( $pFile, 'w+' );
        fwrite( $wFile, serialize( $data ) );
        fclose( $wFile );

        $opts = array( 'f' => $filePath . '/' . neccsNal_Config::CHILD_PROCESS_FILE );
        $obj = NalChildProcess::getBatchInstance( $opts );
        $this->assertTrue( $obj instanceof NalChildProcess );

        // case9
        $data = array(
            'request_method' => 'POST',
            'scenario'       => 'node',
            'function_type'  => 'vfw',
            'nal_conf'       => neccsNal_Config::$nalConfDefault,
            'request-id'     => '20160708120000000000000',
        );
        $pFile = $filePath . '/' . neccsNal_Config::CHILD_PROCESS_FILE;
        $wFile = fopen( $pFile, 'w+' );
        fwrite( $wFile, serialize( $data ) );
        fclose( $wFile );

        $opts = array( 'f' => $filePath . '/' . neccsNal_Config::CHILD_PROCESS_FILE );
        try {
            $obj = NalChildProcess::getBatchInstance( $opts );
        } catch( Exception $e ) {
            $this->assertEquals( $e->getMessage(), "not found class: vfwChildProcess" );
        }

        $this->removeDir( $filePath );
    }

    /**
     * @covers NalChildProcess::fatalBatchError
     * @todo   Implement testFatalBatchError().
     */
    public function testFatalBatchError() {
        // case 1
        try {
            NalChildProcess::fatalBatchError( 'NAL100000', 'test' );
        } catch( Exception $e) {
            $this->assertEquals($e->getMessage(), 'test' );
        }

        // case 2
        $logFile = neccsNal_Config::LOG_DIR . neccsNal_Config::$logFileName[neccsNal_Config::LEV_ERROR];
        $fd = @fopen( $logFile , "w");
        fwrite($fd, "TEST");
        fclose($fd);
        chmod($logFile,0000);
        try{
            NalChildProcess::fatalBatchError( 'NAL100000', 'TEST' );
        } catch( Exception $e ){
            $this->assertEquals( $e->getMessage(), 'TEST' );
        }
        chmod($logFile,0644);
        @unlink($logFile);
    }

    /**
     * @covers NalChildProcess::batchRun
     * @todo   Implement testBatchRun().
     */
    public function testBatchRun() {

        $filePath = '/var/log/nal/job/20160708120000000000000';

        $this->removeDir( $filePath );

        if( !is_dir( $filePath ) ) {
            mkdir( $filePath, 0755, true );
        }

        // case1
        $data = array(
            'request_method' => 'POST',
            'scenario'       => 'node',
            'function_type'  => 'vport',
            'nal_conf'       => neccsNal_Config::$nalConfDefault,
            'request-id'     => '20160708120000000000000',
            'job-id'         => 'create-vport.20160708120000000000000',
            'job_operation'  => 'create-vfw',
        );
        $pFile = $filePath . '/' . neccsNal_Config::CHILD_PROCESS_FILE;
        $wFile = fopen( $pFile, 'w+' );
        fwrite( $wFile, serialize( $data ) );
        fclose( $wFile );

        $opts = array( 'f' => $filePath . '/' . neccsNal_Config::CHILD_PROCESS_FILE );
        try {
            $obj = NalChildProcess::getBatchInstance( $opts );
            $obj->_httpMethod = 'test';
            $obj->batchRun();
        } catch ( Exception $e ) {
            $this->assertContains( "not found method: test", $e->getMessage() );
        }

        // case2
        $opts = array( 'f' => $filePath . '/' . neccsNal_Config::CHILD_PROCESS_FILE );
        try {
            $obj = NalChildProcess::getBatchInstance( $opts );
            $obj->_httpMethod = 'POST';
            $obj->batchRun();
        } catch ( Exception $e ) {
            //$this->assertContains( "not found method: test", $e->getMessage() );
        }

        // case3
        $_SERVER['REQUEST_METHOD'] = 'testpost';
        $_POST['function_type'] = 'vlb';
        $param = array(
                        'request_method' => 'testpost',
                        'function_type'  => 'vlb',
                        'nal_conf'       => neccsNal_Config::$nalConfDefault,
                        'request-id'     => '20160708120000000000000',
                        'job_operation'  => 'create-vfw',
        );
        $ret = new NalChildProcessStb( $param );
        $this->assertEquals($ret->batchRun(),'');

        // case4
        $_SERVER['REQUEST_METHOD'] = 'testpost2';
        $_POST['function_type'] = 'vlb';
        $param = array(
                        'request_method' => 'testpost2',
                        'function_type'  => 'vlb',
                        'nal_conf'       => neccsNal_Config::$nalConfDefault,
                        'request-id'     => '20160708120000000000000',
                        'job_operation'  => 'create-vfw',
        );
        $ret = new NalChildProcessStb( $param );
        $this->assertEquals($ret->batchRun(),'');
    }

    /**
     * @covers NalChildProcess::post
     * @todo   Implement testPost().
     */
    public function testPost() {
        $param = array(
            'request_method' => 'POST',
            'function_type'  => 'vlb',
            'nal_conf'       => neccsNal_Config::$nalConfDefault,
            'request-id'     => '20160708120000000000000',
            'job_operation'  => 'create-vfw',
        );
        $ret = new NalChildProcess( $param );
        $method = new ReflectionMethod( $ret, 'post' );
        $method->setAccessible( true );

        // case 1
        $ret = new NalChildProcessStb( $param );
        $method = new ReflectionMethod( $ret, 'post' );
        $method->setAccessible( true );
        $this->assertEquals($method->invoke($ret),'');
    }

    /**
     * @covers NalChildProcess::put
     * @todo   Implement testPut().
     */
    public function testPut() {
        $param = array(
            'request_method' => 'PUT',
            'function_type'  => 'vfw_port_p',
            'nal_conf'       => neccsNal_Config::$nalConfDefault,
            'request-id'     => '20160708120000000000000',
            'job_operation'  => 'create-vport',
        );
        $ret = new NalChildProcess( $param );
        $method = new ReflectionMethod( $ret, 'put' );
        $method->setAccessible( true );

        // case 1
        $ret = new NalChildProcessStb( $param );
        $method = new ReflectionMethod( $ret, 'put' );
        $method->setAccessible( true );
        $this->assertEquals($method->invoke($ret),'');
    }

    /**
     * @covers NalChildProcess::delete
     * @todo   Implement testDelete().
     */
    public function testDelete() {
        $param = array(
            'request_method' => 'DELETE',
            'function_type'  => 'vlb',
            'nal_conf'       => neccsNal_Config::$nalConfDefault,
            'request-id'     => '20160708120000000000000',
            'job_operation'  => 'delete-vfw',
        );
        $ret = new NalChildProcess( $param );
        $method = new ReflectionMethod( $ret, 'delete' );
        $method->setAccessible( true );

        // case 1
        $ret = new NalChildProcessStb( $param );
        $method = new ReflectionMethod( $ret, 'delete' );
        $method->setAccessible( true );
        $this->assertEquals($method->invoke($ret),'');
    }

    /**
     *  remove Dir
     */
    function removeDir( $dir ) {

        $cnt = 0;
        if(!is_dir($dir)){
            return;
        }
        $handle = opendir($dir);
        if (!$handle) {
            return ;
        }
        while (false !== ($item = readdir($handle))) {
            if ($item === "." || $item === "..") {
                continue;
            }
            $path = $dir . DIRECTORY_SEPARATOR . $item;
            if (is_dir($path)) {
                $cnt = $cnt + $this->removeDir($path);
            } else {
                chmod($path,0644);
                @unlink($path);
            }
        }
        closedir($handle);
        if (!@rmdir($dir)) {
            return ;
        }
    }

    /**
     *  After action
     */
    public function testAfterAction() {
        // after job
        $dir = neccsNal_Config::LOG_DIR . "/job";
        $this->removeDir($dir);
    }
}