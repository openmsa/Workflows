<?php
/**
 * 1.SYSTEM   : 汎用CGI
 * 2.FILE     : Page_env_dev.php
 * 3.FUNCTION : 環境変数設定 dev環境
 * 4.CREATE   : 2011/05/30
 * 5.UPDATE   : 
 * @version 
 */
umask(0022);

// phpエラー出力(1:出力)
//ini_set( 'display_errors', '1' );

/**
 * サービスID
 */
define( 'SERVICEID', 'webapi' );

/**
 * ログ・ワンタイムセッション暗号化キー
 */
define( 'ENC_KEY', '123edcxzaqws' );

/**
 * ディレクトリ関連
 */
define( 'HOME_DIR', BASE_HOME_DIR . 'service/' . SERVICEID . '/' );
define( 'CACHE_DIR', HOME_DIR . 'cache/' );
define( 'CONFIG_DIR', HOME_DIR . 'config/' );
define( 'HTDOCS_DIR', HOME_DIR . 'htdocs/' );
define( 'LIB_DIR', HOME_DIR . 'extlib/' );
define( 'LOG_DIR', '/var/log/bsd1333t/log/' . SERVICEID . '/' );
define( 'TEMPLATE_DIR', HOME_DIR . 'template/' );
define( 'TEMPLATE_C_DIR', HOME_DIR . 'template_c/' );
define( 'TEMPLATE_P_DIR', HOME_DIR . 'template_p/' );
define( 'TEMPLATE_P_C_DIR', HOME_DIR . 'template_p_c/' );

// ベースログディレクトリ
define( 'BASE_LOG_DIR', LOG_DIR . SERVICEID . '_' );

/**
 * 呼出モジュール
 */
define( 'CALL_API_FILE', LIB_DIR . 'WebAPI.php' );
define( 'CALL_API_MOD', 'WebAPI' );

/**
 * メンテナンスファイル
 */
define( 'MAINTE_FILE', CONFIG_DIR . 'ms.txt' );

/**
 * 企業ID設定ファイル
 */
define( 'CONFIG_SYSTEM_DIR', HOME_DIR . 'config/system/' );

/**
 * ドメイン
 */
//define( 'WEBAPI_DOMAIN', 'https://133.208.65.97:825/' );
define( 'WEBAPI_DOMAIN', 'https://tapi.moss.biglobe.ne.jp/' );

/**
 * エラーログ
 */
define( 'ERR_LOG_FILE', BASE_LOG_DIR . 'errlog_%_HOSTNAME_%_%_DATE_%.log');

/**
 * モバイルグループウェア向け
 */
define( 'STR_MG', '_mg');


// **********************
// 文字コード関連
// **********************
// CGI内文字コード
define( 'CGI_CHARCODE', 'utf-8' );
// JSONファイル文字コード
define( 'JSON_CHARCODE', 'utf-8' );

// **********************
// API関連
// **********************
// APIログファイル
define( 'API_LOG_FILE', BASE_LOG_DIR . '%_APINAME_%_%_HOSTNAME_%_%_DATE_%.log');
// APIログファイルフラグ
define( 'API_LOG_FLAG', 1 );
// BOのAPI呼び出し
define( 'API_ASP_FCALL', '/usr/local/bobio/ASP_FunctionCall.test/client/bin/ASP_FunctionCall.test' );
//define( 'API_ASP_FCALL', '/home/ap/bsd1333t/contents/asset/stub/ASP_FunctionCall.stub' );


// **********************
// バリデータ関連
// **********************
// バリデータ設定ファイル格納ディレクトリ(JSON)
define( 'VALID_RULES_DIR', HTDOCS_DIR . '/portal/js/' );
// バリデータ設定ファイル名(JSON)
define( 'VALID_RULES_FNAME', 'chk_data.js' );
// カスタムバリデータ関数クラス名（＝ファイル名）
define( 'VALID_MX_CLASS', 'MxValidate_func' );

// *********************************
// 設定ファイル
// *********************************
define( 'ERROR_MSG_CFG', CONFIG_DIR . 'error_msg.yaml' );
define( 'MOSS_ENV', CONFIG_DIR . 'env.yaml' );

/**
 * デバッグ関連
 */
define( 'DEBUG', '' );

