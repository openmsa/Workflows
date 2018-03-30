<?php
/**
 * 1.SYSTEM   : ����CGI
 * 2.FILE     : Page_env_dev.php
 * 3.FUNCTION : �Ķ��ѿ����� dev�Ķ�
 * 4.CREATE   : 2011/05/30
 * 5.UPDATE   : 
 * @version 
 */
umask(0022);

// php���顼����(1:����)
//ini_set( 'display_errors', '1' );

/**
 * �����ӥ�ID
 */
define( 'SERVICEID', 'webapi' );

/**
 * ������󥿥��ॻ�å����Ź沽����
 */
define( 'ENC_KEY', '123edcxzaqws' );

/**
 * �ǥ��쥯�ȥ��Ϣ
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

// �١������ǥ��쥯�ȥ�
define( 'BASE_LOG_DIR', LOG_DIR . SERVICEID . '_' );

/**
 * �ƽХ⥸�塼��
 */
define( 'CALL_API_FILE', LIB_DIR . 'WebAPI.php' );
define( 'CALL_API_MOD', 'WebAPI' );

/**
 * ���ƥʥ󥹥ե�����
 */
define( 'MAINTE_FILE', CONFIG_DIR . 'ms.txt' );

/**
 * ���ID����ե�����
 */
define( 'CONFIG_SYSTEM_DIR', HOME_DIR . 'config/system/' );

/**
 * �ɥᥤ��
 */
//define( 'WEBAPI_DOMAIN', 'https://133.208.65.97:825/' );
define( 'WEBAPI_DOMAIN', 'https://tapi.moss.biglobe.ne.jp/' );

/**
 * ���顼��
 */
define( 'ERR_LOG_FILE', BASE_LOG_DIR . 'errlog_%_HOSTNAME_%_%_DATE_%.log');

/**
 * ��Х��륰�롼�ץ���������
 */
define( 'STR_MG', '_mg');


// **********************
// ʸ�������ɴ�Ϣ
// **********************
// CGI��ʸ��������
define( 'CGI_CHARCODE', 'utf-8' );
// JSON�ե�����ʸ��������
define( 'JSON_CHARCODE', 'utf-8' );

// **********************
// API��Ϣ
// **********************
// API���ե�����
define( 'API_LOG_FILE', BASE_LOG_DIR . '%_APINAME_%_%_HOSTNAME_%_%_DATE_%.log');
// API���ե�����ե饰
define( 'API_LOG_FLAG', 1 );
// BO��API�ƤӽФ�
define( 'API_ASP_FCALL', '/usr/local/bobio/ASP_FunctionCall.test/client/bin/ASP_FunctionCall.test' );
//define( 'API_ASP_FCALL', '/home/ap/bsd1333t/contents/asset/stub/ASP_FunctionCall.stub' );


// **********************
// �Х�ǡ�����Ϣ
// **********************
// �Х�ǡ�������ե������Ǽ�ǥ��쥯�ȥ�(JSON)
define( 'VALID_RULES_DIR', HTDOCS_DIR . '/portal/js/' );
// �Х�ǡ�������ե�����̾(JSON)
define( 'VALID_RULES_FNAME', 'chk_data.js' );
// ��������Х�ǡ����ؿ����饹̾�ʡ�ե�����̾��
define( 'VALID_MX_CLASS', 'MxValidate_func' );

// *********************************
// ����ե�����
// *********************************
define( 'ERROR_MSG_CFG', CONFIG_DIR . 'error_msg.yaml' );
define( 'MOSS_ENV', CONFIG_DIR . 'env.yaml' );

/**
 * �ǥХå���Ϣ
 */
define( 'DEBUG', '' );

