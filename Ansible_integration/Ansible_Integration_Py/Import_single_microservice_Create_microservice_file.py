import re
import os
import sys
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk import constants

dev_var = Variables()
context = Variables.task_call(dev_var)

#Gather variables from context
variables_line = context['variables_line']
microservice_create_line = context['microservice_create_line']
microservice_name = context['microservice_name']
microservice_skeleton = context['microservice_skeleton']
microservice_dir = context['microservice_dir']

#Gather MS skeleton file path and MS skeleton file name from variable]
microservice_skeleton_name = os.path.basename(microservice_skeleton)
microservice_skeleton_path = os.path.dirname(microservice_skeleton) + '/'

#Sanitize file name
microservice_file_name = re.sub(r'/[| @()]/', r'_', microservice_name) + '.xml'

#Create microservice_dir if not exists
if not os.path.exists(microservice_dir):
    os.makedirs(microservice_dir)

#Copy MS skeleton to new file
cp_command = '/bin/cp '+microservice_skeleton+' '+microservice_dir

if microservice_skeleton_name != microservice_file_name:
    cp_command += ' && /bin/mv '+microservice_dir+microservice_skeleton_name+' '+microservice_dir+microservice_file_name

cp_command += ' && /bin/cp '+microservice_skeleton_path+'.meta_'+microservice_skeleton_name+' '+microservice_dir

if microservice_skeleton_name != microservice_file_name:
    cp_command += ' && mv '+microservice_dir+'.meta_'+microservice_skeleton_name+' '+microservice_dir+'.meta_'+microservice_file_name

result = os.system(cp_command)
if result != 0:
    ret = MSA_API.process_content(constants.FAILED, 'Failed. Coping MS skeleton to new file... NOK.', context, True)
    print(ret)
    sys.exit()

#Write MS name to MS file
sed_command = '/bin/sed -i \'s@ansible_playbook_skeleton@'+microservice_name+'@\' '+microservice_dir+microservice_file_name
result = os.system(sed_command)
if result != 0:
    ret = MSA_API.process_content(constants.FAILED, 'Failed. Writing MS name to MS file... NOK.', context, True)
    print(ret)
    sys.exit()

#Write variables to MS file
sed_command = '/bin/sed -i "s@<variables frozen=\"0\"></variables>@'+variables_line+'@\" '+microservice_dir+microservice_file_name
result = os.system(sed_command)
context.update(SLE_DEBUG_sed_command=sed_command)
context.update(SLE_DEBUG_result=result)
if result != 0:
    ret = MSA_API.process_content(constants.FAILED, 'Failed. Writing variables to MS file... NOK.', context, True)
    print(ret)
    sys.exit()

#Write command to execute on CREAT step to MS file
sed_command = '/bin/sed -i \'s@<operation></operation>@'+microservice_create_line+'@\' '+microservice_dir+microservice_file_name
result = os.system(sed_command)
if result != 0:
    ret = MSA_API.process_content(constants.FAILED, 'Failed. Writing command to execute on CREATE step to MS file... NOK.', context, True)
    print(ret)
    sys.exit()

context['microservice_path'] = microservice_dir + microservice_file_name
context['microservice_file_name'] = microservice_file_name
  
#Looks like we have finished. COngrats!
ret = MSA_API.process_content(constants.ENDED, 'Success. Microservice '+microservice_file_name+'has been created successfully.', context, True)
print(ret)