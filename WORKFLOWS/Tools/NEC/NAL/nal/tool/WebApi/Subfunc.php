<?php

class Subfunc {
// **********************************************************************
// * コンストラクタ
// * [in]
// * $perlmode : 設定時perlモジュール設定
// * [注意事項]
// * メソッド「get_validate_rules」「data_encode」「chgcode」のいずれかを
// * 使用する場合は、必ず $perlmode を設定する事。
// **********************************************************************
	function Subfunc( $perlmode = NULL ){

		$this->perlmode = $perlmode;

		if( isset($perlmode) ){
			try{
				// 文字コード変換処理の為に、perlモジュール「Henkan.pm」をuse
				$perl = new Perl();
				// host05用パス追加
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
// * [関数名]
// *  get_dirlist
// *  処理ディレクトリリスト設定
// * [処理概要]
// *  処理ディレクトリリストを設定する。
// *    例：優先順位は下記のとおり。
// *         1. (基点dir/)コース大分類/コース中分類/コースID/キャンペーンID/
// *         2. (基点dir/)コース大分類/コース中分類/キャンペーンID/
// *         3. (基点dir/)コース大分類/キャンペーンID/
// *         4. (基点dir/)コース大分類/コース中分類/コースID/
// *         5. (基点dir/)コース大分類/コース中分類/
// *         6. (基点dir/)コース大分類/
// *         7. (基点dir/)
// * [引数]
// *  $args['params'] … Page.php の $this->params
// *  $args['dir']    … 基本パラメータリスト
// *  $args['subdir'] … 補助基本パラメータ
// * [返却値]
// *  $dirlist … 処理ディレクトリリスト
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

		// サブディレクトリなしの場合
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
	
		// サブディレクトリありの場合
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

		// 結合
		foreach( $dirlist as $val ){
				array_push( $dirlist2, $val );
		}

		return $dirlist2;
	}

// *****************************************************************
// * [関数名]
// *  get_filepath
// *  ファイルパスリスト設定
// * [処理概要]
// *  ファイルが存在するパスのリストを設定する。
// * [引数]
// *  $args['basedir']  … ファイルパス基点ディレクトリ
// *  $args['dirlist']  … 処理ディレクトリリスト
// *  $args['filename'] … ファイル名
// * [返却値]
// *  $res['pathlist'] … ファイルパスリスト
// *******************************************************************
	function get_filepath( $args ){
		$res = array();

		$basedir  = $args['basedir'];
		$dirlist  = $args['dirlist'];
		$filename = $args['filename'];

		$path = array();
		foreach( $dirlist as $val ){
			// ファイルの存在確認
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
// * [関数名]
// *  get_file
// *  ファイル設定
// * [処理概要]
// *  ディレクトリリストから最も優先度の高いファイルを決定する。
// * [引数]
// *  $args['basedir']  … ファイルパス基点ディレクトリ
// *  $args['dirlist']  … 処理ディレクトリリスト
// *  $args['filename'] … ファイル名
// * [返却値]
// *  $file … ファイル（パス付き）
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
// * [関数名]
// *  get_params
// *  設定ファイル情報パラメータ設定
// * [処理概要]
// *  ファイルからパラメータを設定する。
// *  優先度の高いファイルの設定のみ適用する。
// * [引数]
// *  $args['basedir']  … 設定ファイル基点ディレクトリ
// *  $args['dirlist']  … 処理ディレクトリリスト
// *  $args['filename'] … 設定ファイル名
// * [返却値]
// *  $params … パラメータ
// *******************************************************************
	function get_params( $args ){
		$params = array();

		$file = $this->get_file( $args );

		$params = Spyc::YAMLLoad($file);
		return $params;
	}

// *****************************************************************
// * [関数名]
// *  get_params_merge
// *  設定ファイル情報パラメータ設定（マージ）
// * [処理概要]
// *  ファイルからパラメータを設定する。
// *  存在するファイルを全て参照し、優先度の高い設定で上書きしていく。
// * [引数]
// *  $args['basedir']  … 設定ファイル基点ディレクトリ
// *  $args['dirlist']  … 処理ディレクトリリスト
// *  $args['filename'] … 設定ファイル名
// * [返却値]
// *  $params … パラメータ
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
// * [関数名]
// *  get_params_merge_disp
// *  画面表示用パラメータ設定（マージ）
// * [処理概要]
// *  get_params_mergeの亜種。
// *  画面表示用パラメータ設定ファイルからパラメータを設定する。
// *  存在するファイルを全て参照し、優先度の高い設定で上書きしていく。
// *  ただしキー名「selected」「checked」については、
// *  キー名の中身について優先度の高い設定で上書きしていく。
// * [引数]
// *  $args['basedir']  … 設定ファイル基点ディレクトリ
// *  $args['dirlist']  … 処理ディレクトリリスト
// *  $args['filename'] … 設定ファイル名
// * [返却値]
// *  $params … パラメータ
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
				// キー名が「selected」「checked」の場合
				// キー名の内容を上書き
				if( $key == 'selected' || $key == 'checked' ){
					foreach( $val as $key2 => $val2 ){
						$params[$key][$key2] = $val2;
					}
				}else{
				// その他はキー名ごと上書き
					$params[$key] = $val;
				}
			}
		}

		return $params;
	}

// *****************************************************************
// * [関数名]
// *  get_validate_rules
// *  バリデータルール設定
// * [処理概要]
// *  バリデータルールを、ファイル(JSON)から設定する。
// * [引数]
// *  $args['file']  … バリデータルールファイル
// *  $args['code']  … バリデータルールファイル文字コード
// * [返却値]
// *  正常 … バリデータルール
// *  異常 … なし
// *****************************************************************
	function get_validate_rules( $args ){
		$this->_jsonFile = $args['file'];

		// ファイル存在確認
		if( !(file_exists( $this->_jsonFile )) ) return;

		$this->_jsonCode     = $args['code'];
		$this->_jsonCacheDir = dirname(__FILE__) . '/../cache';
		$this->_jsonCache    = $this->_jsonCacheDir . '/' . md5($this->_jsonFile);

        // ディレクトリ作成
		if ( !(is_dir( $this->_jsonCacheDir )) ) {
			mkdir( $this->_jsonCacheDir, 0755, true );
		}
		return $this->_isJsonCached() ? $this->_jsonCacheLoad() : $this->_jsonCacheStore();
	}

// *****************************************************************
// * [関数名]
// *  _isJsonCached
// * [処理概要]
// *  JSONファイルのキャッシュがあるか判定する
// * [引数]
// *  なし
// * [返却値]
// *  true  … キャッシュロード
// *  false … JSONファイル読み込み、キャッシュ作成
// *****************************************************************
	private function _isJsonCached() {
		clearstatcache();

		// キャッシュ制御
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
// * [関数名]
// *  _jsonCacheLoad
// * [処理概要]
// *  JSONファイルのキャッシュを読み込む
// * [引数]
// *  なし
// * [返却値]
// *  キャッシュ参照結果
// *****************************************************************
	private function _jsonCacheLoad() {
		return unserialize( file_get_contents($this->_jsonCache) );
	}

// *****************************************************************
// * [関数名]
// *  _jsonCacheStore
// * [処理概要]
// *  JSONファイルを読み込み、キャッシュファイル出力
// * [引数]
// *  なし
// * [返却値]
// *  JSONファイル参照結果
// *****************************************************************
	private function _jsonCacheStore() {
		// ファイル読み込み
		$json_str = file_get_contents( $this->_jsonFile );
		if ( $json_str === FALSE ) return;

		// 文字列置換
		$json_str = preg_replace( "/^var[^\n]+\n/" , "{\n", $json_str );
		$json_str = preg_replace( "/\"func\"\s*:\s*([^\,]+)\s*,/" , "\"func\":\"\\1\"," , $json_str );

		// JSONデコードの為、utf-8 に変換
		$json_str = $this->data_encode( $json_str, 'utf-8', $this->_jsonCode );

		// JSONデータからバリデータルールを設定
		$validate_rules = json_decode( $json_str, true );
		if ( $validate_rules === FALSE ) return;

		// ソースの文字コードに再度変換
		$validate_rules = $this->data_encode( $validate_rules, $this->_jsonCode, 'utf-8' );

		$f = fopen( $this->_jsonCache, 'wb');
		fwrite( $f, serialize($validate_rules) );
		fclose( $f );
		return $validate_rules;
	}

// *****************************************************************
// * [関数名]
// *  get_validate_params
// *  画面別バリデータ対象パラメータ設定
// * [処理概要]
// *  画面別のバリデータ対象パラメータのリストを設定する。
// * [引数]
// *  $args['page']  … 画面ID
// *  $args['file']  … バリデータルールファイル
// * [返却値]
// *  $validate_params … 画面IDリスト
// *****************************************************************
	function get_validate_params( $args ){
		$basedir  = $args['basedir'];
		$dirlist  = $args['dirlist'];
		$filename = $args['filename'];
		$page     = $args['page'];

		$res = array();

		// ファイルパス取得
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

		// ファイルが開けない場合はエラー
		if( !($in = fopen( $file, "r" )) ){
			return;
		}

		// 設定ファイル情報取得
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
// * [関数名]
// *  data_encode
// *  データエンコード
// * [処理概要]
// *  データをエンコードする。配列、連想配列も対応
// * [引数]
// *  第1引数 … 対象データ
// *  第2引数 … 変更先文字コード
// *  第3引数 … 変更元文字コード
// * [返却値]
// *  $data … エンコード後データ
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
// * [関数名]
// * create_mxprms
// * 結合パラメータ生成
// * [処理概要]
// *  結合パラメータの値を解析してハッシュ化する。
// * [引数]
// *  $targets … 結合対象パラメータハッシュ
// *  第1引数 … 結合パラメータ値
// * [返却値]
// *  $str … 結合パラメータ値
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
// * [関数名]
// * analyze_mxprms
// * 結合パラメータ解析
// * [処理概要]
// *  結合パラメータの値を解析してハッシュ化する。
// * [引数]
// *  第1引数 … 結合パラメータ値
// * [返却値]
// *  $params … 解析後パラメータ
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
// * [関数名]
// * chgcode
// * 文字コード変換
// *****************************************************************
	function chgcode( $str, $tocode, $fromcode ){
		if ( $tocode === $fromcode ) return $str;

		// 変換先文字コード
		$tc = '';
		if( $tocode == 'euc-jp' ) $tc = 'e';
		if( $tocode == 'shift_jis' ) $tc = 's';
		if( $tocode == 'utf-8' ) $tc = 'w';
		if( $tc == '' ) return $str;

		// 変換元文字コード
		$fc = '';
		if( $fromcode == 'euc-jp' ) $fc = 'E';
		if( $fromcode == 'shift_jis' ) $fc = 'S';
		if( $fromcode == 'utf-8' ) $fc = 'W';
		if( $fc == '' ) return $str;

		if( !(is_null($this->perl)) ){
		// perl の Henkan.pm を使用
			$str_af = $this->perl->{"Henkan::henkan"}( "-${fc}${tc}xm0", $str );
		}else{
		// Perlオブジェクトがない場合は mb_convert_encoding を使用
			$str_af = mb_convert_encoding( $str, $tocode, $fromcode );
		}
		return $str_af;
	}

// *****************************************************************
// * [関数名]
// * getparam , p
// * パラメータ値取得
// * [処理概要]
// * パラメータ値を取得する。未定義の場合は空扱いにする。
// * [引数]
// *  第1引数 … 対象パラメータ名
// *  第2引数 … Page.php の $this->params
// * [返却値]
// *  $value … 対象パラメータ値
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
// * [関数名]
// * kenc_name
// * 都道府県コード⇔名前変換
// * [処理概要]
// * 都道府県のコードと名前と変換する。
// * ※ kenc2name, name2kenc メソッドで使用する内部関数である
// * [引数]
// *  第1引数 … 処理フラグ
// *              1 : コード→名前
// *              2 : 名前→コード
// *  第2引数 … 対象値
// * [返却値]
// *  $result … 変換後の値
// *****************************************************************
	function _kenc_name( $flg = '', $value = '' ){
		$fmt = array(
			'01' => '北海道',
			'02' => '青森県',
			'03' => '岩手県',
			'04' => '宮城県',
			'05' => '秋田県',
			'06' => '山形県',
			'07' => '福島県',
			'08' => '茨城県',
			'09' => '栃木県',
			'10' => '群馬県',
			'11' => '埼玉県',
			'12' => '千葉県',
			'13' => '東京都',
			'14' => '神奈川県',
			'15' => '新潟県',
			'16' => '富山県',
			'17' => '石川県',
			'18' => '福井県',
			'19' => '山梨県',
			'20' => '長野県',
			'21' => '岐阜県',
			'22' => '静岡県',
			'23' => '愛知県',
			'24' => '三重県',
			'25' => '滋賀県',
			'26' => '京都府',
			'27' => '大阪府',
			'28' => '兵庫県',
			'29' => '奈良県',
			'30' => '和歌山県',
			'31' => '鳥取県',
			'32' => '島根県',
			'33' => '岡山県',
			'34' => '広島県',
			'35' => '山口県',
			'36' => '徳島県',
			'37' => '香川県',
			'38' => '愛媛県',
			'39' => '高知県',
			'40' => '福岡県',
			'41' => '佐賀県',
			'42' => '長崎県',
			'43' => '熊本県',
			'44' => '大分県',
			'45' => '宮崎県',
			'46' => '鹿児島県',
			'47' => '沖縄県',
		);

		$result = '';
		// コード→名前
		if( $flg == 1 ){
			$result = $fmt[$value];
		// 名前→コード
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
// * [関数名]
// * kenc2name
// * 都道府県コード=>名前変換
// * [処理概要]
// * 都道府県のコード値から名前に変換する
// * [引数]
// *  第1引数 … 対象値
// * [返却値]
// *  $result … 変換後の値
// *****************************************************************
	function kenc2name( $value = '' ){
		return $this->_kenc_name( 1, $value );
	}

// *****************************************************************
// * [関数名]
// * name2kenc
// * 都道府県名=>コード変換
// * [処理概要]
// * 都道府県名からコード値に変換する
// * [引数]
// *  第1引数 … 対象値
// * [返却値]
// *  $result … 変換後の値
// *****************************************************************
	function name2kenc( $value = '' ){
		return $this->_kenc_name( 2, $value );
	}

// *****************************************************************
// * [関数名]
// * Japanese2Era
// * 元号=>西暦変換
// * [処理概要]
// * 年号と年を元に西暦年に変換する
// * [引数]
// * 第1引数 … 西暦または年号
// *              0:西暦、1:明治、2:大正、3:昭和、4:平成
// * 第2引数 … 年の値
// * [返却値]
// * 西暦に変換後の年の値
// *****************************************************************
	function Japanese2Era( $era, $year ){
		// いずれかの引数が未指定の場合返却しない
		if( !(isset( $era ))  || $era  == '' ) return;
		if( !(isset( $year )) || $year == '' ) return;

		// 年号テーブル
		$tbl = array(
				// 西暦
				'0' => 0,
				// 明治
				'1' => array( 'start' => 1, 'end' => 45, 'plus' => 1867 ),
				// 大正
				'2' => array( 'start' => 1, 'end' => 15, 'plus' => 1911 ),
				// 昭和
				'3' => array( 'start' => 1, 'end' => 64, 'plus' => 1925 ),
				// 平成
				'4' => array( 'start' => 1, 'end' => 99, 'plus' => 1988 ),
				);

		// 年号テーブルに存在しない場合は未返却
		if( !(isset( $tbl[$era] )) ) return;
		// 年が数値ではない場合は未返却
		if( !(preg_match( "/^\d+$/", $year )) ) return;

		//西暦の場合は年をそのまま返却
		if( $era == 0 ) return $year;

		// 以降西暦以外の処理
		// 年が範囲外の場合未返却
		if( $year < $tbl[$era]['start'] || $year > $tbl[$era]['end'] ) return;
		// 西暦に変換して返却
		return $year + $tbl[$era]['plus'];
	}

// *****************************************************************
// * [関数名]
// * cut
// * 丸め
// * [処理概要]
// * valueをバイト数lengthで切り捨てた値を返す。
// * 切り捨てた箇所が２バイト文字の真ん中であった場合、
// * さらに１バイト切り詰める。
// * [引数]
// * 第1引数 … 西暦または年号
// *              0:西暦、1:明治、2:大正、3:昭和、4:平成
// * 第2引数 … 年の値
// * [返却値]
// * 西暦に変換後の年の値
// *****************************************************************
	function cut( $value = '', $length = ''){
		// length が数値では無い場合valueをそのまま返却
		if( !preg_match( "/^\d+/", $length ) ){
			return $value;
		}

		// バイト数lengthでsubstr
		$ret = substr( $value, 0, $length );

		preg_match_all( "/[\x8E\xA1-\xFE]/", $ret, $matches );

		$cnt = count($matches[0]);
		// 2byte文字の個数が奇数だと
		// 終端が2バイト文字の真ん中なのでカット
		if( $cnt % 2 ){
			$ret = substr( $ret, 0, strlen($ret)-1 );
		}
		return $ret;

	}

// *****************************************************************
// * [関数名]
// * h2z
// * 半角=>全角変換
// * [処理概要]
// * 半角を全角に変換する。
// * [引数]
// * 第1引数 … 変換対象文字列
// * [返却値]
// * 変換後文字列
// *****************************************************************
	function h2z( $str ){
		require_once( 'Subfunc/h2z.php' );
		$m = new Subfunc_h2z();
		return $m->exec( $str, '' );
	}

// *****************************************************************
// * [関数名]
// * h2z_old
// * 半角=>全角変換(旧版)
// * [処理概要]
// * 半角を全角に変換する。
// * [引数]
// * 第1引数 … 変換対象文字列
// * [返却値]
// * 変換後文字列
// *****************************************************************
	function h2z_old( $str ){
		require_once( 'Subfunc/h2z.php' );
		$m = new Subfunc_h2z();
		return $m->exec( $str, 1 );
	}

// *****************************************************************
// * [関数名]
// * h2zh
// * 半角=>全角ひらがな変換
// * [処理概要]
// * 半角を全角に変換する。半角カナは全角ひらがなに変換する。
// * 全角カタカナも全角ひらがなに変換する。
// * [引数]
// * 第1引数 … 変換対象文字列
// * [返却値]
// * 変換後文字列
// *****************************************************************
	function h2zh( $str ){
		require_once( 'Subfunc/h2zh.php' );
		$m = new Subfunc_h2zh();
		return $m->exec( $str, '' );
	}

// *****************************************************************
// * [関数名]
// * h2zh_old
// * 半角=>全角ひらがな変換(旧版)
// * [処理概要]
// * 半角を全角に変換する。半角カナは全角ひらがなに変換する。
// * 全角カタカナも全角ひらがなに変換する。
// * [引数]
// * 第1引数 … 変換対象文字列
// * [返却値]
// * 変換後文字列
// *****************************************************************
	function h2zh_old( $str ){
		require_once( 'Subfunc/h2zh.php' );
		$m = new Subfunc_h2zh();
		return $m->exec( $str, 1 );
	}

// *****************************************************************
// * [関数名]
// * hk2zk
// * 半角カタカナ=>全角カタカナ変換
// * [処理概要]
// * 半角カナを全角カタカナに変換する。
// * [引数]
// * 第1引数 … 変換対象文字列
// * [返却値]
// * 変換後文字列
// *****************************************************************
	function hk2zk( $str ){
		require_once( 'Subfunc/hk2zk.php' );
		$m = new Subfunc_hk2zk();
		return $m->exec( $str );
	}

// *****************************************************************
// * [関数名]
// * DMT2GMT
// * [処理概要]
// * 日時をDMT形式からGMT形式に変換する。
// * [引数]
// * 第1引数 … 日時(YYYYMMDDhhmmss)
// * [返却値]
// * GMT形式の日時
// *****************************************************************
	function DMT2GMT( $date = '' ){
		require_once( 'Subfunc/DMT2GMT.php' );
		$m = new Subfunc_DMT2GMT();
		return $m->exec( $date );
	}

}
