<?php
require_once dirname(__FILE__) . '/../../Nal/bin/app/serviceIPv6AddChildProcess.php';

class serviceIPv6AddChildProcessStb extends serviceIPv6AddChildProcess {

    protected function error( $code='', $message, $out='' ) {
        throw new Exception( $message );
    }

    protected function success( $data = array() ) {
    }

    protected function _setOutParam(){
    }

    protected function callJobCenterForDb( $method = '' ){

        if( isset( $this->_p['no_callJobCen_db_flg'] )){
            serviceIPv6AddChildProcess::callJobCenterForDb( $method );
        }

    }

    protected function callJobSchedulerForDb( $method = '' ){

        if( isset( $this->_p['no_callJobSche_db_flg'] )){
            serviceIPv6AddChildProcess::callJobSchedulerForDb( $method );
        }

    }

}