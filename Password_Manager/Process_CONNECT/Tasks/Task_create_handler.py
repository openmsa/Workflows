import time
from msa_sdk.variables import Variables
from msa_sdk.device import Device
from msa_sdk.msa_api import MSA_API
from msa_sdk.orchestration import Orchestration


if __name__ == "__main__":
  
    dev_var = Variables()
    dev_var.add('ip_addr', var_type='String')
    dev_var.add('linux_username', var_type='String')
    dev_var.add('linux_password', var_type='Password')
    dev_var.add('msa_fqdn', var_type='String')
    dev_var.add('msa_user', var_type='String')
    dev_var.add('msa_pass', var_type='Password')
    context = Variables.task_call(dev_var)
  
    Orchestration = Orchestration(context['UBIQUBEID'])
    async_update_list = (context['PROCESSINSTANCEID'],
                         context['TASKID'], context['EXECNUMBER'])

    # (1) create me
    try:
        cust_id = context["UBIQUBEID"][4:]

        entity = Device(customer_id=cust_id,
                        name=f"credentials_manager-{context['ip_addr']}",
                        manufacturer_id="14020601",
                        model_id="14020601",
                        login=context['linux_username'],
                        password=context['linux_password'],
                        password_admin=context['linux_password'],
                        management_address=context['ip_addr'])

        entity.create()
        context["entity_id"] = entity.device_id
        context['linux_password'] = ''
    except Exception as e:
        ret = MSA_API.process_content('WARNING',
                                      f'Can\'t create Entity : {str(e)} {cust_id}',
                                      context, True)
        print(ret)
        exit()

    Orchestration.update_asynchronous_task_details(*async_update_list,
                                                   f'CREDENTIALS MANAGER ENTITY CREATED...')

    time.sleep(2)
    
    # (2) activate me
    try:
        entity.activate()
    except Exception as e:
        ret = MSA_API.process_content('WARNING',
                                      f'Can\'t activate {entity.device_id} : check {str(e)}',
                                      context, True)
        print(ret)
        exit()

    Orchestration.update_asynchronous_task_details(*async_update_list,
                                                   f'CREDENTIALS MANAGER ENTITY ACTIVATED...')
    time.sleep(2)

    ret = MSA_API.process_content('ENDED', f'Credentials Handler Created.', context, True)
    print(ret)