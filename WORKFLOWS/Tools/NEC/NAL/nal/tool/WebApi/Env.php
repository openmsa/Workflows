<?php
// **********************************************************************
// * ���׶��̴Ķ��ѿ����� ����ץ�
// **********************************************************************

// **********************
// �ǥ��쥯�ȥ��Ϣ
// **********************
// �ۡ���ǥ��쥯�ȥ�
define( 'BASE_HOME_DIR', '/home2/bsd1333t/contents/asset/' );

// bin�ǥ��쥯�ȥ�
define( 'BASE_BIN_DIR', BASE_HOME_DIR . 'bin/' );
// ����å���ǥ��쥯�ȥ�
define( 'BASE_CACHE_DIR', BASE_HOME_DIR . 'cache/' );
// ����ե����ǥ��쥯�ȥ�
define( 'BASE_CONFIG_DIR', BASE_HOME_DIR . 'config/' );
// �饤�֥��ǥ��쥯�ȥ�
define( 'BASE_LIB_DIR', BASE_HOME_DIR . 'lib/' );
// PHP�饤�֥��ǥ��쥯�ȥ�
define( 'BASE_PHPLIB_DIR', BASE_HOME_DIR . 'phplib/' );
// �ƥ�ץ졼�ȥǥ��쥯�ȥ�
define( 'BASE_TEMPLATE_DIR', BASE_HOME_DIR . 'template/' );
// ����ѥ���ǥ��쥯�ȥ�
define( 'BASE_TEMPLATE_C_DIR', BASE_HOME_DIR . 'template_c/' );
// �ƥ�ݥ��ǥ��쥯�ȥ�
define( 'BASE_TMP_DIR', BASE_HOME_DIR . 'tmp/' );


// *****************************
// �ѥ�᡼����Ϣ  ���ѹ��Բġ�
// *****************************
// ����CGI�ѥ�᡼���裱����̾�����
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
// �ץ�ӥ塼��Ϣ
// **********************
// �ץ�ӥ塼ɽ���ե饰
define( 'PREVIEW', '1' );


// **********************
// ʸ�������ɴ�Ϣ
// **********************
// CGI��ʸ��������
define( 'BASE_CGI_CHARCODE', 'euc-jp' );
// ����ʸ��������
define( 'BASE_DISP_CHARCODE', 'euc-jp' );


// **********************
// �ǡ����١�����Ϣ
// **********************
// �ǡ����١������ѥե饰
$_BASE_ENV['DB_USE_FLG'] = 1;
// ���ݡ��Ȥ���DB
$_BASE_ENV['PHP_DB_SUPPORT'] = array('mysql', 'pgsql', 'oci');

// PHP��DB��³�����Ǽ�ǥ��쥯�ȥ�
$_BASE_ENV['PHP_DBCONF_DIR'] = BASE_CONFIG_DIR . 'db';

$_BASE_ENV['SERVER_ENVIRONMENT'] = 'test';

$_BASE_ENV['PHP_DB_ENCKEY'] = 'scpf';


// ***********************
// fork�Хå�����
// ***********************
define( 'FORK_YAML_DIR', BASE_TMP_DIR . 'fork/' );
define( 'FORK_YAML_ENCKEY', 'webossfork' );
define( 'FORK_BATCH_PATH', BASE_BIN_DIR . 'http_fork_host05.php' );


// ***********************
// ���󥯥롼�ɥѥ�������
// ***********************
set_include_path(implode(PATH_SEPARATOR, array(
    '.',        // �¹ԥ�����ץȤ�Ʊ���ǥ��쥯�ȥ�
    BASE_PHPLIB_DIR, // PHP�饤�֥��ǥ��쥯�ȥ�
    BASE_LIB_DIR,    // �饤�֥��ǥ��쥯�ȥ�
    get_include_path()
)));
