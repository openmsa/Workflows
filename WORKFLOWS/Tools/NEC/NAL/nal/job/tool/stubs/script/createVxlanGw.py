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
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../../../')
from job.tool.stubs import common


stub_common = common.StubCommon()

argv = sys.argv
script_name = stub_common.get_script_name(argv[0])

output_params = []
output_params.append(script_name)
output_params.append('| id | ' + stub_common.gen_rand_str_hex(32) + ' |')

stub_common.add_script_output_params_to_file(script_name, output_params)

for output in output_params:
    print(output)

exit(0)
