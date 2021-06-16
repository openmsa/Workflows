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
#synchronise device microservices
timeout = 300
obmf.command_synchronize(timeout)

#get microservices instance by microservice object ID.
object_name = 'class_map'

class_map_list = context['class_map_list']
bad_values = dict()
good_values = dict()

if class_map_list:
  for rule in class_map_list:
    object_id     =  str(rule.get('class_map_name'))

    obmf.command_objects_instances_by_id(object_name, object_id)
    response = json.loads(obmf.content)
    context.update(obmf_sync_resp=response)

    #ensure the object inputs are in the response.
    is_class_map_name = False
    ret_acl_name = ''
    if response:
        if object_id in response.get(object_name):
            is_class_map_name = True
            class_map_obj = response.get(object_name).get(object_id)
            if 'access' in class_map_obj:
                if 'acl' in class_map_obj.get('access').get('0'):
                    ret_acl_name = class_map_obj.get('access').get('0').get('acl')
                    context.update(ret_acl_name=ret_acl_name)
    #if response equals empty dictionary it means class map object is not exist in the device yet.
    if not ret_acl_name or is_class_map_name != True:
        MSA_API.task_error( 'Class Map with id="' + object_id + '" does not exist or is not associated with ACL "' + context.get('acl') + '".', context, True)
    #MSA_API.task_success('Class Map with id="' + object_id + '" exists and is associated with ACL "' + ret_acl_name + '".', context, True)
    good_values[object_id]= 1    

if (len(good_values)):
  good_values_string =  ", ".join(good_values.keys())
else: 
  good_values_string =  ""

MSA_API.task_success('Good, Class Map with id=(' + good_values_string + ') exists ', context, True)
