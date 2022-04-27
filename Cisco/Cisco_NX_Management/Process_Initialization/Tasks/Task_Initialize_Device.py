from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.device import Device
from msa_sdk import constants
import requests
import json
import urllib3

if __name__ == "__main__":
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    dev_var = Variables()
    dev_var.add('intialization_input', var_type='String')
    context = Variables.task_call(dev_var)
    
    cisco_me_ip    = context["cisco_me_ip"]
    cisco_me_user  = context["cisco_me_user"]
    cisco_me_pass  = context["cisco_me_pass"]
    
    _url='https://' + cisco_me_ip + '/restconf/data/Cisco-NX-OS-device'

    _headers={'Content-Type':'application/yang.data+xml', 'Accept': 'application/yang.data+xml'}
    
    _payload= context["intialization_input"]
    
    response = requests.patch(url=_url, headers=_headers, data=_payload,auth=(cisco_me_user,cisco_me_pass), verify=False, timeout=120)
    
    output = response.content
    
    ret = MSA_API.process_content('ENDED', f' Device initialization response: {response}', context, True)
    print(ret)