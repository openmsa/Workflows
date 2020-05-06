import json
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order

# List all the parameters required by the task
dev_var = Variables()
dev_var.add('id', var_type='Integer')
dev_var.add('src_ip', var_type='String')
dev_var.add('dst_port', var_type='Integer')
context = Variables.task_call(dev_var)

# read the ID of the selected managed entity  
device_id = context['device']

# extract the database ID
devicelongid = device_id[-3:]

# logToFile("update device $devicelongid");
# build the Microservice JSON params for the CREATE
micro_service_vars_array = {'object_id': context['id'],
                            'src_ip': context['src_ip'],
                            'dst_port': context['dst_port']
                            }
object_id = context['id']
simple_firewall = {'simple_firewall': {object_id: micro_service_vars_array}}

# call the CREATE for simple_firewall MS for each device
order = Order(devicelongid)

# command_execute(self, command, params, timeout=60) 
order.command_execute('CREATE', json.dumps(simple_firewall))
response = json.loads(order.content)
if 'wo_status' not in response.keys():
  ret = MSA_API.process_content('FAILED', f'Policy update failed - {response}', context, True)
elif response['wo_status'] is 'ENDED':
  if 'rules' not in context.keys() or conext['rules'] is '':
    index = 0
  else:
    index = len(context['rules'])
  context['rules'] = {index: {
                              'delete': False,
                              'id': context['id'],
                              'src_ip': context['src_ip'],
                              'dst_port': context['dst_port']
                             }
                       }
  ret = MSA_API.process_content(response['wo_status'], response['wo_comment'], context, True)
else:
  ret = MSA_API.process_content('FAILED', f'Policy update failed - {response}', context, True)
print(ret)
