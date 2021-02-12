import os
import time
import json
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order

dev_var = Variables()
dev_var.add('key_name', var_type='String')
dev_var.add('plain_text_value', var_type='Password')
dev_var.add('key_description', var_type='String')
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
    stream = os.popen(f'{dir_path}/encrypt.sh {plain_text} {enc_key}')
    enc_value = stream.read().strip("\n")
    return enc_value


if __name__ == "__main__":
  
    enc_value = encrypt(context['plain_text_value'], context['key'])
    context['plain_text_value'] = ''
    context['key'] = ''
    
    order = Order(context["entity_id"])
    order.command_synchronize(timeout=60)
  
    # get next key id
    credentials_ms = {'credentials_ms': {'':{'object_id': ''}}}
    order.command_execute('IMPORT', credentials_ms)
    data = json.loads(order.content)
    message = json.loads(data['message'])
    if "credentials_ms" in message.keys():
        oid = len(message['credentials_ms']) + 1
    else:
        oid = 1
    
    # save new item
    credentials_ms = {'credentials_ms': {str(oid):{'object_id': str(oid),
                                                   'key_name': context["key_name"],
                                                   'key_value': enc_value,
                                                   'key_description': context["key_description"]
                                                  }
                                        }
                     }
    order.command_execute('CREATE', credentials_ms)

    ret = MSA_API.process_content('ENDED', f'Credentials storage updated', context, True)
    print(ret)
