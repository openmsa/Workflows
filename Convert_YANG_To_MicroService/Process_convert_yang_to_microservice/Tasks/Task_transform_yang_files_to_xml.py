import copy
import glob
import json
import subprocess
import os

import numpy as np
from re import search
from msa_sdk import constants
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

dev_var = Variables()
dev_var.add('yang_list.0.yang', var_type='String')
dev_var.add('yang_list.0.is_selected', var_type='Boolean')
dev_var.add('yang_list.0.is_yangmainfile', var_type='Boolean')

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
main_yang_file = ''

for st in yang_list:
   # "yang_list": [ {  "yang": "/opt/fmc_repository/Datafiles/YANG/example-1.yang", "is_selected": "false", "is_yangmainfile": "false"  },
   #                { "yang": "/opt/fmc_repository/Datafiles/YANG/example-2.yang", "is_selected": "false", "is_yangmainfile": "false"   } ]
  
  if st.get('is_selected') == True:
    if st.get('yang'):
      yang_filename = context.get('yangs_directory') + '/' + st.get('yang')
      yang_filenames.append(yang_filename)
      if st.get('is_yangmainfile') == True:
        main_yang_file = yang_filename
  
    else:
      ret = MSA_API.process_content(constants.FAILED, 'Selected yang filename is empty from the service instance context.', context, True)
      print(ret)

context['yang_filenames'] = yang_filenames
if main_yang_file =='':
  #take the first yang selected 
  context['main_yang_file'] = yang_filenames[0]
  main_yang_file = yang_filenames[0]
else:
  context['main_yang_file'] = main_yang_file

if selected_number ==0:
  ret = MSA_API.process_content(constants.FAILED, 'No yang file selected', context, True)

xml_output_file =  main_yang_file.replace(context['yangs_extension'],'') + '_output.xml'
context['xml_output_file'] = xml_output_file
yang_path = os.path.dirname(main_yang_file) # run pyang in the given directorie to be able to load other yang generic library dependency 

pyang_command = ' cd "'+yang_path+'";  pyang -f sample-xml-skeleton --sample-xml-skeleton-doctype=config  -o ' + xml_output_file + " " + " ".join(map(str, yang_filenames))
 
try:
  output = subprocess.check_output(pyang_command, shell=True, stderr=subprocess.STDOUT)
except subprocess.CalledProcessError:
  ret = MSA_API.process_content(constants.FAILED, 'Error:' + stderr, context, True)
  print(ret) 

context['pyang_command'] = pyang_command


if len(yang_filenames) >1:
  ret = MSA_API.process_content(constants.ENDED, 'New XML output file: "'+ xml_output_file + '"' , context, True)
else:
  ret = MSA_API.process_content(constants.ENDED, 'New XML output file: "'+ xml_output_file + '"'  , context, True)

print(ret)



