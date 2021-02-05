from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

dev_var = Variables()
dev_var.add('device', var_type='Device')
context = Variables.task_call(dev_var)


if __name__ == "__main__":

    # create me
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
    except Exception as e:
        ret = MSA_API.process_content('WARNING',
                                      f'Can\'t create Entity : {str(e)} {cust_id}',
                                      context, True)
        print(ret)
        exit()

    Orchestration.update_asynchronous_task_details(*async_update_list,
                                                   f'CREDENTIALS MANAGER ENTITY CREATED...')

    time.sleep(2)
    
    # assign dpl and ms
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