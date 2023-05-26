from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk import constants
import requests
import json
import urllib3

if __name__ == "__main__":
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    msa_var = Variables()
    context = Variables.task_call(msa_var)
    
    msa_ip    = context["msa_ip"]
    msa_user  = context["msa_username"]
    msa_pass  = context["msa_password"]
    
    _url='https://' + msa_ip + '/ubi-api-rest/auth/token'

    _headers={'Content-Type': 'application/json'}
    
    _payload = {"username": msa_user,
                "password": msa_pass
                }
    
    response = requests.post(url=_url, headers=_headers, data=json.dumps(_payload),verify=False, timeout=120)
    
    if 'token' in response.json():
        context["msa_token"] = response.json()['token']
        ret = MSA_API.process_content('ENDED', f' MSA Token acquired OK', context, True)
    else:
        error_message = response.json()['message']
        ret = MSA_API.process_content('FAIL', f'MSA get token failed with message : {error_message}', context, True)
    
    print(ret)