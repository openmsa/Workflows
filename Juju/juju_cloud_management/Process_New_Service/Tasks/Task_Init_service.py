from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

dev_var = Variables()
dev_var.add("Juju_me_ref", var_type='Device')
dev_var.add("service_instance_name", var_type='String')
context = Variables.task_call(dev_var)


MSA_API.task_success('Service instance created.', context)

