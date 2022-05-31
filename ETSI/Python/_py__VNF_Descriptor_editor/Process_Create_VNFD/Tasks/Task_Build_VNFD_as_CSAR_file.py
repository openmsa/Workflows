import uuid
import os
import zipfile
import shutil
from os.path import join
from msa_sdk import constants
from msa_sdk.order import Order
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

dev_var = Variables()
dev_var.add('vnfd_name', var_type='String')
dev_var.add('vnfd_contents', var_type='String')
dev_var.add('vnfd_csar_file', var_type='String')
dev_var.add('service_instance_name', var_type='String')
context = Variables.task_call(dev_var)

def zipdir(path, ziph):
    # ziph is zipfile handle
    rootlen = len(path) + 1
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = join(root, file)
            ziph.write(file_path, file_path[rootlen:])
            
if __name__ == '__main__':
    #get 'vnfd_name' from context.
    vnfd_name = context.get('vnfd_name_uuid')
    vnfd_directory_tobuild = '/opt/fmc_repository/Datafiles/NFV/VNFD/' + vnfd_name

    #Archive VNFD_Directory as CSAR
    zipf = zipfile.ZipFile(vnfd_directory_tobuild + '.csar', 'w', zipfile.ZIP_DEFLATED)
    zipdir(vnfd_directory_tobuild, zipf)
    zipf.close()
    
    #Add NSD TOSCA file (csar) path in the context and display in the GUI.
    vnfd_csar_file = vnfd_directory_tobuild + '.csar'
    context.update(vnfd_csar_file=vnfd_csar_file)
    
    #Delete nsd_directory tmp
    shutil.rmtree(vnfd_directory_tobuild)
    
    #Set service_instance_name.
    service_instance_name = context.get('SERVICEINSTANCEID') + '_' + vnfd_name
    context.update(service_instance_name=service_instance_name)

    MSA_API.task_success('VNFD TOSCA Sol001 meta was created successfully.', context, True)