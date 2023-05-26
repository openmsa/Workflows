from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.device import Device
from msa_sdk import constants
import requests
import json
import urllib3

if __name__ == "__main__":
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    msa_var = Variables()
    msa_var.add('msa_ip', var_type='String')
    msa_var.add('msa_username', var_type='String')
    msa_var.add('msa_password', var_type='String')
    context = Variables.task_call(msa_var)
    
    # cisco_me_ip    = context["cisco_me_ip"]
    # cisco_me_user  = context["cisco_me_user"]
    # cisco_me_pass  = context["cisco_me_pass"]
    
    # _url='https://' + cisco_me_ip + '/restconf/data/Cisco-NX-OS-device'

    # _headers={'Content-Type':'application/yang.data+xml', 'Accept': 'application/yang.data+xml'}
    
    # _payload= context["intialization_input"]
    
    # response = requests.patch(url=_url, headers=_headers, data=_payload,auth=(cisco_me_user,cisco_me_pass), verify=False, timeout=120)
    
    # output = response.content
    
    response = "OK"
    ret = MSA_API.process_content('ENDED', f' MSA Details added successfully', context, True)
    print(ret)