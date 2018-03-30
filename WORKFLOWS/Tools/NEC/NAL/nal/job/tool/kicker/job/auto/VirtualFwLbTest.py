import datetime
import json
import os
import subprocess
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../../../../job/')
from conf import config


def execute_job(command, job_input, input_file_path, output_file_path):

    ret = False

    os.environ['NAL_INPUTFILE'] = input_file_path
    os.environ['NAL_OUTPUTFILE'] = output_file_path

    with open(input_file_path, 'w') as f:
        f.write(json.dumps(job_input))

    p = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()

    print(p.returncode)
    print(out.decode('utf-8'))
    print(err.decode('utf-8'))

    if p.returncode == 0:
        with open(output_file_path, 'r') as f:
            job_output = f.read()

        print(type(job_output))
        print(job_output)

        ret = json.loads(job_output)

    return ret

#######################################################################
job_config = config.JobConfig()

IaaS_tenant_id = '1de3cf1741674a0dadd15affdb2ffae2'
IaaS_network_id = 'd6680829-59a5-484b-98c2-36c8849ec8bc'
IaaS_region_id = 'regionOne'
IaaS_segmentation_id = '10'
IaaS_network_type = 'VXLAN'
operation_id = 'naltestusr'

command_base = 'python C:/ICF_AutoCapsule_disabled/gitrepo/nal/job/job.py'
input_dir = 'C:/ICF_AutoCapsule_disabled/gitrepo/nal/job/req/'
output_dir = 'C:/ICF_AutoCapsule_disabled/gitrepo/nal/job/res/'

now_datetime = datetime.datetime.today()

fw_device_type = int(sys.argv[1])
lb_device_type = int(sys.argv[2])

################################################################################
### VirtualFwCreate
job_input = {}
job_input['type'] = job_config.TYPE_FW
job_input['device_type'] = fw_device_type
job_input['IaaS_network_id'] = IaaS_network_id
job_input['IaaS_network_type'] = IaaS_network_type
job_input['IaaS_region_id'] = IaaS_region_id
job_input['IaaS_segmentation_id'] = IaaS_segmentation_id
job_input['IaaS_tenant_id'] = IaaS_tenant_id
job_input['IaaS_tenant_name'] = 'nal_tenant_test' + now_datetime.strftime("%Y%m%d%H%M%S")
job_input['device_name'] = 'naltest_device_fw'
job_input['host_name'] = 'nalFw' + now_datetime.strftime("%Y%m%d%H%M%S")
job_input['network_name'] = 'nal_test_net' + now_datetime.strftime("%Y%m%d%H%M%S")
job_input['operation_id'] = operation_id

job_input['zabbixVIPipAddress'] = '10.0.0.1'
job_input['zabbix01ipAddress'] = '10.0.0.2'
job_input['zabbix02ipAddress'] = '10.0.0.3'
job_input['InterSecWebClientIpAddress'] = '10.0.0.4'
job_input['InterSecStaticRouteIpAddress'] = '10.0.0.5'
job_input['pavmZoneName'] = 'palozone'

job_input['admin_id'] = 'admin'
job_input['admin_pw'] = 'pass'

devicetype = str(job_input['device_type'])

# Execute JOB(tenant_id_convert_create_fw)
input_file_path = input_dir + 'tenant_id_convert_create_fw.csv'
output_file_path = output_dir + 'tenant_id_convert_create_fw.csv'
command = command_base + ' tenant_id_convert_create_fw'

job_output = execute_job(command, job_input, input_file_path, output_file_path)
if job_output == False:
    exit()

for key, val in job_output.items():
    job_input[key] = val

#
# Execute JOB(hostname_check)
input_file_path = input_dir + 'hostname_check.csv'
output_file_path = output_dir + 'hostname_check.csv'
command = command_base + ' hostname_check'

job_output = execute_job(command, job_input, input_file_path, output_file_path)
if job_output == False:
    exit()

# Execute JOB(virtual_msa_port_create)
input_file_path = input_dir + 'virtual_msa_port_create.csv'
output_file_path = output_dir + 'virtual_msa_port_create.csv'
command = command_base + ' virtual_msa_port_create'

job_output = execute_job(command, job_input, input_file_path, output_file_path)
if job_output == False:
    exit()

for key, val in job_output.items():
    job_input[key] = val

# Execute JOB(virtual_pub_port_create)
input_file_path = input_dir + 'virtual_pub_port_create.csv'
output_file_path = output_dir + 'virtual_pub_port_create.csv'
command = command_base + ' virtual_pub_port_create' + devicetype

job_output = execute_job(command, job_input, input_file_path, output_file_path)
if job_output == False:
    exit()

for key, val in job_output.items():
    job_input[key] = val

# Execute JOB(virtual_ext_port_create)
input_file_path = input_dir + 'virtual_ext_port_create.csv'
output_file_path = output_dir + 'virtual_ext_port_create.csv'
command = command_base + ' virtual_ext_port_create' + devicetype

job_output = execute_job(command, job_input, input_file_path, output_file_path)
if job_output == False:
    exit()

for key, val in job_output.items():
    job_input[key] = val

# Execute JOB(virtual_fw_tenant_vlan_port_create)
input_file_path = input_dir + 'virtual_fw_tenant_vlan_port_create.csv'
output_file_path = output_dir + 'virtual_fw_tenant_vlan_port_create.csv'
command = command_base + ' virtual_fw_tenant_vlan_port_create'

job_output = execute_job(command, job_input, input_file_path, output_file_path)
if job_output == False:
    exit()

for key, val in job_output.items():
    job_input[key] = val

# Execute JOB(virtual_fw_server_create)
input_file_path = input_dir + 'virtual_fw_server_create.csv'
output_file_path = output_dir + 'virtual_fw_server_create.csv'
command = command_base + ' virtual_fw_server_create' + devicetype

job_output = execute_job(command, job_input, input_file_path, output_file_path)
if job_output == False:
    exit()

for key, val in job_output.items():
    job_input[key] = val

# Execute JOB(virtual_fw_license_assign)
input_file_path = input_dir + 'virtual_fw_license_assign.csv'
output_file_path = output_dir + 'virtual_fw_license_assign.csv'
command = command_base + ' virtual_fw_license_assign' + devicetype

job_output = execute_job(command, job_input, input_file_path, output_file_path)
if job_output == False:
    exit()

job_input['license_key'] = job_output.get('license_key')

# Execute JOB(virtual_msa_customer_create)
input_file_path = input_dir + 'virtual_msa_customer_create.csv'
output_file_path = output_dir + 'virtual_msa_customer_create.csv'
command = command_base + ' virtual_msa_customer_create'

job_output = execute_job(command, job_input, input_file_path, output_file_path)
if job_output == False:
    exit()

# Execute JOB(virtual_msa_setup)
input_file_path = input_dir + 'virtual_msa_setup.csv'
output_file_path = output_dir + 'virtual_msa_setup.csv'
command = command_base + ' virtual_msa_setup' + devicetype

job_output = execute_job(command, job_input, input_file_path, output_file_path)
if job_output == False:
    exit()

for key, val in job_output.items():
    job_input[key] = val

# Execute JOB(virtual_device_setup)
input_file_path = input_dir + 'virtual_device_setup.csv'
output_file_path = output_dir + 'virtual_device_setup.csv'
command = command_base + ' virtual_device_setup' + devicetype

job_output = execute_job(command, job_input, input_file_path, output_file_path)
if job_output == False:
    exit()

for key, val in job_output.items():
    job_input[key] = val

# Execute JOB(get_job_return_value)
input_file_path = input_dir + 'get_job_return_value.csv'
output_file_path = output_dir + 'get_job_return_value.csv'
command = command_base + ' get_job_return_value'

job_output = execute_job(command, job_input, input_file_path, output_file_path)
if job_output == False:
    exit()

print()
print('*** Create Node Result(Firewall) ***')
print(job_output)
print()

fw_id = job_output['data']['node_id']

################################################################################
### VirtualLbCreate
job_input = {}
job_input['type'] = job_config.TYPE_LB
job_input['device_type'] = lb_device_type
job_input['IaaS_network_id'] = IaaS_network_id
job_input['IaaS_network_type'] = IaaS_network_type
job_input['IaaS_region_id'] = IaaS_region_id
job_input['IaaS_segmentation_id'] = IaaS_segmentation_id
job_input['IaaS_tenant_id'] = IaaS_tenant_id
job_input['IaaS_tenant_name'] = 'nal_tenant_test' + now_datetime.strftime("%Y%m%d%H%M%S")
job_input['device_name'] = 'naltest_device_lb'
job_input['host_name'] = 'nalLb' + now_datetime.strftime("%Y%m%d%H%M%S")
job_input['network_name'] = 'nal_test_net' + now_datetime.strftime("%Y%m%d%H%M%S")
job_input['operation_id'] = operation_id

job_input['zabbixVIPipAddress'] = '10.0.0.1'
job_input['zabbix01ipAddress'] = '10.0.0.2'
job_input['zabbix02ipAddress'] = '10.0.0.3'

devicetype = str(job_input['device_type'])

# Execute JOB(tenant_id_convert_create_lb)
input_file_path = input_dir + 'tenant_id_convert_create_lb.csv'
output_file_path = output_dir + 'tenant_id_convert_create_lb.csv'
command = command_base + ' tenant_id_convert_create_lb'

job_output = execute_job(command, job_input, input_file_path, output_file_path)
if job_output == False:
    exit()

for key, val in job_output.items():
    job_input[key] = val

# Execute JOB(hostname_check)
input_file_path = input_dir + 'hostname_check.csv'
output_file_path = output_dir + 'hostname_check.csv'
command = command_base + ' hostname_check'

job_output = execute_job(command, job_input, input_file_path, output_file_path)
if job_output == False:
    exit()

# Execute JOB(virtual_msa_port_create)
input_file_path = input_dir + 'virtual_msa_port_create.csv'
output_file_path = output_dir + 'virtual_msa_port_create.csv'
command = command_base + ' virtual_msa_port_create'

job_output = execute_job(command, job_input, input_file_path, output_file_path)
if job_output == False:
    exit()

for key, val in job_output.items():
    job_input[key] = val

# Execute JOB(virtual_lb_tenant_vlan_port_create)
input_file_path = input_dir + 'virtual_lb_tenant_vlan_port_create.csv'
output_file_path = output_dir + 'virtual_lb_tenant_vlan_port_create.csv'
command = command_base + ' virtual_lb_tenant_vlan_port_create'

job_output = execute_job(command, job_input, input_file_path, output_file_path)
if job_output == False:
    exit()

for key, val in job_output.items():
    job_input[key] = val

# Execute JOB(virtual_lb_server_create)
input_file_path = input_dir + 'virtual_lb_server_create.csv'
output_file_path = output_dir + 'virtual_lb_server_create.csv'
command = command_base + ' virtual_lb_server_create' + devicetype

job_output = execute_job(command, job_input, input_file_path, output_file_path)
if job_output == False:
    exit()

for key, val in job_output.items():
    job_input[key] = val

exit()

################################################################################
### VirtualFwDelete
job_input = {}
job_input['operation_id'] = operation_id
job_input['IaaS_region_id'] = IaaS_region_id
job_input['IaaS_tenant_id'] = IaaS_tenant_id
job_input['fw_id'] = fw_id

# Execute JOB(tenant_id_convert)
input_file_path = input_dir + 'tenant_id_convert.csv'
output_file_path = output_dir + 'tenant_id_convert.csv'
command = command_base + ' tenant_id_convert'

job_output = execute_job(command, job_input, input_file_path, output_file_path)
if job_output == False:
    exit()

for key, val in job_output.items():
    job_input[key] = val

# Execute JOB(get_vnf_info_fw)
input_file_path = input_dir + 'get_vnf_info_fw.csv'
output_file_path = output_dir + 'get_vnf_info_fw.csv'
command = command_base + ' get_vnf_info_fw'

job_output = execute_job(command, job_input, input_file_path, output_file_path)
if job_output == False:
    exit()

for key, val in job_output.items():
    job_input[key] = val

# Execute JOB(virtual_msa_port_delete)
input_file_path = input_dir + 'virtual_msa_port_delete.csv'
output_file_path = output_dir + 'virtual_msa_port_delete.csv'
command = command_base + ' virtual_msa_port_delete'

job_output = execute_job(command, job_input, input_file_path, output_file_path)
if job_output == False:
    exit()

for key, val in job_output.items():
    job_input[key] = val

# Execute JOB(virtual_pub_port_delete)
input_file_path = input_dir + 'virtual_pub_port_delete.csv'
output_file_path = output_dir + 'virtual_pub_port_delete.csv'
command = command_base + ' virtual_pub_port_delete' + devicetype

job_output = execute_job(command, job_input, input_file_path, output_file_path)
if job_output == False:
    exit()

for key, val in job_output.items():
    job_input[key] = val

# Execute JOB(virtual_ext_port_delete)
input_file_path = input_dir + 'virtual_ext_port_delete.csv'
output_file_path = output_dir + 'virtual_ext_port_delete.csv'
command = command_base + ' virtual_ext_port_delete' + devicetype

job_output = execute_job(command, job_input, input_file_path, output_file_path)
if job_output == False:
    exit()

for key, val in job_output.items():
    job_input[key] = val

# Execute JOB(virtual_tenant_vlan_port_delete)
input_file_path = input_dir + 'virtual_tenant_vlan_port_delete.csv'
output_file_path = output_dir + 'virtual_tenant_vlan_port_delete.csv'
command = command_base + ' virtual_tenant_vlan_port_delete'

job_output = execute_job(command, job_input, input_file_path, output_file_path)
if job_output == False:
    exit()

for key, val in job_output.items():
    job_input[key] = val

# Execute JOB(virtual_fw_server_delete)
input_file_path = input_dir + 'virtual_fw_server_delete.csv'
output_file_path = output_dir + 'virtual_fw_server_delete.csv'
command = command_base + ' virtual_fw_server_delete'

job_output = execute_job(command, job_input, input_file_path, output_file_path)
if job_output == False:
    exit()

# Execute JOB(virtual_fw_license_withdraw)
input_file_path = input_dir + 'virtual_fw_license_withdraw.csv'
output_file_path = output_dir + 'virtual_fw_license_withdraw.csv'
command = command_base + ' virtual_fw_license_withdraw' + devicetype

job_output = execute_job(command, job_input, input_file_path, output_file_path)
if job_output == False:
    exit()

# Execute JOB(virtual_msa_setup_delete)
input_file_path = input_dir + 'virtual_msa_setup_delete.csv'
output_file_path = output_dir + 'virtual_msa_setup_delete.csv'
command = command_base + ' virtual_msa_setup_delete'

job_output = execute_job(command, job_input, input_file_path, output_file_path)
if job_output == False:
    exit()

# Execute JOB(get_job_return_value)
input_file_path = input_dir + 'get_job_return_value.csv'
output_file_path = output_dir + 'get_job_return_value.csv'
command = command_base + ' get_job_return_value'

job_output = execute_job(command, job_input, input_file_path, output_file_path)
if job_output == False:
    exit()

print()
print('*** Delete Node Result(Firewall) ***')
print(job_output)
print()
