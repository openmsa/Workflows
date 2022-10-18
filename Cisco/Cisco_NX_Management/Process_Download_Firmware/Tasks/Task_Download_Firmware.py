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
    dev_var.add('firmware_location', var_type='String')
    dev_var.add('device_destination_path', var_type='String')
    dev_var.add('vrf', var_type='String')
    context = Variables.task_call(dev_var)
    
    cisco_me_ip    = context["cisco_me_ip"]
    cisco_me_user  = context["cisco_me_user"]
    cisco_me_pass  = context["cisco_me_pass"]
    
    _url='https://' + cisco_me_ip + '/ins'

    _headers={'content-type':'application/json'}
    
    _command = "copy " + context["firmware_location"] + " " + context["device_destination_path"] + " vrf " + context["vrf"]
    
    _payload={
      "ins_api":{
      "version": "1.0",
      "type": "cli_conf",
      "chunk": "0",
      "sid": "1",
      "input": _command,
      "output_format": "json"
      }
    }
    
    
    try:
        response = requests.post(url=_url, headers=_headers, data=json.dumps(_payload),auth=(cisco_me_user,cisco_me_pass), verify=False, timeout=600).json()
        output_code = response['ins_api']['outputs']['output']['code']
        if int(output_code) < 400:
            ret = MSA_API.process_content('ENDED', f' Download firmware successful', context, True)
        else : 
            ret = MSA_API.process_content('FAILED', f' Download firmware failed with message: {response}', context, True)
    except requests.exceptions.ReadTimeout: 
        ret = MSA_API.process_content('FAILED', f' Download firmware request timed-out', context, True)
        pass
    
    print(ret)
    
