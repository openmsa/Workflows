<?php
$result = array( '0' => array( 'dc_id' => '1234', 'dc_name'=>'dc_1' ), '1' => array( 'dc_id' => '4321', 'dc_name'=>'dc_2' ) );

header( "Content-Type: application/json; charset=utf-8" );
print json_encode( $result );