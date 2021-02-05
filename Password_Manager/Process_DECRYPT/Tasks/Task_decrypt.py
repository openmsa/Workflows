import os
import time
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.orchestration import Orchestration

dev_var = Variables()
dev_var.add('enc_value', var_type='Password')
dev_var.add('key', var_type='Password')
context = Variables.task_call(dev_var)

# call os function to decrypt
def decrypt(enc_value, enc_key):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    stream = os.popen(f'{dir_path}/decrypt.sh {enc_value} {enc_key}')
    plain_text = stream.read().strip("\n")
    return plain_text
  
# call os function to encrypt value
def encrypt(plain_text, enc_key):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    stream = os.popen(f'{dir_path}/decrypt.sh {enc_value} {enc_key}')
    enc_value = stream.read().strip("\n")
    return enc_value


if __name__ == "__main__":
  
    Orchestration = Orchestration(context['UBIQUBEID'])
    async_update_list = (context['PROCESSINSTANCEID'],
                         context['TASKID'], context['EXECNUMBER'])

    password = decrypt(context['enc_value'], context['key'])
    context['enc_value'] = ''
    context['key'] = ''

    Orchestration.update_asynchronous_task_details(*async_update_list,
                                                   f'{password}')
    time.sleep(10)

    ret = MSA_API.process_content('ENDED', f'Session Expired', context, True)
    print(ret)
