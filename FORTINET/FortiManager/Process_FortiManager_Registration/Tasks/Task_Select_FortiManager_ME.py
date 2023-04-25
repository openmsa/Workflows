'''
Visit http://[YOUR_MSA_URL]/msa_sdk/ to see what you can import.
'''
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

'''
List all the parameters required by the task

You can use var_name convention for your variables
They will display automaticaly as "Var Name"
The allowed types are:
  'String', 'Boolean', 'Integer', 'Password', 'IpAddress',
  'IpMask', 'Ipv6Address', 'Composite', 'OBMFRef', 'Device'

 Add as many variables as needed
'''
dev_var = Variables()
dev_var.add('fmg_me', var_type='Device')
context = Variables.task_call(dev_var)



ret = MSA_API.process_content('ENDED', 'Selected FortiManager ME => '+context['fmg_me']+'', context, True)
print(ret)

