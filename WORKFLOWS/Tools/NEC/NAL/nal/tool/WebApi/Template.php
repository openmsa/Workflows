<?php

require_once( 'Smarty.class.php' );

class Template {
/* ���󥹥ȥ饯�� */
	function Template(){
	}

// * �¹�
// * in:
// * args['params']       = ���Ѥ���ѥ�᡼��
// * args['template_dir'] = �ƥ�ץ졼�ȥǥ��쥯�ȥ�
// * args['compile_dir']  = ����ѥ���ƥ�ץ졼�ȥǥ��쥯�ȥ�
// * args['config_dir']   = ����ե����ǥ��쥯�ȥ�
// * args['cache_dir']    = ����å���ǥ��쥯�ȥ�
// * args['compile_id']   = ����ѥ���ID
// * args['filename']     = �ƥ�ץ졼�ȥե�����̾
// * args['print_flg']    = ���ϥե饰
// *                          1 : ɸ����Ϥ���ʥǥե���ȡ�
// *                          2 : ɸ����Ϥʤ�
// * args['fromcode']     = �Ѵ���ʸ��������
// * args['tocode']       = �Ѵ���ʸ��������
// *                        ���Ѵ������Ѵ��褤���줫����ʤ��ξ��Ϥ��Τޤ��ֵ�
// * out:
// * result['code']    = 0 or -1
// * result['message'] = ���顼��å�����
// * result['string']  = �ƥ�ץ졼�Ƚ��Ϸ��ʸ����
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

		// ���ϥե饰�Υǥե��������
		if( !(isset($print_flg)) || $print_flg == '' ){
			$print_flg = 1;
		}

		// out�ѥ�˥��顼��ǥե��������
		$result = array( 'code' => -1, 'message' => '' );

		// �ѥ�᡼�������å�
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

		// �ƥ�ץ졼�ȥ���å���ǥ��쥯�ȥ꤬¸�ߤ��ʤ����Ϻ���
		if( !(is_dir( $compile_dir )) ){
			$chk = mkdir( $compile_dir, 0777, true );
			if( !($chk) ){
				$result['message'] = 'compile_dir cannot make!';
				return $result;
			}
		}
		// ����å���ǥ��쥯�ȥ꤬¸�ߤ��ʤ����Ϻ���
		if( !(is_dir( $cache_dir )) ){
			$chk = mkdir( $cache_dir, 0755, true );
			if( !($chk) ){
				$result['message'] = 'cache_dir cannot make!';
				return $result;
			}
		}

		// Smarty �������
		$smarty = new Smarty();
		$smarty->template_dir = $template_dir;
		$smarty->compile_dir = $compile_dir;
		$smarty->config_dir = $config_dir;
		$smarty->cache_dir = $cache_dir;
		$smarty->compile_id = $compile_id;
		$smarty->caching = 0;
		$smarty->compile_check = TRUE;

		// �ƥ�ץ졼�ȥ���å�������
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

		// ���Ϸ�̤�ʸ���������Ѵ�
		if( $fromcode !== '' && $tocode !== '' && $fromcode !== $tocode ) {
			require_once 'Subfunc.php';
			$sf = new Subfunc(1);
			$output = $sf->chgcode( $output, $tocode, $fromcode );
		}

		// ���ϥե饰��1�ξ���ɸ�����
		if( isset($print_flg) && $print_flg == 1 ){
			print( $output );
		}

		$result['code'] = 0;
		$result['string'] = $output;
	
		return $result;
	}

    /**
     * ����å���ե�������
     * in: �����ǥ��쥯�ȥ�
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
