<?php

if( $_SERVER['REQUEST_METHOD'] === 'GET' ){

    $uri      = explode( '/', $_SERVER['REQUEST_URI'] );
    $scenario = isset( $uri[6] ) ? $uri[6] : '';
    $pieces = explode("?", $scenario);

    $result = file_get_contents( 'https://127.0.0.1/nalapi/Stub/'. $pieces[0]. '/' );

}else if( $_SERVER['REQUEST_METHOD'] === 'POST' ){

    $result = file_get_contents( 'https://127.0.0.1/nalapi/Stub/post.php' );

}else if( $_SERVER['REQUEST_METHOD'] === 'PUT' ){

    $result = file_get_contents( 'https://127.0.0.1/nalapi/Stub/put.php' );

}else{

    $result = file_get_contents( 'https://127.0.0.1/nalapi/Stub/delete.php' );
}

header( "Content-Type: application/json; charset=utf-8" );
print $result;