<?php

// spyc ( for YAML )
require_once BASE_PHPLIB_DIR . 'spyc.php5';

// ���ץ⥸�塼��
require_once BASE_LIB_DIR . 'Page/Page_API.php';

// �����ӥ��⥸�塼��
require_once LIB_DIR . 'Bo.php';

class APICommon {

    // ****************************************************
    // ���󥹥ȥ饯��
    // ****************************************************
    function __construct( $params ){
        $this->params = $params;
        return;
    }

    /******************************************************
    * �����¹�
    * in  : �ʤ�
    * out : code   : ���� : 0
    *                �۾� : -1
    *       params : �桼����������¹Է��
    ******************************************************/
    function setproc(){
        // �������
        $code = $this->_init();
        if( $code < 0 ){
            $this->setError( '99', __METHOD__.__LINE__, 'init err', '' );
            return array( 'code' => $code, 'params' => $this->params );
        }

        // ʸ���������Ѵ� UTF-8 �� EUC-JP
        $this->chgDecode(0);

        // API�¹� 
        $ret = $this->usrproc2();
        $code = $ret['code'];

        // ���ʸ���Ѵ� EUC-JP => UTF-8
        $this->chgDecode(1);

        return array( 'code' => $code, 'params' => $this->params );
    }

    /******************************************************
    * ʸ���������Ѵ� UTF-8 <-> EUC-JP
    * in  : flg    : 0 : UTF-8  => EUC-JP
    *                1 : EUC-JP => UTF-8
    * out : code   : ���� : 0
    *                �۾� : -1
    *       params : �桼����������¹Է��
    ******************************************************/
    function chgDecode( $flg = 0 ) {

        // ���ʸ���Ѵ� UTF-8 => EUC-JP
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
    * �������
    * in  : �ʤ�
    * out : code   : ���� : 0
    *                �۾� : -1
    *       params : �桼����������¹Է��
    ******************************************************/
    protected function _init(){
        // http header ������
        $this->params['_header'] = $this->_get('env', 'header');

        return 0;
    }

    /******************************************************
    * �¹�APIȽ��
    * in  : �ʤ�
    * out : code   : ���� : 0
    *                �۾� : -1
    *       params : �桼����������¹Է��
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
    * �桼���������2
    * in  : �ʤ�
    * out : code   : ���� : 0
    *                �۾� : -1
    *       params : �桼����������¹Է��
    ******************************************************/
    function usrproc2(){

        // �¹�
        $ret = $this->usrExec();

        // ���פʥѥ�᡼�����
        if ( $ret >= 0 && (!(defined( 'DEBUG' )) || DEBUG != 1) ) {
            unset( $this->params['api'] );
        }

        return array( 'code' => $ret, 'params' => $this->params);
    }

    /******************************************************
    * �桼��������� �¹�
    * in  : �ʤ�
    * out :
    *  �����С��饤������
    ******************************************************/
    function usrExec(){
        return 0;
    }

    /******************************************************
    * ���å�
    * in  : ��1���� �� ��
    *       ��2���� �� ����
    * out : �ʤ�
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
    * ���å�
    * in  : ��1���� �� ����
    *       ��2���� �� ����2
    *       ��3���� �� ����3
    * out : ���ꤷ����������
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
    * ���å��ʻ���Ϣ��������ͤ������
    * in  : ��1���� �� Ϣ������
    *       ��2���� �� ����
    *       ��3���� �� ����2
    *       ��4���� �� ����3
    * out : ���ꤷ����������
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
    * ʸ���������Ѵ�
    * in  : ��1���� �� ʸ���������Ѵ��о�ʸ����
    *     : ��2���� �� �Ѵ����ʸ��������
    *     : ��3���� �� �Ѵ�����ʸ��������
    * out : ʸ���������Ѵ����ʸ����
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
    * YAML�ե������ɤ߹���
    * in  : �ե�����ѥ������Хѥ���
    * out :
    *  ����� �� �ʤ�
    *  �۾�� �� ���顼
    ******************************************************/
    function readYaml( $path ){
        // ����ե�����¸�ߥ����å�
        if ( !file_exists( $path ) ) return;
        return Spyc::YAMLLoad( $path );
    }

    /******************************************************
    * BOAPI�ƤӽФ�
    * in:
    *  $args['api']     : API̾
    *  $args['log_api'] : API̾(��������)
    *  $args['in']      : ����
    * out:
    *  ����� �� null
    *  �۾�� �� �����
    *    �� ���ﰷ����������硢1 ���ֵ�
    *       (error_msg.yaml �� flg == true ������)
    ******************************************************/
    function callBo( $args, $botype = API_ASP_FCALL ) {
        // Ϣ����������å�
        if ( !is_array( $args ) || !is_array( $args['in'] ) ) {
            $this->setError( '99', __METHOD__.__LINE__, 'bo in err' );
            return -1;
        }

        // API̤̾����ξ��ϥ��顼
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

        // API��������
        $file = $this->apiLogPath( $args['log_api'], API_LOG_FLAG );
        if ( $file !== "" ) {
            $bo_param['in']['log']['file'] = $file;
        }

        // �¹�
        $m = new Page_API();
        $result = $m->exec( $bo_param );

        $out = $result['api'][$args['api']];
        $this->params['api'][$args['api']] = $out;
        $bo_cl = isset( $out['out']['out']['BO_CL_CODE'][0] ) ? $out['out']['out']['BO_CL_CODE'][0] : '';

        /**
         * ���顼����
         */
        if ( $out['out']['code'] !== 0 || $bo_cl !== '0' ) {
            if ( $this->_checkBoError( $out['out']['out'], $args['api'] ) === false ) {
                // �����ॢ����
                if( count($out['out']['out']) === 0 ){
                    $this->setError( '11', __METHOD__.__LINE__ );
                   // ���顼��᡼������
                   $this->_set( array( 'errline' => __METHOD__.__LINE__ ), 'session' );
                   $this->sendAlertMail( $out );
                }
                $errlist = $this->_get( 'env', 'BoAlertErr' );
                if( is_array( $errlist )){
                    foreach ( $errlist as $val ) {
                        if ( preg_match( "/^{$val}$/", $bo_cl ) ) {
                            // BO�η�̤���Ϥ��뤿�ᡢsetError���ʤ�
                            // ���顼��᡼������
                            $this->_set( array( 'errline' => __METHOD__.__LINE__ ), 'session' );
                            $this->sendAlertMail( $out );
                        }
                    }
                }
                // ���顼��̤���Ϥ���
                return 1;
            } else {
                /**
                 * true ���ֵѤ��줿���ϡ����ﰷ��
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
    * API�����ϥѥ�����
    * in  : ��1���� �� API̾
    *       ��2���� �� �ѥ��ե饰
    * out : API�����ϥѥ�
    ******************************************************/
    function apiLogPath( $api, $flg = 0 ) {
        $path = "";
        // �ǥե����
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
    * BOAPI IN�ѥ�����᥽�åɸƤӽФ�
    * in  : ��1���� �� env.yaml ��API�ֹ�
    *       ��2���� �� ����ե�������ѥե饰
    * out : BOAPI IN�ѥ�
    ******************************************************/
    function apiIn( $func, $flg = 0 ) {
        // BO ���֥�������
        $bo = new Bo( $this->params );

        // API̾(����WrapperAPI��ͳ�Ǽ¹Ԥ���)
        $exe_api = 'C_WebEngine_wrapper';
        $method  = 'C_WebEngine_wrapper_in';
        $api     = $this->_get('env', 'API', $func);
        if ( !method_exists( $bo, $method ) ) {
            return;
        }

        $in_param = array();

        // ��Х��륰�롼�ץ����������ξ������Ϥ��̤ˤ���
        $log_api = $api;
        $resources = $this->_get( 'session', 'resources' );
        $mg_flg    = $this->_get( 'session', 'mg_flg' );
        if( $mg_flg === '1' ){
            $log_api = $api . STR_MG;
        }else{
            // ������ե饰��1�ξ��ϡ�����ե�������ͤ�����
            if ( $flg !== 1 ) {
                // ����ե�������ɤ߹���
                $in_param = $this->readYaml( CONFIG_DIR . "API/{$log_api}.yaml" );
                if ( !is_array( $in_param ) ) {
                    $this->setError( '99', __METHOD__.__LINE__, "{$log_api} yaml load err", '' );
                    return;
                }
            }
        }

        // �᥽�åɸƤӽФ�
        $in = $bo->$method( $func );

        // ����ե�������ͤ� $in ���ɲþ��
        foreach ( $in as $key => $value ) {
            $in_param[$key] = $value;
        }

        // ���̤ǻ���
        $in_param['REMOTE_HOST']     = getenv('REMOTE_HOST');
        $in_param['REMOTE_ADDR']     = getenv('REMOTE_ADDR');
        $in_param['HTTP_USER_AGENT'] = getenv('HTTP_USER_AGENT');

        /**
         * �������ѥ��ɥ쥹
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
    * BOAPI OUT�ѥ黲�ȥ᥽�åɸƤӽФ�
    * in  :
    *  func �� env.yaml ��API�ֹ�
    * out : BOAPI OUT�ѥ�
    ******************************************************/
    function apiOut( $func, $botype = 'API' ){
        // API̾
        $api = 'C_WebEngine_wrapper';

        // BOAPI�ֵ���
        $res = $this->_get( 'api', $api );

        return $res['out']['out'];
    }

    /******************************************************
    * BOAPI�Υ��顼�����ɻ���
    * in  : ��1���� �� BOAPI�μ¹Է��
    *     : ��2���� �� API̾
    * out : true  �� API�̥��顼�᥽�åɤ�ƤӽФ�
    *       false �� �����ƥ२�顼
    ******************************************************/
    protected function _checkBoError( $out, $api ) {
        // ���顼��å������ե�����
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

        // API��
        foreach ( $config as $cfg ) {
            if ( is_array( $cfg ) === false ) continue;

            foreach ( $cfg as $val ) {
                if ( preg_match( "/^{$val['pattern']}$/", $code ) ) {
                    $this->params['error_msg']['api_err'] = $this->params['error_msg'][$val['msg']];
                    if ( isset( $val['flg'] ) ) $flg = $val['flg'];
                    break;
                }
            }

            // ���顼��å����������ꤷ�� break
            if ( $this->params['error_msg']['api_err'] !== '' ) {
                $log = $flg === true ? false : true;
                $this->setError( '99', __METHOD__.__LINE__,
                                 "API=[{$api}] CODE=[{$code}] MSG=[{$this->params['error_msg']['api_err']}]", $log );
                break;
            }
        }

        /**
         * ���顼������
         */
        unset( $this->params['error_msg']['api'] );
        return $flg;
    }

    /******************************************************
    * ���å�����ѥ��󥹥��󥹤˥��å�
    * in  : �ǡ�����Ϣ�������
    * out : �ʤ�
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
    * ���ϥ��å�����ѥ��󥹥��󥹤˥��å�
    * in  : �ǡ�����Ϣ�������
    * out : �ʤ�
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
    * ���顼������
    * in : ��1���� �� ���顼��å�����������
    *      ��2���� �� __METHOD__ __LINE__
    *      ��3���� �� ���顼�ܺ�
    *      ��4���� �� ���顼������
    * out: �ʤ�
    ******************************************************/
    function setError( $code, $method, $detail = '', $err_code = '' ){

        /**
         * ���顼��å������ե�����
         */
        $this->getErrorMsg();

        // ���顼�ܺ�
        $this->params['err_detail'] = array(
            'code'   => $code ,
            'method' => $method ,
            'detail' => $detail,
            'err_code' => $err_code
        );

        return array( 'code' => 0, 'params' => $this->params );
    }

    /******************************************************
    * ���顼��å���������
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
    * ���顼�����Ͻ���
    * in  : $param : ��������Υ����ϥѥ�᡼��
    * out : �ʤ�
    ******************************************************/
    function _putlog( $param = array() ){
        // �����ϥ��饹������
        if ( class_exists( 'LOG', false ) === false ) {
            require BASE_LIB_DIR . 'Log.php';
        }
        $lm = new LOG();

        // �����ϥե�����̾������
        $outfile   = ERR_LOG_FILE;
        $date      = date('Ymd');
        $hostname  = php_uname('n');

        $outfile = str_replace( "%_DATE_%", $date, $outfile );
        $outfile = str_replace( "%_HOSTNAME_%", $hostname, $outfile );

        // ����������
        $logtime = date('Y/m/d_H:i:s');
        $ipaddr = isset( $_SERVER["REMOTE_ADDR"] ) ? $_SERVER["REMOTE_ADDR"] : '';
        $ua     = isset( $_SERVER["HTTP_USER_AGENT"] ) ? $_SERVER["HTTP_USER_AGENT"] : '';

        // ������ʸ����δ��ܾ���
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

        // ������ʸ��������
        $outline = implode( '|', $outary );

        $outline_put = '';
        foreach( $param as $key=>$value ){
            $outline_put .= $key . "=" . $value . '|';
        }
        $outline .= '|' . $outline_put;

        // �������������
        $log_ary = array( 'str' => $outline, 'file' => $outfile );

        // ������
        $res = $lm->output( $log_ary );

        return;
    }

    /******************************************************
    * ������ʸ���������Ѵ�����
    * in  : ʸ���������Ѵ��о�
    * out : �Ѵ�������ޤ���ñ�����
    ******************************************************/
    function chgCodeArray( $args , $to, $from ){

        $list = array( $to, $from );

        // ����ǤϤʤ���硢1�Ĥ����Ѵ������ֵ�
        if ( !is_array( $args ) ){
            $enc = mb_detect_encoding( $args, $list );
            if ( preg_match( "/$enc/i", $from ) ){
                $args = $this->henkan( $args, $to, $from );
            }
            return $args;
        }

        // �롼�פ������ܤ��Ф����Ѵ�����(�Ƶ�Ū�˽���)
        foreach( $args as $key => $val ){
            $args[$key] = $this->chgCodeArray( $val, $to, $from );
        }
        return $args;
    }

    /******************************************************
    * HTTP�᥽�åɥ����å�
    * in  : �ʤ�
    * out : �ʤ�
    ******************************************************/
    function chkCgiHttpMethod(){
        // ����HTTP�᥽�å�
        $chk_method  = '';
        // �ºݤ�HTTP�᥽�å�
        $http_method = '';
        // �꥽����
        $resources = '';
        // ���ID
        $client_id = '';
        // �¹�URL
        $uri       = $_SERVER['REQUEST_URI'];
        // �ɥᥤ��
        $httphost  = $_SERVER['HTTP_HOST'];

        /**
         * ���ϥѥ�᡼������
         */
        $input   = file_get_contents( 'php://input' );
        // JSON����
        $input_json = json_decode( $input, true );
        // GET/POST����
        $input_post = $_REQUEST;

        if( is_null( $input_json ) ){
            $this->params['session']['in'] = $input_post;
        }else{
            $this->params['session']['in'] = $input_json;
        }


        /**
         * �꥽��������
         */
        $chk_uri = preg_replace( "/^\//", "", $uri );
        $chk_uri = preg_replace( "/".SERVICEID."(-*)(\w)*\//", "", $chk_uri );
        $chk_uri = preg_replace( "/\?(.*)/", "", $chk_uri );
        $ary_uri = explode( '/', $chk_uri );
        if( is_array( $ary_uri) ){
            // �꥽����̾
            $resources = isset( $ary_uri[0] ) ? $ary_uri[0] : '';

            // ���ID
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
            // ��Х��륰�롼�ץ����������ե饰
            $this->params['session']['mg_flg'] = '1';
        }else{
            $this->params['session']['mg_flg'] = '0';
        }

        /**
         * �᥽�å�̾����
         */
        // HTTP�إå��������Ƥ����
        $_HEADER = apache_request_headers();
        $chk_method = isset( $_HEADER['HTTP_X_HTTP_METHOD_OVERRIDE'] )
                           ? $_HEADER['HTTP_X_HTTP_METHOD_OVERRIDE'] : '';

        if( $chk_method === '' ){
            $chk_method = isset( $_SERVER['HTTP_X_HTTP_METHOD_OVERRIDE'] )
                               ? $_SERVER['HTTP_X_HTTP_METHOD_OVERRIDE'] : '';
        }

        $http_method = isset( $_SERVER['REQUEST_METHOD'] )
                            ? $_SERVER['REQUEST_METHOD'] : '';

        // ���ꤵ�줿HTTP�᥽�åɤ������Ǥ��ʤ��ä����
        if( $chk_method === '' ){
            // QueryString��_method�פ����
            $chk_method = isset( $input_post['_method'] ) ? $input_post['_method'] : '';
        }

        if( $chk_method === '' ){
            // ����˼����Ǥ��ʤ��ä���硢�̾��HTTP�᥽�åɤ����
            $chk_method = ( $chk_method !== '' ) ? $chk_method : $http_method;
        }

        // HTTP�᥽�å�
        if( in_array( $chk_method, array('GET','POST','PUT','DELETE') ) === false ){
            $this->setError( '99', __METHOD__.__LINE__, 'no method err ' );
            return array( 'code' => -1, 'params' => $this->params );
        }

        $this->params['session']['http_method'] = $chk_method;

        // �¹Ԥ���API����
        $ret = $this->getExecAPI();

        return array( 'code' => $ret, 'params' => $this->params );
    }

    /******************************************************
    * �Х�ǡ��ȥ����å�
    * in  : �ʤ�
    * out : �ʤ�
    ******************************************************/
    function chkCgiValidate(){
        $client_id = isset( $this->params['session']['client_id'] ) ? $this->params['session']['client_id'] : '';
        $client_pw = isset( $this->params['session']['in']['we_passwd'] ) ? $this->params['session']['in']['we_passwd'] : '';
        $this->params['session']['client_pw'] = $client_pw;

        if( $client_id === '' ){
            // ̤���ꥨ�顼
            $this->setError( '102-3', __METHOD__.__LINE__, 'no client_id' );
            return array( 'code' => -1, 'params' => $this->params );
        }

        if( $client_pw === '' ){
            // ̤���ꥨ�顼
            $this->setError( '102-1', __METHOD__.__LINE__, 'no client_pw' );
            return array( 'code' => -1, 'params' => $this->params );
        }

        // ���ID����ե�����
        $this->params['client'] = $this->readYaml( CONFIG_SYSTEM_DIR . $client_id . '.yaml' );
        if ( empty( $this->params['client'] ) ) {
            // ����ե����뤬¸�ߤ��ʤ�
            $this->setError( '99', __METHOD__.__LINE__, 'no client yaml' );
            return array( 'code' => -1, 'params' => $this->params );
        }

        // API���Ѳ��ݥ����å�
        $res = $this->chkUseAPI();
        if( $res < 0 ){
            $this->setError( '102-2', __METHOD__.__LINE__, 'chk api' );
            return array( 'code' => -1, 'params' => $this->params );
        }

        // ��³�ѥ���ɥ����å�
        $res = $this->chkClientPw( $client_pw );
        if( $res < 0 ){
            $this->setError( '102-1', __METHOD__.__LINE__, 'chk client_pw' );
            return array( 'code' => -1, 'params' => $this->params );
        }

        return array( 'code' => 0, 'params' => $this->params );
    }

    /**
     * ���Ѳ���API�����å�
     *  in  : �ʤ�
     *  out :
     */
    function chkUseAPI(){
        // ���Ѳ���API�����å�
        $apiname     = isset( $this->params['session']['apiname'] ) ? $this->params['session']['apiname'] : '';
        $api_list    = isset( $this->params['client']['useapi_list'] ) ? $this->params['client']['useapi_list'] : array();
        $api_list_mg = isset( $this->params['client']['useapi_list_mg'] ) ? $this->params['client']['useapi_list_mg'] : array();

        $mg_flg    = $this->_get( 'session', 'mg_flg' );
        if( $mg_flg === '1' ){
            // ��Х��륰�롼�ץ���������
            if( !in_array( $apiname, $api_list_mg ) ){
                // �����Բ�
                return -1;
            }
        }else{
            if( !in_array( $apiname, $api_list ) ){
                // �����Բ�
                return -1;
            }
        }

        return 0;
    }

    /**
     * ��³�ѥ���ɥ����å�
     *  in  : we_passwd
     *  out :
     */
    function chkClientPw( $client_pw ){
        $chk_pw = isset( $this->params['client']['client_pw'] ) ? $this->params['client']['client_pw'] : '';
        // �ϥå��岽
        $s_client_pw = sha1( $client_pw );

        if( $chk_pw !== $s_client_pw ){
            // �ѥ�����԰���
            return -1;
        }

        return 0;
    }



    /******************************************************
    * API��̶��̽���
    * in  : API�¹�OUT�ѥ�᡼��
    * out : �����Ѷ��̥ѥ�᡼��
    ******************************************************/
    function getBoAPIOut( $ret ){
        $ses_data = array();

        // ɸ�ॹ�ơ�����
        $ses_data['STATUS_CODE']        = $this->_getParam( $ret, 'BO_CL_CODE', 0 );
        $ses_data['STATUS_DETAIL_CODE'] = $this->_getParam( $ret, 'BO_CL_DETAIL_CODE', 0 );
        $ses_data['ERROR_DETAIL_INFO']  = $this->_getParam( $ret, 'BO_CL_DETAIL_INFO', 0 );
        // snr=�����
        $ses_data['ERROR_DETAIL_INFO']  = preg_replace( "/:snr=(.*)/", "", $ses_data['ERROR_DETAIL_INFO'] );

        if( $ses_data['STATUS_CODE'] === '3' && isset( $ret['valid_err_count'] )){
            // �ѥ�᡼�����顼
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
    * MOSS�����Ը��� ���Ѽ���ϿAPI�η�̤򥻥å���������
    * in  : �ʤ�
    * out : �ʤ�
    ******************************************************/
    function getC_MOSS_Member_my_addOut( $ret ){
        $ses_data = $this->getBoAPIOut( $ret );

        if( $this->_getParam( $ret, 'BO_CL_CODE', 0 ) === '0' ){
            // ǧ�ڥ�������Ⱦ���
            $ses_data['index_free4']      = $this->_getParam( $ret, 'index_free4', 0 );
            $ses_data['index_free_date1'] = $this->_getParam( $ret, 'index_free_date1', 0 );
            $ses_data['index_free_date2'] = $this->_getParam( $ret, 'index_free_date2', 0 );
            $ses_data['index_free_date3'] = $this->_getParam( $ret, 'index_free_date3', 0 );
            $ses_data['index_free1']      = $this->_getParam( $ret, 'index_free1', 0 );
            $ses_data['index_free2']      = $this->_getParam( $ret, 'index_free2', 0 );
            $ses_data['item_free2']       = $this->_getParam( $ret, 'item_free2', 0 );
            $ses_data['item_free10']      = $this->_getParam( $ret, 'item_free10', 0 );
        
            // ���Ѽԥ�������Ⱦ���
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
    * MOSS���ѼԾ����ѹ�API�η�̤򥻥å���������
    * in  : �ʤ�
    * out : �ʤ�
    ******************************************************/
    function getC_MOSS_MemberState_my_chgOut( $ret ){
        $ses_data = $this->getBoAPIOut( $ret );

        if( $this->_getParam( $ret, 'BO_CL_CODE', 0 ) === '0' ){
            // ǧ�ڥ�������Ⱦ���
            $ses_data['index_free4']      = $this->_getParam( $ret, 'index_free4', 0 );
            $ses_data['index_free_date1'] = $this->_getParam( $ret, 'index_free_date1', 0 );
            $ses_data['index_free_date2'] = $this->_getParam( $ret, 'index_free_date2', 0 );
            $ses_data['index_free_date3'] = $this->_getParam( $ret, 'index_free_date3', 0 );
            $ses_data['index_free1']      = $this->_getParam( $ret, 'index_free1', 0 );
            $ses_data['index_free2']      = $this->_getParam( $ret, 'index_free2', 0 );
            $ses_data['item_free2']       = $this->_getParam( $ret, 'item_free2', 0 );
            $ses_data['item_free10']      = $this->_getParam( $ret, 'item_free10', 0 );

            // ʣ������б����ơ�����(���顼���Τ߽���)
            if( $this->_getParam( $ret, 'status_status', 0 ) !== '0' ){
                $ses_data['status_status'] = $this->_getParam( $ret, 'status_status', 0 );
            }
        
            // �ѹ��оݥ�������Ⱦ���
            $ses_data['hi_index_free4']      = $this->_getParam( $ret, 'hi_index_free4', 0 );
            $ses_data['hi_index_free_date1'] = $this->_getParam( $ret, 'hi_index_free_date1', 0 );
            $ses_data['hi_index_free_date2'] = $this->_getParam( $ret, 'hi_index_free_date2', 0 );
            $ses_data['hi_index_free_date3'] = $this->_getParam( $ret, 'hi_index_free_date3', 0 );
            $ses_data['hi_index_free1']      = $this->_getParam( $ret, 'hi_index_free1', 0 );
            $ses_data['hi_index_free2']      = $this->_getParam( $ret, 'hi_index_free2', 0 );
            $ses_data['hi_item_free2']       = $this->_getParam( $ret, 'hi_item_free2', 0 );
            $ses_data['hi_item_free10']      = $this->_getParam( $ret, 'hi_item_free10', 0 );

            // �ѹ��оݥ�������Ⱦ��� n=2��10
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
    * MOSS���Ѽԡ������Ծ����ѹ�API�η�̤򥻥å���������
    * in  : �ʤ�
    * out : �ʤ�
    ******************************************************/
    function getC_MOSS_Member_my_modOut( $ret ){
        $ses_data = $this->getBoAPIOut( $ret );

        if( $this->_getParam( $ret, 'BO_CL_CODE', 0 ) !== '0' ){
            return $ses_data;
        }

        // ǧ�ڥ�������Ⱦ���
        $ses_data['index_free4']      = $this->_getParam( $ret, 'index_free4', 0 );
        $ses_data['index_free_date1'] = $this->_getParam( $ret, 'index_free_date1', 0 );
        $ses_data['index_free_date2'] = $this->_getParam( $ret, 'index_free_date2', 0 );
        $ses_data['index_free_date3'] = $this->_getParam( $ret, 'index_free_date3', 0 );
        $ses_data['index_free1']      = $this->_getParam( $ret, 'index_free1', 0 );
        $ses_data['index_free2']      = $this->_getParam( $ret, 'index_free2', 0 );
        $ses_data['item_free2']       = $this->_getParam( $ret, 'item_free2', 0 );
        $ses_data['item_free10']      = $this->_getParam( $ret, 'item_free10', 0 );
        
        // �ѹ��оݥ�������Ⱦ���(ǧ������="2"�ξ��Τ��ֵ�)
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
    * MOSS���Ѽԡ������Ծ��󻲾�API�η�̤򥻥å���������
    * in  : �ʤ�
    * out : �ʤ�
    ******************************************************/
    function getC_MOSS_Member_my_refOut( $ret ){
        $ses_data = $this->getBoAPIOut( $ret );

        if( $this->_getParam( $ret, 'BO_CL_CODE', 0 ) !== '0' ){
            return $ses_data;
        }

        // ǧ�ڥ�������Ⱦ���
        $ses_data['index_free4']      = $this->_getParam( $ret, 'index_free4', 0 );
        $ses_data['index_free_date1'] = $this->_getParam( $ret, 'index_free_date1', 0 );
        $ses_data['index_free_date2'] = $this->_getParam( $ret, 'index_free_date2', 0 );
        $ses_data['index_free_date3'] = $this->_getParam( $ret, 'index_free_date3', 0 );
        $ses_data['index_free1']      = $this->_getParam( $ret, 'index_free1', 0 );
        $ses_data['index_free2']      = $this->_getParam( $ret, 'index_free2', 0 );
        $ses_data['item_free2']       = $this->_getParam( $ret, 'item_free2', 0 );
        $ses_data['item_free10']      = $this->_getParam( $ret, 'item_free10', 0 );


        // �����оݥ�������Ⱦ���(ǧ������="2"�ξ��Τ��ֵ�)
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
    * MOSS�ѥ�����ѹ�API�η�̤򥻥å���������
    * in  : �ʤ�
    * out : �ʤ�
    ******************************************************/
    function getC_MOSS_Password_my_modOut( $ret ){
        $ses_data = $this->getBoAPIOut( $ret );

        if( $this->_getParam( $ret, 'BO_CL_CODE', 0 ) !== '0' ){
            return $ses_data;
        }

        // ǧ�ڥ�������Ⱦ���
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
    * MOSS�������ݥ���API�η�̤򥻥å���������
    * in  : �ʤ�
    * out : �ʤ�
    ******************************************************/
    function getC_MOSS_GAODNY_my_mente2Out( $ret ){
        $ses_data = $this->getBoAPIOut( $ret );

        if( $this->_getParam( $ret, 'BO_CL_CODE', 0 ) !== '0' ){
            return $ses_data;
        }


        // ǧ�ڥ�������Ⱦ���
        $ses_data['index_free4']      = $this->_getParam( $ret, 'index_free4', 0 );
        $ses_data['index_free_date1'] = $this->_getParam( $ret, 'index_free_date1', 0 );
        $ses_data['index_free_date2'] = $this->_getParam( $ret, 'index_free_date2', 0 );
        $ses_data['index_free_date3'] = $this->_getParam( $ret, 'index_free_date3', 0 );
        $ses_data['index_free1']      = $this->_getParam( $ret, 'index_free1', 0 );
        $ses_data['index_free2']      = $this->_getParam( $ret, 'index_free2', 0 );
        $ses_data['item_free2']       = $this->_getParam( $ret, 'item_free2', 0 );
        $ses_data['item_free10']      = $this->_getParam( $ret, 'item_free10', 0 );

        $dnyfil_type = $this->_get( 'session', 'in', 'dnyfil_type' );

        // ���̥ѥ�᡼�������᡼��������ݥ����פ�����ˤ���ֵ�
        if( $dnyfil_type === 'all_list' ){

            // 1)�᡼��������ݥ�����="all_list"�����򤷤����
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

            // 3)�᡼��������ݥ�����="from_fil", "to_fil", "cc_fil"�ޤ���"subject_fil"�����򤷤����
            $ses_data['dnyfil_data_count'] = $this->_getParam( $ret, 'dnyfil_data_count', 0 );

            if( $ses_data['dnyfil_data_count'] > 0 ){
                $ses_data['dnyfil_type']       = $this->_getParam( $ret, 'dnyfil_type', 0 );
                for( $i = 1; $i <= $ses_data['dnyfil_data_count']; $i++ ){
                    // �ե��륿����������� �ֵ���ʬ����
                    $ses_data["dnyfil_data[{$i}]"]   = $this->_getParam( $ret, 'dnyfil_data', $i );
                }
            }
        }

        return $ses_data;
    }


    /******************************************************
    * ���Ѽ���ϿAPI�η�̤򥻥å���������
    *   �ʥ�Х��륰�롼�ץ�����������
    * in  : �ʤ�
    * out : �ʤ�
    ******************************************************/
    function getC_MOSS_Member_my_add_mgOut( $ret ){
        $ses_data = $this->getBoAPIOut( $ret );

        if( $this->_getParam( $ret, 'BO_CL_CODE', 0 ) === '0' ){
            // ��������Ⱦ���
            $ses_data['index_free4']      = $this->_getParam( $ret, 'index_free4', 0 );
            $ses_data['index_free_date1'] = $this->_getParam( $ret, 'index_free_date1', 0 );
            $ses_data['index_free_date2'] = $this->_getParam( $ret, 'index_free_date2', 0 );
            $ses_data['index_free_date3'] = $this->_getParam( $ret, 'index_free_date3', 0 );
            $ses_data['index_free2']      = $this->_getParam( $ret, 'index_free2', 0 );
        }

        return $ses_data;
    }

    /******************************************************
    * ���ѼԾ����ѹ�API�η�̤򥻥å���������
    *   �ʥ�Х��륰�롼�ץ�����������
    * in  : �ʤ�
    * out : �ʤ�
    ******************************************************/
    function getC_MOSS_MemberState_my_chg_mgOut( $ret ){
        $ses_data = $this->getBoAPIOut( $ret );

        if( $this->_getParam( $ret, 'BO_CL_CODE', 0 ) === '0' ){
            // ǧ�ڥ�������Ⱦ���
            $ses_data['index_free4']      = $this->_getParam( $ret, 'index_free4', 0 );
            $ses_data['index_free_date1'] = $this->_getParam( $ret, 'index_free_date1', 0 );
            $ses_data['index_free_date2'] = $this->_getParam( $ret, 'index_free_date2', 0 );
            $ses_data['index_free_date3'] = $this->_getParam( $ret, 'index_free_date3', 0 );
            $ses_data['index_free2']      = $this->_getParam( $ret, 'index_free2', 0 );
        }

        return $ses_data;
    }

    /******************************************************
    * ���ѼԾ����ѹ�API�η�̤򥻥å���������
    *   �ʥ�Х��륰�롼�ץ�����������
    * in  : �ʤ�
    * out : �ʤ�
    ******************************************************/
    function getC_MOSS_Member_my_mod_mgOut( $ret ){
        $ses_data = $this->getBoAPIOut( $ret );

        if( $this->_getParam( $ret, 'BO_CL_CODE', 0 ) !== '0' ){
            return $ses_data;
        }

        // ��������Ⱦ���
        $ses_data['index_free4']      = $this->_getParam( $ret, 'index_free4', 0 );
        $ses_data['index_free_date1'] = $this->_getParam( $ret, 'index_free_date1', 0 );
        $ses_data['index_free_date2'] = $this->_getParam( $ret, 'index_free_date2', 0 );
        $ses_data['index_free_date3'] = $this->_getParam( $ret, 'index_free_date3', 0 );
        $ses_data['index_free2']      = $this->_getParam( $ret, 'index_free2', 0 );

        return $ses_data;
    }

    /******************************************************
    * ���ѼԾ��󻲾�API�η�̤򥻥å���������
    *   �ʥ�Х��륰�롼�ץ�����������
    * in  : �ʤ�
    * out : �ʤ�
    ******************************************************/
    function getC_MOSS_Member_my_ref_mgOut( $ret ){
        $ses_data = $this->getBoAPIOut( $ret );
        if( $this->_getParam( $ret, 'BO_CL_CODE', 0 ) !== '0' ){
            return $ses_data;
        }

        // ��������Ⱦ���
        $ses_data['index_free4']      = $this->_getParam( $ret, 'index_free4', 0 );
        $ses_data['index_free_date1'] = $this->_getParam( $ret, 'index_free_date1', 0 );
        $ses_data['index_free_date2'] = $this->_getParam( $ret, 'index_free_date2', 0 );
        $ses_data['index_free_date3'] = $this->_getParam( $ret, 'index_free_date3', 0 );
        $ses_data['index_free2']      = $this->_getParam( $ret, 'index_free2', 0 );

        return $ses_data;
    }

    /******************************************************
    * �ѥ�����ѹ�API�η�̤򥻥å���������
    *   �ʥ�Х��륰�롼�ץ�����������
    * in  : �ʤ�
    * out : �ʤ�
    ******************************************************/
    function getC_MOSS_Password_my_mod_mgOut( $ret ){
        $ses_data = $this->getBoAPIOut( $ret );

        if( $this->_getParam( $ret, 'BO_CL_CODE', 0 ) !== '0' ){
            return $ses_data;
        }

        // ��������Ⱦ���
        $ses_data['index_free4']      = $this->_getParam( $ret, 'index_free4', 0 );
        $ses_data['index_free_date1'] = $this->_getParam( $ret, 'index_free_date1', 0 );
        $ses_data['index_free_date2'] = $this->_getParam( $ret, 'index_free_date2', 0 );
        $ses_data['index_free_date3'] = $this->_getParam( $ret, 'index_free_date3', 0 );
        $ses_data['index_free2']      = $this->_getParam( $ret, 'index_free2', 0 );

        return $ses_data;
    }

    /******************************************************
    * Web���󥸥�������ʥꥪWrapperAPI
    * in  : �ʤ�
    * out : �ʤ�
    ******************************************************/
    function setC_WebEngine_wrapper( $no, $api_name ){
        $error = $this->callBo( $this->apiIn( $no ) );
        if( $error < 0 ){
             return;
        }

        // �ֵ��ͻ���
        $ret = $this->apiOut( $no );

        $mg_flg    = $this->_get( 'session', 'mg_flg' );
        if( $mg_flg === '1' ){
            $api_name = $api_name . STR_MG;
        }
        $execapi = "get{$api_name}Out";
        if( !method_exists( $this, $execapi ) ){
            return -1;
        }

        // ���å����˳�Ǽ
        $ses_data = $this->$execapi( $ret );
        $this->setOutSession( $ses_data );
        return;
    }

    /******************************************************
    * ���顼��᡼������
    * in  : BO API�ֵ���
    * out : �ʤ�
    ******************************************************/
    protected function sendAlertMail( $out ){
        require_once( BASE_LIB_DIR . '/Mail.php' );

        $mail = $this->_get( 'env', 'AlertMail' );

        // �᡼�������ʤ��ξ�硢return
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
            // BOAPI�ƽФ����顼
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

        // ���顼���ѥ�᡼��
        $para   = array();
        $puterr = array();
        $puterr['STATUS_CODE'] = $bo_cl;
        $puterr['STATUS_DETAIL_CODE'] = $bo_det;
        $puterr['ERROR_DETAIL_INFO']  = $bo_info;
        $this->params['puterr'] = $puterr;

        // �᡼������
        $ret = $m->sendmail( $args );
        if( $ret['code'] < 0 || $ret['code'] === false ) {
            $para = array( 'sendAlertMailErr' => __METHOD__.__LINE__);
        }

        // ���顼������
        $this->_putlog($para);
    }
}
