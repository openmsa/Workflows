import pandas
import glob
import json
import os.path as osp
from msa_sdk import constants
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

dev_var = Variables()
dev_var.add('spreadsheets_directory', var_type='String')
dev_var.add('spreadsheets_extension', var_type='String')
dev_var.add('spreadsheet_list.0.spreadsheet', var_type='String')
dev_var.add('spreadsheet_list.0.is_selected', var_type='Boolean')
dev_var.add('spreadsheet_list.0.device_external_ref', var_type='String')


context = Variables.task_call(dev_var)

####################################################
#                                                  #
#                FUNCTIONS                         #
#                                                  #
####################################################

def get_device_reference_from_sheet(df, device_ref_row_index, column_filter):
    for key, value in df.iteritems():
        if key == column_filter:
            device_ref = df.iloc[device_ref_row_index][key]
            
    return device_ref


####################################################
#                                                  #
#                MAIN CODE                         #
#                                                  #
####################################################

#Constant variables
#
#Sheet name where is located the device external reference (Hostname)
SHEET_NAME_CONTAINING_DEVICE_REF = 'Main'
#Sheet Columns key (name) where is located the device external reference (Hostname)
FILTER_COLUMN_NAME = 'Unnamed: 1'
#Sheet row index where is located the device external reference (Hostname)
SHEET_DEVICE_REF_ROW_INDEX = 2

'''
List spreadsheet files from repository.
'''
spreadsheets_directory = context['spreadsheets_directory']
spreadsheets_extension = context['spreadsheets_extension']

if not spreadsheets_directory:
    spreadsheets_directory = '/opt/fmc_repository/Datafiles/GWAN_RAB'
  
if not spreadsheets_extension:
    spreadsheets_extension = '.xlsx'

#list the spreadsheet files from specified directory in the MSA repositary data.  
pattern = spreadsheets_directory + '/*' + spreadsheets_extension
spreadsheet_list = glob.glob(pattern)

# check if at least one spreadsheet file is available. If not exit and return failed.
if not spreadsheet_list:
    ret = MSA_API.process_content(FAILED, 'No spreadsheed file found from \'' + spreadsheets_directory + '\' directory.', context, True)
    print(ret)	

#spreadsheet_list_restructured = [dict(spreadsheet=st, is_selected='false') for st in spreadsheet_list]
spreadsheet_list_restructured = []

for st in spreadsheet_list:
    df = pandas.read_excel('file:' + st, sheet_name=SHEET_NAME_CONTAINING_DEVICE_REF)
    #defined the position of the device reference from the sheet name 'Main'
    device_ext_ref = get_device_reference_from_sheet(df, SHEET_DEVICE_REF_ROW_INDEX, FILTER_COLUMN_NAME)
    #device_external_ref is mandatory, if it is empty return FAILED.
    if not device_ext_ref:
        ret = MSA_API.process_content(FAILED, 'Device external reference (hostname) is empty from sheet called ' + SHEET_NAME_CONTAINING_DEVICE_REF + '.', context, True)
        print(ret)
    #create spreadsheet dictionaries list.
    spreadsheet_basename = osp.basename(st)
    spreadsheet_dict = dict(spreadsheet=spreadsheet_basename, is_selected='false', device_external_ref=device_ext_ref)
    spreadsheet_list_restructured.append(spreadsheet_dict)
#store in the context 'device_external_ref' and 'spreadsheet_list'
context['spreadsheet_list'] = spreadsheet_list_restructured


ret = MSA_API.process_content(constants.ENDED, 'Spreadsheet list acquisition is done successfully.', context, True)
print(ret)

