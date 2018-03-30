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
output_params.append('/home/admin/20160620035201981_id_rsa')
output_params.append('ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAv64xaqWLJQew04BR1GzVAmEuhEjE9xBSt0wPWO9fBq85JqWHbxczNXAqf4ZE0pwr+8J+rMrx6e7gS14ualc1zBYQDM8qH/l8wvuPtwUyTLbEXYtqBT0qIp+ezfzcwbmQ4nsJ1jQCA2oqiMEwezpWoLTQtscbjeL2JFNA5c+70Yf4M6mb8WnWbF4RvxzmjykcwdoCs6MaL2f2hLi+f0ggpqZ+awcrtfb6o39WQUiT3d06Rlmg6RfQ5k4niyFXWLCpWa5DZulk0UGAPq9dUv0dLc6Tu42cimghY2o7Hc+bolzqE7TzAJrCHLf9Kl2de0z4p8QH4JG5x+6/QR9INRpjqw== sms@msa1')

stub_common.add_script_output_params_to_file(script_name, output_params)

for output in output_params:
    print(output)

exit(0)
