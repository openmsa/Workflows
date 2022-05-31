import json
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order

# List all the parameters required by the task
dev_var = Variables()
dev_var.add('device_id', var_type='Device')
dev_var.add('Name', var_type='String')
dev_var.add('object_id', var_type='String')
dev_var.add('State', var_type='String')
dev_var.add('PublicDnsName', var_type='String')
dev_var.add('private_ip', var_type='String')
dev_var.add('keyPair', var_type='String')
dev_var.add('imageId', var_type='String')

context = Variables.task_call(dev_var)

# read the ID of the selected managed entity
device_id = context['device_id']

# extract the database ID
devicelongid = device_id[3:]

# build the Microservice JSON params
#{"Gateway":"0"}
#micro_service_vars_array = {"object_id":object_id}
object_parameters = {}

object_parameters['vm'] = {}
object_parameters['vm']['test']= {}
object_parameters['vm']['test']['Name']= context['Name']
object_parameters['vm']['test']['imageId']= context['imageId']



# call the CREATE for the specified MS for each device
order = Order(devicelongid)
order.command_execute('CREATE', object_parameters)

# convert dict object into json
content = json.loads(order.content)

context['ResourceId']=''
context['create_result']=content
if content.get('message'):
    content_message=json.loads(content['message'])
    if content_message.get('Vms'):
        if content_message.get('Vms').get('row'):
            context['create_result_row']=content_message['Vms']['row']
            if content_message.get('Vms').get('row').get('VmId'):
                context['ResourceId']=content_message['Vms']['row']['VmId']

# check if the response is OK
if order.response.ok:
    ret = MSA_API.process_content('ENDED',
                                  f'STATUS: {content["status"]}, \
                                    MESSAGE: successfull',
                                  context, True)
else:
    ret = MSA_API.process_content('FAILED',
                                  f'Import failed \
                                  - {order.content}',
                                  context, True)


print(ret)

