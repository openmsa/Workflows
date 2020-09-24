'''
example curl http://49.135.32.214:9999/restconf/wdm2/add/1/1 -X POST 

Visit http://[YOUR_MSA_URL]/msa_sdk/ to see what you can import.
'''
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
import requests

dev_var = Variables()

context = Variables.task_call(dev_var)

#x = requests.post('https://w3schools.com/python/demopage.htm')
x = requests.post('http://49.135.32.214:9999/restconf/wdm2/add/1/1')

ok = "OK" in x.text

if ok:
  ret = MSA_API.process_content('ENDED', f'{x.text}', context, True)
else:
  ret = MSA_API.process_content('FAILED', f'{x.text}', context, True)
print(ret)

