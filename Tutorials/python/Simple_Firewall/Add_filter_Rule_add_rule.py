
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

dev_var = Variables()
dev_var.add('id', var_type='Integer')
dev_var.add('src_ip', var_type='String')
dev_var.add('dst_port', var_type='Integer')

# port code from 
# https://github.com/openmsa/Workflows/blob/master/Tutorials/php/Simple_Firewall/Add_filter_Rule_add_rule.php



ret = MSA_API.process_content('ENDED', 'port/IP blocked', context, True)
print(ret)
