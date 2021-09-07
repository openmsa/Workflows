import json
from msa_sdk import constants
from msa_sdk.order import Order
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

dev_var = Variables()
dev_var.add('static_routing.0.source_address', var_type='IPAddress')
dev_var.add('static_routing.0.subnet_mask',    var_type='IPMask')
dev_var.add('static_routing.0.vlan_id',        var_type='String')
dev_var.add('static_routing.0.nexthop',        var_type='IPAddress')
dev_var.add('static_routing.0.distance',       var_type='Interger')
context = Variables.task_call(dev_var)
 
#get device_id from context
device_id = context['device_id'][3:]
# instantiate device object
obmf  = Order(device_id=device_id)

static_routing = context['static_routing']
good_values = []
object_name = 'static_route'

command = 'IMPORT'
params = dict()
params[object_name] = "0"
#Import the given device microservice from the device, the MS values in the UI will be not updated
obmf.command_call(command, 0, params)   

if static_routing:
  response = json.loads(obmf.content)
  context.update(obmf_sync_resp=response)

  device_static_routes= []
  #load all existing static route on the device
  if 'entity' in response and 'message' in response.get('entity'):
    message = response.get('entity').get('message')
  else:
    message = ''; 
  if message:
    #Convert message into array
    message = json.loads(message) 
    # "message": "{"static_route":{"16af293452008658e4a6a26994caa813":{"source_address":"10.100.100.32","mask":"255.255.255.255","vlan_id":"GigabitEthernet2","next_hop":"10.166.129.14","distance":null},"5e610ef59deda1f418b2939563101c1a":{"source_address":"10.100.100.33","mask":"255.255.255.255","vlan_id":"GigabitEthernet2","next_hop":"10.166.129.14","distance":null},"625507266441f7a5b5c261278e7a1a9a":{"source_address":"10.100.100.34","mask":"255.255.255.255","vlan_id":"GigabitEthernet2","next_hop":"10.166.129.14","distance":null},"8f692c4a11a97093aded03b0182a73de":{"source_address":"10.100.100.35","mask":"255.255.255.255","vlan_id":"GigabitEthernet2
    if message.get(object_name).values():
      for rule in message.get(object_name).values():
        device_rule = dict();
        device_rule['static_route_ip']        = rule.get('source_address')
        device_rule['static_route_mask']      = rule.get('mask')
        device_rule['static_route_vlan_id']   = rule.get('vlan_id')
        device_rule['static_route_next_ho']   = rule.get('next_hop')
        if rule.get('distance') and rule.get('distance') != "null":
          device_rule['static_route_distance'] = rule.get('distance')
        else:
          # Set the default 'Distance' value in the Catalyst ME.
          device_rule['static_route_distance']  = '1'

        device_static_routes.append(device_rule)
 
  for rule in static_routing:
    #rule: {"distance": "",  "flag": "DEL",  "nexthop": "10.166.239.14",  "source_address": "10.166.156.128", "subnet_mask": "255.255.255.224",  "vlan_id": "GigabitEthernet2"}, {"distance": "","flag": "DEL","nexthop": "10.166.239.14","source_address": "10.166.174.16","subnet_mask": "255.255.255.240", "vlan_id": "GigabitEthernet2"}
    source_address = rule.get('source_address')
    src_mask  = rule.get('subnet_mask')
    vlan_id   = rule.get('vlan_id')
    next_hop  = rule.get('nexthop')
    distance  = rule.get('distance')
   
    #ensure the object inputs are in the response.
    is_static_route_matched = False
 
    # Loop on all static routes on the device
    for device_rule in device_static_routes:
      ret_static_route_ip       = device_rule['static_route_ip']
      ret_static_route_mask     = device_rule['static_route_mask'] 
      ret_static_route_vlan_id  = device_rule['static_route_vlan_id']
      ret_static_route_next_hop = device_rule['static_route_next_ho'] 
      ret_static_route_distance = device_rule['static_route_distance']
      if distance is None or distance == '' or distance == None:
        distance = '1'
      if source_address == ret_static_route_ip and src_mask == ret_static_route_mask and vlan_id == ret_static_route_vlan_id and next_hop == ret_static_route_next_hop and distance == ret_static_route_distance:
        is_static_route_matched = True
        break    # break here
    if is_static_route_matched != False:
      wanted = 'source_address=' + str(source_address) +'|mask= ' + str(src_mask) +'|vlan_id=' + str(vlan_id) + '|next_hop=' + str(next_hop) +'|distance='+ str(distance)
      MSA_API.task_error('Static Routing with ('+wanted+'), was found on device' , context, True)

    good_values.append('src= '+str(source_address) +'|mask= ' + str(src_mask) +'|vlan_id=' + str(vlan_id)+'...')    

if (len(good_values)):
  if (len(good_values) <10):
    good_values_string =  ", ".join(good_values)
  else:
    good_values_string =  "to many to display..."
else: 
  good_values_string =  ""

MSA_API.task_success('Static Routing (' + good_values_string + ') does not exist in the device.', context, True)
