from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.orchestration import Orchestration
import json


#Define variables
dev_var = Variables()
dev_var.add('var_value', var_type='String')
context = Variables.task_call(dev_var)

#Get sub-tenant ID
OrchestrationObject = Orchestration(context['UBIQUBEID'])

#active_workflow contains workflow instances what ARE NOT in ARCHIVED state
active_workflow = dict()

#matched_workflow contains workflow details where requested valued matched
matched_workflow = dict()

#Retrive all workflow instanes of particular sub-tenant
OrchestrationObject.list_service_instances()

#Walk through the instances and add to list non archived ones
for service in json.loads(OrchestrationObject.content):
  if service['state'] != 'ARCHIVED' and str(service['id']) != str(context['service_id']):
    if service['name'] not in active_workflow:
      active_workflow[service['name']] = list()
    active_workflow[service['name']].append({'id': service['id'], 'state': service['state']})

    
#Walk through non archived instances and check value among its variables
for workflow, details in active_workflow.items():
  for instance in details:
    OrchestrationObject.get_service_variables(instance['id'])
    for var in json.loads(OrchestrationObject.content):
      if var['value'] == context['var_value']:
        if workflow not in matched_workflow:
          matched_workflow[workflow] = dict()
        if instance['id'] not in matched_workflow[workflow]:
          matched_workflow[workflow][instance['id']] = {'state': instance['state'], 			  											'variable_list': list()}
        matched_workflow[workflow][instance['id']]['variable_list'].append(var)

#Create context variable to show in GUI
context['matched'] = list()

#Finish successfully if at least one WF was found, show warning else
if not len(matched_workflow):
  ret = MSA_API.process_content('WARNING', 'There is no workflow with requested value', context, True)
else:
  for workflow, details in matched_workflow.items():
    for instance, vars in details.items():
      for var in vars['variable_list']:
        context['matched'].append({'workflow_name': workflow,
                                   'instance_id': instance,
                                   'variable_name': var['name'],
                                   'variable_value': var['value'],
                                   'variable_comment': var['comment']
        						   })
  ret = MSA_API.process_content('ENDED', 'There are {} workflows what contain requested value'.format(len(matched_workflow)), context, True)
print(ret)

