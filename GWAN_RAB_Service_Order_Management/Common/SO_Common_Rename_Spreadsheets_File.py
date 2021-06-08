import json
import os
import sys
import pathlib
import datetime
from msa_sdk import constants
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

dev_var = Variables()
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


OLD_FOLDER = context['spreadsheets_directory'] + '/old'

spreadsheet_filename   = context['spreadsheet_filename']
spreadsheets_directory = context['spreadsheets_directory']
filename = os.path.basename(spreadsheet_filename)
dt   = datetime.datetime.today()
fullday = str(dt.year) + dt.strftime('%m') + dt.strftime('%d')
filename = 'run_'+ fullday + '_' + filename 
new_spreadsheet_filename = OLD_FOLDER + '/' + filename
# Test file exists
if not os.path.isfile(spreadsheet_filename):
  MSA_API.task_error(" Spreadsheet Filename  '" + spreadsheet_filename + "' not found", context, True)
  sys.exit()

#Check that the directorie old exist, else create it 
if not os.path.exists(OLD_FOLDER):
    try:
        os.makedirs(OLD_FOLDER)
    except OSError as exc: # Guard against race condition
        if exc.errno != errno.EEXIST:
            raise

os.rename(spreadsheet_filename, new_spreadsheet_filename)

MSA_API.task_success(" Spreadsheet Filename '" + spreadsheet_filename + "' move to '" + new_spreadsheet_filename + "'", context, True)
