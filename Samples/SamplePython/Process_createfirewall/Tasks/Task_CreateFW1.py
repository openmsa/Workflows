'''
Created on 28-Mar-2019

@author: prasadh
'''

import sys
sys.path.append('/opt/fmc_repository/Process/Reference/Common')

from common import *
from constants import *
from utility import *
import time

def list_args():
  create_var_def('fw_name', 'Device')
  create_var_def('sleep', 'Integer')
  create_var_def('device.0.id', 'Device')

time.sleep(int(context['sleep']))

ret = prepare_json_response(ENDED, 'Task OK', context, True)
print(ret)
