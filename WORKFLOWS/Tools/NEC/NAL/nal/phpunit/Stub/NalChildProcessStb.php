<?php
require_once dirname(__FILE__) . '/../../Nal/bin/NalChildProcess.php';

class NalChildProcessStb extends NalChildProcess {
    protected function testpost() {
    }
    protected function error( $code, $message, $out='' ) {
    }
    protected function execCheckJob( $retry, $max ) {
    }
}