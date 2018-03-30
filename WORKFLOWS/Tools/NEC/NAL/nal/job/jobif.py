# -*- coding: utf-8 -*-

#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#  
#       http://www.apache.org/licenses/LICENSE-2.0
#  
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.
#  
#  COPYRIGHT  (C)  NEC  CORPORATION  2017
#  
# import jobmethod
import importlib
import json
import os
import sys
import traceback

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')

print('start job_exec')

# Get Filepath From OS Environ Variables
nal_input_file = os.environ.get('NAL_INPUTFILE')
nal_output_file = os.environ.get('NAL_OUTPUTFILE')

if len(nal_input_file) == 0:
    print('not set NAL_INPUTFILE')
    exit(91)

if len(nal_output_file) == 0:
    print('not set NAL_OUTPUTFILE')
    exit(92)

# Check Parameter
if len(sys.argv) != 2:
    print('wrong number of arguments. job.py <job_automation class_name>')
    exit(93)

# Get Parameter
job_method_name = sys.argv[1]
print('job_automation method_name=' + job_method_name)

# Get Input Parameters From InputFile(NAL)
try:
    with open(nal_input_file, 'r') as f:
        job_input = json.loads(f.read())
except:
    print('cannot read ' + nal_input_file)
    exit(96)

# Create Instance(Job Automation Distributer)
try:

    job_module = importlib.import_module('auto.method')
    class_attr = getattr(job_module, 'JobAutoMethod')
    job_instance = class_attr(job_input.get('request-id', '-'))
    job_method_attr = getattr(job_instance, job_method_name)

except:
    print(traceback.format_exc())
    print('cannot create instance:' + job_method_name)
    exit(95)

# Execute Job Automation
try:
    job_output = job_method_attr(job_input)
except:
    job_instance.output_log_fatal(__name__, traceback.format_exc())
    print('error occured in job_exec')
    exit(97)

# Add Output Parameters To InputFile(NAL)
job_input.update(job_output)
try:
    with open(nal_input_file, 'w') as f:
        f.write(json.dumps(job_input))
except:
    job_instance.output_log_fatal(__name__, traceback.format_exc())
    print('cannot write ' + nal_input_file)
    exit(98)

# Put Output Parameters To OutputFile(NAL)
try:
    with open(nal_output_file, 'w') as f:
        f.write(json.dumps(job_output))
except:
    job_instance.output_log_fatal(__name__, traceback.format_exc())
    print('cannot write ' + nal_output_file)
    exit(98)

print('end job_exec')
exit(0)
