import json
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

context = Variables.task_call()

ms_vars_dict_list = []
device_ip_list = context["device_ip_list"]

if __name__ == "__main__":

    '''
    Generate data in format.
    ms_vars_dict = {"namespace": ,
                    "pod_name": ,
                    "container_name": ,
                    "remote_ip":
                    }
    '''

    for ip in device_ip_list: 
        ms_vars_dict = {"namespace": context['service_namespace'],
                        "pod_name": ip.replace(".", "-"),
                        "container_name": ip.replace(".", "-"),
                        "remote_ip": ip,
                        "pkt_size": context['pkt_size'],
                        "pkt_count": context['pkt_count']
                        }
        ms_vars_dict_list.append(ms_vars_dict)

    context['ms_vars_dict_list'] = ms_vars_dict_list 


    ret = MSA_API.process_content('ENDED', f'DATA {context["ms_vars_dict_list"]}', context, True)
    print(ret)