<?php

class Subfunc {
// **********************************************************************
// * ���󥹥ȥ饯��
// * [in]
// * $perlmode : �����perl�⥸�塼������
// * [��ջ���]
// * �᥽�åɡ�get_validate_rules�ס�data_encode�ס�chgcode�פΤ����줫��
// * ���Ѥ�����ϡ�ɬ�� $perlmode �����ꤹ�����
// **********************************************************************
	function Subfunc( $perlmode = NULL ){

		$this->perlmode = $perlmode;

		if( isset($perlmode) ){
			try{
				// ʸ���������Ѵ������ΰ٤ˡ�perl�⥸�塼���Henkan.pm�פ�use
				$perl = new Perl();
				// host05�ѥѥ��ɲ�
				$perl->eval('use Henkan;');
				$this->perl = $perl;
			}catch( Exception $e ){
				$this->perl = NULL;
			}
		}else{
			$this->perl = NULL;
		}
	}

// *****************************************************************
// * [�ؿ�̾]
// *  get_dirlist
// *  �����ǥ��쥯�ȥ�ꥹ������
// * [��������]
// *  �����ǥ��쥯�ȥ�ꥹ�Ȥ����ꤹ�롣
// *    �㡧ͥ���̤ϲ����ΤȤ��ꡣ
// *         1. (����dir/)��������ʬ��/��������ʬ��/������ID/�����ڡ���ID/
// *         2. (����dir/)��������ʬ��/��������ʬ��/�����ڡ���ID/
// *         3. (����dir/)��������ʬ��/�����ڡ���ID/
// *         4. (����dir/)��������ʬ��/��������ʬ��/������ID/
// *         5. (����dir/)��������ʬ��/��������ʬ��/
// *         6. (����dir/)��������ʬ��/
// *         7. (����dir/)
// * [����]
// *  $args['params'] �� Page.php �� $this->params
// *  $args['dir']    �� ���ܥѥ�᡼���ꥹ��
// *  $args['subdir'] �� ������ܥѥ�᡼��
// * [�ֵ���]
// *  $dirlist �� �����ǥ��쥯�ȥ�ꥹ��
// *******************************************************************
	function get_dirlist( $args ) {
		$params = array();
		if( isset($args['params']) ){
			$params = $args['params'];
		}
		$dir = array();
		if( isset($args['dir']) ){
			$dir    = $args['dir'];
		}
		$subdir = '';
		if( isset($args['subdir']) ){
			$subdir = $args['subdir'];
		}

		// ���֥ǥ��쥯�ȥ�ʤ��ξ��
		$dirlist = array();
		$tmp_dir = '';
		array_unshift( $dirlist, $tmp_dir );
		foreach( $dir as $val ){
			if( $val == '' ){
				break;
			}
			if( !( isset($params['param'][$val]) && $params['param'][$val] != '' ) ){
				break;
			}
			$tmp_dir .= $params['param'][$val] . '/';
			array_unshift( $dirlist, $tmp_dir );
		}
	
		// ���֥ǥ��쥯�ȥꤢ��ξ��
		$dirlist2 = array();
		if( $subdir != '' &&
			isset($params['param'][$subdir]) && $params['param'][$subdir] != '' ){

			foreach( $dirlist as $val ){
				if( $val == '' ){
					continue;
				}
				array_push( $dirlist2, $val . $params['param'][$subdir] . '/' );
			}
		}

		// ���
		foreach( $dirlist as $val ){
				array_push( $dirlist2, $val );
		}

		return $dirlist2;
	}

// *****************************************************************
// * [�ؿ�̾]
// *  get_filepath
// *  �ե�����ѥ��ꥹ������
// * [��������]
// *  �ե����뤬¸�ߤ���ѥ��Υꥹ�Ȥ����ꤹ�롣
// * [����]
// *  $args['basedir']  �� �ե�����ѥ������ǥ��쥯�ȥ�
// *  $args['dirlist']  �� �����ǥ��쥯�ȥ�ꥹ��
// *  $args['filename'] �� �ե�����̾
// * [�ֵ���]
// *  $res['pathlist'] �� �ե�����ѥ��ꥹ��
// *******************************************************************
	function get_filepath( $args ){
		$res = array();

		$basedir  = $args['basedir'];
		$dirlist  = $args['dirlist'];
		$filename = $args['filename'];

		$path = array();
		foreach( $dirlist as $val ){
			// �ե������¸�߳�ǧ
			$file = $basedir . '/' . $val . '/' . $filename;
			$file = preg_replace( "/\/\//", "/", $file );
			if( file_exists( $file ) ){
				array_push( $path, $val );
			}
		}

		$res = array( 'pathlist' => $path );
		return $res;
	}

// *****************************************************************
// * [�ؿ�̾]
// *  get_file
// *  �ե���������
// * [��������]
// *  �ǥ��쥯�ȥ�ꥹ�Ȥ���Ǥ�ͥ���٤ι⤤�ե��������ꤹ�롣
// * [����]
// *  $args['basedir']  �� �ե�����ѥ������ǥ��쥯�ȥ�
// *  $args['dirlist']  �� �����ǥ��쥯�ȥ�ꥹ��
// *  $args['filename'] �� �ե�����̾
// * [�ֵ���]
// *  $file �� �ե�����ʥѥ��դ���
// *****************************************************************
	function get_file( $args ){
		$file = '';

		$basedir  = $args['basedir'];
		$dirlist  = $args['dirlist'];
		$filename = $args['filename'];

		$res = $this->get_filepath( $args );
		$pathlist = array();
		if( isset($res['pathlist']) && $res['pathlist'] != '' ){
			$pathlist = $res['pathlist'];
		}

		if( isset($pathlist[0]) ){
			$file = $basedir;
			if( $pathlist[0] != '' ) $file .= '/' . $pathlist[0];
			$file .= '/' . $filename;
		}

		$file = preg_replace( "/\/\//", "/", $file );

		return $file;
	}

// *****************************************************************
// * [�ؿ�̾]
// *  get_params
// *  ����ե��������ѥ�᡼������
// * [��������]
// *  �ե����뤫��ѥ�᡼�������ꤹ�롣
// *  ͥ���٤ι⤤�ե����������Τ�Ŭ�Ѥ��롣
// * [����]
// *  $args['basedir']  �� ����ե���������ǥ��쥯�ȥ�
// *  $args['dirlist']  �� �����ǥ��쥯�ȥ�ꥹ��
// *  $args['filename'] �� ����ե�����̾
// * [�ֵ���]
// *  $params �� �ѥ�᡼��
// *******************************************************************
	function get_params( $args ){
		$params = array();

		$file = $this->get_file( $args );

		$params = Spyc::YAMLLoad($file);
		return $params;
	}

// *****************************************************************
// * [�ؿ�̾]
// *  get_params_merge
// *  ����ե��������ѥ�᡼������ʥޡ�����
// * [��������]
// *  �ե����뤫��ѥ�᡼�������ꤹ�롣
// *  ¸�ߤ���ե���������ƻ��Ȥ���ͥ���٤ι⤤����Ǿ�񤭤��Ƥ�����
// * [����]
// *  $args['basedir']  �� ����ե���������ǥ��쥯�ȥ�
// *  $args['dirlist']  �� �����ǥ��쥯�ȥ�ꥹ��
// *  $args['filename'] �� ����ե�����̾
// * [�ֵ���]
// *  $params �� �ѥ�᡼��
// *******************************************************************
	function get_params_merge( $args ){
		$basedir  = $args['basedir'];
		$dirlist  = $args['dirlist'];
		$filename = $args['filename'];

		$params = array();

		$args = array( 'basedir' => $basedir,
						'dirlist' => $dirlist,
						'filename' => $filename,
					);
		$res = $this->get_filepath( $args );
		$pathlist = $res['pathlist'];
	
		if( !( isset( $pathlist ) ) ){
			return $params;
		}

		for( $i = count($pathlist)-1; $i>=0; $i-- ){
			$file = $basedir . $pathlist[$i] . $filename;
			$yaml = Spyc::YAMLLoad($file);
			if( !( isset($yaml) && $yaml != '' ) ){
				continue;
			}
			foreach( $yaml as $key => $val ){
				$params[$key] = $val;
			}
		}

		return $params;
	}

// *****************************************************************
// * [�ؿ�̾]
// *  get_params_merge_disp
// *  ����ɽ���ѥѥ�᡼������ʥޡ�����
// * [��������]
// *  get_params_merge�ΰ��
// *  ����ɽ���ѥѥ�᡼������ե����뤫��ѥ�᡼�������ꤹ�롣
// *  ¸�ߤ���ե���������ƻ��Ȥ���ͥ���٤ι⤤����Ǿ�񤭤��Ƥ�����
// *  ����������̾��selected�ס�checked�פˤĤ��Ƥϡ�
// *  ����̾����ȤˤĤ���ͥ���٤ι⤤����Ǿ�񤭤��Ƥ�����
// * [����]
// *  $args['basedir']  �� ����ե���������ǥ��쥯�ȥ�
// *  $args['dirlist']  �� �����ǥ��쥯�ȥ�ꥹ��
// *  $args['filename'] �� ����ե�����̾
// * [�ֵ���]
// *  $params �� �ѥ�᡼��
// *******************************************************************
	function get_params_merge_disp( $args ){
		$basedir  = $args['basedir'];
		$dirlist  = $args['dirlist'];
		$filename = $args['filename'];

		$params = array();

		$args = array( 'basedir' => $basedir,
						'dirlist' => $dirlist,
						'filename' => $filename,
					);
		$res = $this->get_filepath( $args );
		$pathlist = $res['pathlist'];
	
		if( !( isset( $pathlist ) ) ){
			return $params;
		}

		for( $i = count($pathlist)-1; $i>=0; $i-- ){
			$file = $basedir . $pathlist[$i] . $filename;
			$yaml = Spyc::YAMLLoad($file);
			if( !( isset($yaml) && $yaml != '' ) ){
				continue;
			}
			foreach( $yaml as $key => $val ){
				if( !(isset($val)) || $val == '' ){
					continue;
				}
				// ����̾����selected�ס�checked�פξ��
				// ����̾�����Ƥ���
				if( $key == 'selected' || $key == 'checked' ){
					foreach( $val as $key2 => $val2 ){
						$params[$key][$key2] = $val2;
					}
				}else{
				// ����¾�ϥ���̾���Ⱦ��
					$params[$key] = $val;
				}
			}
		}

		return $params;
	}

// *****************************************************************
// * [�ؿ�̾]
// *  get_validate_rules
// *  �Х�ǡ����롼������
// * [��������]
// *  �Х�ǡ����롼��򡢥ե�����(JSON)�������ꤹ�롣
// * [����]
// *  $args['file']  �� �Х�ǡ����롼��ե�����
// *  $args['code']  �� �Х�ǡ����롼��ե�����ʸ��������
// * [�ֵ���]
// *  ���� �� �Х�ǡ����롼��
// *  �۾� �� �ʤ�
// *****************************************************************
	function get_validate_rules( $args ){
		$this->_jsonFile = $args['file'];

		// �ե�����¸�߳�ǧ
		if( !(file_exists( $this->_jsonFile )) ) return;

		$this->_jsonCode     = $args['code'];
		$this->_jsonCacheDir = dirname(__FILE__) . '/../cache';
		$this->_jsonCache    = $this->_jsonCacheDir . '/' . md5($this->_jsonFile);

        // �ǥ��쥯�ȥ����
		if ( !(is_dir( $this->_jsonCacheDir )) ) {
			mkdir( $this->_jsonCacheDir, 0755, true );
		}
		return $this->_isJsonCached() ? $this->_jsonCacheLoad() : $this->_jsonCacheStore();
	}

// *****************************************************************
// * [�ؿ�̾]
// *  _isJsonCached
// * [��������]
// *  JSON�ե�����Υ���å��夬���뤫Ƚ�ꤹ��
// * [����]
// *  �ʤ�
// * [�ֵ���]
// *  true  �� ����å������
// *  false �� JSON�ե������ɤ߹��ߡ�����å������
// *****************************************************************
	private function _isJsonCached() {
		clearstatcache();

		// ����å�������
		$flg = false;
		$f   = $this->_jsonCacheDir . '/' . php_uname("n");
		if ( file_exists($f) ) {
			$stat  = filemtime( $f );
			$lstat = filemtime( dirname(__FILE__) . "/Env.php" );
			if ( $stat < $lstat ) {
				$files = scandir( $this->_jsonCacheDir );
				foreach ( $files as $file ) {
					if ( $file === '.' || $file === '..' ) continue;
					unlink( $this->_jsonCacheDir . '/' . $file );
				}
				touch($f);

			} elseif ( file_exists($this->_jsonCache) &&
                      (filemtime($this->_jsonFile) <= filemtime($this->_jsonCache)) ) {
				$flg = true;
			}
		} else {
			touch($f);
		}
		return $flg;
	}

// *****************************************************************
// * [�ؿ�̾]
// *  _jsonCacheLoad
// * [��������]
// *  JSON�ե�����Υ���å�����ɤ߹���
// * [����]
// *  �ʤ�
// * [�ֵ���]
// *  ����å��廲�ȷ��
// *****************************************************************
	private function _jsonCacheLoad() {
		return unserialize( file_get_contents($this->_jsonCache) );
	}

// *****************************************************************
// * [�ؿ�̾]
// *  _jsonCacheStore
// * [��������]
// *  JSON�ե�������ɤ߹��ߡ�����å���ե��������
// * [����]
// *  �ʤ�
// * [�ֵ���]
// *  JSON�ե����뻲�ȷ��
// *****************************************************************
	private function _jsonCacheStore() {
		// �ե������ɤ߹���
		$json_str = file_get_contents( $this->_jsonFile );
		if ( $json_str === FALSE ) return;

		// ʸ�����ִ�
		$json_str = preg_replace( "/^var[^\n]+\n/" , "{\n", $json_str );
		$json_str = preg_replace( "/\"func\"\s*:\s*([^\,]+)\s*,/" , "\"func\":\"\\1\"," , $json_str );

		// JSON�ǥ����ɤΰ١�utf-8 ���Ѵ�
		$json_str = $this->data_encode( $json_str, 'utf-8', $this->_jsonCode );

		// JSON�ǡ�������Х�ǡ����롼�������
		$validate_rules = json_decode( $json_str, true );
		if ( $validate_rules === FALSE ) return;

		// ��������ʸ�������ɤ˺����Ѵ�
		$validate_rules = $this->data_encode( $validate_rules, $this->_jsonCode, 'utf-8' );

		$f = fopen( $this->_jsonCache, 'wb');
		fwrite( $f, serialize($validate_rules) );
		fclose( $f );
		return $validate_rules;
	}

// *****************************************************************
// * [�ؿ�̾]
// *  get_validate_params
// *  �����̥Х�ǡ����оݥѥ�᡼������
// * [��������]
// *  �����̤ΥХ�ǡ����оݥѥ�᡼���Υꥹ�Ȥ����ꤹ�롣
// * [����]
// *  $args['page']  �� ����ID
// *  $args['file']  �� �Х�ǡ����롼��ե�����
// * [�ֵ���]
// *  $validate_params �� ����ID�ꥹ��
// *****************************************************************
	function get_validate_params( $args ){
		$basedir  = $args['basedir'];
		$dirlist  = $args['dirlist'];
		$filename = $args['filename'];
		$page     = $args['page'];

		$res = array();

		// �ե�����ѥ�����
		$args = array( 'basedir' => $basedir,
						'dirlist' => $dirlist,
						'filename' => $filename,
					);
		$res = $this->get_filepath( $args );
		$path = $res['pathlist'];
	
		if( !( isset( $path ) ) ){
			return $res;
		}

		$file = $basedir . $path[0] . $filename;

		// �ե����뤬�����ʤ����ϥ��顼
		if( !($in = fopen( $file, "r" )) ){
			return;
		}

		// ����ե�����������
		$hash = array();
		$key = '';
		$list = array();
		while( $l = fgets( $in ) ){
			$l = chop($l);
			if( preg_match( "/^([^:\s]+)\s*:\s*(.*)\s*$/", $l, $match ) ){
				if( $match[2] != '' ){
					$hash[$match[1]] = preg_split( "/\,/" , $match[2] );
				}else{
					$hash[$match[1]] = array();
				}
			}
		}
		fclose($in);

		return $hash[$page];
	}

// *****************************************************************
// * [�ؿ�̾]
// *  data_encode
// *  �ǡ������󥳡���
// * [��������]
// *  �ǡ����򥨥󥳡��ɤ��롣����Ϣ��������б�
// * [����]
// *  ��1���� �� �оݥǡ���
// *  ��2���� �� �ѹ���ʸ��������
// *  ��3���� �� �ѹ���ʸ��������
// * [�ֵ���]
// *  $data �� ���󥳡��ɸ�ǡ���
// *****************************************************************
	function data_encode( $data, $tocode, $fromcode ){
		if ( $tocode === $fromcode ) return $data;
		if ( !(is_array( $data )) ) {
			$data = $this->chgcode( $data, $tocode, $fromcode );
			$data = preg_replace( "/\r\n/", "\n", $data ) ;
			$data = preg_replace( "/\r/", "\n", $data ) ;
			return $data;
		}else{
			foreach( $data as $key => $val ){
				$data[$key] = $this->data_encode( $data[$key], $tocode, $fromcode );
			}
		}
		return $data;
	}

// *****************************************************************
// * [�ؿ�̾]
// * create_mxprms
// * ���ѥ�᡼������
// * [��������]
// *  ���ѥ�᡼�����ͤ���Ϥ��ƥϥå��岽���롣
// * [����]
// *  $targets �� ����оݥѥ�᡼���ϥå���
// *  ��1���� �� ���ѥ�᡼����
// * [�ֵ���]
// *  $str �� ���ѥ�᡼����
// *****************************************************************
	function create_mxprms( $targets ){
		$str = '';

		foreach( $targets as $key => $val ){
			if( $str != '' ) $str .= '&';
			$str .= $key . '=' . urlencode($val);
		}

		return $str;
	}

// *****************************************************************
// * [�ؿ�̾]
// * analyze_mxprms
// * ���ѥ�᡼������
// * [��������]
// *  ���ѥ�᡼�����ͤ���Ϥ��ƥϥå��岽���롣
// * [����]
// *  ��1���� �� ���ѥ�᡼����
// * [�ֵ���]
// *  $params �� ���ϸ�ѥ�᡼��
// *****************************************************************
	function analyze_mxprms( $string ){
		$params = array();

		if( !( isset($string) && $string != '' ) ){
			return $params;
		}

		$lst = explode( '&', $string );
		foreach( $lst as $val ){
			$lst2 = explode( '=', $val );
			$params[$lst2[0]] = urldecode($lst2[1]);
		}

		return $params;
	}

// *****************************************************************
// * [�ؿ�̾]
// * chgcode
// * ʸ���������Ѵ�
// *****************************************************************
	function chgcode( $str, $tocode, $fromcode ){
		if ( $tocode === $fromcode ) return $str;

		// �Ѵ���ʸ��������
		$tc = '';
		if( $tocode == 'euc-jp' ) $tc = 'e';
		if( $tocode == 'shift_jis' ) $tc = 's';
		if( $tocode == 'utf-8' ) $tc = 'w';
		if( $tc == '' ) return $str;

		// �Ѵ���ʸ��������
		$fc = '';
		if( $fromcode == 'euc-jp' ) $fc = 'E';
		if( $fromcode == 'shift_jis' ) $fc = 'S';
		if( $fromcode == 'utf-8' ) $fc = 'W';
		if( $fc == '' ) return $str;

		if( !(is_null($this->perl)) ){
		// perl �� Henkan.pm �����
			$str_af = $this->perl->{"Henkan::henkan"}( "-${fc}${tc}xm0", $str );
		}else{
		// Perl���֥������Ȥ��ʤ����� mb_convert_encoding �����
			$str_af = mb_convert_encoding( $str, $tocode, $fromcode );
		}
		return $str_af;
	}

// *****************************************************************
// * [�ؿ�̾]
// * getparam , p
// * �ѥ�᡼���ͼ���
// * [��������]
// * �ѥ�᡼���ͤ�������롣̤����ξ��϶������ˤ��롣
// * [����]
// *  ��1���� �� �оݥѥ�᡼��̾
// *  ��2���� �� Page.php �� $this->params
// * [�ֵ���]
// *  $value �� �оݥѥ�᡼����
// *****************************************************************
	function getparam( $key, $params ){
		$value = '';
		if( isset($params['param'][$key]) ){
			$value = $params['param'][$key];
		}
		return $value;
	}
	function p( $key, $params ){
		return $this->getparam( $key, $params );
	}

// *****************************************************************
// * [�ؿ�̾]
// * kenc_name
// * ��ƻ�ܸ������ɢ�̾���Ѵ�
// * [��������]
// * ��ƻ�ܸ��Υ����ɤ�̾�����Ѵ����롣
// * �� kenc2name, name2kenc �᥽�åɤǻ��Ѥ��������ؿ��Ǥ���
// * [����]
// *  ��1���� �� �����ե饰
// *              1 : �����ɢ�̾��
// *              2 : ̾����������
// *  ��2���� �� �о���
// * [�ֵ���]
// *  $result �� �Ѵ������
// *****************************************************************
	function _kenc_name( $flg = '', $value = '' ){
		$fmt = array(
			'01' => '�̳�ƻ',
			'02' => '�Ŀ���',
			'03' => '��긩',
			'04' => '�ܾ븩',
			'05' => '���ĸ�',
			'06' => '������',
			'07' => 'ʡ�縩',
			'08' => '��븩',
			'09' => '���ڸ�',
			'10' => '���ϸ�',
			'11' => '��̸�',
			'12' => '���ո�',
			'13' => '�����',
			'14' => '�����',
			'15' => '���㸩',
			'16' => '�ٻ���',
			'17' => '���',
			'18' => 'ʡ�温',
			'19' => '������',
			'20' => 'Ĺ�',
			'21' => '���츩',
			'22' => '�Ų���',
			'23' => '���θ�',
			'24' => '���Ÿ�',
			'25' => '���츩',
			'26' => '������',
			'27' => '�����',
			'28' => 'ʼ�˸�',
			'29' => '���ɸ�',
			'30' => '�²λ���',
			'31' => 'Ļ�踩',
			'32' => '�纬��',
			'33' => '������',
			'34' => '���縩',
			'35' => '������',
			'36' => '���縩',
			'37' => '���',
			'38' => '��ɲ��',
			'39' => '���θ�',
			'40' => 'ʡ����',
			'41' => '���츩',
			'42' => 'Ĺ�긩',
			'43' => '���ܸ�',
			'44' => '��ʬ��',
			'45' => '�ܺ긩',
			'46' => '�����縩',
			'47' => '���츩',
		);

		$result = '';
		// �����ɢ�̾��
		if( $flg == 1 ){
			$result = $fmt[$value];
		// ̾����������
		}else if( $flg == 2 ){
			$fmt2 = array();
			foreach( $fmt as $key => $val ){
				$fmt2[$val] = $key;
			}
			$result = $fmt2[$value];
		}
		return $result;
	}

// *****************************************************************
// * [�ؿ�̾]
// * kenc2name
// * ��ƻ�ܸ�������=>̾���Ѵ�
// * [��������]
// * ��ƻ�ܸ��Υ������ͤ���̾�����Ѵ�����
// * [����]
// *  ��1���� �� �о���
// * [�ֵ���]
// *  $result �� �Ѵ������
// *****************************************************************
	function kenc2name( $value = '' ){
		return $this->_kenc_name( 1, $value );
	}

// *****************************************************************
// * [�ؿ�̾]
// * name2kenc
// * ��ƻ�ܸ�̾=>�������Ѵ�
// * [��������]
// * ��ƻ�ܸ�̾���饳�����ͤ��Ѵ�����
// * [����]
// *  ��1���� �� �о���
// * [�ֵ���]
// *  $result �� �Ѵ������
// *****************************************************************
	function name2kenc( $value = '' ){
		return $this->_kenc_name( 2, $value );
	}

// *****************************************************************
// * [�ؿ�̾]
// * Japanese2Era
// * ����=>�����Ѵ�
// * [��������]
// * ǯ���ǯ�򸵤�����ǯ���Ѵ�����
// * [����]
// * ��1���� �� ����ޤ���ǯ��
// *              0:����1:������2:������3:���¡�4:ʿ��
// * ��2���� �� ǯ����
// * [�ֵ���]
// * ������Ѵ����ǯ����
// *****************************************************************
	function Japanese2Era( $era, $year ){
		// �����줫�ΰ�����̤����ξ���ֵѤ��ʤ�
		if( !(isset( $era ))  || $era  == '' ) return;
		if( !(isset( $year )) || $year == '' ) return;

		// ǯ��ơ��֥�
		$tbl = array(
				// ����
				'0' => 0,
				// ����
				'1' => array( 'start' => 1, 'end' => 45, 'plus' => 1867 ),
				// ����
				'2' => array( 'start' => 1, 'end' => 15, 'plus' => 1911 ),
				// ����
				'3' => array( 'start' => 1, 'end' => 64, 'plus' => 1925 ),
				// ʿ��
				'4' => array( 'start' => 1, 'end' => 99, 'plus' => 1988 ),
				);

		// ǯ��ơ��֥��¸�ߤ��ʤ�����̤�ֵ�
		if( !(isset( $tbl[$era] )) ) return;
		// ǯ�����ͤǤϤʤ�����̤�ֵ�
		if( !(preg_match( "/^\d+$/", $year )) ) return;

		//����ξ���ǯ�򤽤Τޤ��ֵ�
		if( $era == 0 ) return $year;

		// �ʹ�����ʳ��ν���
		// ǯ���ϰϳ��ξ��̤�ֵ�
		if( $year < $tbl[$era]['start'] || $year > $tbl[$era]['end'] ) return;
		// ������Ѵ������ֵ�
		return $year + $tbl[$era]['plus'];
	}

// *****************************************************************
// * [�ؿ�̾]
// * cut
// * �ݤ�
// * [��������]
// * value��Х��ȿ�length���ڤ�ΤƤ��ͤ��֤���
// * �ڤ�ΤƤ��ս꤬���Х���ʸ���ο�����Ǥ��ä���硢
// * ����ˣ��Х����ڤ�ͤ�롣
// * [����]
// * ��1���� �� ����ޤ���ǯ��
// *              0:����1:������2:������3:���¡�4:ʿ��
// * ��2���� �� ǯ����
// * [�ֵ���]
// * ������Ѵ����ǯ����
// *****************************************************************
	function cut( $value = '', $length = ''){
		// length �����ͤǤ�̵�����value�򤽤Τޤ��ֵ�
		if( !preg_match( "/^\d+/", $length ) ){
			return $value;
		}

		// �Х��ȿ�length��substr
		$ret = substr( $value, 0, $length );

		preg_match_all( "/[\x8E\xA1-\xFE]/", $ret, $matches );

		$cnt = count($matches[0]);
		// 2byteʸ���θĿ����������
		// ��ü��2�Х���ʸ���ο�����ʤΤǥ��å�
		if( $cnt % 2 ){
			$ret = substr( $ret, 0, strlen($ret)-1 );
		}
		return $ret;

	}

// *****************************************************************
// * [�ؿ�̾]
// * h2z
// * Ⱦ��=>�����Ѵ�
// * [��������]
// * Ⱦ�Ѥ����Ѥ��Ѵ����롣
// * [����]
// * ��1���� �� �Ѵ��о�ʸ����
// * [�ֵ���]
// * �Ѵ���ʸ����
// *****************************************************************
	function h2z( $str ){
		require_once( 'Subfunc/h2z.php' );
		$m = new Subfunc_h2z();
		return $m->exec( $str, '' );
	}

// *****************************************************************
// * [�ؿ�̾]
// * h2z_old
// * Ⱦ��=>�����Ѵ�(����)
// * [��������]
// * Ⱦ�Ѥ����Ѥ��Ѵ����롣
// * [����]
// * ��1���� �� �Ѵ��о�ʸ����
// * [�ֵ���]
// * �Ѵ���ʸ����
// *****************************************************************
	function h2z_old( $str ){
		require_once( 'Subfunc/h2z.php' );
		$m = new Subfunc_h2z();
		return $m->exec( $str, 1 );
	}

// *****************************************************************
// * [�ؿ�̾]
// * h2zh
// * Ⱦ��=>���ѤҤ餬���Ѵ�
// * [��������]
// * Ⱦ�Ѥ����Ѥ��Ѵ����롣Ⱦ�ѥ��ʤ����ѤҤ餬�ʤ��Ѵ����롣
// * ���ѥ������ʤ����ѤҤ餬�ʤ��Ѵ����롣
// * [����]
// * ��1���� �� �Ѵ��о�ʸ����
// * [�ֵ���]
// * �Ѵ���ʸ����
// *****************************************************************
	function h2zh( $str ){
		require_once( 'Subfunc/h2zh.php' );
		$m = new Subfunc_h2zh();
		return $m->exec( $str, '' );
	}

// *****************************************************************
// * [�ؿ�̾]
// * h2zh_old
// * Ⱦ��=>���ѤҤ餬���Ѵ�(����)
// * [��������]
// * Ⱦ�Ѥ����Ѥ��Ѵ����롣Ⱦ�ѥ��ʤ����ѤҤ餬�ʤ��Ѵ����롣
// * ���ѥ������ʤ����ѤҤ餬�ʤ��Ѵ����롣
// * [����]
// * ��1���� �� �Ѵ��о�ʸ����
// * [�ֵ���]
// * �Ѵ���ʸ����
// *****************************************************************
	function h2zh_old( $str ){
		require_once( 'Subfunc/h2zh.php' );
		$m = new Subfunc_h2zh();
		return $m->exec( $str, 1 );
	}

// *****************************************************************
// * [�ؿ�̾]
// * hk2zk
// * Ⱦ�ѥ�������=>���ѥ��������Ѵ�
// * [��������]
// * Ⱦ�ѥ��ʤ����ѥ������ʤ��Ѵ����롣
// * [����]
// * ��1���� �� �Ѵ��о�ʸ����
// * [�ֵ���]
// * �Ѵ���ʸ����
// *****************************************************************
	function hk2zk( $str ){
		require_once( 'Subfunc/hk2zk.php' );
		$m = new Subfunc_hk2zk();
		return $m->exec( $str );
	}

// *****************************************************************
// * [�ؿ�̾]
// * DMT2GMT
// * [��������]
// * ������DMT��������GMT�������Ѵ����롣
// * [����]
// * ��1���� �� ����(YYYYMMDDhhmmss)
// * [�ֵ���]
// * GMT����������
// *****************************************************************
	function DMT2GMT( $date = '' ){
		require_once( 'Subfunc/DMT2GMT.php' );
		$m = new Subfunc_DMT2GMT();
		return $m->exec( $date );
	}

}
