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
dev_var.add('nsd_name', var_type='String')
dev_var.add('nsd_contents', var_type='String')
dev_var.add('nsd_csar_file', var_type='String')
context = Variables.task_call(dev_var)

def zipdir(path, ziph):
    # ziph is zipfile handle
    rootlen = len(path) + 1
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = join(root, file)
            ziph.write(file_path, file_path[rootlen:])

if __name__ == '__main__':
    #get uuid from context.
    uuid_gen = context.get('uuid_gen')

    nsd_name = uuid_gen
    if 'nsd_name' in context:
        name = context.get('nsd_name')
        if name:
            nsd_name = name + '_' + uuid_gen

    nsd_directory_tobuild = '/opt/fmc_repository/Datafiles/NFV/NSD/' + nsd_name

    #Archive NSD_Directory as CSAR
    zipf = zipfile.ZipFile(nsd_directory_tobuild + '.csar', 'w', zipfile.ZIP_DEFLATED)
    zipdir(nsd_directory_tobuild, zipf)
    zipf.close()
    
    #Add NSD TOSCA file (csar) path in the context and display in the GUI.
    nsd_csar_file = nsd_directory_tobuild + '.csar'
    context.update(nsd_csar_file=nsd_csar_file)
    
    #Delete nsd_directory tmp
    shutil.rmtree(nsd_directory_tobuild)

    MSA_API.task_success('NSD TOSCA Sol001 meta was created successfully.', context, True)