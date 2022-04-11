import json
import time
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.device import Device
from msa_sdk.customer import Customer
from msa_sdk import constants
import openstack
import re

from custom.ETSI.NfviVim import NfviVim
from custom.ETSI.VnfLcmSol003 import VnfLcmSol003
from custom.ETSI.VnfPkgSol005 import VnfPkgSol005

dev_var = Variables()
context = Variables.task_call(dev_var)

subtenant_ext_ref = context['UBIQUBEID']
vnf_service_instance_ref = context.get('SERVICEINSTANCEREFERENCE')

if __name__ == "__main__":
	
	if "is_third_party_vnfm" in context:
		is_third_party_vnfm = context.get('is_third_party_vnfm')
		if is_third_party_vnfm == 'true':
			MSA_API.task_success('Skip for 3rd party VNFM.', context)
	
	#Get VIM infos.
	auth_url = context.get('auth_url')
	password = context.get('password')
	project_id = context.get('project_id')
	user_domain_id = context.get('domain_id')
	domain_id_var_conf_attr = context.get('domain_id_var_conf_attr')
	
	customer_id = subtenant_ext_ref[4:]
	
	ip_pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
	auth_url_ip = ip_pattern.search(auth_url)[0]
	
	# Create a Subtenant object
	customer = Customer()
	
	#Get Subtenant Managed Enties list.
	customer_ME_list = customer.get_device_list_by_id(customer_id)
	
	vim_me_id = ""
	
	for device_id in customer_ME_list:
		meObject = Device(customer_id = customer_id, device_id = device_id)
		meObject.read()
		if ((meObject.management_address == auth_url_ip) and (meObject.password == password) and (meObject.get_configuration_variable("TENANT_ID").get("value") == project_id) and (meObject.get_configuration_variable(domain_id_var_conf_attr).get("value") == user_domain_id)):
			vim_me_id = meObject.device_id
			context['vim_device'] = subtenant_ext_ref[:3] + str(vim_me_id)
			break
	
	if vim_me_id:
		MSA_API.task_success('Resolved VIM managed entity id.', context)
	else:
		MSA_API.task_error('Unable to resolve VIM managed entiy id ' + auth_url_ip, context)