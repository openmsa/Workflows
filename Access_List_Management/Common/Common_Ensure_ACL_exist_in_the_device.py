import json
from msa_sdk import constants
from msa_sdk.order import Order
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

dev_var = Variables()
dev_var.add('acl_name', var_type='String')
dev_var.add('acl.0.condition', var_type='String')
dev_var.add('acl.0.protocol', var_type='String')
dev_var.add('acl.0.src_address', var_type='String')
dev_var.add('acl.0.src_wildcard', var_type='String')
dev_var.add('acl.0.src_port', var_type='String')
dev_var.add('acl.0.dst_address', var_type='String')
dev_var.add('acl.0.dst_wildcard', var_type='String')
dev_var.add('acl.0.dst_port', var_type='String')
context = Variables.task_call(dev_var)

####################################################
#                                                  #
#                FUNCTIONS                         #
#                                                  #
####################################################
'''
Get parameters values from dictionary.

@param input_acl_dict:
    Input Access-list dictionary to be added or deleted.
@param device_acls_dict: 
    Access-list dictionary from device running configuration.
@return is_all_acl_entries_matched: 
    True if all the access-list entries from device running configuration are matched to the input access-list entries otherwise False.
'''
def is_input_acl_matched_to_device_acl(input_acl_dict, device_acls_dict):
    #if one of the ACL entry is not matched to the input ACL entries from the device ACL entries return False.
    is_all_acl_entries_matched = False
    #ensure that input acl variables values are available in the acl rule from the device running configuration.
    for acl in input_acl_dict:
        condition = acl.get('condition')
        protocol = acl.get('protocol')
        src_address = acl.get('src_address')
        src_wildcard = acl.get('src_wildcard')
        src_port = acl.get('src_port')
        dst_address = acl.get('dst_address')
        dst_wildcard = acl.get('dst_wildcard')
        dst_port = acl.get('dst_port')
        
        for key, device_acl  in device_acls_dict.items():   
            #case_1: 'permit tcp 192.168.1.0 255.255.255.0 eq www 10.10.10.0 255.255.255.0 neq pop3'
            if condition and protocol and src_address and src_wildcard and src_port and dst_address and dst_wildcard and dst_port:
                if condition == device_acl.get('condition') and protocol == device_acl.get('protocol') and src_address == device_acl.get('src_address') and src_wildcard == device_acl.get('src_wildcard') and src_port == device_acl.get('src_port')and dst_address == device_acl.get('dst_address') and dst_wildcard == device_acl.get('dst_wildcard') and dst_port == device_acl.get('dst_port'):
                    is_all_acl_entries_matched = True
            
            #case_2: 'permit tcp 192.168.1.0 255.255.255.0 10.10.10.0 255.255.255.0'            
            elif condition and protocol and src_address and src_wildcard and dst_address and dst_wildcard:
                if condition == device_acl.get('condition') and protocol == device_acl.get('protocol') and src_address == device_acl.get('src_address') and src_wildcard == device_acl.get('src_wildcard') and dst_address == device_acl.get('dst_address') and dst_wildcard == device_acl.get('dst_wildcard'):
                    is_all_acl_entries_matched = True
            
            #case_3: 'permit tcp host 192.168.1.24 host 10.10.10.65'
                if condition and protocol and src_address and dst_address:
                    if condition == device_acl.get('condition') and protocol == device_acl.get('protocol') and src_address == device_acl.get('src_address') and dst_address == device_acl.get('dst_address'):
                        is_all_acl_entries_matched = True
        
    return is_all_acl_entries_matched
####################################################
#                                                  #
#                MAIN CODE                         #
#                                                  #
####################################################

#get device_id from context
device_id = context['device_id'][3:]
# instantiate device object
obmf  = Order(device_id=device_id)

object_name = 'access_lists'

command = 'IMPORT'
params = dict()
params[object_name] = "0"
#synchronise the given device microservice
obmf.command_call(command, 0, params) # put 0 to not update the db

#get microservices instance by microservice object ID.
object_id = context.get('acl_name')
response = json.loads(obmf.content)
context.update(obmf_sync_resp=response)

#ensure the object inputs are in the response.
is_acl_matched = False
#ensure that all acl rules from context['acl'] dict are in response['acl']

#response={'entity': {'commandId': 0, 'status': 'OK', 'message': '{"access_lists":{"A":{"object_id":"A"},"AL_600104-6003G011":{"object_id":"AL_600104-6003G011","acl":{"10":{"index":"10","condition":"permit","protocol":"ip","any_src":"","src_address_host":"","src_address":"10.166.174.16","src_wildcard":"0.0.0.15","src_op":"","src_port":"","any_dst":"","dst_address_host":"","dst_address":"10.188.94.192","dst_wildcard":"0.0.0.15","dst_op":"","dst_port":"","opt":""},"20":{"index":"20","condition":"permit","protocol":"ip","any_src":"","src_address_host":"","src_address":"10.166.174.1","src_wildcard":"0.0.0.16","src_op":"","src_port":"","any_dst":"","dst_address_host":"","dst_address":"10.188.94.193","dst_wildcard":"0.0.0.16","dst_op":"","dst_port":"","opt":""}}},"IP-Adm-V4-Int-ACL-global":{"object_id":"IP-Adm-V4-Int-ACL-global","acl":{"10":{"index":"10","condition":"..:........
message = response.get('entity').get('message')

if message:
    #Convert message into array
    message = json.loads(message)
    if message.get(object_name) and object_id  in message.get(object_name):

        is_acl_matched = True
        #input_acl_list = context.get('acl')
        #device_acls_dict = response.get(object_name).get(object_id).get('acl')
        #is_acl_matched = is_input_acl_matched_to_device_acl(input_acl_list, device_acls_dict)

#if response equals empty dictionary it means class map object is not exist in the device yet.
if is_acl_matched != True:
    MSA_API.task_error('ACL with id="' + object_id + '" does not exist in the device.', context, True)
MSA_API.task_success('ACL with id="' + object_id + '" exists in the device.', context, True)