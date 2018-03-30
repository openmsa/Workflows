<?php
/**
 * 1.SYSTEM   :
 * 2.FUNCTION : OpenStack Client nova_servers
 *
 * @version $Id: $
 */
require_once dirname(__FILE__). '/NovaServiceCatalog.php';
require_once dirname(__FILE__). '/../base/OscClientBase.php';
require_once dirname(__FILE__). '/../KeyStoneClient/OscTokens.php';

class UsageReports extends OscClientBase{

    const SERVER_ACTION_RESUME          = 'resume';
    const SERVER_ACTION_RESETNETWORK    = 'resetNetwork';
    const SERVER_ACTION_SUSPEND         = 'suspend';
    const SERVER_ACTION_REBOOT          = 'reboot';
    const SERVER_ACTION_RESIZE          = 'resize';
    const SERVER_ACTION_CONFIRMRESIZE   = 'confirmResize';
    const SERVER_ACTION_OS_STOP         = 'os-stop';
    const SERVER_ACTION_OS_START        = 'os-start';
    const SERVER_ACTION_GETCONSOLE      = 'os-getVNCConsole';

    const SERVER_STATUS_ACTIVE          = 'ACTIVE';
    const SERVER_STATUS_ERROR           = 'ERROR';
    const SERVER_STATUS_SUSPEND         = 'SUSPENDED';
    const SERVER_STATUS_PAUSE           = 'PAUSED';
    const SERVER_STATUS_RESIZE          = 'RESIZE';
    const SERVER_STATUS_VERIFY_RESIZE   = 'VERIFY_RESIZE';
    const SERVER_STATUS_SHUTOFF         = 'SHUTOFF';

    const SERVER_REBOOT_TYPE_SOFT       = 'SOFT';
    const SERVER_REBOOT_TYPE_HARD       = 'HARD';

    const SERVER_ITEM_NOT_FOUND         = 'itemNotFound';

    const SERVER_TASK_STATE_NULL        = null;

    const SERVER_TYPE_CONSOLE_NOVNC     = 'novnc';

    const SERVER_RESPONSE_BADREQUEST         = 'badRequest';
    const SERVER_RESPONSE_ITEMNOTFOUND       = 'itemNotFound';
    const SERVER_RESPONSE_CONFLICTINGREQUEST = 'conflictingRequest';
    const SERVER_RESPONSE_COMPUTEFAULT       = 'computeFault';


    // get endpoint
    public static function getEndpoints($tenantName=null, $tenantId=null, $endpoint=array(), $project_id=null){

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

        return array( $endPointArray, $tokenId );
    }

    /**
     * referCPU storage used
     *
     * @param  <Array>  $endPointArray
     * @param  <String> $tenant_name
     *
     * @return <Array>  OpenStack response
     * @throws Exception
     */
    public function getUsageReport($endPointArray,$tenant_name, $token_id){

        //REST API
        $OscRest = new OscRest();

        $resp = array();

        //get token
        $token_id = OscCommon::getTokenId($endPointArray);

        //endpoint
        $url = NovaServiceCatalog::getNovaEndpoint($endPointArray);

        //endpoint
        if ( !strlen($url) ){
            throw new Exception( OscConst::Exception_message(__METHOD__, OscConst::Exce_Message_08, ''));
        }

        //REST URL
        $url .= '/os-simple-tenant-usage/' . $tenant_name;

        try{
            // REST
            $resp = $OscRest->rest_get($url, $token_id, array() );

        } catch ( Exception $e ) {
            throw new Exception( OscConst::Exception_message(__METHOD__, OscConst::Exce_Message_02, $e),  $e->getCode(), $e);
        }

        //OpenStack
        if( !(is_array($resp) && array_key_exists('tenant_usage', $resp)) ) {
            throw new Exception( OscConst::Exception_message(__METHOD__, OscConst::Exce_Message_12, (is_array($resp) ? json_encode($resp) : $resp)));
        }

        return $resp;
    }

    /**
     * list CPU,storage used
     *
     * @param  <Array>  $endPointArray
     *
     * @return <Array>  OpenStack response
     * @throws Exception
     */
    public function listUsageReport($endPointArray, $token_id, $region_id){

        //REST API
        $OscRest = new OscRest();

        $resp = array();

        //endpoint
        $url = NovaServiceCatalog::getNovaEndpoint($endPointArray, $region_id);

        //endpoint
        if ( !strlen($url) ){
            throw new Exception( OscConst::Exception_message(__METHOD__, OscConst::Exce_Message_08, ''));
        }

        //REST URL
        $url .= '/os-simple-tenant-usage?detailed=1';

        try{
            // REST
            $resp = $OscRest->rest_get($url, $token_id, array() );

        } catch ( Exception $e ) {
            throw new Exception( OscConst::Exception_message(__METHOD__, OscConst::Exce_Message_02, $e),  $e->getCode(), $e);
        }

        //OpenStack
        if( !(is_array($resp) && array_key_exists('tenant_usages', $resp)) ) {
            throw new Exception( OscConst::Exception_message(__METHOD__, OscConst::Exce_Message_12, (is_array($resp) ? json_encode($resp) : $resp)));
        }

        return $resp;
    }

}
