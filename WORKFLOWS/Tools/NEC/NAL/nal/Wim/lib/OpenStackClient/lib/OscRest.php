<?php
/**
 * 1.SYSTEM   :
 * 2.FUNCTION : OpenStack Client REST I/F
 *
 * @version $Id: OscRest.php 2012-11-27$
 */
require_once dirname(__FILE__). '/../lib/OscCommon.php';
require_once dirname(__FILE__). '/../conf/OscConst.php';

class OscRest {
    private static $_instance = null;

    /** HTTP Method **/
    const HTTP_GET      = 'GET';
    const HTTP_POST     = 'POST';
    const HTTP_PUT      = 'PUT';
    const HTTP_DELETE   = 'DELETE';

    /** cilent common */
    protected $_common;
    protected $_endPointArray;
    protected $_requestId;

    public function __construct() {

//         $this->_common = new commonClient();
    }

    public static function getInstance() {
        if ( is_null( self::$_instance ) ) {
            self::$_instance = new self();
        }
        return self::$_instance;
    }
    /**
     * REST GET
     *
     * @param  <String>       $url
     * @param  <String>       $token
     * @param  <String/Array> $param
     *
     * @return <Array>  OpenStack response
     * @throws Exception
     */
    public function rest_get($url, $token, $param) {

        $param_string = '';
        if(is_array($param)){
            $param_string = json_encode($param, true);
        } else {
            $param_string = $param;
        }

        //init
        $ret = array();

        //check
        if ( empty( $url ) ) {
            throw new Exception( 'url required' );
        } else {
            // set cul init
            $ch = curl_init($url);
            // set HEADER curl parame
            curl_setopt($ch, CURLOPT_HTTPHEADER, array('X-Auth-Token:'.$token,'Content-type: application/json'));
            // curl option GET
            curl_setopt($ch, CURLOPT_HTTPGET, true);
            curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, FALSE);
            curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
            curl_setopt($ch, CURLOPT_FOLLOWLOCATION, false);
            curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, 2);
            curl_setopt($ch, CURLINFO_HEADER_OUT, true);
            //curl
            $var = curl_exec($ch);

            if($var === false){
                $curl_error = curl_error($ch);
                $curl_errno = curl_errno($ch);
                curl_close($ch);
                throw new Exception( 'curl_error:' . $curl_error . ',curl_errno:' . $curl_errno);
            }

            //curl
            curl_close($ch);

            $ret = json_decode($var, true);

            // if json error occured, throw error
            if (json_last_error() !== JSON_ERROR_NONE) {
                $json_last_error_no = json_last_error();
                $json_last_error_code = OscCommon::getJsonErrorCode($json_last_error_no);

                throw new Exception( 'json_last_error:' . $json_last_error_no . ',json_last_error_code:' . $json_last_error_code . ',ret:' . $var);
            }

        }

        return $ret;
    }
    /**
     * REST POST
     *
     * @param  <String>       $url
     * @param  <String>       $token
     * @param  <String/Array> $param
     *
     * @return <Array>  OpenStack response
     * @throws Exception
     */
    public function rest_post($url, $token, $param) {

        $param_string = '';
        if(is_array($param)){
            $param_string = json_encode($param, true);
        } else {
            $param_string = $param;
        }

        //init
        $ret = array();
        //check
        if ( empty( $url ) ) {
            throw new Exception( 'url required' );
        } else {
            // set cul init
            $ch = curl_init($url);
            // set HEADER curl parame
            if ( empty ( $token ) ) {
                  curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-type: application/json'));
            }else{
                  curl_setopt($ch, CURLOPT_HTTPHEADER, array('X-Auth-Token:'.$token, 'Content-type: application/json'));
            }
            //curl option POST
            curl_setopt($ch, CURLOPT_POST, true);
            curl_setopt($ch, CURLOPT_POSTFIELDS, $param);
            curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, FALSE);
            curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
            curl_setopt($ch, CURLINFO_HEADER_OUT, true);
            curl_setopt($ch, CURLOPT_HEADER, 1);
            curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);

            //curl
            $var = curl_exec($ch);
            $info = curl_getinfo ($ch);

            $header = substr($var, 0, $info["header_size"]);
            $var = substr($var, $info["header_size"]);

            if($var === false){
                $curl_error = curl_error($ch);
                $curl_errno = curl_errno($ch);
                curl_close($ch);
                throw new Exception( 'curl_error:' . $curl_error . ',curl_errno:' . $curl_errno);
            }

            //curl
            curl_close($ch);

            $ret = json_decode($var, true);

            // if json error occured, throw error
            if (json_last_error() !== JSON_ERROR_NONE) {
                $json_last_error_no = json_last_error();
                $json_last_error_code = OscCommon::getJsonErrorCode($json_last_error_no);

                throw new Exception( 'json_last_error:' . $json_last_error_no . ',json_last_error_code:' . $json_last_error_code . ',ret:' . $var);
            }

        }

        return array( $header, $ret );
    }
    /**
     * REST PUT
     *
     * @param  <String>       $url
     * @param  <String>       $token
     * @param  <String/Array> $param
     *
     * @return <Array>  OpenStack response
     * @throws Exception
     */
    public function rest_put($url, $token, $param) {

        $param_string = '';
        if(is_array($param)){
            $param_string = json_encode($param, true);
        } else {
            $param_string = $param;
        }

        //init
        $ret = array();
        //check
        if ( empty( $url ) ) {
            throw new Exception( 'url required' );
        } else {
            // set cul init
            $ch = curl_init($url);
            // set HEADER curl parame
            if ( empty ( $token ) ) {
                  curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-type: application/json'));
            }else{
                  curl_setopt($ch, CURLOPT_HTTPHEADER, array('X-Auth-Token:'.$token, 'Content-type: application/json'));
            }
            //curl option PUT
            curl_setopt($ch, CURLOPT_CUSTOMREQUEST, 'PUT');
            curl_setopt($ch, CURLOPT_FAILONERROR, false);
            curl_setopt($ch, CURLOPT_POSTFIELDS, $param);
            curl_setopt($ch, CURLOPT_POST, true);
            curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, FALSE);
            curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
            curl_setopt($ch, CURLINFO_HEADER_OUT, true);
            //curl
            $var = curl_exec($ch);

            if($var === false){
                $curl_error = curl_error($ch);
                $curl_errno = curl_errno($ch);
                curl_close($ch);
                throw new Exception( 'curl_error:' . $curl_error . ',curl_errno:' . $curl_errno);
            }

            //curl
            curl_close($ch);
            $ret = array();
            $ret = json_decode($var, true);

            // if json error occured, throw error
            if (json_last_error() !== JSON_ERROR_NONE) {
                $json_last_error_no = json_last_error();
                $json_last_error_code = OscCommon::getJsonErrorCode($json_last_error_no);

                throw new Exception( 'json_last_error:' . $json_last_error_no . ',json_last_error_code:' . $json_last_error_code . ',ret:' . $var);
            }

        }

        return $ret;
    }
    /**
     * REST DELETE
     *
     * @param  <String>       $url
     * @param  <String>       $token
     * @param  <String/Array> $param
     *
     * @return <Array>  OpenStack response
     * @throws Exception
     */
    public function rest_delete($url, $token, $param) {

        $param_string = '';
        if(is_array($param)){
            $param_string = json_encode($param, true);
        } else {
            $param_string = $param;
        }

        //init
        $ret = array();
        //check
        if ( empty( $url ) ) {
            throw new Exception( 'url required' );
        } else {
            // set cul init
            $ch = curl_init($url);
            // set HEADER curl parame
            if ( empty ( $token ) ) {
                  curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-type: application/json'));
            }else{
                  curl_setopt($ch, CURLOPT_HTTPHEADER, array('X-Auth-Token:'.$token, 'Content-type: application/json'));
            }
            //curl option DELETE
            curl_setopt($ch, CURLOPT_CUSTOMREQUEST, 'DELETE');
            curl_setopt($ch, CURLOPT_FAILONERROR, false);

            if(!is_array($param) and !empty($param)){
                curl_setopt($ch, CURLOPT_POSTFIELDS, $param);
                curl_setopt($ch, CURLOPT_POST, true);
            }
            curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, FALSE);
            curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
            curl_setopt($ch, CURLINFO_HEADER_OUT, true);
            //curl
            $var = curl_exec($ch);

            if($var === false){
                $curl_error = curl_error($ch);
                $curl_errno = curl_errno($ch);
                curl_close($ch);
                throw new Exception( 'curl_error:' . $curl_error . ',curl_errno:' . $curl_errno);
            }

            // get HTTP status
            $curl_getinfoOut = curl_getinfo($ch);
            $httpStatus = intval($curl_getinfoOut['http_code']);

            //curl
            curl_close($ch);
            $ret = array();
            $ret = json_decode($var, true);

            // if json error occured, throw error
            if (json_last_error() !== JSON_ERROR_NONE) {
                $json_last_error_no = json_last_error();
                $json_last_error_code = OscCommon::getJsonErrorCode($json_last_error_no);

                throw new Exception( 'json_last_error:' . $json_last_error_no . ',json_last_error_code:' . $json_last_error_code . ',ret:' . $var, OscConst::HTTP_ERRCODE_NO + $httpStatus);
            }

        }

        return $ret;
    }

    /**
     * REST UPLOAD (GLANCE)
     *
     * @param  url
     * @param  token
     * @param  method
     * @param  parameter(POST)
     * @return Openstack
     */
    public function rest_upload($url, $token, $method, $param) {

        $param_string = '';
        if(is_array($param)){
            $param_string = json_encode($param, true);
        } else {
            $param_string = $param;
        }

        $message = 'requestId' . "\t" . $this->_requestId . "\t" . 'request  url' . "\t" . $url . "\t" . 'method' . "\t" . $method . "\t" . 'param' . "\t" . $param_string;
        $this->_common->writeInfoLog($this->_common->_getLogData_log4php(OscConst::LOG_STATUS_START, $message, __METHOD__, $this->_common->getCalledMethod(debug_backtrace())));

        //init
        $ret = array();
        //check
        if ( empty( $url ) ) {
            throw new Exception( 'url required' );
        } else {
            // set cul init
            $ch = curl_init($url);
            // set HEADER curl parame
            $que = json_decode($param,true);
            $header = array(
                'X-Auth-Token:' . $token,
                'Content-type: application/json',
                //'x-image-meta-id:' . $que['image']['id'],
                'x-image-meta-name:' . $que['image']['name'],
                'x-image-meta-container_format:' . $que['image']['container_format'],
                'x-image-meta-disk_format:' . $que['image']['disk_format'],
                'x-image-meta-is_public:' . $que['image']['is_public'],
                'x-image-meta-owner:' . $que['image']['owner'],
                'x-image-meta-size:' . $que['image']['size'],
                'x-image-meta-min_ram:' . $que['image']['min_ram'],
                'x-image-meta-min_disk:' . $que['image']['min_disk'],
                'x-glance-api-copy-from:' . $que['image']['copy_from'],
            );
            curl_setopt($ch, CURLOPT_HTTPHEADER, $header);

            $message = 'requestId' . "\t" . $this->_requestId . "\t" . 'curl header ' . "\t" . $url . "\t" . 'header' . "\t" . json_encode($header, true);
            $this->_common->writeInfoLog($this->_common->_getLogData_log4php('', $message, __METHOD__, $this->_common->getCalledMethod(debug_backtrace())));

            //curl option POST
            curl_setopt($ch, CURLOPT_POST, true);
            curl_setopt($ch, CURLOPT_POSTFIELDS, $param);
            curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, FALSE);
            curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
            curl_setopt($ch, CURLINFO_HEADER_OUT, true);
            //curl
            $var = curl_exec($ch);

            $message = 'requestId' . "\t" . $this->_requestId . "\t" . 'curl op  url' . "\t" . $url . "\t" . 'curl_getinfo' . "\t" . json_encode(curl_getinfo($ch), true);
            $this->_common->writeInfoLog($this->_common->_getLogData_log4php('', $message, __METHOD__, $this->_common->getCalledMethod(debug_backtrace())));

            if($var === false){
                $curl_error = curl_error($ch);
                $curl_errno = curl_errno($ch);
                curl_close($ch);
                $message = ' response url' . "\t" . $url . "\t" . 'var' . "\t" . $var . "\t" . 'curl_error' . "\t" . $curl_error . "\t" . 'curl_errno' . "\t" . $curl_errno;
                $this->_common->writeErrorLog($this->_common->_getLogData_log4php(OscConst::LOG_STATUS_ERROR, $message, __METHOD__, $this->_common->getCalledMethod(debug_backtrace())));
                throw new Exception( 'curl_error:' . $curl_error . ',curl_errno:' . $curl_errno);
            }

            //curl
            curl_close($ch);
            $ret = json_decode($var, true);

            // if json error occured, throw error
            if (json_last_error() !== JSON_ERROR_NONE) {
                $json_last_error_no = json_last_error();
                $json_last_error_code = OscCommon::getJsonErrorCode($json_last_error_no);

                $message = ' response url' . "\t" . $url . "\t" . 'var' . "\t" . $var . "\t" . 'json_last_error' . "\t" . $json_last_error_no . "\t" . 'json_last_error_code' . "\t" . $json_last_error_code;
                $this->_common->writeErrorLog($this->_common->_getLogData_log4php(OscConst::LOG_STATUS_ERROR, $message, __METHOD__, $this->_common->getCalledMethod(debug_backtrace())));
                throw new Exception( 'json_last_error:' . $json_last_error_no . ',json_last_error_code:' . $json_last_error_code . ',ret:' . $var);
            }

        }

        $message = 'requestId' . "\t" . $this->_requestId . "\t" . 'response url' . "\t" . $url . "\t" . 'var' . "\t" . $var;
        $this->_common->writeInfoLog($this->_common->_getLogData_log4php(OscConst::LOG_STATUS_COMPLATE, $message, __METHOD__, $this->_common->getCalledMethod(debug_backtrace())));

        return $ret;
    }

    /**
     * REST UPDATE (GLANCE)
     *
     * @param  url
     * @param  token
     * @param  method
     * @param  parameter(POST)
     * @return Openstack
     */
    public function rest_update($url, $token, $method, $param) {

        $param_string = '';
        if(is_array($param)){
            $param_string = json_encode($param, true);
        } else {
            $param_string = $param;
        }

        $message = 'requestId' . "\t" . $this->_requestId . "\t" . 'request  url' . "\t" . $url . "\t" . 'method' . "\t" . $method . "\t" . 'param' . "\t" . $param_string;
        $this->_common->writeInfoLog($this->_common->_getLogData_log4php(OscConst::LOG_STATUS_START, $message, __METHOD__, $this->_common->getCalledMethod(debug_backtrace())));

        //init
        $ret = array();
        //check
        if ( empty( $url ) ) {
            throw new Exception( 'url required' );
        } else {
            // set cul init
            $ch = curl_init($url);
            // set HEADER curl parame
            $que = json_decode($param,true);
            $header = array(
                'X-Auth-Token:' . $token,
                'Content-type: application/json',
                'x-glance-registry-purge-props: false',
                //'x-image-meta-id:' . $que['id'],
                'x-image-meta-name:' . $que['name'],
                'x-image-meta-container_format:' . $que['container_format'],
                'x-image-meta-disk_format:' . $que['disk_format'],
                'x-image-meta-is_public:' . $que['is_public'],
                'x-image-meta-owner:' . $que['owner'],
                'x-image-meta-size:' . $que['size'],
                'x-image-meta-min_ram:' . $que['min_ram'],
                'x-image-meta-min_disk:' . $que['min_disk'],
            );
            curl_setopt($ch, CURLOPT_HTTPHEADER, $header);
            //curl option PUT
            curl_setopt($ch, CURLOPT_CUSTOMREQUEST, 'PUT');
            curl_setopt($ch, CURLOPT_FAILONERROR, false);
            curl_setopt($ch, CURLOPT_POSTFIELDS, $param);
            curl_setopt($ch, CURLOPT_POST, false);
            curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, FALSE);
            curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
            curl_setopt($ch, CURLINFO_HEADER_OUT, true);
            //curl
            $var = curl_exec($ch);

            $message = 'requestId' . "\t" . $this->_requestId . "\t" . 'curl op  url' . "\t" . $url . "\t" . 'curl_getinfo' . "\t" . json_encode(curl_getinfo($ch), true);
            $this->_common->writeInfoLog($this->_common->_getLogData_log4php('', $message, __METHOD__, $this->_common->getCalledMethod(debug_backtrace())));

            if($var === false){
                $curl_error = curl_error($ch);
                $curl_errno = curl_errno($ch);
                curl_close($ch);
                $message = ' response url' . "\t" . $url . "\t" . 'var' . "\t" . $var . "\t" . 'curl_error' . "\t" . $curl_error . "\t" . 'curl_errno' . "\t" . $curl_errno;
                $this->_common->writeErrorLog($this->_common->_getLogData_log4php(OscConst::LOG_STATUS_ERROR, $message, __METHOD__, $this->_common->getCalledMethod(debug_backtrace())));
                throw new Exception( 'curl_error:' . $curl_error . ',curl_errno:' . $curl_errno);
            }

            //curl
            curl_close($ch);
            $ret = array();
            $ret = json_decode($var, true);

            // if json error occured, throw error
            if (json_last_error() !== JSON_ERROR_NONE) {
                $json_last_error_no = json_last_error();
                $json_last_error_code = OscCommon::getJsonErrorCode($json_last_error_no);

                $message = ' response url' . "\t" . $url . "\t" . 'var' . "\t" . $var . "\t" . 'json_last_error' . "\t" . $json_last_error_no . "\t" . 'json_last_error_code' . "\t" . $json_last_error_code;
                $this->_common->writeErrorLog($this->_common->_getLogData_log4php(OscConst::LOG_STATUS_ERROR, $message, __METHOD__, $this->_common->getCalledMethod(debug_backtrace())));
                throw new Exception( 'json_last_error:' . $json_last_error_no . ',json_last_error_code:' . $json_last_error_code . ',ret:' . $var);
            }

        }

        $message = 'requestId' . "\t" . $this->_requestId . "\t" . 'response url' . "\t" . $url . "\t" . 'var' . "\t" . $var;
        $this->_common->writeInfoLog($this->_common->_getLogData_log4php(OscConst::LOG_STATUS_COMPLATE, $message, __METHOD__, $this->_common->getCalledMethod(debug_backtrace())));

        return $ret;
    }
}
