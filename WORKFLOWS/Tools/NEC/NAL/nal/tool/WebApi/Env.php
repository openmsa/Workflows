<?php
// **********************************************************************
// * 基盤共通環境変数設定 サンプル
// **********************************************************************

// **********************
// ディレクトリ関連
// **********************
// ホームディレクトリ
define( 'BASE_HOME_DIR', '/home2/bsd1333t/contents/asset/' );

// binディレクトリ
define( 'BASE_BIN_DIR', BASE_HOME_DIR . 'bin/' );
// キャッシュディレクトリ
define( 'BASE_CACHE_DIR', BASE_HOME_DIR . 'cache/' );
// コンフィグディレクトリ
define( 'BASE_CONFIG_DIR', BASE_HOME_DIR . 'config/' );
// ライブラリディレクトリ
define( 'BASE_LIB_DIR', BASE_HOME_DIR . 'lib/' );
// PHPライブラリディレクトリ
define( 'BASE_PHPLIB_DIR', BASE_HOME_DIR . 'phplib/' );
// テンプレートディレクトリ
define( 'BASE_TEMPLATE_DIR', BASE_HOME_DIR . 'template/' );
// コンパイルディレクトリ
define( 'BASE_TEMPLATE_C_DIR', BASE_HOME_DIR . 'template_c/' );
// テンポラリディレクトリ
define( 'BASE_TMP_DIR', BASE_HOME_DIR . 'tmp/' );


// *****************************
// パラメータ関連  ★変更不可★
// *****************************
// 汎用CGIパラメータ第１階層名を指定
define( 'PARAM', 'param' );
define( 'PARAM_IN', 'param_in' );
define( 'SVC', 'svc' );
define( 'CTRL', 'ctrl' );
define( 'DISP', 'disp' );
define( 'ERROR', 'error' );
define( 'DB', 'db' );
define( 'VALI', 'vali' );
define( 'API', 'api' );
define( 'EXECFLOW', 'execflow' );
define( 'OPT', 'opt' );


// **********************
// プレビュー関連
// **********************
// プレビュー表示フラグ
define( 'PREVIEW', '1' );


// **********************
// 文字コード関連
// **********************
// CGI内文字コード
define( 'BASE_CGI_CHARCODE', 'euc-jp' );
// 画面文字コード
define( 'BASE_DISP_CHARCODE', 'euc-jp' );


// **********************
// データベース関連
// **********************
// データベース使用フラグ
$_BASE_ENV['DB_USE_FLG'] = 1;
// サポートするDB
$_BASE_ENV['PHP_DB_SUPPORT'] = array('mysql', 'pgsql', 'oci');

// PHP用DB接続情報格納ディレクトリ
$_BASE_ENV['PHP_DBCONF_DIR'] = BASE_CONFIG_DIR . 'db';

$_BASE_ENV['SERVER_ENVIRONMENT'] = 'test';

$_BASE_ENV['PHP_DB_ENCKEY'] = 'scpf';


// ***********************
// forkバッチ設定
// ***********************
define( 'FORK_YAML_DIR', BASE_TMP_DIR . 'fork/' );
define( 'FORK_YAML_ENCKEY', 'webossfork' );
define( 'FORK_BATCH_PATH', BASE_BIN_DIR . 'http_fork_host05.php' );


// ***********************
// インクルードパスの設定
// ***********************
set_include_path(implode(PATH_SEPARATOR, array(
    '.',        // 実行スクリプトと同じディレクトリ
    BASE_PHPLIB_DIR, // PHPライブラリディレクトリ
    BASE_LIB_DIR,    // ライブラリディレクトリ
    get_include_path()
)));
