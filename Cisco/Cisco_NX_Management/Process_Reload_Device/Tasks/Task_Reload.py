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

    _headers={'content-type':'application/json'}
    
    _payload={
      "ins_api":{
      "version": "1.0",
      "type": "cli_conf",
      "chunk": "0",
      "sid": "1",
      "input": "reload",
      "output_format": "json"
      }
    }
    
    try:
        response = requests.post(url=_url, headers=_headers, data=json.dumps(_payload),auth=(cisco_me_user,cisco_me_pass), verify=False, timeout=120).json()
    except requests.exceptions.ReadTimeout: 
        pass
    
    new_device = Device()
    new_device.management_address = cisco_me_ip
    ping_timeout = 0
    
    while ping_timeout <= 300:
        new_device.ping(new_device.management_address)
        content = json.loads(new_device.content)
        if content["status"] == 'OK':
            break;
        ping_timeout += 30
        time.sleep(30)
    
    if new_device.response.ok:
        ret = MSA_API.process_content('ENDED',
                                  f'STATUS: {content["status"]}, \
                                    MESSAGE: {content["message"]}',
                                  context, True)
    print(ret)