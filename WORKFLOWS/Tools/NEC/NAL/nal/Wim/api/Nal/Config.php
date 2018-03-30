<?php
#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#  
#       http://www.apache.org/licenses/LICENSE-2.0
#  
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.
#  
#  COPYRIGHT  (C)  NEC  CORPORATION  2017
#  
/**
 * 1.SYSTEM   : API Controller
 * 2.FUNCTION : neccsNal_Config.php
 */

class neccsNal_Config {

    /** BASIC authentication */
    const BASIC_AUTH_ID = 'u_nal';
    const BASIC_AUTH_PW = 'nal@admin';

    /** Return header */
    const CONTENT_TYPE_JSON = 'Content-type: application/json; charset=utf-8';
    const CONTENT_TYPE_URLENCODE = 'Content-Type: application/x-www-form-urlencoded';

    /** Status */
    const STATUS_SUCCESS = 'success';
    const STATUS_WARNING = 'warning';
    const STATUS_ERROR   = 'error';

    /** Error level */
    const LEV_INFO  = 'INFO';
    const LEV_WARN  = 'WARN';
    const LEV_ERROR = 'ERROR';

    /** Error name */
    const SUCCESS_CODE       = 'NAL100000';
    const API_INTERNAL_ERROR = 'NAL140001';
    const PARAMETER_ERROR    = 'NAL110001';
    const JOB_EXEC_ERROR     = 'NAL120001';
    const REST_API_ERROR     = 'NAL130001';
    const OPENSTACK_API_ERROR = 'NAL150001';

    /** Error code by the error level List */
    public static $errorLevelCode = array(
        // INFO
        self::SUCCESS_CODE        => self::LEV_INFO,
        //WARN
        // ERROR
        self::API_INTERNAL_ERROR  => self::LEV_ERROR,
        self::PARAMETER_ERROR     => self::LEV_ERROR,
        self::JOB_EXEC_ERROR      => self::LEV_ERROR,
        self::REST_API_ERROR      => self::LEV_ERROR,
        self::OPENSTACK_API_ERROR => self::LEV_ERROR,
    );

    /** Error Code */
    public static $errorCode = array(
        self::STATUS_SUCCESS => array(
            'code'    => 'NAL100000',
            'message' => ''
        ),
        self::STATUS_ERROR => array(
            'code'    => 'NAL140001',
            'message' => 'A system error occurred.'
        )
    );

    // JobCenter
    const JOB_CENTER    = '1';
    // JobScheduler
    const JOB_SCHEDULER = '2';
      /**Settings files of NAL API */
    const NAL_CONF_PATH = '/usr/local/bin/nal.ini';

    /** Configuration files of NAL API
     * (If you can not be acquired from the configuration file of NAL API) */
    public static $nalConfDefault = array(
        'root_inoutfile' => '/var/log/nal/wimjob',
        'api_type'       => 'wim',
        'job_type'       => '1',
    );

    // Mode when you run(JobScheduler)
    const JOB_EXEC_MODE  = 1;
    // Mode when checking the execution status(JobScheduler)
    const JOB_CHECK_MODE = 2;

    /** HTTP method */
    const HTTP_GET    = 'GET';
    const HTTP_POST   = 'POST';
    const HTTP_PUT    = 'PUT';
    const HTTP_DELETE = 'DELETE';

    /** Function name */
    const NODE      = 'node';
    const SERVICE   = 'service';
    const RESOURCE  = 'resource';

    /** commodity */
    const VFW       = 'vfw';
    const VLB       = 'vlb';
    const PFW       = 'pfw';
    const PLB       = 'plb';
    const GLOBALIP  = 'globalip';
    const EXT_GLOBALIP    = 'ext_globalip';
    const DCCONNECT       = 'dcconnect';
    const LICENSE         = 'license';
    const ALLNODE         = 'all_node';
    const ALLDCCONNECT    = 'all_dcconnect';
    const ALLRESOURCE     = 'all_resource';
    const PNF             = 'pnf';
    const CPU_LIST        = 'cpu_list';
    const CPU_DETAIL      = 'cpu_detail';
    const MEMORY_LIST     = 'memory_list';
    const MEMORY_DETAIL   = 'memory_detail';
    const STORAGE_LIST    = 'storage_list';
    const STORAGE_DETAIL  = 'storage_detail';
    const GLOBALIP_PAYOUT = 'globalip_payout';
    const GLOBALIP_RETURN = 'globalip_return';
    const APPLIANCES      = 'appliances';
    const MSA_VLAN        = 'msa_vlan';
    const WAN_VLAN        = 'wan_vlan';
    const BANDWIDTH       = 'bandwidth';
    const SERVICE_SETTING = 'serviceSetting';
    const VFWIPV6ADD      = 'vfwIPv6Add';
    const VLBIPV6ADD      = 'vlbIPv6Add';
    const SERVICEIPV6ADD  = 'serviceIPv6Add';
    const PFWIPV6ADD      = 'pfwIPv6Add';
    const PLBIPV6ADD      = 'plbIPv6Add';

    /** commodity(PUT) */
    const VFW_PORT_POST   = 'vfw_port_p';
    const VFW_PORT_DELETE = 'vfw_port_d';
    const PFW_PORT_POST   = 'pfw_port_p';
    const PFW_PORT_DELETE = 'pfw_port_d';

    /**
     * Available methods list
     *
     * commodity => array(
     *     HTTP method => array( GET Operasion type )
     */
    public static $tradeMaterialList = array(
        self::NODE => array(
            self::VFW => array(
                self::HTTP_GET,
                self::HTTP_POST,
                self::HTTP_DELETE,
            ),
            self::VLB => array(
                self::HTTP_GET,
                self::HTTP_POST,
                self::HTTP_DELETE,
            ),
            self::PFW => array(
                self::HTTP_GET,
                self::HTTP_POST,
                self::HTTP_DELETE,
            ),
            self::PLB => array(
                self::HTTP_GET,
                self::HTTP_POST,
                self::HTTP_DELETE,
            ),
            self::VFW_PORT_POST => array(
                self::HTTP_PUT,
            ),
            self::VFW_PORT_DELETE => array(
                self::HTTP_PUT,
            ),
            self::PFW_PORT_POST => array(
                self::HTTP_PUT,
            ),
            self::PFW_PORT_DELETE => array(
                self::HTTP_PUT,
            ),
            self::LICENSE => array(
                self::HTTP_PUT,
            ),
            self::ALLNODE => array(
                self::HTTP_GET,
            ),
            self::VFWIPV6ADD => array(
                self::HTTP_PUT,
            ),
            self::VLBIPV6ADD => array(
                self::HTTP_PUT,
            ),
            self::PFWIPV6ADD => array(
                self::HTTP_PUT,
            ),
            self::PLBIPV6ADD => array(
                self::HTTP_PUT,
            ),
        ),
        self::SERVICE => array(
            self::ALLDCCONNECT => array(
                self::HTTP_GET,
            ),
            self::DCCONNECT => array(
                self::HTTP_GET,
                self::HTTP_POST,
                self::HTTP_PUT,
                self::HTTP_DELETE,
            ),
            self::BANDWIDTH => array(
                self::HTTP_PUT,
            ),
            self::SERVICE_SETTING => array(
                self::HTTP_PUT,
            ),
            self::SERVICEIPV6ADD => array(
                self::HTTP_PUT,
            )
        ),
        self::RESOURCE => array(
            self::ALLRESOURCE => array(
                self::HTTP_GET,
            ),
            self::GLOBALIP => array(
                self::HTTP_GET,
            ),
            self::GLOBALIP_PAYOUT => array(
                self::HTTP_PUT,
            ),
            self::GLOBALIP_RETURN => array(
                self::HTTP_PUT,
            ),
            self::LICENSE => array(
                self::HTTP_GET,
            ),
            self::PNF => array(
                self::HTTP_GET,
            ),
            self::CPU_LIST => array(
                self::HTTP_GET,
            ),
            self::CPU_DETAIL => array(
                self::HTTP_GET,
            ),
            self::MEMORY_LIST => array(
                self::HTTP_GET,
            ),
            self::MEMORY_DETAIL => array(
                self::HTTP_GET,
            ),
            self::STORAGE_LIST => array(
                self::HTTP_GET,
            ),
            self::STORAGE_DETAIL => array(
                self::HTTP_GET,
            ),
            self::EXT_GLOBALIP => array(
                self::HTTP_GET,
                self::HTTP_PUT,
            ),
            self::APPLIANCES => array(
                self::HTTP_GET,
            ),
            self::MSA_VLAN => array(
                self::HTTP_GET,
            ),
            self::SERVICE => array(
                self::HTTP_GET,
            ),
            self::WAN_VLAN => array(
                self::HTTP_GET,
            )
        ),
    );

    // The default value for the number of retries
    const DEFAULT_MAX      = 270;
    const DEFAULT_INTERVAL = 10;
    const DCCONNECT_WIM_SUCCESS_WAITING = 10;
    const DCCONNECT_WIM_STATUS_CHANGE_WAITING = 60;

    /**
     * function/HTTP method by number of retries
     *
     * function => array(
     *     HTTP methods => array( number of retries,interval )
     * )
     */
    public static $retrySettingList = array(
        self::DCCONNECT => array(
            self::HTTP_POST   => array( 'retry_max' => self::DEFAULT_MAX, 'retry_interval' => self::DEFAULT_INTERVAL ),
            self::HTTP_PUT    => array( 'retry_max' => self::DEFAULT_MAX, 'retry_interval' => self::DEFAULT_INTERVAL ),
            self::HTTP_DELETE => array( 'retry_max' => self::DEFAULT_MAX, 'retry_interval' => self::DEFAULT_INTERVAL ),
        ),
        self::BANDWIDTH => array(
            self::HTTP_PUT    => array( 'retry_max' => self::DEFAULT_MAX, 'retry_interval' => self::DEFAULT_INTERVAL ),
        ),
        self::SERVICE_SETTING => array(
            self::HTTP_PUT    => array( 'retry_max' => self::DEFAULT_MAX, 'retry_interval' => self::DEFAULT_INTERVAL ),
        ),
        self::SERVICEIPV6ADD => array(
            self::HTTP_PUT    => array( 'retry_max' => self::DEFAULT_MAX, 'retry_interval' => self::DEFAULT_INTERVAL ),
        )
    );

    /** List of merchandise another operation type(PUT) */
    public static $putOperationList = array(
        self::VFW_PORT_POST    => 'create-vport',
        self::VFW_PORT_DELETE  => 'delete-vport',
        self::PFW_PORT_POST    => 'create-pport',
        self::PFW_PORT_DELETE  => 'delete-pport'
    );

    /** Directory path */
    const DIR_PATH = '%ROOT_DIR%/%UUID%';

    /** Various file name */
    const IN_FILE  = 'IN.json';
    const OUT_FILE = 'OUT.json';
    const CHILD_PROCESS_FILE = 'ChildProcess';
    const IN_XMLFILE = 'in.xml';

    /** Command to invoke the JobCenter(For execution) */
    const CMD_JOB_CENTER = '/usr/lib/nqs/gui/bin/jnwsubmitcmd';

    /** Command to invoke the JobCenter(For completion confirmation) */
    const CMD_JOB_CENTER_CHECK = "/usr/lib/nqs/gui/bin/jnwsummary -j trk=%JOBID% | grep -v 'TRACKER-ID' | awk '{printf(\"%s\", $4);}'";

    /** Command to invoke the JobScheduler(For execution) */
    const CMD_JOB_SCHEDULER = 'curl -d @%FILE% http://localhost:4444';

    /** JOB Scheduler Definition of the Input parameters */
    const  FORMAT_JOB_SCHEDULER_IN = <<<  STR
<?xml version="1.0" encoding="UTF-8"?>
<add_order  job_chain="/NAL/%SCENARIO%/%JOBNAME%" at="now">
<params>
%PARAMLIST%
</params>
</add_order>
STR;

    /** JOB Scheduler Definition of the Input parameters(BODY) */
    const  FORMAT_JOB_SCHEDULER_IN_BODY = '<param name="%KEY%" value="%VALUE%" />';

    /** JOB Scheduler Definition of the Input parameters(Status check) */
    const  FORMAT_JOB_SCHEDULER_IN_STATUS = <<<  STR
<?xml version="1.0" encoding="UTF-8"?>
<show_order job_chain="/NAL/%SCENARIO%/%JOBNAME%" order="%JOBID%"/>
STR;
    /** JOB SCHEDULER During execution  */
    const JOBSCHEDULER_STATUS_RUNNING  = '01';

    /** Job execution completion confirmation state */
    const JOB_STATUS_RUN  = 'run';
    const JOB_STATUS_DONE = 'done';

    /** Task Status List */
    const TASK_STATUS_RUNNING = '0';
    const TASK_STATUS_SUCCESS = '1';
    const TASK_STATUS_ERROR   = '9';

    /** List of resource names */
    const RESOURCE_PODS            = 'pods';
    const RESOURCE_TENANTS         = 'tenants';
    const RESOURCE_VLANS           = 'vlans';
    const RESOURCE_PORTS           = 'ports';
    const RESOURCE_DC_CON_GROUPS   = 'dc-con-groups';
    const RESOURCE_DC_CON_MEMBERS  = 'dc-con-members';
    const RESOURCE_ENDPOINS        = 'nal-endpoints';
    const RESOURCE_GLOBAL_IP_ADDR  = 'global-ip-addresses';
    const RESOURCE_LICENSES        = 'licenses';
    const RESOURCE_DCS             = 'dcs';
    const RESOURCE_QUOTAS          = 'quotas';
    const RESOURCE_APLS            = 'appliances';
    const RESOURCE_MSA             = 'msa-vlan';
    const RESOURCE_WAN             = 'dc-vlans';
    const RESOURCE_ENDPOINS_WIM    = 'wim-endpoints';
    const RESOURCE_CONFIG          = 'nal-configs';
    const RESOURCE_CONFIG_WIM      = 'wim-configs';
    const RESOURCE_CONTRACT        = 'contracts';
    const RESOURCE_THRESHOLDS      = 'thresholds';

    /**
     * List of resources to be specified at the time of reference(Single API)
     *
     * commodity => Resource name
     *
     */
    public static $setReferResource = array(
        self::GLOBALIP  => self::RESOURCE_GLOBAL_IP_ADDR,
        self::LICENSE   => self::RESOURCE_LICENSES,
        self::PNF       => self::RESOURCE_APLS,
        self::DCCONNECT => self::RESOURCE_DC_CON_GROUPS,
        self::ALLDCCONNECT => self::RESOURCE_DC_CON_GROUPS,
        self::ALLNODE      => self::RESOURCE_APLS,
        self::VFW          => self::RESOURCE_PORTS,
        self::PFW          => self::RESOURCE_PORTS,
        self::VLB          => self::RESOURCE_PORTS,
        self::PLB          => self::RESOURCE_PORTS,
        self::EXT_GLOBALIP => self::RESOURCE_GLOBAL_IP_ADDR,
    );

    /**
     * List of resources to be specified at the time of reference(Multiple API)
     *
     * commodity => array(
     *     key => array( resource name1,resource name2 )
     * )
     */
    public static $setReferResourceCustom = array(
        self::VFW       => array(
            'vnf_info'  => self::RESOURCE_APLS,
            'port_info' => self::RESOURCE_PORTS,
        ),
        self::VLB       => array(
            'vnf_info'  => self::RESOURCE_APLS,
            'port_info' => self::RESOURCE_PORTS,
        ),
        self::PFW       => array(
            'pnf_info'   => self::RESOURCE_APLS,
            'port_info'  => self::RESOURCE_PORTS,
        ),
        self::PLB       => array(
            'pnf_info'   => self::RESOURCE_APLS,
            'port_info'  => self::RESOURCE_PORTS,
        ),
        self::ALLRESOURCE => array(
            'globalip_info' => self::RESOURCE_GLOBAL_IP_ADDR,
            'license_info'  => self::RESOURCE_LICENSES,
            'pnf_info'      => self::RESOURCE_APLS,
            'quota_info'    => self::RESOURCE_QUOTAS,
        ),
        self::DCCONNECT   => array(
            'dc_info'        => self::RESOURCE_DCS,
            'dc_group_info'  => self::RESOURCE_DC_CON_GROUPS,
            'dc_member_info' => self::RESOURCE_DC_CON_MEMBERS,
        ),
    );

    /** API URL */
    const API_URL = 'http://10.169.11.5/';
    const API_URL_LIST = 'rest/api/index.py/';

    /** WIM API URL */
    const WIM_API_URL = 'http://127.0.0.1/Wim/';
    /** NAL API URL */
    const NAL_API_URL = 'http://127.0.0.1/Nal/';

    /** Log output destination file path */
    const LOG_DIR = '/var/log/nal/';

    /** Log file name */
    public static $logFileName = array(
        self::LEV_INFO  => 'nal_api_trace.log',
        self::LEV_WARN  => 'nal_api_trace.log',
        self::LEV_ERROR => 'nal_api_trace.log',
    );

    /** HTTP status code(success) */
    public static $successHttpStatus = array(
        '200','201','204'
    );

    /** HTTP status code(No data) */
    public static $notFoundHttpStatus = array(
        '500'
    );

    const API_TYPE_NAL = 'nal';
    const API_TYPE_WIM = 'wim';

    /** API Code at the time of the successful completion */
    public static $successApiCode = array(
        'NAL100000'
    );

    /** API Code at the time of the abnormal termination */
    public static $errorApiCode = array(
        'NAL140001','NAL110001','NAL120001','NAL1300010','NAL150001'
    );

    /** Regular expression to get the ID(delete) */
    const DELETE_JOB_PATTERN = '/delete/';

    /** JOB to call when you register the information */
    const CREATE_DC_FINAL = 'create-dcconnectFinalization';

    /** JOB referred to when you want to delete the information */
    const DELETE_DC_FINAL = 'delete-dcconnectFinalization';

    /** JOB to call to when to update the information */
    const UPDATE_DC_FINAL = 'update-dcconnectFinalization';

    /** JOB name when finalizing bandwidth change */
    const UPDATE_BANDWIDTH_FINAL = 'update-bandwidthFinalization';

    /** JOB name at finalization of service setting change */
    const UPDATE_SERVICE_SETTING_FINAL = 'update-serviceSettingFinalization';

    /** JOB name at finalization of service setting change */
    const UPDATE_SERVICE_IPV6_ADD_FINAL = 'update-serviceIPv6AddFinalization';

    /** Specify the dc_id of the DC that I have */
    const MY_DC_ID = 'dc02';

    /** List of APL type */
    const APL_TYPE_VIRTUAL = '1'; // Virtual
    const APL_TYPE_PHYSICS = '2'; // Physics

    /** HTTP time out */
    const CURL_TIMEOUT = 2700;

    /** global ip status update mappinng */
    public static $globalIpUpdateStatus = array(
        '0' => '201',
        '2' => '202'
    );

    /** service device_type list */
    public static $serviceTypeList = array(
        self::FIREFLY => array('1'),
        self::CISCO   => array('2', '3', '4'),
    );

    /** use_type list */
    const USE_TYPE_NAL   = '1';
    const USE_TYPE_WIM   = '2';
    const USE_TYPE_SHARE = '3';

    // type list
    const TYPE_FW     = 1;
    const TYPE_LB     = 2;
    const TYPE_ROUTER = 3;

    // device_type list
    // vfw
    const INTERSECINT = 1;
    const FORTIGATE   = 2;
    const PALOALTO    = 3;
    const INTERSECPUB = 4;
    const FORTIGATE541 = 5;
    // vlb
    const INTERSECLB = 1;
    const BIGIPVE    = 2;
    const VTHUNDER   = 3;
    const VTHUNDER411 = 4;

    // router
    const FIREFLY = 1;
    const CISCO   = 2;
    // pfw
    const PFW_FORTIGATE       = 1;
    const PFW_PALOALTO        = 2;
    const PFW_FORTIGATE_SHARE = 3;
    const PFW_PALOALTO_SHARE  = 4;
    // plb
    const PLB_BIGIP         = 1;
    const PLB_THUNDER       = 2;
    const PLB_BIGIP_SHARE   = 3;
    const PLB_THUNDER_SHARE = 4;

    const FOTIGATE_USABLE_TIME = 4;

    // nw_resource_kind list
    const NW_RESOURCE_KIND_GLOBALIP = 1;
    const NW_RESOURCE_KIND_LICENSE  = 2;
    const NW_RESOURCE_KIND_PNF      = 3;
    const NW_RESOURCE_KIND_MSA      = 4;
    const NW_RESOURCE_KIND_WAN      = 5;

    public static $useCntStatusList = array(
        self::LICENSE => array(
                           self::TYPE_FW => array(
                             self::INTERSECINT => array( 1, 2 ),
                             self::FORTIGATE   => array( 1, 2 ),
                             self::PALOALTO    => array( 1, 2 ),
                             self::INTERSECPUB => array( 1, 2 ),
                             self::FORTIGATE541 => array( 1, 2 ),
                           ),
                           self::TYPE_LB => array(
                             self::INTERSECLB => array( 1, 2 ),
                             self::BIGIPVE    => array( 1, 2 ),
                             self::VTHUNDER   => array( 1, 2 ),
                             self::VTHUNDER411 => array( 1, 2 ),
                           ),
        ),
        self::GLOBALIP => array( 101, 201, 202 ),
        self::EXT_GLOBALIP => array( 201, 202 ),
        self::PNF => array(
                           self::TYPE_FW => array(
                             self::PFW_FORTIGATE       => array( 1, 2, 9, 0 ),
                             self::PFW_PALOALTO        => array( 1, 2, 9, 0 ),
                             self::PFW_FORTIGATE_SHARE => array( 1, 2, 9, 0 ),
                             self::PFW_PALOALTO_SHARE  => array( 1, 2, 9, 0 ),
                           ),
                           self::TYPE_LB => array(
                             self::PLB_BIGIP         => array( 1, 2, 9, 0 ),
                             self::PLB_THUNDER       => array( 1, 2, 9, 0 ),
                             self::PLB_BIGIP_SHARE   => array( 1, 2, 9, 0 ),
                             self::PLB_THUNDER_SHARE => array( 1, 2, 9, 0 ),
                           ),
        ),
        self::MSA_VLAN => array( 1 ),
        self::WAN_VLAN => array( 1 ),
    );

    public static $UnavailableCntStatusList = array(
        self::LICENSE => array(
                           self::TYPE_FW => array(
                             self::INTERSECINT => array(),
                             self::FORTIGATE   => array( 3 ),
                             self::PALOALTO    => array( 3 ),
                             self::INTERSECPUB => array(),
                             self::FORTIGATE541 => array( 3 ),
                           ),
                           self::TYPE_LB => array(
                             self::INTERSECLB => array(),
                             self::BIGIPVE   => array( 3 ),
                             self::VTHUNDER    => array( 3 ),
                             self::VTHUNDER411 => array( 3 ),
                           ),
        ),
        self::PNF => array(
                           self::TYPE_FW => array(
                             self::PFW_FORTIGATE       => array( 0 ),
                             self::PFW_PALOALTO        => array( 0 ),
                             self::PFW_FORTIGATE_SHARE => array( 0 ),
                             self::PFW_PALOALTO_SHARE  => array( 0 ),
                           ),
                           self::TYPE_LB => array(
                             self::PLB_BIGIP         => array( 0 ),
                             self::PLB_THUNDER       => array( 0 ),
                             self::PLB_BIGIP_SHARE   => array( 0 ),
                             self::PLB_THUNDER_SHARE => array( 0 ),
                           ),
        ),
    );

    public static $allResourceParam = array(
        self::LICENSE => array(
                             // FW
                             array(
                                 'nw_resource_kind' => '2',
                                 'function_type'    => 'license',
                                 'apl_type'         => '1',
                                 'type'             => '1',
                                 'device_type'      => '1',
                                 'type_detail'      => '',
                                 'redundant_configuration_flg' => '',
                             ),
                             array(
                                 'nw_resource_kind' => '2',
                                 'function_type'    => 'license',
                                 'apl_type'         => '1',
                                 'type'             => '1',
                                 'device_type'      => '2',
                                 'type_detail'      => '',
                                 'redundant_configuration_flg' => '',
                             ),
                             array(
                                 'nw_resource_kind' => '2',
                                 'function_type'    => 'license',
                                 'apl_type'         => '1',
                                 'type'             => '1',
                                 'device_type'      => '3',
                                 'type_detail'      => array( '1', '2', '3', '4', '5', '6', '7' ),
                                 'redundant_configuration_flg' => '',
                             ),
                             array(
                                 'nw_resource_kind' => '2',
                                 'function_type'    => 'license',
                                 'apl_type'         => '1',
                                 'type'             => '1',
                                 'device_type'      => '4',
                                 'type_detail'      => '',
                                 'redundant_configuration_flg' => '',
                             ),
                             array(
                                 'nw_resource_kind' => '2',
                                 'function_type'    => 'license',
                                 'apl_type'         => '1',
                                 'type'             => '1',
                                 'device_type'      => '5',
                                 'type_detail'      => '',
                                 'redundant_configuration_flg' => '',
                             ),
                             // LB
                             array(
                                 'nw_resource_kind' => '2',
                                 'function_type'    => 'license',
                                 'apl_type'         => '1',
                                 'type'             => '2',
                                 'device_type'      => '1',
                                 'type_detail'      => '',
                                 'redundant_configuration_flg' => '',
                             ),
                             array(
                                 'nw_resource_kind' => '2',
                                 'function_type'    => 'license',
                                 'apl_type'         => '1',
                                 'type'             => '2',
                                 'device_type'      => '2',
                                 'type_detail'      => '',
                                 'redundant_configuration_flg' => '',
                             ),
                             array(
                                 'nw_resource_kind' => '2',
                                 'function_type'    => 'license',
                                 'apl_type'         => '1',
                                 'type'             => '2',
                                 'device_type'      => '3',
                                 'type_detail'      => '',
                                 'redundant_configuration_flg' => '',
                             ),
                             array(
                                 'nw_resource_kind' => '2',
                                 'function_type'    => 'license',
                                 'apl_type'         => '1',
                                 'type'             => '2',
                                 'device_type'      => '4',
                                 'type_detail'      => '',
                                 'redundant_configuration_flg' => '',
                             ),
                             // ROUTER
                             array(
                                 'nw_resource_kind' => '2',
                                 'function_type'    => 'license',
                                 'apl_type'         => '1',
                                 'type'             => '3',
                                 'device_type'      => '1',
                                 'type_detail'      => '',
                                 'redundant_configuration_flg' => '',
                             ),
                             array(
                                 'nw_resource_kind' => '2',
                                 'function_type'    => 'license',
                                 'apl_type'         => '1',
                                 'type'             => '3',
                                 'device_type'      => '2',
                                 'type_detail'      => array( '1', '2', '3', '4', '5', '6', '7', '8', '9' ),
                                 'redundant_configuration_flg' => '',
                             ),
        ),
        self::PNF => array(
                             // FW
                             array(
                                 'nw_resource_kind' => '3',
                                 'function_type'    => 'pnf',
                                 'apl_type'         => '2',
                                 'type'             => '1',
                                 'device_type'      => '1',
                                 'type_detail'      => '',
                                 'redundant_configuration_flg' => array( '0', '1' ),
                             ),
                             array(
                                 'nw_resource_kind' => '3',
                                 'function_type'    => 'pnf',
                                 'apl_type'         => '2',
                                 'type'             => '1',
                                 'device_type'      => '2',
                                 'type_detail'      => '',
                                 'redundant_configuration_flg' => array( '0', '1' ),
                             ),
                             array(
                                 'nw_resource_kind' => '3',
                                 'function_type'    => 'pnf',
                                 'apl_type'         => '2',
                                 'type'             => '1',
                                 'device_type'      => '3',
                                 'type_detail'      => '',
                                 'redundant_configuration_flg' => '',
                             ),
                             array(
                                 'nw_resource_kind' => '3',
                                 'function_type'    => 'pnf',
                                 'apl_type'         => '2',
                                 'type'             => '1',
                                 'device_type'      => '4',
                                 'type_detail'      => '',
                                 'redundant_configuration_flg' => '',
                             ),
                             // LB
                             array(
                                 'nw_resource_kind' => '3',
                                 'function_type'    => 'pnf',
                                 'apl_type'         => '2',
                                 'type'             => '2',
                                 'device_type'      => '1',
                                 'type_detail'      => '',
                                 'redundant_configuration_flg' => array( '0', '1' ),
                             ),
                             array(
                                 'nw_resource_kind' => '3',
                                 'function_type'    => 'pnf',
                                 'apl_type'         => '2',
                                 'type'             => '2',
                                 'device_type'      => '2',
                                 'type_detail'      => '',
                                 'redundant_configuration_flg' => array( '0', '1' ),
                             ),
                             array(
                                 'nw_resource_kind' => '3',
                                 'function_type'    => 'pnf',
                                 'apl_type'         => '2',
                                 'type'             => '2',
                                 'device_type'      => '3',
                                 'type_detail'      => '',
                                 'redundant_configuration_flg' => '',
                             ),
                             array(
                                 'nw_resource_kind' => '3',
                                 'function_type'    => 'pnf',
                                 'apl_type'         => '2',
                                 'type'             => '2',
                                 'device_type'      => '4',
                                 'type_detail'      => '',
                                 'redundant_configuration_flg' => '',
                             ),
        ),
        self::GLOBALIP => array(
                             'nw_resource_kind' => '1',
                             'function_type'    => 'globalip',
                             'apl_type'         => '',
                             'type'             => '',
                             'device_type'      => '',
                             'type_detail'      => '',
                             'redundant_configuration_flg' => '',
        ),
        self::MSA_VLAN => array(
                             'nw_resource_kind' => '4',
                             'function_type'    => 'msa_vlan',
                             'apl_type'         => '',
                             'type'             => '',
                             'device_type'      => '',
                             'type_detail'      => '',
                             'redundant_configuration_flg' => '',
        ),
        self::WAN_VLAN => array(
                             'nw_resource_kind' => '5',
                             'function_type'    => 'wan_vlan',
                             'apl_type'         => '',
                             'type'             => '',
                             'device_type'      => '',
                             'type_detail'      => '',
                             'redundant_configuration_flg' => '',
        ),
        self::CPU_LIST => array(
                             'nw_resource_kind' => '6',
                             'function_type'    => 'cpu_list',
                             'apl_type'         => '',
                             'type'             => '',
                             'device_type'      => '',
                             'redundant_configuration_flg' => '',
        ),
        self::MEMORY_LIST => array(
                             'nw_resource_kind' => '7',
                             'function_type'    => 'memory_list',
                             'apl_type'         => '',
                             'type'             => '',
                             'device_type'      => '',
                             'redundant_configuration_flg' => '',
        ),
        self::STORAGE_LIST => array(
                             'nw_resource_kind' => '8',
                             'function_type'    => 'storage_list',
                             'apl_type'         => '',
                             'type'             => '',
                             'device_type'      => '',
                             'redundant_configuration_flg' => '',
        ),
        self::EXT_GLOBALIP => array(
                             'nw_resource_kind' => '1',
                             'function_type'    => 'ext_globalip' ,
                             'apl_type'         => '',
                             'type'             => '',
                             'device_type'      => '',
                             'type_detail'      => '',
                             'redundant_configuration_flg' => '',
        ),
    );

    /** endopoint type */
    const ENDPOINT_TYPE_VIM = '1';

    /** config type */
    const CONFIG_TYPE_COMMON = '5';

    /** contract_kind list */
    const CONTRACT_KIND_GLOBALIP = '1';
    const CONTRACT_KIND_NODE     = '2';
    const CONTRACT_KIND_SERVICE  = '3';

}
