<?php
 /* 1.SYSTEM   : OpenG
 * 2.FUNCTION : OpenStack Client nova_flavor
 *
 * @version $Id: OscFlavors.php 2016-03-03 $
 */
require_once dirname(__FILE__). '/NovaServiceCatalog.php';
require_once dirname(__FILE__). '/../base/OscClientBase.php';
require_once dirname(__FILE__). '/../KeyStoneClient/OscTokens.php';

class OscFlavors extends OscClientBase{

    // get endpoint
    public static function getEndpoints($tenantName=null, $tenantId=null, $endpoint=array()){

        $tokens = new OscTokens();

        // endpoint
        if( !empty( $endpoint ) ){
            $userId       = $endpoint['user_id'];
            $userPassword = $endpoint['user_password'];
            $endPoint     = $endpoint['endpoint'];
            $project_id   = $endpoint['admin_tenant_id'];
        }else{
            $userId       = neccsNal_Config::$userId;
            $userPassword = neccsNal_Config::$userPassword;
            $endPoint     = neccsNal_Config::$endPoint;
        }

        $tokenId = $tokens->createToken($userId, $userPassword, $endPoint);
        list( $endPointArray, $tokenId ) = $tokens->getEndpoints($tokenId, $userId, $userPassword, $tenantName, $tenantId, $endPoint, $project_id);

        return array( $endPointArray, $tokenId);
    }

    /**
     * listFlavor
     */
    public function listFlavorsDetail($endPointArray, $token_id, $region_id) {

        //REST API Instantiation
        $OscRest = new OscRest();

        $resp = array();

        // Argument check
        if ( empty( $endPointArray ) ) {
            throw new Exception( OscConst::Exception_message(__METHOD__, OscConst::Exce_Message_01, ''));
        }

        // get endpoint info
        $url = NovaServiceCatalog::getNovaEndpoint($endPointArray, $region_id);

        // check exist endpoint
        if ( empty($url) ){
            // If there is no endpoint, return Error message without authority
            throw new Exception( OscConst::Exception_message(__METHOD__, OscConst::Exce_Message_08, ''));
        }

        //set rest api
        $url .= '/flavors/detail';

        try{
            // REST API
            $resp = $OscRest->rest_get($url, $token_id, array() );

        } catch ( Exception $e ) {
            throw new Exception( OscConst::Exception_message(__METHOD__, OscConst::Exce_Message_02, $e),  $e->getCode(), $e);
        }

        // OpenStack return value check
        if( !(is_array($resp) && array_key_exists('flavors', $resp)) ) {
            throw new Exception( OscConst::Exception_message(__METHOD__, OscConst::Exce_Message_12, (is_array($resp) ? json_encode($resp) : $resp)));
        }

        return $resp;
    }
}
?>
