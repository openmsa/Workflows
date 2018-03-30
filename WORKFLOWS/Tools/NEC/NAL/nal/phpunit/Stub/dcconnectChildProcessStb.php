<?php
require_once dirname(__FILE__) . '/../../Nal/bin/app/dcconnectChildProcess.php';

class dcconnectChildProcessStb extends dcconnectChildProcess {

    protected function error( $code='', $message, $out='' ) {
        throw new Exception( $message );
    }

    protected function success( $data = array() ) {
    }

    protected function _execWimApi( $url, $param='', $httpMethod, $noproxy='' ) {

        $res = array(
            'result' => array(
                'status'     => 'success',
                'error-code' => 'NAL100000',
                'message'    => '',
            ),
            'data' => array(
                          'wim_check_dcconnect' => '1',
                      ),
            'request-id' => '20160708120000000000000',
        );

        return $res;

    }

    protected function _setOutParam(){
    }

    protected function _deleteDirectory(){
    }

    protected function execCheckNal( $retry, $max ) {

        if( isset( $this->_p['no_execCheckNal_flg'] )){
            dcconnectChildProcess::execCheckNal( $retry, $max );
        }
    }

    protected function _makeInFile( $result, $all_flg = '0' ){

        if( isset( $this->_p['no_makeInFile_flg'] )){
            dcconnectChildProcess::_makeInFile( $result, $all_flg );
        }
    }

    protected function callJobCenterForDb( $method = '' ){

        if( isset( $this->_p['no_callJobCen_db_flg'] )){
            dcconnectChildProcess::callJobCenterForDb( $method );
        }

    }

    protected function callJobSchedulerForDb( $method = '' ){

        if( isset( $this->_p['no_callJobSche_db_flg'] )){
            dcconnectChildProcess::callJobSchedulerForDb( $method );
        }

    }

    protected function checkJobCenterForDb( $retry, $max ){

        if( isset( $this->_p['no_checkJobCen_db_flg'] )){
            dcconnectChildProcess::checkJobCenterForDb( $retry, $max );
        }

    }

    protected function checkJobSchedulerForDb( $retry, $max ){

        if( isset( $this->_p['no_checkJobSche_db_flg'] )){
            dcconnectChildProcess::checkJobSchedulerForDb( $retry, $max );
        }

    }

    protected function checkJobCenterNal( $retry, $max ){

        if( isset( $this->_p['no_checkJobCen_nal_flg'] ) ){
            dcconnectChildProcess::checkJobCenterNal( $retry, $max );
        }
    }

    protected function checkJobSchedulerNal( $retry, $max ){

        if( isset( $this->_p['no_checkJobSche_nal_flg'] ) ){
            dcconnectChildProcess::checkJobSchedulerNal( $retry, $max );
        }
    }

}