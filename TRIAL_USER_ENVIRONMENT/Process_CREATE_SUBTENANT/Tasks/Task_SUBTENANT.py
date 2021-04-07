import json
from msa_sdk.variables import Variables
from msa_sdk.customer import Customer
from msa_sdk.msa_api import MSA_API
from msa_sdk.lookup import Lookup

def get_customer_id(name, customer_ids):
    for item in customer_ids:
        if item["name"] == name:
           return item["id"], item["ubiId"]
    return 'NA', 'NA'

if __name__ == "__main__":

    dev_var = Variables()
    # dev_var.add('ten_prefix', var_type='String')
    dev_var.add('subtenant_name', var_type='String')
    context = Variables.task_call(dev_var)
    
    context["tenant_prefix"] = context["UBIQUBEID"][:3]

    Customer().create_customer_by_prefix(context["tenant_prefix"] ,
                                         context["subtenant_name"])
    
    search = Lookup()
    search.look_list_customer_ids()
    
    try:
        customer_ids = search.content
        customer_ids = json.loads(customer_ids)
        id_tuple = get_customer_id(context["subtenant_name"], customer_ids)
        context["subtenant_id"] = id_tuple[0]
        context["long_subtenant_id"] = id_tuple[1]
    except Exception as e:
        ret = MSA_API.process_content('WARNING',
                                      f'CAN\'T FIND CUSTOMER ID, SEE ERROR: {str(e)}',
                                      context, True)
        print(ret)
        exit()
        

    ret = MSA_API.process_content('ENDED',
                                  f'SUBTENANT CREATED. \
                                  NAME: {context["subtenant_name"]} \
                                  ID: {context["subtenant_id"]}',
                                  context, True)
    print(ret)

