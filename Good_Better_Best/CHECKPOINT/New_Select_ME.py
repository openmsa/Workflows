import json
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order

dev_var = Variables()
dev_var.add('device', var_type='Device')
dev_var.add('gateway', var_type='String')
dev_var.add('ip_address', var_type='String')
dev_var.add('profile', var_type='String')

context = Variables.task_call(dev_var)

# read the ID of the selected managed entity
device_id = context['device']
object_id = context['gateway']
ip_address = context['ip_address']
profile = context['profile']

# extract the database ID
devicelongid = device_id[-3:]

# build the Microservice JSON params for the CREATE
#{"Gateway":{"undefined":{"name":"hgu001","ipv4_address":"1.1.1.1","firewall":true,"vpn":true}}}

micro_service_vars_array = {"object_id":object_id,
                            "ip_address":ip_address,
                            "firewall":"true",
                            "vpn":"true",
                            "application_control":"true",
                            "ips":"true",
                            "content_awareness":"true",
                            "url_filtering":"false",
                            "anti_virus":"false",
                            "anti_bot":"false",
                            "anti_spam":"false",
                            "threat_emulation":"false",
                            "threat_extraction":"false"
                            }

#object_id = context['id']
if profile == "better":
  micro_service_vars_array = {"object_id":object_id,
                              "ip_address":ip_address,
                            "firewall":"true",
                            "vpn":"true",
                            "application_control":"true",
                            "ips":"true",
                            "content_awareness":"true",
                            "url_filtering":"true",
                            "anti_virus":"true",
                            "anti_bot":"true",
                            "anti_spam":"true",
                            "threat_emulation":"false",
                            "threat_extraction":"false"
                            }
elif profile == "best":
  micro_service_vars_array = {"object_id":object_id,
                              "ip_address":ip_address,
                            "firewall":"true",
                            "vpn":"true",
                            "application_control":"true",
                            "ips":"true",
                            "content_awareness":"true",
                            "url_filtering":"true",
                            "anti_virus":"true",
                            "anti_bot":"true",
                            "anti_spam":"true",
                            "threat_emulation":"true",
                            "threat_extraction":"true"
                            }
gateway = {"Gateway": {object_id: micro_service_vars_array}}

# call the CREATE for simple_firewall MS for each device
order = Order(devicelongid)
order.command_execute('CREATE', gateway)

# convert dict object into json
content = json.loads(order.content)

# check if the response is OK
if order.response.ok:
#    ret = MSA_API.process_content('ENDED',
#                                  f'STATUS: {content["status"]}, \
#                                    MESSAGE: {content["message"]}',
#                                  context, True)
    ret = MSA_API.process_content('ENDED',
                                  f'STATUS: {content["status"]}, \
                                    MESSAGE: Gateway {object_id}',
                                  context, True)
else:
    ret = MSA_API.process_content('FAILED',
                                  f'Gateway Creation failed \
                                  - {order.content}',
                                  context, True)

print(ret)
