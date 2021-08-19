from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

from custom.ETSI.VnfLcmSol003 import VnfLcmSol003
from custom.ETSI.VnfPkgSol005 import VnfPkgSol005


if __name__ == "__main__":

    dev_var = Variables()
    dev_var.add('nfvo_device', var_type='Device')
    dev_var.add('vnf_pkg_id', var_type='OBMFRef')
    dev_var.add('vnf_instance_name', var_type='String')
    dev_var.add('vnf_instance_description', var_type='String')
    # dev_var.add('device_manufacturer', var_type='String')
    # dev_var.add('device_model', var_type='String')
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

    vnfLcm = VnfLcmSol003(context["mano_ip"], context["mano_port"])
    vnfLcm.set_parameters(context['mano_user'], context['mano_pass'])
    
    vnfPkg = VnfPkgSol005(context["mano_ip"], context["mano_port"])
    vnfPkg.set_parameters(context['mano_user'], context['mano_pass'])
    
    r1 = vnfPkg.vnf_packages_get_package(context["vnf_pkg_id"])
    
    context["vnfd_id"] = r1.json()["vnfdId"]
    
    metadata = {"deviceManufacturer": context["device_manufacturer"],
                "deviceModel": context["device_model"]
                }

    payload = {"vnfdId": context["vnfd_id"],
               "vnfInstanceName": "",
               "vnfInstanceDescription": "",
               "metadata": metadata
               }
    
    r2 = vnfLcm.vnf_lcm_create_instance(payload)
    
    lcm_data = r2.json()
    context["vnf_instance_id"] = lcm_data['id']

    ret = MSA_API.process_content('ENDED', f'{r1}, {r2}',
                                  context, True)
    print(ret)