<?php
/**
 * 1.SYSTEM   :
 * 2.FUNCTION : OpenStack Client
 *
 * @version $Id:$
 */

class OscCommon {

    /**
     * get token ID
     */
    public static function getTokenId($header){

        $array_header = array();
        foreach (explode("\n", $header) as $line) {
            if( strpos( $line, ":" ) === false ){
                continue;
            }

            list( $name, $value ) = explode( ":", $line, 2 );
            $value = ltrim( $value );

            $array_header[$name]  = $value;
        }

        $tokenId = isset( $array_header['X-Subject-Token'] ) ? str_replace( array("\r\n", "\r", "\n"), '', $array_header['X-Subject-Token'] ): '';

        if(!strlen( $tokenId)){
            throw new Exception( OscConst::Exception_message(__METHOD__, OscConst::Exce_Message_06 , ''));
        }

        return $tokenId;
    }

    // endpoint(VIM)
    public static function getEndpoints($tenantName=null, $tenantId=null){

        echo $tenantName . "\n";
        echo $tenantId . "\n";
        $tokens = new OscTokens();

        $userId       = ApiConfig::$userId;
        $userPassword = ApiConfig::$userPassword;
        $endPoint     = ApiConfig::$endPoint;

        $tokenId = $tokens->createToken($userId, $userPassword, $endPoint);
        $endPointArray =$tokens->getEndpoints($tokenId, $userId, $userPassword, $tenantName, $tenantId, $endPoint);

        return $endPointArray;
    }

    // endpoint(IaaS)
    public static function getIaaSEndpoints($tenantName=null, $tenantId=null){

        echo $tenantName . "\n";
        echo $tenantId . "\n";
        $tokens = new OscTokens();

        $userId       = ApiConfig::$IaaSuserId;
        $userPassword = ApiConfig::$IaaSuserPassword;
        $endPoint     = ApiConfig::$IaaSendPoint;

        $tokenId = $tokens->createToken($userId, $userPassword, $endPoint);
        $endPointArray =$tokens->getEndpoints($tokenId, $userId, $userPassword, $tenantName, $tenantId, $endPoint);

        return $endPointArray;
    }

    /**
     * Get json error code
     *
     * @return : json error code
     *
     */
    public static function getJsonErrorCode($json_error_no) {

        $jsonErrorCode = 'JSON UNKNOWN ERROR';

        switch ($json_error_no) {

            case JSON_ERROR_NONE:
                $jsonErrorCode = 'JSON_ERROR_NONE';
                break;
            case JSON_ERROR_DEPTH:
                $jsonErrorCode = 'JSON_ERROR_DEPTH';
                break;
            case JSON_ERROR_STATE_MISMATCH:
                $jsonErrorCode = 'JSON_ERROR_STATE_MISMATCH';
                break;
            case JSON_ERROR_CTRL_CHAR:
                $jsonErrorCode = 'JSON_ERROR_CTRL_CHAR';
                break;
            case JSON_ERROR_SYNTAX:
                $jsonErrorCode = 'JSON_ERROR_SYNTAX';
                break;
            case JSON_ERROR_UTF8:
                $jsonErrorCode = 'JSON_ERROR_UTF8';
                break;
            default:
                break;

        }

        return $jsonErrorCode;
    }

}
