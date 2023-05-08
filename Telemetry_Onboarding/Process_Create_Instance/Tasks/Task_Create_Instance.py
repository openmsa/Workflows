from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

if __name__ == "__main__":
    dev_var = Variables()
    dev_var.add('kibana_username', var_type='String')
    dev_var.add('kibana_password', var_type='String')
    dev_var.add('kibana_index_id', var_type='String')
    dev_var.add('kibana_index_name', var_type='String')
    
    context = Variables.task_call(dev_var)
    
    context["kibana_index_name"] = context["kibana_index_id"]
    
    ret = MSA_API.process_content('ENDED', 'Instance created', context, True)
    print(ret)
