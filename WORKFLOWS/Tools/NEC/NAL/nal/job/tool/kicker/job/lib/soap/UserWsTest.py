import os
import sys
import traceback

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../../../../../job/')
from conf import config
from lib.soap.msa import userws


customer_name = 'cm_nma001'
customer_id = 'cm001'

try:
    client = userws.UserWs(config.JobConfig())

    # create_customer
    print('create_customer')
    output = client.create_customer(customer_name)
    print(type(output))
    print(output)
    print()

    # delete_customer_by_id
    print('delete_customer_by_id')
    msa_params = {}
    output = client.delete_customer_by_id(customer_id)
    print(type(output))
    print(output)

except:
    print('NG')
    print(traceback.format_exc())
