from msa_sdk.variables import Variables
from msa_sdk.customer import Customer
from msa_sdk.msa_api import MSA_API

if __name__ == "__main__":
  
    dev_var = Variables()
    context = Variables.task_call()

    Customer().delete_customer_by_id(context["subtenant_id"])

    ret = MSA_API.process_content('ENDED',
                                  f'SUBTENANT DELETED. \
                                  NAME: {context["subtenant_name"]} \
                                  ID: {context["subtenant_id"]}',
                                  context, True)
    print(ret)