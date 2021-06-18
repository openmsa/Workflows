import json
from msa_sdk import constants
from msa_sdk.order import Order
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
dev_var = Variables()
dev_var.add('class_map_list.0.class_map_name', var_type='String')
dev_var.add('class_map_list.0.method', var_type='String')
dev_var.add('class_map_list.0.acl_name', var_type='String')
context = Variables.task_call(dev_var)

#get device_id from context
device_id = context['device_id'][3:]
# instantiate device object
obmf  = Order(device_id=device_id)



#get microservices instance by microservice object ID.
object_name = 'class_map'

command = 'IMPORT'
params = dict()
params[object_name] = "0"
#synchronise the given device microservice
obmf.command_call(command, 0, params) # put 0 to not update the db

class_map_list = context['class_map_list']
bad_values = dict()
good_values = dict()

if class_map_list:
  for rule in class_map_list:
    object_id     =  str(rule.get('class_map_name'))

    #LED obmf.command_objects_instances_by_id(object_name, object_id)
    response = json.loads(obmf.content)
    context.update(obmf_sync_resp=response)
    message = response.get('entity').get('message')

    if message:
        #Convert message into array
        message = json.loads(message)
        if message.get(object_name) and object_id  in message.get(object_name):
           #if response equals empty dictionary it means class map object is not exist in the device yet.
 
          MSA_API.task_error( 'Class Map with id="' + object_id + '" is already exists in the device.', context, True)
    #MSA_API.task_success('Class Map with id="' + object_id + '" does not exist in the device.', context, True)
    good_values[object_id]= 1    

if (len(good_values)):
  good_values_string =  ", ".join(good_values.keys())
else: 
  good_values_string =  ""

MSA_API.task_success('Good, Class Map with id=(' + good_values_string + ') not exist in the device. ', context, True)
