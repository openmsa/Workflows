import json
import re
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.device import Device
from msa_sdk.order import Order

dev_var = Variables()

context = Variables.task_call(dev_var)

for devices in context['devices']:
	me_managementAddress = devices['ip']
	me_password = devices['password']
	me_login = devices['username']
	me_name = devices['name']
	me_manufacturerId = "17"
	me_modelId = "15102617"
	me_customerid = context['UBIQUBEID'][4:]
	
	device = Device(customer_id=me_customerid, name=me_name, manufacturer_id=me_manufacturerId,model_id=me_modelId, 
	login=me_login, password=me_password, password_admin="", management_address=me_managementAddress, management_port="22", 
	device_external="", log_enabled=True, log_more_enabled=True, mail_alerting=True, reporting=True, snmp_community='ubiqube',device_id="")

	cmd_ret=device.create()
	devices['id'] = cmd_ret.get('id')
	device.activate()

MSA_API.task_success(' Fortigate Managed Entities have been created ' , context, True)
