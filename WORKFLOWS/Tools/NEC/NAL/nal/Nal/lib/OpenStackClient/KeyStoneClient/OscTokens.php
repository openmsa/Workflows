<?php
/**
 * 1.SYSTEM   : OpenG
 * 2.FUNCTION : OpenStack Client Keystone_token
 *
 * @version $Id: $
 */
require_once dirname(__FILE__). '/../base/OscClientBase.php';

class OscTokens extends OscClientBase{

    /**
     * construct
     */
    public function __construct() {
    }

    /**
     * create basic token
     *
     * @param  <String> $user_name
     * @param  <String> $password
     * @param  <String> $endPoint
     *
     * @return <String>token ID
     * @throws Exception
     */
    public function createToken($user_name, $password, $endPoint) {

        //REST
        $OscRest = new OscRest();

        $resp = array();

        //check
        if( empty( $user_name ) || empty( $password) ){
            throw new Exception( OscConst::Exception_message(__METHOD__ , OscConst::Exce_Message_01, ''));
        }

        $url = $endPoint . '/auth/tokens';

        $param = json_encode(
                     array(
                         'auth' => array(
                             'identity' => array(
                                 'methods' => array(
                                     'password',
                                 ),
                                 'password' => array(
                                     'user' => array(
                                         'domain' => array(
                                             'name' => 'Default',
                                         ),
                                         'name' => $user_name,
                                         'password' => $password,
                                     ),
                                 ),
                             ),
                         ),
                     )
        );

        try{

            list( $header, $resp ) = $OscRest->rest_post($url, '', $param);

        } catch ( Exception $e ) {
            throw new Exception( OscConst::Exception_message(__METHOD__, OscConst::Exce_Message_03, $e ), $e->getCode(), $e);
        }
        //OpenStack
        if(!array_key_exists('token', $resp)){
            throw new Exception( OscConst::Exception_message(__METHOD__, OscConst::Exce_Message_09, ''));
        }

        //get basic token ID
        $token_id = OscCommon::getTokenId( $header );

        return  $token_id;
    }

    /**
     * get endpoint
     *
     * @param  <String> $token_id
     * @param  <String> $user_name
     * @param  <String> $password
     * @param  <String> $tenant_name
     * @param  <String> $tenant_id
     * @param  <String> $endPoint
     *
     * @return <Array>  JSON
     * @throws Exception
     */
    public function getEndpoints($token_id, $user_name, $password, $tenant_name=null, $tenant_id=null, $endPoint, $project_id=null) {

        //REST API
        $OscRest = new OscRest();

        $resp = array();

        //check
        if( !strlen( $token_id ) || !strlen( $user_name ) || !strlen( $password ) || (!strlen( $tenant_name ) && !strlen($tenant_id)) || !strlen( $project_id )){
            throw new Exception( OscConst::Exception_message(__METHOD__, OscConst::Exce_Message_01, ''));
        }

        //REST URL
        $url = $endPoint . '/auth/tokens';

        //REST
        try{
            //POST
            $tokenArray = array(
                             'auth' => array(
                                 'identity' => array(
                                     'methods' => array(
                                         'password',
                                     ),
                                     'password' => array(
                                         'user' => array(
                                             'domain' => array(
                                                 'name' => 'Default',
                                             ),
                                             'name' => $user_name,
                                             'password' => $password,
                                         ),
                                     ),
                                 ),
                                 'scope' => array(
                                     'project' => array(
                                         'id' => $project_id,
                                     ),
                                 ),
                             ),
                         );

            // REST
            list( $header, $resp ) = $OscRest->rest_post($url, $token_id, json_encode($tokenArray));

        } catch ( Exception $e ) {
            throw new Exception( OscConst::Exception_message(__METHOD__, OscConst::Exce_Message_03, $e),  $e->getCode(), $e);
        }

        if(empty( $resp)){
            throw new Exception( OscConst::Exception_message(__METHOD__, OscConst::Exce_Message_09 , ''));
        }

        //get basic token ID
        $token_id = OscCommon::getTokenId( $header );

        return array( $resp, $token_id );
    }
}
?>
