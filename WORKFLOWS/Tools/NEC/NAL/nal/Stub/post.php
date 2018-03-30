<?php

$result['id'] = '100';

header( "Content-Type: application/json; charset=utf-8" );
print json_encode( $result );