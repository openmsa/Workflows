import json
from msa_sdk.variables import Variables
from msa_sdk.order import Order

# List all the parameters required by the task
dev_var = Variables()
dev_var.add('src_ip', var_type='String')
dev_var.add('dst_port', var_type='Integer')
context = Variables.task_call(dev_var)

# read the ID of the selected managed entity
device_id = context['device']
# extract the database ID
devicelongid = device_id[-3:]

# build the Microservice JSON params for the CREATE
micro_service_vars_array = {
                            "playbook_path": "/opt/playbooks/createFW.yml",
                            "extra_vars": "\"dport="+context['dst_port']+" ip="+context['src_ip']+"\""}

playbook = {"AnsiblePlaybook": {"":micro_service_vars_array}}

# call the CREATE for simple_firewall MS for each device
order = Order(devicelongid)
order.command_execute('CREATE', playbook)



# convert dict object into json
content = json.loads(order.content)
order.command_synchronize(10)
# check if the response is OK
print(order.process_content('ENDED',
                                  f'STATUS: {content["status"]}, \
                                    MESSAGE: {content["message"]}',
                                  context, True))
