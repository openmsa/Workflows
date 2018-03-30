<?php

// spyc ( for YAML )
require_once BASE_PHPLIB_DIR . 'spyc.php5';

// 基盤モジュール
require_once BASE_LIB_DIR . 'Page/Page_API.php';

// サービスモジュール
require_once LIB_DIR . 'Bo.php';

class APICommon {

    // ****************************************************
    // コンストラクタ
    // ****************************************************
    function __construct( $params ){
        $this->params = $params;
        return;
    }

    /******************************************************
    * 処理実行
    * in  : なし
    * out : code   : 正常 : 0
    *                異常 : -1
    *       params : ユーザ定義処理実行結果
    ******************************************************/
    function setproc(){
        // 初期処理
        $code = $this->_init();
        if( $code < 0 ){
            $this->setError( '99', __METHOD__.__LINE__, 'init err', '' );
            return array( 'code' => $code, 'params' => $this->params );
        }

        // 文字コード変換 UTF-8 → EUC-JP
        $this->chgDecode(0);

        // API実行 
        $ret = $this->usrproc2();
        $code = $ret['code'];

        // 一括文字変換 EUC-JP => UTF-8
        $this->chgDecode(1);

        return array( 'code' => $code, 'params' => $this->params );
    }

    /******************************************************
    * 文字コード変換 UTF-8 <-> EUC-JP
    * in  : flg    : 0 : UTF-8  => EUC-JP
    *                1 : EUC-JP => UTF-8
    * out : code   : 正常 : 0
    *                異常 : -1
    *       params : ユーザ定義処理実行結果
    ******************************************************/
    function chgDecode( $flg = 0 ) {

        // 一括文字変換 UTF-8 => EUC-JP
        $ses = $this->_get( 'session' );

        if( $flg === 0 ){
            $ses = $this->chgCodeArray( $ses, 'euc-jp', 'utf-8' );
        }else{
            $ses = $this->chgCodeArray( $ses, 'utf-8', 'euc-jp' );
        }
        $this->setSession( $ses );

        return array( 'code' => 0, 'params' => $this->params);
    }

    /******************************************************
    * 初期処理
    * in  : なし
    * out : code   : 正常 : 0
    *                異常 : -1
    *       params : ユーザ定義処理実行結果
    ******************************************************/
    protected function _init(){
        // http header を設定
        $this->params['_header'] = $this->_get('env', 'header');

        return 0;
    }

    /******************************************************
    * 実行API判定
    * in  : なし
    * out : code   : 正常 : 0
    *                異常 : -1
    *       params : ユーザ定義処理実行結果
    ******************************************************/
    function getExecAPI(){
        $env       = $this->_get( 'env', 'ResMetCheck' );
        $method    = $this->_get( 'session', 'http_method' );
        $resources = $this->_get( 'session', 'resources' );
        $apiname = '';

        if( !is_array( $env ) ){
            $this->setError( '99', __METHOD__.__LINE__, 'APIchk no env file', '' );
            return -1;
        }

        if( isset( $env[$resources][$method] ) && $env[$resources][$method] != '' ){ 
             $apiname = $env[$resources][$method]; 
        }

        $this->_set( array( 'apiname' => $apiname ), 'session' );

        return 0;
    }

    /******************************************************
    * ユーザ定義処理2
    * in  : なし
    * out : code   : 正常 : 0
    *                異常 : -1
    *       params : ユーザ定義処理実行結果
    ******************************************************/
    function usrproc2(){

        // 実行
        $ret = $this->usrExec();

        // 不要なパラメータ削除
        if ( $ret >= 0 && (!(defined( 'DEBUG' )) || DEBUG != 1) ) {
            unset( $this->params['api'] );
        }

        return array( 'code' => $ret, 'params' => $this->params);
    }

    /******************************************************
    * ユーザ定義処理 実行
    * in  : なし
    * out :
    *  オーバーライド前提
    ******************************************************/
    function usrExec(){
        return 0;
    }

    /******************************************************
    * セッタ
    * in  : 第1引数 … 値
    *       第2引数 … キー
    * out : なし
    ******************************************************/
    protected function _set( $param, $key = 'param' ){
        if ( is_array( $param ) && count( $param ) > 0 ) {
            foreach ( $param as $k => $val ) {
                $this->params[$key][$k] = $val;
            }
        } else {
            $this->params[$key] = $param;
        }
    }

    /******************************************************
    * ゲッタ
    * in  : 第1引数 … キー
    *       第2引数 … キー2
    *       第3引数 … キー3
    * out : 指定したキーの値
    ******************************************************/
    protected function _get( $key = 'param', $key2 = '', $key3 = '' ) {
        $val = '';
        if ( $key2 === '' ) {
            $val = isset( $this->params[$key] ) ? $this->params[$key] : '';
        } elseif ( $key3 === '' ) {
            $val = isset( $this->params[$key][$key2] ) ? $this->params[$key][$key2] : '';
        } else {
            if ( isset( $this->params[$key][$key2] ) ) {
                $val = isset( $this->params[$key][$key2][$key3] ) ? $this->params[$key][$key2][$key3] : '';
            }
        }
        return $val;
    }

    /******************************************************
    * ゲッタ（指定連想配列の値を取得）
    * in  : 第1引数 … 連想配列
    *       第2引数 … キー
    *       第3引数 … キー2
    *       第4引数 … キー3
    * out : 指定したキーの値
    ******************************************************/
    protected function _getParam( $param, $key = '', $key2 = '', $key3 = '' ) {
        $val = '';
        if ( $key2 === '' ) {
            $val = isset( $param[$key] ) ? $param[$key] : '';
        } elseif ( $key3 === '' ) {
            $val = isset( $param[$key][$key2] ) ? $param[$key][$key2] : '';
        } else {
            if ( isset( $param[$key][$key2] ) ) {
                $val = isset( $param[$key][$key2][$key3] ) ? $param[$key][$key2][$key3] : '';
            }
        }
        return $val;
    }

    /******************************************************
    * 文字コード変換
    * in  : 第1引数 … 文字コード変換対象文字列
    *     : 第2引数 … 変換後の文字コード
    *     : 第3引数 … 変換前の文字コード
    * out : 文字コード変換後の文字列
    ******************************************************/
    function henkan( $str, $to, $from ) {
        if ( $to === $from ) {
            return $str;
        }
        if ( !(isset( $this->params['subfunc'] )) ) {
            require_once BASE_LIB_DIR . 'Subfunc.php';
            $this->params['subfunc'] = new Subfunc(1);
        }
        return $this->params['subfunc']->chgcode( $str, $to, $from );
    }

    /******************************************************
    * YAMLファイル読み込み
    * in  : ファイルパス（絶対パス）
    * out :
    *  正常時 … なし
    *  異常時 … エラー
    ******************************************************/
    function readYaml( $path ){
        // 設定ファイル存在チェック
        if ( !file_exists( $path ) ) return;
        return Spyc::YAMLLoad( $path );
    }

    /******************************************************
    * BOAPI呼び出し
    * in:
    *  $args['api']     : API名
    *  $args['log_api'] : API名(ログ出力用)
    *  $args['in']      : 設定
    * out:
    *  正常時 … null
    *  異常時 … 負の値
    *    ※ 正常扱いしたい場合、1 を返却
    *       (error_msg.yaml の flg == true を設定)
    ******************************************************/
    function callBo( $args, $botype = API_ASP_FCALL ) {
        // 連想配列チェック
        if ( !is_array( $args ) || !is_array( $args['in'] ) ) {
            $this->setError( '99', __METHOD__.__LINE__, 'bo in err' );
            return -1;
        }

        // API名未指定の場合はエラー
        if ( empty( $args['api'] ) ) {
            $this->setError( '99', __METHOD__.__LINE__, 'no boapi name' );
            return -2;
        }

        if ( empty( $args['timeout'] ) ) {
            $args['timeout'] = $this->_get('env', 'BoTimeout');
        }

        $bo_param = array(
            'params' => $this->params,
            'in' => array(
                'flag'  => 3,
                'bobio' => array(
                    'call'    => $botype,
                    'api'     => $args['api'] ,
                    'timeout' => $args['timeout']
                ),
                'in'  => $args['in'] ,
                'log' => array(
                    'flag'    => $this->_get('env', 'APILOG', 'LogMode') ,
                    'enc'     => $this->_get('env', 'APILOG', 'EncMode') ,
                    'enc_key' => ENC_KEY ,
                )
            )
        );

        // APIログ出力先
        $file = $this->apiLogPath( $args['log_api'], API_LOG_FLAG );
        if ( $file !== "" ) {
            $bo_param['in']['log']['file'] = $file;
        }

        // 実行
        $m = new Page_API();
        $result = $m->exec( $bo_param );

        $out = $result['api'][$args['api']];
        $this->params['api'][$args['api']] = $out;
        $bo_cl = isset( $out['out']['out']['BO_CL_CODE'][0] ) ? $out['out']['out']['BO_CL_CODE'][0] : '';

        /**
         * エラー処理
         */
        if ( $out['out']['code'] !== 0 || $bo_cl !== '0' ) {
            if ( $this->_checkBoError( $out['out']['out'], $args['api'] ) === false ) {
                // タイムアウト
                if( count($out['out']['out']) === 0 ){
                    $this->setError( '11', __METHOD__.__LINE__ );
                   // アラームメール送信
                   $this->_set( array( 'errline' => __METHOD__.__LINE__ ), 'session' );
                   $this->sendAlertMail( $out );
                }
                $errlist = $this->_get( 'env', 'BoAlertErr' );
                if( is_array( $errlist )){
                    foreach ( $errlist as $val ) {
                        if ( preg_match( "/^{$val}$/", $bo_cl ) ) {
                            // BOの結果を出力するため、setErrorしない
                            // アラームメール送信
                            $this->_set( array( 'errline' => __METHOD__.__LINE__ ), 'session' );
                            $this->sendAlertMail( $out );
                        }
                    }
                }
                // エラー結果も出力する
                return 1;
            } else {
                /**
                 * true が返却された場合は、正常扱い
                 */
                $method = "{$args['api']}_error";
                if ( method_exists( $this, $method ) ) {
                    if ( $this->$method( $out['out']['out'] ) === false ) {
                        return -1;
                    }
                }
                return 1;
            }
        }
        return 0;
    }

    /******************************************************
    * APIログ出力パス生成
    * in  : 第1引数 … API名
    *       第2引数 … パスフラグ
    * out : APIログ出力パス
    ******************************************************/
    function apiLogPath( $api, $flg = 0 ) {
        $path = "";
        // デフォルト
        if ( $flg === 0 ) return $path;

        $path = API_LOG_FILE;
        $date      = date('Ymd');
        $hostname  = php_uname('n');

        $path = str_replace( "%_DATE_%", $date, $path );
        $path = str_replace( "%_HOSTNAME_%", $hostname, $path );
        $path = str_replace( "%_APINAME_%", $api, $path );

        return $path;
    }

    /******************************************************
    * BOAPI INパラ作成メソッド呼び出し
    * in  : 第1引数 … env.yaml のAPI番号
    *       第2引数 … 設定ファイル使用フラグ
    * out : BOAPI INパラ
    ******************************************************/
    function apiIn( $func, $flg = 0 ) {
        // BO オブジェクト
        $bo = new Bo( $this->params );

        // API名(全てWrapperAPI経由で実行する)
        $exe_api = 'C_WebEngine_wrapper';
        $method  = 'C_WebEngine_wrapper_in';
        $api     = $this->_get('env', 'API', $func);
        if ( !method_exists( $bo, $method ) ) {
            return;
        }

        $in_param = array();

        // モバイルグループウェア向けの場合ログ出力を別にする
        $log_api = $api;
        $resources = $this->_get( 'session', 'resources' );
        $mg_flg    = $this->_get( 'session', 'mg_flg' );
        if( $mg_flg === '1' ){
            $log_api = $api . STR_MG;
        }else{
            // 初期化フラグが1の場合は、設定ファイルの値を初期化
            if ( $flg !== 1 ) {
                // 設定ファイルの読み込み
                $in_param = $this->readYaml( CONFIG_DIR . "API/{$log_api}.yaml" );
                if ( !is_array( $in_param ) ) {
                    $this->setError( '99', __METHOD__.__LINE__, "{$log_api} yaml load err", '' );
                    return;
                }
            }
        }

        // メソッド呼び出し
        $in = $bo->$method( $func );

        // 設定ファイルの値に $in で追加上書き
        foreach ( $in as $key => $value ) {
            $in_param[$key] = $value;
        }

        // 共通で指定
        $in_param['REMOTE_HOST']     = getenv('REMOTE_HOST');
        $in_param['REMOTE_ADDR']     = getenv('REMOTE_ADDR');
        $in_param['HTTP_USER_AGENT'] = getenv('HTTP_USER_AGENT');

        /**
         * 埋め込み用アドレス
         */
        if ( isset( $in_param['to_address'] ) ) {
            $in_param['to_label'] = $in_param['to_address'];
        }
        if ( isset( $in_param['from_address'] ) ) {
            $in_param['from_label'] = $in_param['from_address'];
        }
        if ( isset( $in_param['mail_template'] ) ) {
            $in_param['an_domain'] = $this->_get('svc', 'user_path');
            $in_param['ask_url']   = $this->_get('ml_tplt', 'ask_url');
        }

        $args = array(
            'api'      => $exe_api ,
            'log_api'  => $log_api ,
            'in'   => $in_param ,
            'func' => $func
        );
        return $args;
    }

    /******************************************************
    * BOAPI OUTパラ参照メソッド呼び出し
    * in  :
    *  func … env.yaml のAPI番号
    * out : BOAPI OUTパラ
    ******************************************************/
    function apiOut( $func, $botype = 'API' ){
        // API名
        $api = 'C_WebEngine_wrapper';

        // BOAPI返却値
        $res = $this->_get( 'api', $api );

        return $res['out']['out'];
    }

    /******************************************************
    * BOAPIのエラーコード参照
    * in  : 第1引数 … BOAPIの実行結果
    *     : 第2引数 … API名
    * out : true  … API別エラーメソッドを呼び出し
    *       false … システムエラー
    ******************************************************/
    protected function _checkBoError( $out, $api ) {
        // エラーメッセージファイル
        if ( $this->getErrorMsg() === false ) {
            return false;
        }

        $config = array(
            $this->_get('error_msg', 'api', $api),
            $this->_get('error_msg', 'api', 'common')
        );
        if ( $config[0] === '' && $config[1] === '' ) return false;

        $clcode  = isset( $out['BO_CL_CODE'][0] )        ? $out['BO_CL_CODE'][0]        : '';
        $dcode   = isset( $out['BO_CL_DETAIL_CODE'][0] ) ? $out['BO_CL_DETAIL_CODE'][0] : '';
        $status  = isset( $out['status_status'][0] )     ? $out['status_status'][0]     : '';
        $dstatus = isset( $out['status_det'][0] )        ? $out['status_det'][0]        : '';
        $code    = "{$clcode}_{$dcode}_{$status}_{$dstatus}";

        $this->params['error_msg']['api_err'] = '';
        $flg = false;

        // API別
        foreach ( $config as $cfg ) {
            if ( is_array( $cfg ) === false ) continue;

            foreach ( $cfg as $val ) {
                if ( preg_match( "/^{$val['pattern']}$/", $code ) ) {
                    $this->params['error_msg']['api_err'] = $this->params['error_msg'][$val['msg']];
                    if ( isset( $val['flg'] ) ) $flg = $val['flg'];
                    break;
                }
            }

            // エラーメッセージを設定して break
            if ( $this->params['error_msg']['api_err'] !== '' ) {
                $log = $flg === true ? false : true;
                $this->setError( '99', __METHOD__.__LINE__,
                                 "API=[{$api}] CODE=[{$code}] MSG=[{$this->params['error_msg']['api_err']}]", $log );
                break;
            }
        }

        /**
         * エラー設定削除
         */
        unset( $this->params['error_msg']['api'] );
        return $flg;
    }

    /******************************************************
    * セッション用インスタンスにセット
    * in  : データ（連想配列）
    * out : なし
    ******************************************************/
    function setSession( $data ){
        if ( !is_array( $data ) ) return;

        foreach ( $data as $key => $val ) {
            if ( is_array( $val ) ) {
                foreach ( $val as $k => $v ) {
                    $this->params['session'][$key][$k] = $v;
                }
            } else {
                $this->params['session'][$key] = $val;
            }
        }
    }

    /******************************************************
    * 出力セッション用インスタンスにセット
    * in  : データ（連想配列）
    * out : なし
    ******************************************************/
    function setOutSession( $data ){
        if ( !is_array( $data ) ) return;

        foreach ( $data as $key => $val ) {
            if ( is_array( $val ) ) {
                foreach ( $val as $k => $v ) {
                    $this->params['session']['out'][$key][$k] = $v;
                }
            } else {
                $this->params['session']['out'][$key] = $val;
            }
        }
    }

    /******************************************************
    * エラーの設定
    * in : 第1引数 … エラーメッセージコード
    *      第2引数 … __METHOD__ __LINE__
    *      第3引数 … エラー詳細
    *      第4引数 … エラーコード
    * out: なし
    ******************************************************/
    function setError( $code, $method, $detail = '', $err_code = '' ){

        /**
         * エラーメッセージファイル
         */
        $this->getErrorMsg();

        // エラー詳細
        $this->params['err_detail'] = array(
            'code'   => $code ,
            'method' => $method ,
            'detail' => $detail,
            'err_code' => $err_code
        );

        return array( 'code' => 0, 'params' => $this->params );
    }

    /******************************************************
    * エラーメッセージ取得
    * in :
    * out:
    ******************************************************/
    public function getErrorMsg() {
        if ( $this->_get('error_msg') === '' ) {
            $this->params['error_msg'] = $this->readYaml( ERROR_MSG_CFG );
            if ( empty( $this->params['error_msg'] ) ) {
                return false;
            }
        }
    }

    /******************************************************
    * エラーログ出力処理
    * in  : $param : 配列形式のログ出力パラメータ
    * out : なし
    ******************************************************/
    function _putlog( $param = array() ){
        // ログ出力クラスを生成
        if ( class_exists( 'LOG', false ) === false ) {
            require BASE_LIB_DIR . 'Log.php';
        }
        $lm = new LOG();

        // ログ出力ファイル名を生成
        $outfile   = ERR_LOG_FILE;
        $date      = date('Ymd');
        $hostname  = php_uname('n');

        $outfile = str_replace( "%_DATE_%", $date, $outfile );
        $outfile = str_replace( "%_HOSTNAME_%", $hostname, $outfile );

        // ログ設定内容
        $logtime = date('Y/m/d_H:i:s');
        $ipaddr = isset( $_SERVER["REMOTE_ADDR"] ) ? $_SERVER["REMOTE_ADDR"] : '';
        $ua     = isset( $_SERVER["HTTP_USER_AGENT"] ) ? $_SERVER["HTTP_USER_AGENT"] : '';

        // ログ出力文字列の基本情報
        $outline = '';
        $outary  = array( $logtime
                        , 'IPADDR=' . $ipaddr
                        , 'UA=' . $ua
                        , 'REQUEST_URI=' . (isset( $_SERVER['REQUEST_URI'] ) ? $_SERVER['REQUEST_URI'] : '')
                        , 'METHOD=' . $this->_get( 'session', 'http_method' )
                        , 'LINE=' . $this->_get( 'err_detail', 'method' )
                        , 'STATUS_CODE=' . $this->_get( 'puterr', 'STATUS_CODE' )
                        , 'STATUS_DETAIL_CODE=' . $this->_get( 'puterr', 'STATUS_DETAIL_CODE' )
                        , 'ERROR_DETAIL_INFO=' . $this->_get( 'puterr', 'ERROR_DETAIL_INFO' )
                        , 'ERRCODE=' . $this->_get( 'err_detail', 'err_code' )
                        , 'MSG=' . $this->_get( 'err_detail', 'detail' )
                        );

        // ログ出力文字列生成
        $outline = implode( '|', $outary );

        $outline_put = '';
        foreach( $param as $key=>$value ){
            $outline_put .= $key . "=" . $value . '|';
        }
        $outline .= '|' . $outline_put;

        // ログ情報配列作成
        $log_ary = array( 'str' => $outline, 'file' => $outfile );

        // ログ出力
        $res = $lm->output( $log_ary );

        return;
    }

    /******************************************************
    * 配列一括文字コード変換処理
    * in  : 文字コード変換対象
    * out : 変換後配列または単一項目
    ******************************************************/
    function chgCodeArray( $args , $to, $from ){

        $list = array( $to, $from );

        // 配列ではない場合、1つだけ変換して返却
        if ( !is_array( $args ) ){
            $enc = mb_detect_encoding( $args, $list );
            if ( preg_match( "/$enc/i", $from ) ){
                $args = $this->henkan( $args, $to, $from );
            }
            return $args;
        }

        // ループで全項目に対して変換処理(再起的に処理)
        foreach( $args as $key => $val ){
            $args[$key] = $this->chgCodeArray( $val, $to, $from );
        }
        return $args;
    }

    /******************************************************
    * HTTPメソッドチェック
    * in  : なし
    * out : なし
    ******************************************************/
    function chkCgiHttpMethod(){
        // 指定HTTPメソッド
        $chk_method  = '';
        // 実際のHTTPメソッド
        $http_method = '';
        // リソース
        $resources = '';
        // 企業ID
        $client_id = '';
        // 実行URL
        $uri       = $_SERVER['REQUEST_URI'];
        // ドメイン
        $httphost  = $_SERVER['HTTP_HOST'];

        /**
         * 入力パラメータ取得
         */
        $input   = file_get_contents( 'php://input' );
        // JSON形式
        $input_json = json_decode( $input, true );
        // GET/POST形式
        $input_post = $_REQUEST;

        if( is_null( $input_json ) ){
            $this->params['session']['in'] = $input_post;
        }else{
            $this->params['session']['in'] = $input_json;
        }


        /**
         * リソース取得
         */
        $chk_uri = preg_replace( "/^\//", "", $uri );
        $chk_uri = preg_replace( "/".SERVICEID."(-*)(\w)*\//", "", $chk_uri );
        $chk_uri = preg_replace( "/\?(.*)/", "", $chk_uri );
        $ary_uri = explode( '/', $chk_uri );
        if( is_array( $ary_uri) ){
            // リソース名
            $resources = isset( $ary_uri[0] ) ? $ary_uri[0] : '';

            // 企業ID
            $client_id = isset( $ary_uri[1] ) ? $ary_uri[1] : '';
        }

        if( $resources === '' ){
            $this->setError( '99', __METHOD__.__LINE__, 'no resources' );
            return array( 'code' => -1, 'params' => $this->params );
        }
        if( $client_id === '' ){
            $this->setError( '102-3', __METHOD__.__LINE__, 'no_client_id' );
            return array( 'code' => -1, 'params' => $this->params );
        }
        $this->params['session']['resources'] = $resources;
        $this->params['session']['client_id'] = $client_id;

        if( $resources === 'MGMOSSMEMBER' || $resources === 'MGMOSSMEMBERPWD' ){
            // モバイルグループウェア向けフラグ
            $this->params['session']['mg_flg'] = '1';
        }else{
            $this->params['session']['mg_flg'] = '0';
        }

        /**
         * メソッド名取得
         */
        // HTTPヘッダーの内容を取得
        $_HEADER = apache_request_headers();
        $chk_method = isset( $_HEADER['HTTP_X_HTTP_METHOD_OVERRIDE'] )
                           ? $_HEADER['HTTP_X_HTTP_METHOD_OVERRIDE'] : '';

        if( $chk_method === '' ){
            $chk_method = isset( $_SERVER['HTTP_X_HTTP_METHOD_OVERRIDE'] )
                               ? $_SERVER['HTTP_X_HTTP_METHOD_OVERRIDE'] : '';
        }

        $http_method = isset( $_SERVER['REQUEST_METHOD'] )
                            ? $_SERVER['REQUEST_METHOD'] : '';

        // 指定されたHTTPメソッドが取得できなかった場合
        if( $chk_method === '' ){
            // QueryString「_method」を取得
            $chk_method = isset( $input_post['_method'] ) ? $input_post['_method'] : '';
        }

        if( $chk_method === '' ){
            // さらに取得できなかった場合、通常のHTTPメソッドを指定
            $chk_method = ( $chk_method !== '' ) ? $chk_method : $http_method;
        }

        // HTTPメソッド
        if( in_array( $chk_method, array('GET','POST','PUT','DELETE') ) === false ){
            $this->setError( '99', __METHOD__.__LINE__, 'no method err ' );
            return array( 'code' => -1, 'params' => $this->params );
        }

        $this->params['session']['http_method'] = $chk_method;

        // 実行するAPI決定
        $ret = $this->getExecAPI();

        return array( 'code' => $ret, 'params' => $this->params );
    }

    /******************************************************
    * バリデートチェック
    * in  : なし
    * out : なし
    ******************************************************/
    function chkCgiValidate(){
        $client_id = isset( $this->params['session']['client_id'] ) ? $this->params['session']['client_id'] : '';
        $client_pw = isset( $this->params['session']['in']['we_passwd'] ) ? $this->params['session']['in']['we_passwd'] : '';
        $this->params['session']['client_pw'] = $client_pw;

        if( $client_id === '' ){
            // 未設定エラー
            $this->setError( '102-3', __METHOD__.__LINE__, 'no client_id' );
            return array( 'code' => -1, 'params' => $this->params );
        }

        if( $client_pw === '' ){
            // 未設定エラー
            $this->setError( '102-1', __METHOD__.__LINE__, 'no client_pw' );
            return array( 'code' => -1, 'params' => $this->params );
        }

        // 企業ID設定ファイル
        $this->params['client'] = $this->readYaml( CONFIG_SYSTEM_DIR . $client_id . '.yaml' );
        if ( empty( $this->params['client'] ) ) {
            // 設定ファイルが存在しない
            $this->setError( '99', __METHOD__.__LINE__, 'no client yaml' );
            return array( 'code' => -1, 'params' => $this->params );
        }

        // API使用可否チェック
        $res = $this->chkUseAPI();
        if( $res < 0 ){
            $this->setError( '102-2', __METHOD__.__LINE__, 'chk api' );
            return array( 'code' => -1, 'params' => $this->params );
        }

        // 接続パスワードチェック
        $res = $this->chkClientPw( $client_pw );
        if( $res < 0 ){
            $this->setError( '102-1', __METHOD__.__LINE__, 'chk client_pw' );
            return array( 'code' => -1, 'params' => $this->params );
        }

        return array( 'code' => 0, 'params' => $this->params );
    }

    /**
     * 利用可否APIチェック
     *  in  : なし
     *  out :
     */
    function chkUseAPI(){
        // 利用可否APIチェック
        $apiname     = isset( $this->params['session']['apiname'] ) ? $this->params['session']['apiname'] : '';
        $api_list    = isset( $this->params['client']['useapi_list'] ) ? $this->params['client']['useapi_list'] : array();
        $api_list_mg = isset( $this->params['client']['useapi_list_mg'] ) ? $this->params['client']['useapi_list_mg'] : array();

        $mg_flg    = $this->_get( 'session', 'mg_flg' );
        if( $mg_flg === '1' ){
            // モバイルグループウェア向け
            if( !in_array( $apiname, $api_list_mg ) ){
                // 使用不可
                return -1;
            }
        }else{
            if( !in_array( $apiname, $api_list ) ){
                // 使用不可
                return -1;
            }
        }

        return 0;
    }

    /**
     * 接続パスワードチェック
     *  in  : we_passwd
     *  out :
     */
    function chkClientPw( $client_pw ){
        $chk_pw = isset( $this->params['client']['client_pw'] ) ? $this->params['client']['client_pw'] : '';
        // ハッシュ化
        $s_client_pw = sha1( $client_pw );

        if( $chk_pw !== $s_client_pw ){
            // パスワード不一致
            return -1;
        }

        return 0;
    }



    /******************************************************
    * API結果共通処理
    * in  : API実行OUTパラメータ
    * out : 出力用共通パラメータ
    ******************************************************/
    function getBoAPIOut( $ret ){
        $ses_data = array();

        // 標準ステータス
        $ses_data['STATUS_CODE']        = $this->_getParam( $ret, 'BO_CL_CODE', 0 );
        $ses_data['STATUS_DETAIL_CODE'] = $this->_getParam( $ret, 'BO_CL_DETAIL_CODE', 0 );
        $ses_data['ERROR_DETAIL_INFO']  = $this->_getParam( $ret, 'BO_CL_DETAIL_INFO', 0 );
        // snr=を除去
        $ses_data['ERROR_DETAIL_INFO']  = preg_replace( "/:snr=(.*)/", "", $ses_data['ERROR_DETAIL_INFO'] );

        if( $ses_data['STATUS_CODE'] === '3' && isset( $ret['valid_err_count'] )){
            // パラメータエラー
            $ses_data['valid_err_count'] = $this->_getParam( $ret, 'valid_err_count', 0 );
            $valid_err = 'valid_err_snr.in.';
            $keyword = '';
            $chk_key = array();
            foreach ( $ret as $key => $val ){
                if( preg_match( "/valid_err_snr.in.(.*)_val/", $key ) ){
                   $keyword = preg_replace( "/valid_err_snr.in./", "", $key );
                   $keyword = preg_replace( "/_val/", "", $keyword );
                   array_push( $chk_key,  $keyword );
                }
            }

            $i = 1;
            foreach( $chk_key as $keyword ){
                $ses_data[$valid_err . $keyword . "[{$i}]"] = $this->_getParam( $ret, $valid_err . $keyword, 0 );
                $ses_data["{$valid_err}{$keyword}_val[{$i}]"] = $this->_getParam( $ret, $valid_err . $keyword . '_val', 0 );
                $ses_data["{$valid_err}{$keyword}_code[{$i}]"] = $this->_getParam( $ret, $valid_err . $keyword . '_code', 0 );
                $i++;
            }
        }

        return $ses_data;
    }

    /******************************************************
    * MOSS管理者向け 利用者登録APIの結果をセッションに設定
    * in  : なし
    * out : なし
    ******************************************************/
    function getC_MOSS_Member_my_addOut( $ret ){
        $ses_data = $this->getBoAPIOut( $ret );

        if( $this->_getParam( $ret, 'BO_CL_CODE', 0 ) === '0' ){
            // 認証アカウント情報
            $ses_data['index_free4']      = $this->_getParam( $ret, 'index_free4', 0 );
            $ses_data['index_free_date1'] = $this->_getParam( $ret, 'index_free_date1', 0 );
            $ses_data['index_free_date2'] = $this->_getParam( $ret, 'index_free_date2', 0 );
            $ses_data['index_free_date3'] = $this->_getParam( $ret, 'index_free_date3', 0 );
            $ses_data['index_free1']      = $this->_getParam( $ret, 'index_free1', 0 );
            $ses_data['index_free2']      = $this->_getParam( $ret, 'index_free2', 0 );
            $ses_data['item_free2']       = $this->_getParam( $ret, 'item_free2', 0 );
            $ses_data['item_free10']      = $this->_getParam( $ret, 'item_free10', 0 );
        
            // 利用者アカウント情報
            $ses_data['hi_index_free4']      = $this->_getParam( $ret, 'hi_index_free4', 0 );
            $ses_data['hi_index_free_date1'] = $this->_getParam( $ret, 'hi_index_free_date1', 0 );
            $ses_data['hi_index_free_date2'] = $this->_getParam( $ret, 'hi_index_free_date2', 0 );
            $ses_data['hi_index_free_date3'] = $this->_getParam( $ret, 'hi_index_free_date3', 0 );
            $ses_data['hi_index_free1']      = $this->_getParam( $ret, 'hi_index_free1', 0 );
            $ses_data['hi_index_free2']      = $this->_getParam( $ret, 'hi_index_free2', 0 );
            $ses_data['hi_item_free2']       = $this->_getParam( $ret, 'hi_item_free2', 0 );
            $ses_data['hi_item_free10']      = $this->_getParam( $ret, 'hi_item_free10', 0 );
        }

        return $ses_data;
    }

    /******************************************************
    * MOSS利用者状態変更APIの結果をセッションに設定
    * in  : なし
    * out : なし
    ******************************************************/
    function getC_MOSS_MemberState_my_chgOut( $ret ){
        $ses_data = $this->getBoAPIOut( $ret );

        if( $this->_getParam( $ret, 'BO_CL_CODE', 0 ) === '0' ){
            // 認証アカウント情報
            $ses_data['index_free4']      = $this->_getParam( $ret, 'index_free4', 0 );
            $ses_data['index_free_date1'] = $this->_getParam( $ret, 'index_free_date1', 0 );
            $ses_data['index_free_date2'] = $this->_getParam( $ret, 'index_free_date2', 0 );
            $ses_data['index_free_date3'] = $this->_getParam( $ret, 'index_free_date3', 0 );
            $ses_data['index_free1']      = $this->_getParam( $ret, 'index_free1', 0 );
            $ses_data['index_free2']      = $this->_getParam( $ret, 'index_free2', 0 );
            $ses_data['item_free2']       = $this->_getParam( $ret, 'item_free2', 0 );
            $ses_data['item_free10']      = $this->_getParam( $ret, 'item_free10', 0 );

            // 複数件数対応ステータス(エラー時のみ出力)
            if( $this->_getParam( $ret, 'status_status', 0 ) !== '0' ){
                $ses_data['status_status'] = $this->_getParam( $ret, 'status_status', 0 );
            }
        
            // 変更対象アカウント情報
            $ses_data['hi_index_free4']      = $this->_getParam( $ret, 'hi_index_free4', 0 );
            $ses_data['hi_index_free_date1'] = $this->_getParam( $ret, 'hi_index_free_date1', 0 );
            $ses_data['hi_index_free_date2'] = $this->_getParam( $ret, 'hi_index_free_date2', 0 );
            $ses_data['hi_index_free_date3'] = $this->_getParam( $ret, 'hi_index_free_date3', 0 );
            $ses_data['hi_index_free1']      = $this->_getParam( $ret, 'hi_index_free1', 0 );
            $ses_data['hi_index_free2']      = $this->_getParam( $ret, 'hi_index_free2', 0 );
            $ses_data['hi_item_free2']       = $this->_getParam( $ret, 'hi_item_free2', 0 );
            $ses_data['hi_item_free10']      = $this->_getParam( $ret, 'hi_item_free10', 0 );

            // 変更対象アカウント情報 n=2〜10
            for( $i = 2; $i <= 10; $i++ ){
                if( $this->_getParam( $ret, 'hi_index_free4', $i ) !== '' ) { 
                    $ses_data["hi_index_free4[{$i}]"]      = $this->_getParam( $ret, 'hi_index_free4', $i );
                }
                if( $this->_getParam( $ret, 'hi_index_free_date1', $i ) !== '' ) { 
                    $ses_data["hi_index_free_date1[{$i}]"] = $this->_getParam( $ret, 'hi_index_free_date1', $i );
                }
                if( $this->_getParam( $ret, 'hi_index_free_date2', $i ) !== '' ) { 
                    $ses_data["hi_index_free_date2[{$i}]"] = $this->_getParam( $ret, 'hi_index_free_date2', $i );
                }
                if( $this->_getParam( $ret, 'hi_index_free_date3', $i ) !== '' ) { 
                    $ses_data["hi_index_free_date3[{$i}]"] = $this->_getParam( $ret, 'hi_index_free_date3', $i );
                }
                if( $this->_getParam( $ret, 'hi_index_free1', $i ) !== '' ) { 
                    $ses_data["hi_index_free1[{$i}]"]      = $this->_getParam( $ret, 'hi_index_free1', $i );
                }
                if( $this->_getParam( $ret, 'hi_index_free2', $i ) !== '' ) { 
                    $ses_data["hi_index_free2[{$i}]"]      = $this->_getParam( $ret, 'hi_index_free2', $i );
                }
                if( $this->_getParam( $ret, 'hi_item_free2', $i ) !== '' ) { 
                    $ses_data["hi_item_free2[{$i}]"]       = $this->_getParam( $ret, 'hi_item_free2', $i );
                }
                if( $this->_getParam( $ret, 'hi_item_free10', 0 ) !== '' ) { 
                    $ses_data["hi_item_free10[{$i}]"]      = $this->_getParam( $ret, 'hi_item_free10', $i );
                }
                if( $this->_getParam( $ret, 'status_status', $i ) !== '' 
                        && $this->_getParam( $ret, 'status_status', $i ) !== '0' ){
                    $ses_data["status_status[{$i}]"]       = $this->_getParam( $ret, 'status_status', $i );
                }
            }
        }

        return $ses_data;
    }

    /******************************************************
    * MOSS利用者・管理者情報変更APIの結果をセッションに設定
    * in  : なし
    * out : なし
    ******************************************************/
    function getC_MOSS_Member_my_modOut( $ret ){
        $ses_data = $this->getBoAPIOut( $ret );

        if( $this->_getParam( $ret, 'BO_CL_CODE', 0 ) !== '0' ){
            return $ses_data;
        }

        // 認証アカウント情報
        $ses_data['index_free4']      = $this->_getParam( $ret, 'index_free4', 0 );
        $ses_data['index_free_date1'] = $this->_getParam( $ret, 'index_free_date1', 0 );
        $ses_data['index_free_date2'] = $this->_getParam( $ret, 'index_free_date2', 0 );
        $ses_data['index_free_date3'] = $this->_getParam( $ret, 'index_free_date3', 0 );
        $ses_data['index_free1']      = $this->_getParam( $ret, 'index_free1', 0 );
        $ses_data['index_free2']      = $this->_getParam( $ret, 'index_free2', 0 );
        $ses_data['item_free2']       = $this->_getParam( $ret, 'item_free2', 0 );
        $ses_data['item_free10']      = $this->_getParam( $ret, 'item_free10', 0 );
        
        // 変更対象アカウント情報(認証方式="2"の場合のみ返却)
        $auth_method_kbn = $this->_get( 'session', 'in', 'auth_method_kbn' );

        if( $auth_method_kbn === '2' ){
            $ses_data['hi_index_free4']      = $this->_getParam( $ret, 'hi_index_free4', 0 );
            $ses_data['hi_index_free_date1'] = $this->_getParam( $ret, 'hi_index_free_date1', 0 );
            $ses_data['hi_index_free_date2'] = $this->_getParam( $ret, 'hi_index_free_date2', 0 );
            $ses_data['hi_index_free_date3'] = $this->_getParam( $ret, 'hi_index_free_date3', 0 );
            $ses_data['hi_index_free1']      = $this->_getParam( $ret, 'hi_index_free1', 0 );
            $ses_data['hi_index_free2']      = $this->_getParam( $ret, 'hi_index_free2', 0 );
            $ses_data['hi_item_free2']       = $this->_getParam( $ret, 'hi_item_free2', 0 );
            $ses_data['hi_item_free10']      = $this->_getParam( $ret, 'hi_item_free10', 0 );
        }

        return $ses_data;
    }

    /******************************************************
    * MOSS利用者・管理者情報参照APIの結果をセッションに設定
    * in  : なし
    * out : なし
    ******************************************************/
    function getC_MOSS_Member_my_refOut( $ret ){
        $ses_data = $this->getBoAPIOut( $ret );

        if( $this->_getParam( $ret, 'BO_CL_CODE', 0 ) !== '0' ){
            return $ses_data;
        }

        // 認証アカウント情報
        $ses_data['index_free4']      = $this->_getParam( $ret, 'index_free4', 0 );
        $ses_data['index_free_date1'] = $this->_getParam( $ret, 'index_free_date1', 0 );
        $ses_data['index_free_date2'] = $this->_getParam( $ret, 'index_free_date2', 0 );
        $ses_data['index_free_date3'] = $this->_getParam( $ret, 'index_free_date3', 0 );
        $ses_data['index_free1']      = $this->_getParam( $ret, 'index_free1', 0 );
        $ses_data['index_free2']      = $this->_getParam( $ret, 'index_free2', 0 );
        $ses_data['item_free2']       = $this->_getParam( $ret, 'item_free2', 0 );
        $ses_data['item_free10']      = $this->_getParam( $ret, 'item_free10', 0 );


        // 参照対象アカウント情報(認証方式="2"の場合のみ返却)
        $auth_method_kbn = $this->_get( 'session', 'in', 'auth_method_kbn' );

        if( $auth_method_kbn === '2' ){
            $ses_data['mst.index_free4']      = $this->_getParam( $ret, 'mst.index_free4', 0 );
            $ses_data['mst.index_free_date1'] = $this->_getParam( $ret, 'mst.index_free_date1', 0 );
            $ses_data['mst.index_free_date2'] = $this->_getParam( $ret, 'mst.index_free_date2', 0 );
            $ses_data['mst.index_free_date3'] = $this->_getParam( $ret, 'mst.index_free_date3', 0 );
            $ses_data['mst.index_free1']      = $this->_getParam( $ret, 'mst.index_free1', 0 );
            $ses_data['mst.index_free2']      = $this->_getParam( $ret, 'mst.index_free2', 0 );
            $ses_data['mst.item_free10']      = $this->_getParam( $ret, 'mst.item_free10', 0 );
            $ses_data['mst.item_free22']      = $this->_getParam( $ret, 'mst.item_free22', 0 );
            $ses_data['mst.item_free23']      = $this->_getParam( $ret, 'mst.item_free23', 0 );
            $ses_data['mst.item_free24']      = $this->_getParam( $ret, 'mst.item_free24', 0 );
            $ses_data['mst.item_free25']      = $this->_getParam( $ret, 'mst.item_free25', 0 );
            $ses_data['mst.item_free26']      = $this->_getParam( $ret, 'mst.item_free26', 0 );
            $ses_data['mst.item_free27']      = $this->_getParam( $ret, 'mst.item_free27', 0 );
            $ses_data['mst.item_free28']      = $this->_getParam( $ret, 'mst.item_free28', 0 );
        }

        return $ses_data;
    }

    /******************************************************
    * MOSSパスワード変更APIの結果をセッションに設定
    * in  : なし
    * out : なし
    ******************************************************/
    function getC_MOSS_Password_my_modOut( $ret ){
        $ses_data = $this->getBoAPIOut( $ret );

        if( $this->_getParam( $ret, 'BO_CL_CODE', 0 ) !== '0' ){
            return $ses_data;
        }

        // 認証アカウント情報
        $ses_data['index_free4']      = $this->_getParam( $ret, 'index_free4', 0 );
        $ses_data['index_free_date1'] = $this->_getParam( $ret, 'index_free_date1', 0 );
        $ses_data['index_free_date2'] = $this->_getParam( $ret, 'index_free_date2', 0 );
        $ses_data['index_free_date3'] = $this->_getParam( $ret, 'index_free_date3', 0 );
        $ses_data['index_free1']      = $this->_getParam( $ret, 'index_free1', 0 );
        $ses_data['index_free2']      = $this->_getParam( $ret, 'index_free2', 0 );
        $ses_data['item_free2']       = $this->_getParam( $ret, 'item_free2', 0 );
        $ses_data['item_free10']      = $this->_getParam( $ret, 'item_free10', 0 );

        return $ses_data;
    }

    /******************************************************
    * MOSS受信拒否メンテAPIの結果をセッションに設定
    * in  : なし
    * out : なし
    ******************************************************/
    function getC_MOSS_GAODNY_my_mente2Out( $ret ){
        $ses_data = $this->getBoAPIOut( $ret );

        if( $this->_getParam( $ret, 'BO_CL_CODE', 0 ) !== '0' ){
            return $ses_data;
        }


        // 認証アカウント情報
        $ses_data['index_free4']      = $this->_getParam( $ret, 'index_free4', 0 );
        $ses_data['index_free_date1'] = $this->_getParam( $ret, 'index_free_date1', 0 );
        $ses_data['index_free_date2'] = $this->_getParam( $ret, 'index_free_date2', 0 );
        $ses_data['index_free_date3'] = $this->_getParam( $ret, 'index_free_date3', 0 );
        $ses_data['index_free1']      = $this->_getParam( $ret, 'index_free1', 0 );
        $ses_data['index_free2']      = $this->_getParam( $ret, 'index_free2', 0 );
        $ses_data['item_free2']       = $this->_getParam( $ret, 'item_free2', 0 );
        $ses_data['item_free10']      = $this->_getParam( $ret, 'item_free10', 0 );

        $dnyfil_type = $this->_get( 'session', 'in', 'dnyfil_type' );

        // 共通パラメータ部　メール受信拒否タイプの設定により返却
        if( $dnyfil_type === 'all_list' ){

            // 1)メール受信拒否タイプ="all_list"を選択した場合
            $ses_data['fil_total_count']    = $this->_getParam( $ret, 'fil_total_count', 0 );
            $ses_data['fil_from_count']     = $this->_getParam( $ret, 'fil_from_count', 0 );
            $ses_data['fil_to_count']       = $this->_getParam( $ret, 'fil_to_count', 0 );
            $ses_data['fil_cc_count']       = $this->_getParam( $ret, 'fil_cc_count', 0 );
            $ses_data['fil_subject_count']  = $this->_getParam( $ret, 'fil_subject_count', 0 );
            $ses_data['fil_subject_status'] = $this->_getParam( $ret, 'fil_subject_status', 0 );
            $ses_data['fil_from_status']    = $this->_getParam( $ret, 'fil_from_status', 0 );
        }

        if( $dnyfil_type === 'from_fil' ||  $dnyfil_type ===  'to_fil'
                ||  $dnyfil_type === 'cc_fil' ||  $dnyfil_type === 'subject_fil' ){

            // 3)メール受信拒否タイプ="from_fil", "to_fil", "cc_fil"または"subject_fil"を選択した場合
            $ses_data['dnyfil_data_count'] = $this->_getParam( $ret, 'dnyfil_data_count', 0 );

            if( $ses_data['dnyfil_data_count'] > 0 ){
                $ses_data['dnyfil_type']       = $this->_getParam( $ret, 'dnyfil_type', 0 );
                for( $i = 1; $i <= $ses_data['dnyfil_data_count']; $i++ ){
                    // フィルタ条件設定内容 返却値分出力
                    $ses_data["dnyfil_data[{$i}]"]   = $this->_getParam( $ret, 'dnyfil_data', $i );
                }
            }
        }

        return $ses_data;
    }


    /******************************************************
    * 利用者登録APIの結果をセッションに設定
    *   （モバイルグループウェア向け）
    * in  : なし
    * out : なし
    ******************************************************/
    function getC_MOSS_Member_my_add_mgOut( $ret ){
        $ses_data = $this->getBoAPIOut( $ret );

        if( $this->_getParam( $ret, 'BO_CL_CODE', 0 ) === '0' ){
            // アカウント情報
            $ses_data['index_free4']      = $this->_getParam( $ret, 'index_free4', 0 );
            $ses_data['index_free_date1'] = $this->_getParam( $ret, 'index_free_date1', 0 );
            $ses_data['index_free_date2'] = $this->_getParam( $ret, 'index_free_date2', 0 );
            $ses_data['index_free_date3'] = $this->_getParam( $ret, 'index_free_date3', 0 );
            $ses_data['index_free2']      = $this->_getParam( $ret, 'index_free2', 0 );
        }

        return $ses_data;
    }

    /******************************************************
    * 利用者状態変更APIの結果をセッションに設定
    *   （モバイルグループウェア向け）
    * in  : なし
    * out : なし
    ******************************************************/
    function getC_MOSS_MemberState_my_chg_mgOut( $ret ){
        $ses_data = $this->getBoAPIOut( $ret );

        if( $this->_getParam( $ret, 'BO_CL_CODE', 0 ) === '0' ){
            // 認証アカウント情報
            $ses_data['index_free4']      = $this->_getParam( $ret, 'index_free4', 0 );
            $ses_data['index_free_date1'] = $this->_getParam( $ret, 'index_free_date1', 0 );
            $ses_data['index_free_date2'] = $this->_getParam( $ret, 'index_free_date2', 0 );
            $ses_data['index_free_date3'] = $this->_getParam( $ret, 'index_free_date3', 0 );
            $ses_data['index_free2']      = $this->_getParam( $ret, 'index_free2', 0 );
        }

        return $ses_data;
    }

    /******************************************************
    * 利用者情報変更APIの結果をセッションに設定
    *   （モバイルグループウェア向け）
    * in  : なし
    * out : なし
    ******************************************************/
    function getC_MOSS_Member_my_mod_mgOut( $ret ){
        $ses_data = $this->getBoAPIOut( $ret );

        if( $this->_getParam( $ret, 'BO_CL_CODE', 0 ) !== '0' ){
            return $ses_data;
        }

        // アカウント情報
        $ses_data['index_free4']      = $this->_getParam( $ret, 'index_free4', 0 );
        $ses_data['index_free_date1'] = $this->_getParam( $ret, 'index_free_date1', 0 );
        $ses_data['index_free_date2'] = $this->_getParam( $ret, 'index_free_date2', 0 );
        $ses_data['index_free_date3'] = $this->_getParam( $ret, 'index_free_date3', 0 );
        $ses_data['index_free2']      = $this->_getParam( $ret, 'index_free2', 0 );

        return $ses_data;
    }

    /******************************************************
    * 利用者情報参照APIの結果をセッションに設定
    *   （モバイルグループウェア向け）
    * in  : なし
    * out : なし
    ******************************************************/
    function getC_MOSS_Member_my_ref_mgOut( $ret ){
        $ses_data = $this->getBoAPIOut( $ret );
        if( $this->_getParam( $ret, 'BO_CL_CODE', 0 ) !== '0' ){
            return $ses_data;
        }

        // アカウント情報
        $ses_data['index_free4']      = $this->_getParam( $ret, 'index_free4', 0 );
        $ses_data['index_free_date1'] = $this->_getParam( $ret, 'index_free_date1', 0 );
        $ses_data['index_free_date2'] = $this->_getParam( $ret, 'index_free_date2', 0 );
        $ses_data['index_free_date3'] = $this->_getParam( $ret, 'index_free_date3', 0 );
        $ses_data['index_free2']      = $this->_getParam( $ret, 'index_free2', 0 );

        return $ses_data;
    }

    /******************************************************
    * パスワード変更APIの結果をセッションに設定
    *   （モバイルグループウェア向け）
    * in  : なし
    * out : なし
    ******************************************************/
    function getC_MOSS_Password_my_mod_mgOut( $ret ){
        $ses_data = $this->getBoAPIOut( $ret );

        if( $this->_getParam( $ret, 'BO_CL_CODE', 0 ) !== '0' ){
            return $ses_data;
        }

        // アカウント情報
        $ses_data['index_free4']      = $this->_getParam( $ret, 'index_free4', 0 );
        $ses_data['index_free_date1'] = $this->_getParam( $ret, 'index_free_date1', 0 );
        $ses_data['index_free_date2'] = $this->_getParam( $ret, 'index_free_date2', 0 );
        $ses_data['index_free_date3'] = $this->_getParam( $ret, 'index_free_date3', 0 );
        $ses_data['index_free2']      = $this->_getParam( $ret, 'index_free2', 0 );

        return $ses_data;
    }

    /******************************************************
    * Webエンジン向けシナリオWrapperAPI
    * in  : なし
    * out : なし
    ******************************************************/
    function setC_WebEngine_wrapper( $no, $api_name ){
        $error = $this->callBo( $this->apiIn( $no ) );
        if( $error < 0 ){
             return;
        }

        // 返却値参照
        $ret = $this->apiOut( $no );

        $mg_flg    = $this->_get( 'session', 'mg_flg' );
        if( $mg_flg === '1' ){
            $api_name = $api_name . STR_MG;
        }
        $execapi = "get{$api_name}Out";
        if( !method_exists( $this, $execapi ) ){
            return -1;
        }

        // セッションに格納
        $ses_data = $this->$execapi( $ret );
        $this->setOutSession( $ses_data );
        return;
    }

    /******************************************************
    * アラームメール送信
    * in  : BO API返却値
    * out : なし
    ******************************************************/
    protected function sendAlertMail( $out ){
        require_once( BASE_LIB_DIR . '/Mail.php' );

        $mail = $this->_get( 'env', 'AlertMail' );

        // メール送信なしの場合、return
        if( $mail['flag'] <= 0  ){ return; }

        $hios_no  = $mail['hios_no'];
        $alerm_no = $mail['alerm_no'];
        $hostname = php_uname("n");
        $time     = date('Y/m/d H:i:s');
        $apiname  = $this->_getParam( $out, 'in', 'bobio', 'api' );
        $bo_out   = $this->_getParam( $out, 'out', 'out' );
        $bo_req   = $this->_getParam( $bo_out, 'BO_REQUEST_ID', 0 );
        $bo_cl    = $this->_getParam( $bo_out, 'BO_CL_CODE', 0 );
        $bo_det   = $this->_getParam( $bo_out, 'BO_CL_DETAIL_CODE', 0 );
        $bo_info  = $this->_getParam( $bo_out, 'BO_CL_DETAIL_INFO', 0 );
        $client_id = $this->_get( 'session', 'client_id' );
        $errline   = $this->_get( 'session', 'errline' );

        $subject = sprintf( $mail['subject'], $hios_no, $hostname, $time, $alerm_no );

        $body_h  = sprintf( $mail['body_h'], $alerm_no, $hostname, $time, $hostname, $client_id, $apiname, $errline );
        $body_bo = sprintf( $mail['body_bo'], $bo_req, $bo_cl, $bo_det, $bo_info );
        $body_to = $mail['body_timeout'];

        $body = '';
        $err_code = $this->_get( 'err_detail', 'code' );
        if( $err_code === '11' ){
            // BOAPI呼出しエラー
            $body = $body_h . $body_to; 
        }else{
            $body = $body_h . $body_bo;
        }
        $body = str_replace( '\n', "\n", $body ); 

        $args = array(
            'from'    => $mail['from'],
            'to'      => $mail['to'],
            'cc'      => $mail['cc'],
            'errto'   => $mail['errto'],
            'subject' => $subject,
            'body'    => $body
            );
        $m = new Mail();

        // エラーログパラメータ
        $para   = array();
        $puterr = array();
        $puterr['STATUS_CODE'] = $bo_cl;
        $puterr['STATUS_DETAIL_CODE'] = $bo_det;
        $puterr['ERROR_DETAIL_INFO']  = $bo_info;
        $this->params['puterr'] = $puterr;

        // メール送信
        $ret = $m->sendmail( $args );
        if( $ret['code'] < 0 || $ret['code'] === false ) {
            $para = array( 'sendAlertMailErr' => __METHOD__.__LINE__);
        }

        // エラーログ出力
        $this->_putlog($para);
    }
}
