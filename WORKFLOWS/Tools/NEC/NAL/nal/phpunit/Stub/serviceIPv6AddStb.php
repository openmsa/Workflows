<?php
require_once dirname(__FILE__) . '/../../Nal/api/app/serviceIPv6Add.php';

class serviceIPv6AddStb extends serviceIPv6Add {

    protected function _execApi( $url, $param='', $noproxy='' ) {
        return array();
    }

    protected function success( $data = array() ) {
        return;
    }

    protected function error( $code='', $massage, $out = array() ) {
        return;
    }
}