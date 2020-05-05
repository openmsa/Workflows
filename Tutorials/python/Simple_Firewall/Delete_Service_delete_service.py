from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API


ret = MSA_API.process_content('ENDED', 'Firewall service deleted', context, True)
print(ret)
