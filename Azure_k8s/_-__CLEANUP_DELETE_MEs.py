import json
from msa_sdk.lookup import Lookup
from msa_sdk.device import Device
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

dev_var = Variables()
context = Variables.task_call()

# prepare device list, by id
cust_ref = context["UBIQUBEID"]
search = Lookup()
search.look_list_device_by_customer_ref(cust_ref)
device_list = search.content
device_list = json.loads(device_list)

me_list_deleted = []
try:
    for me in device_list:
        Device(device_id=me['id']).delete()
        me_list_deleted.append(me['name'])
    if len(me_list_deleted) == 0:
        me_list_deleted.append('...nothing to delete...')
    ret = MSA_API.process_content('ENDED', f'Next devices were deleted: {me_list_deleted}', context, True)
    print(ret)
except Exception as e:
    ret = MSA_API.process_content('FAILED',
                                  f'ERROR: {str(e)}',
                                  context, True)
    print(ret)