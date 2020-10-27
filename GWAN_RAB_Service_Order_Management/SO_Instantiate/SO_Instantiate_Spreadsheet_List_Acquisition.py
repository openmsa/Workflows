import pandas
import glob
import json
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

dev_var = Variables()
dev_var.add('spreadsheets_directory', var_type='String')
dev_var.add('spreadsheets_extension', var_type='String')
dev_var.add('spreadsheet_list.0.spreadsheet', var_type='String')
dev_var.add('spreadsheet_list.0.is_selected', var_type='Boolean')


context = Variables.task_call(dev_var)

'''
List spreadsheet files from repository.
'''
spreadsheets_directory = context['spreadsheets_directory']
spreadsheets_extension = context['spreadsheets_extension']

if not spreadsheets_directory:
	spreadsheets_directory = '/opt/fmc_repository/Datafiles/GWAN_RAB'
  
if not spreadsheets_extension:
	spreadsheets_extension = '.xlsx'
  
pattern = spreadsheets_directory + '/*' + spreadsheets_extension
spreadsheet_list = glob.glob(pattern)

# check if at least one spreadsheet file is available. If not exit and return failed.
if not spreadsheet_list:
	ret = MSA_API.process_content('FAILED', 'No spreadsheed file found from \'' + spreadsheets_directory + '\' directory.', context, True)
	print(ret)	

spreadsheet_list_restructured = [dict(spreadsheet=st, is_selected='false') for st in spreadsheet_list]

context['spreadsheet_list'] = spreadsheet_list_restructured;

json_str = json.dumps(spreadsheet_list)
ret = MSA_API.process_content('ENDED', 'Spreadsheet list acquisition is done successfully.', context, True)
print(ret)

