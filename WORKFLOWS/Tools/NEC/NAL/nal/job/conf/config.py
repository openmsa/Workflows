# -*- coding: utf-8 -*-

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
import importlib
import inspect


CONFIG_MODULE_PATH = 'job.conf.config'


class JobConfig:

    """JOB Config For Every Environment."""

    def __init__(self):

        # Import Module(ApiConfig(Env))
        module = importlib.import_module(CONFIG_MODULE_PATH + self.ENV)

        # Create Instance(ApiConfig(Env))
        class_config_env = getattr(
            module, __class__.__name__ + self.ENV[0].upper() + self.ENV[1:])
        config_env = class_config_env()

        # Add Instance Variables From ApiConfig(Env)
        config_env_list = inspect.getmembers(
                            config_env, lambda a: not(inspect.isroutine(a)))

        for val in config_env_list:
            if val[0].startswith('__') == False:
                self.__dict__[val[0]] = val[1]

    ### Config Section #######################################################

    # ENV_DEV  : For Local Environment/Integrated Environment(Internal)
    # ENV_REL  : For Integrated Environment(External)
    ENV_DEV = 'dev'
    ENV_REL = 'rel'

    # Select Environment
    ENV = ENV_REL

    # Character Set
    CHAR_SET = 'utf-8'

    # Definition For Log
    LOG_DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
    LOG_PASSWORD_MASK = '***'
    LOG_DECORATE_LINE = '****************************************************'

    # Definition For VLAN
    USE_GATEWAY_ADDR_VLAN_IP = True

    # Definition For NAL(TiemOut)
    PROV_TIMEOUT = 1000

    # Definition For apl_type
    APL_TYPE_VR = 1  # Virtual
    APL_TYPE_PH = 2  # Physical

    # Definition For network_type
    NW_TYPE_IN = 1  # Internal
    NW_TYPE_EX = 2  # External

    # Definition For network_type_detail
    NW_TYPE_TENANT = 1  # Internal
    NW_TYPE_EXTRA = 2  # Extra
    NW_TYPE_PUBLIC = 3  # Public
    NW_TYPE_MSA = 4  # MSA
    NW_TYPE_WAN = 5  # WAN

    # Definition For network_name
    NW_NAME_PUB = 'pub_lan'
    NW_NAME_EXT = 'ext_lan'
    NW_NAME_IDC = 'idc_lan'

    # Network Type Name
    NW_TYPE_VXLAN = 'VXLAN'
    NW_TYPE_VLAN = 'VLAN'

    # Definition For DB Client(RestAPI)
    REST_URI_TENANT = 'tenants'
    REST_URI_POD = 'pods'
    REST_URI_VXLANGW_POD = 'vxlangw-pods'
    REST_URI_APL = 'appliances'
    REST_URI_GLOBAL_IP = 'global-ip-addresses'
    REST_URI_VLAN = 'vlans'
    REST_URI_PORT = 'ports'
    REST_URI_LICENSE = 'licenses'
    REST_URI_MSA_VLAN = 'msa-vlan'
    REST_URI_PNF_VLAN = 'pnf-vlan'
    REST_URI_NAL_ENDPOINT = 'nal-endpoints'
    REST_URI_NAL_CONFIG = 'nal-configs'
    REST_URI_WIM_ENDPOINT = 'wim-endpoints'
    REST_URI_WIM_CONFIG = 'wim-configs'
    REST_URI_WIM_DC = 'dcs'
    REST_URI_WIM_DC_CON_GROUP = 'dc-con-groups'
    REST_URI_WIM_DC_CON_MEMBER = 'dc-con-members'
    REST_URI_WIM_DC_CON_VLAN = 'dc-vlans'
    REST_URI_WIM_DC_SEGMENT_MNG = 'dc-segment'

    OS_SERVER_BOOT_COUNT = 10
    OS_SERVER_BOOT_INTERVAL = 30
    OS_SERVER_REBOOT_COUNT = 10
    OS_SERVER_REBOOT_INTERVAL = 30
    OS_SERVER_WAIT_TIME = 0
    OS_SERVER_WAIT_TIME_FOR_ATTACH = 60
    OS_SERVER_WAIT_TIME_PALOALTO = 120
    OS_SERVER_WAIT_TIME_CSR_LICENSE = 120

    OS_PORT_CREATE_RETRY_COUNT = 10
    OS_PORT_CREATE_WAIT_TIME = 1
    OS_ERR_MSG_PORT_DUPLICATED = 'HTTP Error 409: Conflict'

    SOAP_SSH_ERR_STR = 'Connection closed by peer'

    MSA_PROVISIONING_CHECK_COUNT = 10
    MSA_PROVISIONING_RETRY_COUNT = 10
    MSA_PROVISIONING_WAIT_TIME = 30
    MSA_AFTER_ATTACH_COUNT = 10
    MSA_AFTER_ATTACH_INTERVAL = 1
    MSA_SSH_RETRY_COUNT = 12
    MSA_SSH_RETRY_INTERVAL = 1

    SSH_CONNECTION_COUNT = 10
    SSH_CONNECTION_INTERVAL = 30

    # Definition Router NameList: Virtual Router
    VM_ROUTER_NODE_NAME1 = 'ce01'
    VM_ROUTER_NODE_NAME2 = 'ce02'

    # Definition For type
    TYPE_FW = 1  # Firewall
    TYPE_LB = 2  # LoadBalancer
    TYPE_RT = 3  # Router

    # Definition For device_type: Virtual Firewall
    DEV_TYPE_IS_VM_SG = 1
    DEV_TYPE_FORTI_GATE = 2
    DEV_TYPE_PALO_ALTO = 3
    DEV_TYPE_IS_VM_SG_PUB = 4

    # Definition For Device Type: Virtual LoadBalancer
    DEV_TYPE_IS_VM_LB = 1
    DEV_TYPE_BIG_IP = 2
    DEV_TYPE_VTHUNDER = 3

    # Definition For device_type Type: Virtual Router
    DEV_TYPE_VSRX = 1
    DEV_TYPE_CSRV = 2

    # Definition For device_type: Physical Firewall
    DEV_TYPE_PHY_FORTIGATE = 1
    DEV_TYPE_PHY_PALOALTO = 2
    DEV_TYPE_PHY_FORTIGATE_SHARE = 3
    DEV_TYPE_PHY_PALOALTO_SHARE = 4

    # Definition For Device Type: Physical LoadBalancer
    DEV_TYPE_PHY_BIGIP = 1
    DEV_TYPE_PHY_THUNDER = 2
    DEV_TYPE_PHY_BIGIP_SHARE = 3
    DEV_TYPE_PHY_THUNDER_SHARE = 4

    # Definition For Group Type: Inter DC
    GROUP_TYPE_VSRX = 1
    GROUP_TYPE_CSRV = 2
    GROUP_TYPE_CSRV_TUNNEL_ESP = 3
    GROUP_TYPE_CSRV_TUNNEL_AH = 4

    # Difinition For Template
    TEMPLATE_INIT_PROV_IS_VM_SG = '/InitProviInterSecSG.tpl'
    TEMPLATE_INIT_PROV_IS_VM_LB = '/InitProviInterSecLB.tpl'
    TEMPLATE_INIT_PROV_IS_VM_CSR = '/InitProviCSR1000v.tpl'
    TEMPLATE_INIT_PROV_IS_VM_FORTIGATE = '/InitProviFortigateVM.tpl'
    TEMPLATE_INIT_PROV_IS_VM_PALOALTO_INIT_CFG \
                                    = '/InitProviPaloaltoVMInitCfg.tpl'
    TEMPLATE_INIT_PROV_IS_VM_PALOALTO_BOOTSTRAP \
                                    = '/InitProviPaloaltoVMBootstrap.tpl'
