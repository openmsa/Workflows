<?php

require_once( 'Smarty.class.php' );

class Template {
/* コンストラクタ */
	function Template(){
	}

// * 実行
// * in:
// * args['params']       = 使用するパラメータ
// * args['template_dir'] = テンプレートディレクトリ
// * args['compile_dir']  = コンパイルテンプレートディレクトリ
// * args['config_dir']   = コンフィグディレクトリ
// * args['cache_dir']    = キャッシュディレクトリ
// * args['compile_id']   = コンパイルID
// * args['filename']     = テンプレートファイル名
// * args['print_flg']    = 出力フラグ
// *                          1 : 標準出力あり（デフォルト）
// *                          2 : 標準出力なし
// * args['fromcode']     = 変換元文字コード
// * args['tocode']       = 変換先文字コード
// *                        ※変換元、変換先いずれか設定なしの場合はそのまま返却
// * out:
// * result['code']    = 0 or -1
// * result['message'] = エラーメッセージ
// * result['string']  = テンプレート出力結果文字列
// *
	function exec( $args ){
		$params = $args['params'];

		$template_dir = $args['template_dir'];
		$compile_dir  = $args['compile_dir'];
		$config_dir   = $args['config_dir'];
		$cache_dir    = $args['cache_dir'];
		$compile_id = '';
		if( isset($args['compile_id']) ){
			$compile_id   = $args['compile_id'];
		}
		$filename     = $args['filename'];
		$print_flg = '';
		if( isset($args['print_flg']) ){
			$print_flg = $args['print_flg'];
		}
		$fromcode     = isset( $args['fromcode'] ) ? $args['fromcode'] : '';
		$tocode       = isset( $args['tocode'] ) ? $args['tocode'] : '';

		// 出力フラグのデフォルト設定
		if( !(isset($print_flg)) || $print_flg == '' ){
			$print_flg = 1;
		}

		// outパラにエラーをデフォルト設定
		$result = array( 'code' => -1, 'message' => '' );

		// パラメータチェック
		if( !($template_dir) ){
				$result['message'] = 'no template_dir!';
				return $result;
		}
		if( !($compile_dir) ){
				$result['message'] = 'no compile_dir!';
				return $result;
		}
		if( !($config_dir) ){
				$result['message'] = 'no config_dir!';
				return $result;
		}
		if( !($cache_dir) ){
				$result['message'] = 'no cache_dir!';
				return $result;
		}

		// テンプレートキャッシュディレクトリが存在しない場合は作成
		if( !(is_dir( $compile_dir )) ){
			$chk = mkdir( $compile_dir, 0777, true );
			if( !($chk) ){
				$result['message'] = 'compile_dir cannot make!';
				return $result;
			}
		}
		// キャッシュディレクトリが存在しない場合は作成
		if( !(is_dir( $cache_dir )) ){
			$chk = mkdir( $cache_dir, 0755, true );
			if( !($chk) ){
				$result['message'] = 'cache_dir cannot make!';
				return $result;
			}
		}

		// Smarty 初期設定
		$smarty = new Smarty();
		$smarty->template_dir = $template_dir;
		$smarty->compile_dir = $compile_dir;
		$smarty->config_dir = $config_dir;
		$smarty->cache_dir = $cache_dir;
		$smarty->compile_id = $compile_id;
		$smarty->caching = 0;
		$smarty->compile_check = TRUE;

		// テンプレートキャッシュ制御
		$lstat = lstat(dirname(__FILE__)."/Env.php") ;
		$f     = dirname(__FILE__)."/" . php_uname("n") ;
		if( file_exists($f) ) {
			$stat  = stat($f) ;
			if( $stat['mtime'] < $lstat['mtime'] ) {
                Template::_clearCache( TEMPLATE_C_DIR );
				touch($f);
             }
		} else {
            Template::_clearCache( TEMPLATE_C_DIR );
			touch($f);
		}

		foreach( $params as $key => $val ){
			$smarty->assign( $key, $val );
		}

		$output = $smarty->fetch( $filename );
		if( !($output) ){
			$result['message'] = 'output nothing!';
			return $result;
		}

		// 出力結果を文字コード変換
		if( $fromcode !== '' && $tocode !== '' && $fromcode !== $tocode ) {
			require_once 'Subfunc.php';
			$sf = new Subfunc(1);
			$output = $sf->chgcode( $output, $tocode, $fromcode );
		}

		// 出力フラグが1の場合は標準出力
		if( isset($print_flg) && $print_flg == 1 ){
			print( $output );
		}

		$result['code'] = 0;
		$result['string'] = $output;
	
		return $result;
	}

    /**
     * キャッシュファイル削除
     * in: 起点ディレクトリ
     */
    private static function _clearCache( $dir ) {
        $files = scandir( $dir );
        foreach ( $files as $file ) {
            if ( $file === '.' || $file === '..' ) {
                continue;
            }
            $target = $dir . $file;
            if ( is_dir( $target ) ) {
                Template::_clearCache( $target . '/' );
            } else {
                @unlink( $target );
            }
        }
    }
}
