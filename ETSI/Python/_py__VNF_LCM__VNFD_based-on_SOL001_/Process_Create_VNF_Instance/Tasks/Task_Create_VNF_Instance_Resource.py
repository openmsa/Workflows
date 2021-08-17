from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

from custom.ETSI.VnfLcmSol003 import VnfLcmSol003


if __name__ == "__main__":

    dev_var = Variables()
    dev_var.add('mano_user', var_type='String')
    dev_var.add('mano_pass', var_type='Password')
    dev_var.add('nfvo_device', var_type='Device')
    dev_var.add('vnf_pkg_id', var_type='OBMFRef')
    dev_var.add('vnfd_id', var_type='String')
    dev_var.add('vnf_instance_name', var_type='String')
    dev_var.add('vnf_instance_description', var_type='String')
    dev_var.add('device_manufacturer', var_type='String')
    dev_var.add('device_model', var_type='String')
    context = Variables.task_call(dev_var)

    vnfLcm = VnfLcmSol003('10.31.1.245', '8080')
    vnfLcm.set_parameters(context['mano_user'], context['mano_pass'])
    
    metadata = {"deviceManufacturer": context["device_manufacturer"],
                "deviceModel": context["device_model"]
                }

    payload = {"vnfdId": context["vnfd_id"],
               "vnfInstanceName": "",
               "vnfInstanceDescription": "",
               "metadata": metadata
               }
    
    r = vnfLcm.vnf_lcm_create_instance(payload)
    
    lcm_data = r.json()
    context["vnf_instance_id"] = lcm_data['id']

    ret = MSA_API.process_content('ENDED', f'{r}, {context["vnf_instance_id"]}',
                                  context, True)
    print(ret)