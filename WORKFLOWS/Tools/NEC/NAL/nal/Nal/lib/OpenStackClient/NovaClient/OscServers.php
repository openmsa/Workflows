<?php
/**
 * 1.SYSTEM   :
 * 2.FUNCTION : OpenStack Client nova_servers処理クラス
 *
 * @version $Id: OscServers.php 2016-03-01 $
 */
require_once ROOT_PATH . '/lib/OpenStackClient/base/OscClientBase.php';
require_once ROOT_PATH . '/lib/OpenStackClient/NovaClient/NovaServiceCatalog.php';

class OscServers extends OscClientBase{

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


    /**
     * サーバー一覧参照
     *
     * @param  <Array>  $endPointArray  :エンドポイント(連想配列)【必須】
     *
     * @return <Array>  OpenStackからの返却レスポンス（JSON値をarray値に変換）
     * @throws Exception
     */
    public function listServers($endPointArray){

        //REST API インスタンス作成
        $OscRest = new OscRest();

        $resp = array();

        //引数確認
        if ( !(is_array( $endPointArray ) && count($endPointArray)) ) {
            throw new Exception( OscConst::Exception_message(__METHOD__, OscConst::Exce_Message_01, ''));
        }

        //トークン取得
        $token_id = OscCommon::getTokenId($endPointArray);

        //endpoint取得
        $url = NovaServiceCatalog::getNovaEndpoint($endPointArray);

        //endpointが存在するかのチェック
        if ( !strlen($url) ){
            //endpointが無い場合は、権限無しとしてErrorメッセージを返す
            throw new Exception( OscConst::Exception_message(__METHOD__, OscConst::Exce_Message_08, ''));
        }

        //REST URL作成
        $url .= '/servers/detail';

        //REST処理
        try{
            $resp = $OscRest->rest_get($url, $token_id, array() );

        } catch ( Exception $e ) {
            throw new Exception( OscConst::Exception_message(__METHOD__, OscConst::Exce_Message_02, $e),  $e->getCode(), $e);
        }

        //OpenStack返却値チェック
        if( !(is_array($resp) && array_key_exists('servers', $resp)) ) {
            throw new Exception( OscConst::Exception_message(__METHOD__, OscConst::Exce_Message_12, (is_array($resp) ? json_encode($resp) : $resp)));
        }

        return $resp;
    }

    /**
     * サーバー詳細参照
     *
     * @param  <Array>  $endPointArray  :エンドポイント(連想配列)【必須】
     * @param  <String> $server_id      :サーバーID　　　　　　　【必須】
     *
     * @return <Array>  OpenStackからの返却レスポンス（JSON値をarray値に変換）
     * @throws Exception
     */
    public function getServer($endPointArray, $server_id){

        //REST API インスタンス作成
        $OscRest = new OscRest();

        $resp = array();

        //引数確認
        if ( !(is_array( $endPointArray ) && count($endPointArray)) || !strlen( $server_id )) {
            throw new Exception( OscConst::Exception_message(__METHOD__, OscConst::Exce_Message_01, ''));
        }

        //トークン取得
        $token_id = OscCommon::getTokenId($endPointArray);

        //endpoint取得
        $url = NovaServiceCatalog::getNovaEndpoint($endPointArray);

        //endpointが存在するかのチェック
        if ( !strlen($url) ){
            //endpointが無い場合は、権限無しとしてErrorメッセージを返す
            throw new Exception( OscConst::Exception_message(__METHOD__, OscConst::Exce_Message_08, ''));
        }

        //REST URL作成
        $url .= '/servers/' . $server_id;

        try{
            // REST実行
            $resp = $OscRest->rest_get($url, $token_id, array() );

        } catch ( Exception $e ) {
            throw new Exception( OscConst::Exception_message(__METHOD__, OscConst::Exce_Message_02, $e),  $e->getCode(), $e);
        }

        //OpenStack返却値チェック
        if( !(is_array($resp) && array_key_exists('server', $resp)) ) {
            throw new Exception( OscConst::Exception_message(__METHOD__, OscConst::Exce_Message_12, (is_array($resp) ? json_encode($resp) : $resp)));
        }

        return $resp;
    }

    /**
     *
     * サーバ作成
     *
     * @param  <Array>  $endPointArray     :エンドポイント(連想配列)【必須】
     * @param  <String> $name              :サーバー名　　　　　　　【必須】
     * @param  <String> $imageRef          :イメージID　　　　　　　【必須】
     * @param  <String> $flavorRef         :フレーバーID　　　　　　【必須】
     * @param  <Array>  $networks          :ネットワーク　　　　　　【必須】※APIリファレンスでは任意だが実際は省略するとエラーになる
     * @param  <Array>  $security_groups   :セキュリティグループ　　【任意】
     * @param  <Array>  $metadata          :メタデータ　　　　　　　【任意】
     * @param  <String> $key_name          :キーペア名　　　　　　　【任意】
     * @param  <String> $availability_zone :アベイラビリティゾーン　【任意】
     * @param  <String> $user_data         :ユーザー定義　　　　　　【任意】
     *
     * @return <Array>  OpenStackからの返却レスポンス（JSON値をarray値に変換）
     * @throws Exception
     */
    public function createServer($endPointArray,
                                 $name,
                                 $imageRef ,
                                 $flavorRef,
                                 $networks,
                                 $security_groups   = null,
                                 $metadata          = null,
                                 $key_name          = null,
                                 $availability_zone = null,
                                 $user_data         = null,
                                 $config_drive      = false) {

        //REST API インスタンス作成
        $OscRest = new OscRest();

        $resp = array();

        //引数確認
        if ( !(is_array( $endPointArray ) && count($endPointArray)) ) {
            throw new Exception( OscConst::Exception_message(__METHOD__, OscConst::Exce_Message_01, ''));
        }

        //トークン取得
        $token_id = OscCommon::getTokenId($endPointArray);


        echo "server catalog -----------------------------\n";
        var_dump($endPointArray);
        echo "server catalog -----------------------------\n";



        //endpoint取得
        $url = NovaServiceCatalog::getNovaEndpoint($endPointArray);

        //endpointが存在するかのチェック
        if ( !strlen($url) ){
            //endpointが無い場合は、権限無しとしてErrorメッセージを返す
            throw new Exception( OscConst::Exception_message(__METHOD__, OscConst::Exce_Message_08, ''));
        }

        //REST URL作成
        $url .= '/servers';

        //リクエストパラメータ設定
        $var = array('server' => array(
                'name'      => $name,
                'imageRef'  => $imageRef,
                'flavorRef' => $flavorRef,
                'networks'  => $networks,
            )
        );

        if(!is_null($security_groups)){
            $var['server']['security_groups'] = $security_groups;
        }

        if(!is_null($metadata)){
            $var['server']['metadata'] = $metadata;
        }

        if (!is_null($key_name)) {
            $var['server']['key_name'] = $key_name;
        }

        if (!is_null($availability_zone)) {
            $var['server']['availability_zone'] = $availability_zone;
        }

        if (!is_null($user_data)) {
            $userDataEncoded = base64_encode($user_data);

            // エンコードに失敗した場合（FALSEが返却された場合）
            if (!$userDataEncoded) {
                throw new Exception('base64 encoding is failed.');
            }

            $var['server']['user_data'] = $userDataEncoded;
        }

        $var['server']['config_drive'] = $config_drive;

        try{


            echo "server create -----------------------------\n";
            var_dump($url);
            var_dump($token_id);
            var_dump(json_encode($var));




            // REST実行
            $resp = $OscRest->rest_post($url, $token_id, json_encode($var) );

            var_dump($resp);
            echo "server create -----------------------------\n";




        } catch ( Exception $e ) {
            throw new Exception( OscConst::Exception_message(__METHOD__, OscConst::Exce_Message_02, $e),  $e->getCode(), $e);
        }

        //OpenStack返却値チェック
        if( !(is_array($resp) && array_key_exists('server', $resp)) ) {
            throw new Exception( OscConst::Exception_message(__METHOD__, OscConst::Exce_Message_12, (is_array($resp) ? json_encode($resp) : $resp)));
        }

        return $resp;
    }

    /**
     * サーバー削除
     * @param  <Array>  $endPointArray     :エンドポイント(連想配列)【必須】
     * @param  <String> $server_id         :サーバーID　　　　　　　【必須】
     * @return 正常時：戻り値無し(null)
     * @throws Exception
     */
    public function deleteServer($endPointArray, $server_id) {

        //REST API インスタンス作成
        $OscRest = new OscRest();

        $resp = array();

        //引数確認
        if ( !(is_array( $endPointArray ) && count($endPointArray)) ) {
            throw new Exception( OscConst::Exception_message(__METHOD__, OscConst::Exce_Message_01, ''));
        }

        //トークン取得
        $token_id = OscCommon::getTokenId($endPointArray);

        //endpoint取得
        $url = NovaServiceCatalog::getNovaEndpoint($endPointArray);

        //endpointが存在するかのチェック
        if ( !strlen($url) ){
            //endpointが無い場合は、権限無しとしてErrorメッセージを返す
            throw new Exception( OscConst::Exception_message(__METHOD__, OscConst::Exce_Message_08, ''));
        }

        //REST URL作成
        $url .= '/servers/' . $server_id;

        try{
            // REST実行
            $resp = $OscRest->rest_delete($url, $token_id, array() );

        } catch ( Exception $e ) {
            throw new Exception( OscConst::Exception_message(__METHOD__, OscConst::Exce_Message_02, $e),  $e->getCode(), $e);
        }

        //OpenStack返却値チェック
        if( !is_null($resp) ) {
            throw new Exception( OscConst::Exception_message(__METHOD__, OscConst::Exce_Message_12, (is_array($resp) ? json_encode($resp) : $resp)));
        }

        return $resp;
    }

    /**
     * サーバー操作
     */
    public function actionServer($endPointArray, $server_id, $actionkey, $bootType=null, $resizedFlavor = null, $consoleType = null){

        //REST API インスタンス作成
        $OscRest = new OscRest();

        $resp = array();

        //引数確認
        if ( !(is_array( $endPointArray ) && count($endPointArray) && strlen($server_id) ) ) {
            throw new Exception( OscConst::Exception_message(__METHOD__, OscConst::Exce_Message_01, ''));
        }

        //トークン取得
        $token_id = OscCommon::getTokenId($endPointArray);

        //endpoint取得
        $url = NovaServiceCatalog::getNovaEndpoint($endPointArray);

        //endpointが存在するかのチェック
        if ( !strlen($url) ){
            //endpointが無い場合は、権限無しとしてErrorメッセージを返す
            throw new Exception( OscConst::Exception_message(__METHOD__, OscConst::Exce_Message_08, ''));
        }

        // REST URL作成
        $url .= '/servers/' . $server_id . '/action';

        // リクエストパラメータ設定
        switch($actionkey){
            case self::SERVER_ACTION_REBOOT:
                $var = array( $actionkey => array( 'type' => $bootType ) );
                break;

            case self::SERVER_ACTION_RESIZE:
                $var = array( $actionkey => array( 'flavorRef' => $resizedFlavor ) );
                break;

            case self::SERVER_ACTION_GETCONSOLE:
                $var = array( $actionkey => array( 'type' => $consoleType ) );
                break;

            default:
                $var = array( $actionkey => null );
                break;
        }

        try{
            // REST実行
            $resp = $OscRest->rest_post( $url, $token_id, json_encode($var) );

        } catch ( Exception $e ) {
            throw new Exception( OscConst::Exception_message(__METHOD__, OscConst::Exce_Message_02, $e),  $e->getCode(), $e);
        }

        //OpenStack返却値チェック
        if($actionkey == self::SERVER_ACTION_GETCONSOLE){

            if( !(is_array($resp) && array_key_exists('console', $resp)) ) {
                throw new Exception( OscConst::Exception_message(__METHOD__, OscConst::Exce_Message_12, (is_array($resp) ? json_encode($resp) : $resp)));
            }

        }else{

            if( !is_null($resp) ) {
                throw new Exception( OscConst::Exception_message(__METHOD__, OscConst::Exce_Message_12, (is_array($resp) ? json_encode($resp) : $resp)));
            }
        }

        return $resp;
    }

    /**
     * インターフェース接続
     */
    public function attachInterface($endPointArray, $server_id, $port_id = null , $net_id = null , $ip_address = null ) {

        //REST API インスタンス作成
        $OscRest = new OscRest();

        $resp = array();

        //引数確認
        if ( !(is_array( $endPointArray ) && count($endPointArray) && strlen($server_id)) ) {
            throw new Exception( OscConst::Exception_message(__METHOD__, OscConst::Exce_Message_01, ''));
        }

        //トークン取得
        $token_id = OscCommon::getTokenId($endPointArray);

        //endpoint取得
        $url = NovaServiceCatalog::getNovaEndpoint($endPointArray);

        //endpointが存在するかのチェック
        if ( !strlen($url) ){
            //endpointが無い場合は、権限無しとしてErrorメッセージを返す
            throw new Exception( OscConst::Exception_message(__METHOD__, OscConst::Exce_Message_08, ''));
        }

        //REST URL作成
        $url .= '/servers/' . $server_id . '/os-interface';

        // リクエストパラメータ設定
        $var = array('interfaceAttachment' => array());

        if (strlen($port_id)){

            $var['interfaceAttachment'] += array('port_id'  => $port_id);

        } elseif (strlen($net_id)) {

            $var['interfaceAttachment'] += array('net_id'  => $net_id);

        } elseif (strlen($ip_address)) {

            $var['interfaceAttachment'] += array('fixed_ips' =>
                array(
                    array('ip_address'  => $ip_address)
                )
            );
        }

        try{
            // REST実行
            $resp = $OscRest->rest_post($url, $token_id, json_encode($var) );

var_dump($resp);

        } catch ( Exception $e ) {
            throw new Exception( OscConst::Exception_message(__METHOD__, OscConst::Exce_Message_02, $e),  $e->getCode(), $e);
        }

        //OpenStack返却値チェック
        if( !(is_array($resp) && array_key_exists('interfaceAttachment', $resp)) ) {
            throw new Exception( OscConst::Exception_message(__METHOD__, OscConst::Exce_Message_12, (is_array($resp) ? json_encode($resp) : $resp)));
        }

        return $resp;
    }

    /**
     * インタフェース解除
     */
    public function detachInterface($endPointArray, $server_id, $port_id) {

        //REST API インスタンス作成
        $OscRest = new OscRest();

        $resp = array();

        //引数確認
        if ( empty( $endPointArray ) || !strlen($server_id) || !strlen($port_id) ) {
            throw new Exception( OscConst::Exception_message(__METHOD__, OscConst::Exce_Message_01, ''));
        }

        //トークン取得
        $token_id = OscCommon::getTokenId($endPointArray);

        //endpoint取得
        $url = NovaServiceCatalog::getNovaEndpoint($endPointArray);

        //endpointが存在するかのチェック
        if ( !strlen($url) ){
            //endpointが無い場合は、権限無しとしてErrorメッセージを返す
            throw new Exception( OscConst::Exception_message(__METHOD__, OscConst::Exce_Message_08, ''));
        }

        //REST URL作成
        $url .= '/servers/' . $server_id . '/os-interface/' . $port_id;

        try{
            // REST実行
            $resp = $OscRest->rest_delete($url, $token_id, array() );

        } catch ( Exception $e ) {
            throw new Exception( OscConst::Exception_message(__METHOD__, OscConst::Exce_Message_02, $e),  $e->getCode(), $e);
        }

        //OpenStack返却値チェック
        if( !is_null($resp) ) {
            throw new Exception( OscConst::Exception_message(__METHOD__, OscConst::Exce_Message_12, (is_array($resp) ? json_encode($resp) : $resp)));
        }

        return $resp;
    }

    /**
     * インタフェース一覧参照
     */
    public function listInterfaces($endPointArray, $server_id) {

        //REST API インスタンス作成
        $OscRest = new OscRest();

        $resp = array();

        //引数確認
        if ( empty( $endPointArray ) || !strlen($server_id)) {
            throw new Exception( OscConst::Exception_message(__METHOD__, OscConst::Exce_Message_01, ''));
        }

        //トークン取得
        $token_id = OscCommon::getTokenId($endPointArray);

        //endpoint取得
        $url = NovaServiceCatalog::getNovaEndpoint($endPointArray);

        //endpointが存在するかのチェック
        if ( !strlen($url) ){
            //endpointが無い場合は、権限無しとしてErrorメッセージを返す
            throw new Exception( OscConst::Exception_message(__METHOD__, OscConst::Exce_Message_08, ''));
        }

        //REST URL作成
        $url .= '/servers/' . $server_id . '/os-interface';

        try{
            // REST実行
            $resp = $OscRest->rest_get($url, $token_id, array() );

        } catch ( Exception $e ) {
            throw new Exception( OscConst::Exception_message(__METHOD__, OscConst::Exce_Message_02, $e),  $e->getCode(), $e);
        }

        //OpenStack返却値チェック
        if( !(is_array($resp) && array_key_exists('interfaceAttachments', $resp)) ) {
            throw new Exception( OscConst::Exception_message(__METHOD__, OscConst::Exce_Message_12, (is_array($resp) ? json_encode($resp) : $resp)));
        }

        return $resp;
    }

    /**
     * サーバーリビルド
     */
    public function rebuildServer($endPointArray, $server_id, $image_id, $host_name){

        //REST API インスタンス作成
        $OscRest = new OscRest();

        $resp = array();

        //引数確認
        if ( empty( $endPointArray ) || !strlen( $server_id ) || !strlen( $image_id ) || !strlen( $host_name ) ) {
            throw new Exception( OscConst::Exception_message(__METHOD__, OscConst::Exce_Message_01, ''));
        }

        //トークン取得
        $token_id = OscCommon::getTokenId($endPointArray);

        //endpoint取得
        $url = NovaServiceCatalog::getNovaEndpoint($endPointArray);

        //endpointが存在するかのチェック
        if ( !strlen($url) ){
            //endpointが無い場合は、権限無しとしてErrorメッセージを返す
            throw new Exception( OscConst::Exception_message(__METHOD__, OscConst::Exce_Message_08, ''));
        }

        //REST URL作成
        $url .= '/servers/' . $server_id . '/action';

        //リクエストパラメータ設定
        $var = array( 'rebuild' => array('imageRef'=>$image_id, 'name'=>$host_name) );

        try{
            // REST実行
            $resp = $OscRest->rest_post( $url, $token_id, json_encode($var) );

        } catch ( Exception $e ) {
            throw new Exception( OscConst::Exception_message(__METHOD__, OscConst::Exce_Message_02, $e),  $e->getCode(), $e);
        }

        return $resp;
    }

    /**
     * サーバーリセット(reset-state)
     */
    public function resetStateServer($endPointArray, $server_id){

        //REST API インスタンス作成
        $OscRest = new OscRest();

        $resp = array();

        //引数確認
        if ( empty( $endPointArray ) || !strlen( $server_id ) ) {
            throw new Exception( OscConst::Exception_message(__METHOD__, OscConst::Exce_Message_01, ''));
        }

        //トークン取得
        $token_id = OscCommon::getTokenId($endPointArray);

        //endpoint取得
        $url = NovaServiceCatalog::getNovaEndpoint($endPointArray);

        //endpointが存在するかのチェック
        if ( !strlen($url) ){
            //endpointが無い場合は、権限無しとしてErrorメッセージを返す
            throw new Exception( OscConst::Exception_message(__METHOD__, OscConst::Exce_Message_08, ''));
        }

        //REST URL作成
        $url .= '/servers/' . $server_id . '/action';

        //リクエストパラメータ設定
        $var = array( 'os-resetState' => array('state' => 'active') );

        try{
            // REST実行
            $resp = $OscRest->rest_post( $url, $token_id, json_encode($var) );

        } catch ( Exception $e ) {
            throw new Exception( OscConst::Exception_message(__METHOD__, OscConst::Exce_Message_02, $e),  $e->getCode(), $e);
        }

        return $resp;
    }

    /**
     *
     * サーバー強制削除(FORCE-DELETE)
     *
     */
    public function forceDeleteServer($endPointArray, $server_id){

        //REST API インスタンス作成
        $OscRest = new OscRest();

        $resp = array();

        //引数確認
        if ( empty( $endPointArray ) || !strlen( $server_id ) ) {
            throw new Exception( OscConst::Exception_message(__METHOD__, OscConst::Exce_Message_01, ''));
        }

        //トークン取得
        $token_id = OscCommon::getTokenId($endPointArray);

        //endpoint取得
        $url = NovaServiceCatalog::getNovaEndpoint($endPointArray);

        //endpointが存在するかのチェック
        if ( !strlen($url) ){
            //endpointが無い場合は、権限無しとしてErrorメッセージを返す
            throw new Exception( OscConst::Exception_message(__METHOD__, OscConst::Exce_Message_08, ''));
        }

        //REST URL作成
        $url .= '/servers/' . $server_id . '/action';

        //リクエストパラメータ設定
        $var = array( 'forceDelete' => null );

        try{
            // REST実行
            $resp = $OscRest->rest_post( $url, $token_id, json_encode($var) );

        } catch ( Exception $e ) {
            throw new Exception( OscConst::Exception_message(__METHOD__, OscConst::Exce_Message_02, $e),  $e->getCode(), $e);
        }

        return $resp;
    }

}
