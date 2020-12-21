from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

dev_var = Variables()
# Global
dev_var.add('tenant_id', var_type='String')
dev_var.add('client_id', var_type='String')
dev_var.add('client_secret', var_type='Password')
dev_var.add('subscription_id', var_type='String')
dev_var.add('resource_group', var_type='String')
dev_var.add('location', var_type='String')
# Security Group
dev_var.add('sec_gr_name', var_type='String')
dev_var.add('rule_name', var_type='String')
dev_var.add('priority', var_type='String')
dev_var.add('permit_ip_addr', var_type='String')
dev_var.add('permit_proto', var_type='String')
dev_var.add('permit_port', var_type='String')
# Virtual Network
dev_var.add('virt_net_name', var_type='String')
dev_var.add('virt_net_ip_prefix', var_type='String')
# Subnet
dev_var.add('subnet_name', var_type='String')
dev_var.add('subnet_ip_prefix', var_type='String')
# Public IP
dev_var.add('public_ip_name', var_type='String')
dev_var.add('vm_label', var_type='String')
# NIC
dev_var.add('net_iface_name', var_type='String')
# VM
dev_var.add('vm_name', var_type='String')
dev_var.add('vmSize', var_type='String')
dev_var.add('sku', var_type='String')
dev_var.add('offer', var_type='String')
dev_var.add('publisher', var_type='String')
dev_var.add('version', var_type='String')
dev_var.add('vm_username', var_type='String')
dev_var.add('vm_secret', var_type='Password')
dev_var.add('vm_qty', var_type='Integer')
dev_var.add('master_qty', var_type='Integer')
# MSA
dev_var.add('msa_fqdn', var_type='String')
dev_var.add('msa_user', var_type='String')
dev_var.add('msa_pass', var_type='Password')
dev_var.add('dpl_k8s', var_type='String')
dev_var.add('dpl_linux', var_type='String')
# Jira
dev_var.add('jira_fqdn', var_type='String')
dev_var.add('jira_user', var_type='String')
dev_var.add('jira_project_id', var_type='String')
dev_var.add('jira_pass', var_type='Password')


context = Variables.task_call(dev_var)

context['wf_name'] = 'AZURE K8S LCM'

ret = MSA_API.process_content('ENDED', f'DATA RETRIEVED. WORKFLOW INSTANCE CREATED.', context, True)
print(ret)