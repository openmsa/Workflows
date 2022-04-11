import sys
import json
from msa_sdk import constants
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

from custom.ETSI.VnfLcmSol003 import VnfLcmSol003
from custom.ETSI.VnfLcmOpOccsSol003 import VnfLcmOpOccsSol003
from custom.ETSI.VnfPkgSol005 import VnfPkgSol005


if __name__ == "__main__":

    dev_var = Variables()
    context = Variables.task_call(dev_var)
    
    if context.get('is_vnf_instance_exist') != True:
        vnfPkg = VnfPkgSol005(context["nfvo_mano_ip"], context["nfvo_mano_port"])
        vnfPkg.set_parameters(context['nfvo_mano_user'], context['nfvo_mano_pass'])
        r1 = vnfPkg.vnf_packages_get_package(context["vnf_pkg_id"])
        var_check = r1.json()["operationalState"]
        if var_check != 'ENABLED':
            MSA_API.task_error('VNF package is '+var_check, context)
        vnfLcm = VnfLcmSol003(context["mano_ip"], context["mano_port"], context['mano_base_url'])
        vnfLcm.set_parameters(context['mano_user'], context['mano_pass'])
        
        content = {'flavourId': 'flavor'}
        
        if "is_third_party_vnfm" in context:
            is_third_party_vnfm = context.get('is_third_party_vnfm')
            if is_third_party_vnfm == 'true':
                content = {"flavourId":"default","vimConnectionInfo":{"0":{"id":"VIM-regionOne-Zone-A","vimId":"0551a37b-7130-498a-9667-84a6b0f503cf","vimType":"ETSINFV.OPENSTACK_KEYSTONE.V_3","interfaceInfo":{"endpoint":"https://keystone.tmtc.pujlab.tmone.my:5000/v3"},"accessInfo":{"project":"admin","domainName":"admin_domain","username":"admin","password":"aish4Eivai4monei"}}},"extVirtualLinks":[{"id":"mgt0_ext_network","vimConnectionId":"VIM-regionOne-Zone-A","resourceId":"8fb7008f-76e4-42d3-ba42-a0f37c387941","extCps":[{"cpdId":"mgt0","cpConfig":{"cpConfigKey":{"cpInstanceId":"mgt0_ext_network","cpProtocolData":[{"layerProtocol":"IP_OVER_ETHERNET","ipOverEthernet":{"ipAddresses":[{"type":"IPV4","numDynamicAddresses":1,"subnetId":"6d3290a8-de22-424f-a45d-bc982d3cdf10"}]}}]}}}]},{"id":"pkt0_ext_network","vimConnectionId":"VIM-regionOne-Zone-A","resourceId":"8fb7008f-76e4-42d3-ba42-a0f37c387941","extCps":[{"cpdId":"pkt0","cpConfig":{"cpConfigKey":{"cpInstanceId":"pkt0_ext_network","cpProtocolData":[{"layerProtocol":"IP_OVER_ETHERNET","ipOverEthernet":{"ipAddresses":[{"type":"IPV4","numDynamicAddresses":1,"subnetId":"6d3290a8-de22-424f-a45d-bc982d3cdf10"}]}}]}}}]},{"id":"pkt1_ext_network","vimConnectionId":"VIM-regionOne-Zone-A","resourceId":"8fb7008f-76e4-42d3-ba42-a0f37c387941","extCps":[{"cpdId":"pkt1","cpConfig":{"cpConfigKey":{"cpInstanceId":"pkt1_ext_network","cpProtocolData":[{"layerProtocol":"IP_OVER_ETHERNET","ipOverEthernet":{"ipAddresses":[{"type":"IPV4","numDynamicAddresses":1,"subnetId":"6d3290a8-de22-424f-a45d-bc982d3cdf10"}]}}]}}}]},{"id":"oam_mgt0_ext_network","vimConnectionId":"VIM-regionOne-Zone-A","resourceId":"8fb7008f-76e4-42d3-ba42-a0f37c387941","extCps":[{"cpdId":"oam_mgt0","cpConfig":{"cpConfigKey":{"cpInstanceId":"oam_mgt0_ext_network","cpProtocolData":[{"layerProtocol":"IP_OVER_ETHERNET","ipOverEthernet":{"ipAddresses":[{"type":"IPV4","numDynamicAddresses":1,"subnetId":"6d3290a8-de22-424f-a45d-bc982d3cdf10"}]}}]}}}]}]}
                
        r = vnfLcm.vnf_lcm_instantiate_vnf(context["vnf_instance_id"], content)
    
        location = ''
        try:
            location = r.headers['Location']
        except:
            MSA_API.task_error('Instantiate VNF message: ' + json.dumps(r.json()), context)
        
        context["vnf_lcm_op_occ_id"] = location.split("/")[-1]
        
        ret = MSA_API.process_content(vnfLcm.state, f'{r}', context, True)
        print(ret)
        sys.exit()
    else:
        vnfLcmOpOccs = VnfLcmOpOccsSol003(context["mano_ip"], context["mano_port"], context['mano_base_url'])
        vnfLcmOpOccs.set_parameters(context['mano_user'], context['mano_pass'])
        
        vnf_instance_id = context['vnf_instance_id']
        
        vnf_lcm_op_occ_id = vnfLcmOpOccs.vnf_lcm_op_occs_get_id(vnf_instance_id)
        context["vnf_lcm_op_occ_id"] = vnf_lcm_op_occ_id
        
        #MSA_API.task_error('The VNF managed entities are created.' + vnf_lcm_op_occ_id, context)
    
    ret = MSA_API.process_content(vnfLcmOpOccs.state, f'VNF Instance context is stored.', context, True)
    print(ret)
    sys.exit()