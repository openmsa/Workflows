from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.device import Device

from custom.ETSI.NsLcmSol005 import NsLcmSol005
from custom.ETSI.NsdSol005 import NsdSol005


if __name__ == "__main__":

    dev_var = Variables()
    dev_var.add('nfvo_device', var_type='Device')
    dev_var.add('vnfm_device', var_type='Device')
    dev_var.add('ns_package_id', var_type='String')
    context = Variables.task_call(dev_var)
    
    mano_me_id = context["nfvo_device"][3:]
    mano_ip    = Device(device_id=mano_me_id).management_address
    mano_var   = Device(device_id=mano_me_id).get_configuration_variable("HTTP_PORT")
    mano_port  = mano_var.get("value")
    mano_user  = Device(device_id=mano_me_id).login
    mano_pass  = Device(device_id=mano_me_id).password
    
    context["mano_ip"]   = mano_ip
    context["mano_port"] = mano_port
    context["mano_user"] = mano_user
    context["mano_pass"] = mano_pass
    
    nsLcm = NsLcmSol005(context["mano_ip"], context["mano_port"])
    nsLcm.set_parameters(context['mano_user'], context['mano_pass'])
    
    nsd = NsdSol005(context["mano_ip"], context["mano_port"])
    nsd.set_parameters(context['mano_user'], context['mano_pass'])
    
    r1 = nsd.nsd_descriptors_get(context['ns_package_id'])
    
    if nsd.state != "ENDED":
        ret = MSA_API.process_content(nsd.state, f'{r1.content}', context, True)
        print(ret)
        exit()
    
    context['ns_package_id'] = r1.json()["nsdId"]
    
    content = {"nsdId": context['ns_package_id']}

    r2 = nsLcm.ns_lcm_create_instance(content)
    
    context["ns_instance"] = r2.json()

    ret = MSA_API.process_content(nsLcm.state, f'{r1}, {r2}', context, True)
    print(ret)