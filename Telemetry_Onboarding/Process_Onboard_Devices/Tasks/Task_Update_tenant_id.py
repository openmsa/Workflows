from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.device import Device
import requests
import urllib3
import json

if __name__ == "__main__":
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    dev_var = Variables()
    context = Variables.task_call(dev_var)
    
    cust_id = context["UBIQUBEID"][4:]
    tenant_id = context["UBIQUBEID"][:3]
    devices = context["devices"]
    pattern_id = context["kibana_index_id"]
    kibana_username = context["kibana_username"]
    kibana_password = context["kibana_password"]
    
    _url = 'http://msa-kibana:5601/kibana/api/index_patterns/index_pattern/{}/runtime_field'.format(pattern_id)

    _headers = {'Content-Type':'application/json', 'kbn-xsrf' : 'true'}
    
    _payload = """
def source = doc['tag.device.keyword'].value;
""";
    
    for device in devices:
      me_id = device["device"][3:]
      me_ip    = Device(device_id=me_id).management_address
      block = '''if (source == "{}") {{
  emit("{}");
  return;
}}
'''.format(me_ip,tenant_id)
      
      _payload += block
    
    _data = {
    "name": "tenant_id",
    "runtimeField": {
    "type": "keyword",
    "script": {
    "source": _payload
    }
    }
    }

    try:
        response = requests.put(url=_url, headers=_headers, data=json.dumps(_data),auth=(kibana_username,kibana_password), timeout=240)
        output_code = response.status_code
        if int(output_code) < 400:
            response_json = response.json()
            context["kibana_index_name"] = response_json["index_pattern"]["title"]
            ret = MSA_API.process_content('ENDED', f' tenant_id update in kibana index {context["kibana_index_name"]} successful', context, True)
        else : 
            ret = MSA_API.process_content('FAIL', f' tenant_id update in kibana index failed with message: {response.text}', context, True)
    except requests.exceptions.ConnectionError: 
        ret = MSA_API.process_content('FAIL', f' ConnectionError Please check kibana URL', context, True)
        pass
    
    print(ret)
