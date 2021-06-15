import json
from msa_sdk import constants
from msa_sdk.order import Order
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

dev_var = Variables()


dev_var.add('static_routing.0.source_address', var_type='IPAddress')
dev_var.add('static_routing.0.subnet_mask',    var_type='IPMask')
dev_var.add('static_routing.0.vlan_id',        var_type='Interger')
dev_var.add('static_routing.0.nexthop',        var_type='IPAddress')
dev_var.add('static_routing.0.distance',       var_type='Interger')
context = Variables.task_call(dev_var)

#get device_id from context
device_id = context['device_id'][3:]
# instantiate device object
obmf  = Order(device_id=device_id)
#synchronise device microservices
timeout = 300
obmf.command_synchronize(timeout)

static_routing = context['static_routing']
bad_values = dict()
good_values = dict()
object_name = 'static_route'

if static_routing:
  for rule in static_routing:
    #get microservices instance by microservice object ID.
    object_id = rule.get('source_address')
    src_mask  = rule.get('subnet_mask')
    vlan_id   = rule.get('vlan_id')
    next_hop  = rule.get('nexthop')
    distance  = rule.get('distance')

    obmf.command_objects_instances_by_id(object_name, object_id)
    response = json.loads(obmf.content)
    context.update(obmf_sync_resp=response)

    #ensure the object inputs are in the response.
    is_static_route_matched = False
    obj_id = object_id.replace('.', "_")
    if response:
        if obj_id in response.get(object_name): 
            sr = response.get(object_name).get(obj_id)
            ret_static_route_ip = sr.get('object_id')
            ret_static_route_mask = sr.get('mask')
            ret_static_route_vlan_id = sr.get('vlan_id')
            ret_static_route_next_hop = sr.get('next_hop')
            ret_static_route_distance = sr.get('distance')
            if distance == '1' and ret_static_route_distance == 'null':
                # Set the default 'Distance' value in th Catalyst ME.
                ret_static_route_distance = '1'
            if object_id == ret_static_route_ip and src_mask == ret_static_route_mask and vlan_id == ret_static_route_vlan_id and next_hop == ret_static_route_next_hop and distance == ret_static_route_distance:
                is_static_route_matched = True

    #if response equals empty dictionary it means StaticRouting object is not exist in the device yet.
    if is_static_route_matched != False:
        MSA_API.task_error('Static Routing with id="' + obj_id + '" exists in the device.', context, True)
    good_values[obj_id]= 1    
    #MSA_API.task_success('Static Routing with id="' + obj_id + '" does not exist in the device.', context, True)
            

if (len(good_values)):
  good_values_string =  ", ".join(good_values.keys())
else: 
  good_values_string =  ""

MSA_API.task_success('Static Routing (' + good_values_string + ') does not exist in the device.', context, True)