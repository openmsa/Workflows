<?php

$CURL_CMD = "/usr/bin/curl";
$CURL_OPENSTACK = "";

// Process logs file
define('PROCESS_LOGS_DIRECTORY', '/opt/wildfly/logs/processLog/');
define('PROCESS_LOGS_FILE', '/opt/wildfly/logs/processLog/process.log');
define('UBI_JENTREPRISE_DIRECTORY', '/opt/ubi-jentreprise/');

// FMC Repository directories
define('FMC_REPOSITORY_DIRECTORY', '/opt/fmc_repository/');
define('MICRO_SERVICE_DIRECTORY', 'CommandDefinition');
define('TEMPLATE_DIRECTORY', 'Configuration');
define('WORKFLOW_DIRECTORY', 'Process');
define('LICENSE_DIRECTORY', 'License');
define('FIRMWARE_DIRECTORY', 'Firmware');
define('REPORT_DIRECTORY', 'Reports');
define('DOCUMENTATION_DIRECTORY', 'Documentation');

// Filepaths and variable to get the ncroot password
define('VARS_CTX_FILE', '/opt/configurator/vars.ubiqube.net.ctx');
define('WEB_NODE_PRIV_IP', 'UBI_VSOC_SES_PRIVIP');
define('WEB_NODE_PUB_IP', 'UBI_VSOC_SES_PUBIP');
define('WEB_NODE_HTTP_PORT', 'UBI_VSOC_SES_PORT');
define('NCROOT_PASSWORD_VARIABLE', 'UBI_SES_NCROOT_PASSWORD');
define('EMAIL_FROM', 'UBI_MAIL_FROM');
define('ENCP_SCRIPT', '/opt/configurator/script/encp.sh');

// JSON content-type : application/json
define('CONTENT_TYPE_APP_JSON', 'Content-Type : application/json');

// REST Operations
define('OP_POST', 'POST');
define('OP_GET', 'GET');
define('OP_PUT', 'PUT');
define('OP_PATCH', 'PATCH');
define('OP_DELETE', 'DELETE');

// SNMP COMMUNITY DEFAULT VALUE
define('SNMP_COMMUNITY_DEFAULT', 'Default');


// New Line/Line Break Symbol in XML
define('NEW_LINE', '&#10;');
define('AMPERSAND', '&amp;');

// executeCommand Command Names
define('CMD_CREATE', 'CREATE');
define('CMD_IMPORT', 'IMPORT');
define('CMD_UPDATE', 'UPDATE');
define('CMD_DELETE' , 'DELETE');
define('CMD_READ' , 'READ');
define('CMD_LIST' , 'LIST');
define('CMD_SYNCHRONIZE', 'SYNCHRONIZE OBJECTS');

// Poll Sleep params
define('FILE_LOCK_TIMEOUT', 300);
define('FILE_LOCK_STATUS_CHECK_SLEEP', 2);
define('SLEEP_BETWEEN_PINGS', 30);
define('MAX_PING_COUNT', 20);
define('SLEEP_BETWEEN_SSH_RETRY', 30);
define('MAX_SSH_COUNT', 20);
define('DEVICE_STATUS_CHECK_SLEEP', 10);
define('DEVICE_STATUS_CHANGE_TIMEOUT', 600);
define('PROVISIONING_STATUS_CHECK_SLEEP', 10);
define('LINUX_CMD_OUTPUT_CHECK_SLEEP', 10);
define('LINUX_CMD_OUTPUT_CHECK_TIMEOUT', 600);
define('PUSH_CONFIG_CHECK_SLEEP', 10);
define('PUSH_CONFIG_TIMEOUT', 600);
define('UPDATE_CONFIG_CHECK_SLEEP', 10);
define('UPDATE_CONFIG_TIMEOUT', 600);
define('DEVICE_BACKUP_CHECK_SLEEP', 10);
define('DEVICE_BACKUP_TIMEOUT', 600);
define('PROCESS_STATUS_CHECK_SLEEP', 10);
define('STATUS_BLINK_SLEEP', 2);

// SEC Engine Commands
define('SMS_CMD_SSH_STATUS', 'SSHSTATUS');

// Default Port no.
define('SSH_DEFAULT_PORT_NO', 22);

// ERROR Codes
define('ERROR', 'ERROR');
define('ENDED_SUCCESSFULLY', 'ENDED SUCCESSFULLY');

// Task Status
define('STATUS_OK', 'OK');
define('NOTRUN', 'NOTRUN');
define('NONE', 'NONE');

// MSA Device Status
define('UP', 'UP');
define('UNREACHABLE', 'UNREACHABLE');
define('NEVERREACHED', 'NEVERREACHED');

// WO status codes
define('ENDED', 'ENDED');
define('FAILED', 'FAIL');
define('RUNNING', 'RUNNING');
define('WARNING', 'WARNING');
define('PAUSED', 'PAUSE');

// MSA TAG for entities
define('TAG_OPERATOR', 'O');
define('TAG_CUSTOMER', 'A');
define('TAG_MANAGER', 'G');
define('TAG_PROFILE', 'PR');

define('TEMPLATES_HOME_DIR', '/opt/fmc_repository/Configuration/');
define('MICRO_SERVICES_HOME_DIR', '/opt/fmc_repository/CommandDefinition/');
define('WORKFLOWS_HOME_DIR', '/opt/fmc_repository/Process/');

$workflow_internal_params = array('EXECNUMBER', 'PROCESSINSTANCEID', 'SERVICEINSTANCEID', 'SERVICEINSTANCEREFERENCE', 'TASKID', 'UBIQUBEID', 'service_id');

//objects sync timeouts
define('OBJECTS_SYNCHRONIZATION_CONNECTION_TIMEOUT', 600);
define('OBJECTS_SYNCHRONIZATION_MAX_TIME', 600)

?>