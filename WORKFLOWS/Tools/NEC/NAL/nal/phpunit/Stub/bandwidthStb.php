<?php
require_once dirname(__FILE__) . '/../../Nal/api/app/bandwidth.php';

class bandwidthStb extends bandwidth {

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