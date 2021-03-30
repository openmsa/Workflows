import copy
import glob
import json
import subprocess

import numpy as np
from re import search
from msa_sdk import constants
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

dev_var = Variables()
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

# Check multiple or missing yang file selection.
selected_number = 0
yang_list_json= json.dumps(context['yang_list'])
yang_list = json.loads(yang_list_json)

if yang_list:
    for st in yang_list:
        if st.get('is_selected') == True:
            selected_number += 1
else:
  ret = MSA_API.process_content(constants.FAILED, 'yang list is empty.', context, True)
  print(ret)
   
# Retrieve selected yang_filename from the list.
yang_filename = ''
yang_filenames = []

for st in yang_list:
   # "yang_list": [ {  "yang": "/opt/fmc_repository/Datafiles/YANG/example-1.yang", "is_selected": "false" },
                   # { "yang": "/opt/fmc_repository/Datafiles/YANG/example-2.yang", "is_selected": "false"  } ]
  if st.get('is_selected') == True:
    if st.get('yang'):
      #yang_filename = context.get('yangs_directory') + '/' + st.get('yang')
      yang_filename = context.get('yangs_directory') + '/' + st.get('yang')
      yang_filenames.append(yang_filename)

    else:
      ret = MSA_API.process_content(constants.FAILED, 'Selected yang filename is empty from the service instance context.', context, True)
      print(ret)

context['yang_filenames'] = yang_filenames

if selected_number ==0:
  ret = MSA_API.process_content(constants.FAILED, 'No yang file selected', context, True)

output_file =  yang_filename.replace(context['yangs_extension'],'') + '_output.xml'
context['output_file'] = output_file

#Run pyang on all files together
# pyang -f sample-xml-skeleton --sample-xml-skeleton-doctype=config -o generated_conf.xml oneos-staticroute.yang dependency/oneos-common.yang dependency/oneos-glob.yang dependency/oneos-vrf.yang dependency/oneos-route-glob.yang
# Before, you have to install  confd-basic-7.5.1.linux.x86_64.zip   from https://developer.cisco.com/site/confD/downloads/   
# Unzip and run to install :
# sh confd-basic-7.5.1.linux.x86_64.installer.bin /opt/yang/confd-basic

#Try pyang simple
pyang_command = ' pyang -f sample-xml-skeleton --sample-xml-skeleton-doctype=config  -o ' + output_file + " " + " ".join(map(str, yang_filenames))
 
try:
  #Try pyang simple
  output = subprocess.check_output(pyang_command, shell=True, stderr=subprocess.STDOUT)
except subprocess.CalledProcessError:
  #Try pyang with confD to load some cisco config functions, needed for some yang files
  pyang_command = 'source /opt/yang/confd-basic/confdrc; ' + pyang_command 
  try:
    output = subprocess.check_output(pyang_command, shell=True, stderr=subprocess.STDOUT)
  except subprocess.CalledProcessError:
    ret = MSA_API.process_content(constants.FAILED, 'Error:' + stderr, context, True)
    print(ret) 

context['pyang_command'] = pyang_command


if len(yang_filenames) >1:
  #ret = MSA_API.process_content(constants.ENDED, 'Yangs files "' + " ,".join(map(str, yang_filenames)) + '" are parsed successfully into "'+ output_file + '"' , context, True)
  ret = MSA_API.process_content(constants.ENDED, 'New XML output file: "'+ output_file + '"' , context, True)
else:
  ret = MSA_API.process_content(constants.ENDED, 'New XML output file: "'+ output_file + '"'  , context, True)

print(ret)


