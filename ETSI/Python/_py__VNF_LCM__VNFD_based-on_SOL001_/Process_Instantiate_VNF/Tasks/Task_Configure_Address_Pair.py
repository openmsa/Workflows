'''
Visit http://[YOUR_MSA_URL]/msa_sdk/ to see what you can import.
'''
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
import requests
import openstack

from custom.ETSI.NfviVim import NfviVim
from custom.ETSI.VnfLcmSol003 import VnfLcmSol003
from custom.ETSI.VnfPkgSol005 import VnfPkgSol005
'''
List all the parameters required by the task

You can use var_name convention for your variables
They will display automaticaly as "Var Name"
The allowed types are:
  'String', 'Boolean', 'Integer', 'Password', 'IpAddress',
  'IpMask', 'Ipv6Address', 'Composite', 'OBMFRef', 'Device'

 Add as many variables as needed
'''
dev_var = Variables()
context = Variables.task_call(dev_var)

process_id = context['SERVICEINSTANCEID']

if "is_third_party_vnfm" in context:
	is_third_party_vnfm = context.get('is_third_party_vnfm')
	if is_third_party_vnfm == 'true':
		MSA_API.task_success('Skip for 3rd party VNFM.', context)

vnfLcm = VnfLcmSol003(context["mano_ip"], context["mano_port"], context['mano_base_url'])
vnfLcm.set_parameters(context['mano_user'], context['mano_pass'])

r = vnfLcm.vnf_lcm_get_vnf_instance_details(context["vnf_instance_id"])

vnfResourcesList = r.json()["instantiatedVnfInfo"]["vnfcResourceInfo"]
context["vnfResourceId"] = vnfResourcesList[0]["computeResource"]["resourceId"]
server_id=context["vnfResourceId"]
#vnfName = context['vnf_instance_name']
#MSA_API.task_success('Got VNF server Id', context, True)

conn = openstack.connection.Connection(region_name='RegionOne', auth=dict(auth_url='https://10.12.43.250:5000', username='admin', password='aish4Eivai4monei', project_id='4cfb66cfcc134ed887256260387d2d27', user_domain_id='51383b70017f4eddbff1265df3daf5f3'), compute_api_version='2', identity_interface='public', verify=False)
access_token=conn.authorize()

session = requests.Session()
session.headers.update({'X-Auth-Token': access_token})


ifs=conn.compute.server_interfaces(server_id)
vwaf_usr_seg_port=''
vwaf_virt_port=''
vwaf_mac=''
for ifa in ifs:
	if ifa.net_id == '0559809f-c415-46c6-9b87-3d87cefa8224':
		vwaf_usr_seg_port=ifa.port_id
	elif ifa.net_id == '3f2dde54-70c1-41cc-b1c6-f651199d71b0':
		vwaf_virt_port=ifa.port_id
		vwaf_mac=ifa.mac_addr
		
serv = conn.compute.get_server(server_id)
img=serv.image.id
img_name=conn.image.get_image(img).name

if "vsrx" in img_name.lower():
	#vSRX VNF for Tenant1-UserSegment-vWAF network
	url='http://10.12.41.201:8082/virtual-machine-interface/' + vwaf_usr_seg_port
	body={  "virtual-machine-interface": {
		"virtual_machine_interface_allowed_address_pairs": {
	      "allowed_address_pair": [
		{
		  "ip": {
		    "ip_prefix": "10.12.66.68",
		    "ip_prefix_len": 32
		  },
		  "mac": "00:00:5e:00:01:01",
		  "address_mode": "active-standby"
		}
	      ]
	    }
	  }
	}
	session.put(url, data=body)

	#vSRX VNF for Tenant1-VirtualServer-vWAF network
	url='http://10.12.41.201:8082/virtual-machine-interface/' + vwaf_virt_port
	body={
	  "virtual-machine-interface": {
		"virtual_machine_interface_allowed_address_pairs": {
	      "allowed_address_pair": [
		{
		  "ip": {
		    "ip_prefix": "10.12.66.35",
		    "ip_prefix_len": 32
		  },
		  "mac": "00:00:5e:00:01:02",
		  "address_mode": "active-standby"
		}
	      ]
	    }
	  }
	}
	session.put(url, data=body)
elif "vwaf" in img_name.lower():
		#vwaf VNF  for Tenant1-VirtualServer-vWAF network
	url='http://10.12.41.201:8082/virtual-machine-interface/' + vwaf_virt_port
	body={
	  "virtual-machine-interface": {
		"virtual_machine_interface_allowed_address_pairs": {
	      "allowed_address_pair": [
		{
		  "ip": {
		    "ip_prefix": "10.12.66.51",
		    "ip_prefix_len": 32
		  },
		  "mac": vwaf_mac,
		  "address_mode": "active-active"
		}
	      ]
	    }
	  }
	}
	session.put(url, data=body)

	#vwaf VNF  for Tenant1-VirtualServer-vWAF network
	url='http://10.12.41.201:8082/virtual-machine-interface/' + vwaf_virt_port
	body={
	  "virtual-machine-interface": {
		"virtual_machine_interface_allowed_address_pairs": {
	      "allowed_address_pair": [
		{
		  "ip": {
		    "ip_prefix": "10.12.66.52",
		    "ip_prefix_len": 32
		  },
		  "mac": vwaf_mac,
		  "address_mode": "active-active"
		}
	      ]
	    }
	  }
	}
	session.put(url, data=body)


ret = MSA_API.process_content('ENDED', 'Task OK', context, True)
print(ret)

