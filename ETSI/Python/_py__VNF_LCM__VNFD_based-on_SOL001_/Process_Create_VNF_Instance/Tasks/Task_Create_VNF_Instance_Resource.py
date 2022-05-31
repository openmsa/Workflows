from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.device import Device
from msa_sdk import constants

from custom.ETSI.VnfLcmSol003 import VnfLcmSol003
from custom.ETSI.VnfPkgSol005 import VnfPkgSol005


if __name__ == "__main__":

    dev_var = Variables()
    dev_var.add('nfvo_device', var_type='Device')
    dev_var.add('vnfm_device', var_type='Device')
    dev_var.add('vnf_pkg_id', var_type='OBMFRef')
    dev_var.add('vnf_instance_name', var_type='String')
    dev_var.add('vnf_instance_description', var_type='String')
    dev_var.add('is_vnf_instance_exist', var_type='Boolean')
    dev_var.add('vnf_instance_id', var_type='String')
    dev_var.add('ns_service_instance_ref', var_type='String')
    context = Variables.task_call(dev_var)
    
    mano_me_id = context["vnfm_device"][3:]
    mano_ip    = Device(device_id=mano_me_id).management_address
    mano_var   = Device(device_id=mano_me_id).get_configuration_variable("HTTP_PORT")
    mano_port  = mano_var.get("value")
    mano_user  = Device(device_id=mano_me_id).login
    mano_pass  = Device(device_id=mano_me_id).password
    
    context["mano_ip"]   = mano_ip
    context["mano_port"] = mano_port
    context["mano_user"] = mano_user
    context["mano_pass"] = mano_pass
    
    nfvo_mano_me_id = context["nfvo_device"][3:]
    nfvo_mano_ip    = Device(device_id=nfvo_mano_me_id).management_address
    nfvo_mano_var   = Device(device_id=nfvo_mano_me_id).get_configuration_variable("HTTP_PORT")
    nfvo_mano_port  = nfvo_mano_var.get("value")
    nfvo_mano_user  = Device(device_id=nfvo_mano_me_id).login
    nfvo_mano_pass  = Device(device_id=nfvo_mano_me_id).password
    
    context["nfvo_mano_ip"]   = nfvo_mano_ip
    context["nfvo_mano_port"] = nfvo_mano_port
    context["nfvo_mano_user"] = nfvo_mano_user
    context["nfvo_mano_pass"] = nfvo_mano_pass
    
    #Create VNF Instance resources.
    vnfLcm = VnfLcmSol003(context["mano_ip"], context["mano_port"])
    vnfLcm.set_parameters(context['mano_user'], context['mano_pass'])
    
    #Create VNF LCM service instance of an existing VNF Instance.
    if context.get('is_vnf_instance_exist') == True:
        vnf_instance_id = context.get('vnf_instance_id')
        
        MSA_API.task_success('VNF LCM service instance is created for VNF instance id: {vnf_instance_id}.', context)
    
    vnfPkg = VnfPkgSol005(context["nfvo_mano_ip"], context["nfvo_mano_port"])
    vnfPkg.set_parameters(context['nfvo_mano_user'], context['nfvo_mano_pass'])
    
    r1 = vnfPkg.vnf_packages_get_package(context["vnf_pkg_id"])

    if vnfPkg.state != "ENDED":
        ret = MSA_API.process_content(vnfPkg.state, f'{r1}',
                                      context, True)
        print(ret)
        exit()
        
    context["vnfd_id"] = r1.json()["vnfdId"]
    
    metadata = {"deviceManufacturer": "",
                "deviceModel": ""
                }

    payload = {"vnfdId": context["vnfd_id"],
               "vnfInstanceName": "",
               "vnfInstanceDescription": "",
               "metadata": metadata
               }
    
    r2 = vnfLcm.vnf_lcm_create_instance(payload)
    
    lcm_data = r2.json()
    context["vnf_instance_id"] = lcm_data['id']

    ret = MSA_API.process_content(vnfLcm.state, f'{r1}, {r2}',
                                  context, True)
    print(ret)