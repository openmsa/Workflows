import glob
import fnmatch
import os
import json
import os.path as osp
from msa_sdk import constants
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

dev_var = Variables()
dev_var.add('yangs_directory', var_type='String')
dev_var.add('yangs_extension', var_type='String')
dev_var.add('yang_list.0.yang', var_type='String')
dev_var.add('yang_list.0.is_selected', var_type='Boolean')


context = Variables.task_call(dev_var)

####################################################
#                                                  #
#                FUNCTIONS                         #
#                                                  #
####################################################


####################################################
#                                                  #
#                MAIN CODE                         #
#                                                  #
####################################################

#Constant variables

'''
List yang files from repository.
'''
yangs_directory = context['yangs_directory']
yangs_extension = context['yangs_extension']

if not yangs_directory:
    yangs_directory = '/opt/fmc_repository/Datafiles/GWAN_RAB'
  
if not yangs_extension:
    yangs_extension = '.yang'

#list the yang files from specified directory recursivly in the MSA repositary data.  
yang_list = []
for root, dirnames, filenames in os.walk(yangs_directory):
  for filename in fnmatch.filter(filenames, '*'+yangs_extension):
    root_simple=root.replace(yangs_directory,'') 
    root_simple=root_simple.replace('/','',1) 
    yang_list.append(os.path.join(root_simple, filename))

# check if at least one yang file is available. If not exit and return failed.
if not yang_list:
    ret = MSA_API.process_content(constants.FAILED, 'No Yang files found from \'' + yangs_directory + '\' directory. with extension \'' + yangs_extension +'\'', context, True)
    print(ret)	

yang_list_restructured = [dict(yang=st, is_selected='false') for st in yang_list]
#store in the context 'yang_list'
context['yang_list'] = yang_list_restructured

ret = MSA_API.process_content(constants.ENDED, 'yang list acquisition is done successfully.', context, True)
print(ret)

