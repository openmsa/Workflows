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
  create_var_def('sleep2', 'Integer')

context['totalSleep'] = int(context['sleep']) + int(context['sleep2'])

time.sleep(int(context['totalSleep']))

ret = prepare_json_response(ENDED, 'Task OK', context, True)
print(ret)
