from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.device import Device
from msa_sdk import constants
import requests
import json
import urllib3
import time

if __name__ == "__main__":
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    dev_var = Variables()
    context = Variables.task_call(dev_var)
    
    cisco_me_ip    = context["cisco_me_ip"]
    cisco_me_user  = context["cisco_me_user"]
    cisco_me_pass  = context["cisco_me_pass"]

    _url='https://' + cisco_me_ip + '/ins'

    _headers={'content-type':'application/json-rpc'}
    
    _command="copy running-config startup-config"
    
    _payload={
      "jsonrpc": "2.0",
      "method": "cli",
      "params": {
        "cmd": _command,
        "version": 1
      },
      "id": 1
    }
    
    try:
        response = requests.post(url=_url, headers=_headers, data=json.dumps(_payload),auth=(cisco_me_user,cisco_me_pass), verify=False, timeout=120).json()
    except requests.exceptions.ReadTimeout: 
        pass
    
    ret = MSA_API.process_content('ENDED', f' Copy running-config to startup-config response: {response}', context, True)
    print(ret)
    
