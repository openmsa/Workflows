import json
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

context = Variables.task_call()

ms_vars_dict_list = []
device_ip_list = context["device_ip_list"]

'''
Generate data in format.
ms_vars_dict = {"namespace": ,
                "pod_name": ,
                "container_name": ,
                "remote_ip":
                }
'''

for ip in device_ip_list.values(): 
    ms_vars_dict = {"namespace": context['namespace'],
                    "pod_name": ip.replace(".", "-"),
                    "container_name": ip.replace(".", "-"),
                    "remote_ip": ip,
                    "packet_size": context['packet_size'],
                    "packet_count": context['packet_count']
                    }
    ms_vars_dict_list.append(ms_vars_dict)
    
context['ms_vars_dict_list'] = ms_vars_dict_list 


ret = MSA_API.process_content('ENDED', f'DATA {context["ms_vars_dict_list"]}', context, True)
print(ret)