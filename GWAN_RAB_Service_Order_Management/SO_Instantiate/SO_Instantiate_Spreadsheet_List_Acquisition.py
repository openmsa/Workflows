import pandas
import glob
import json
import os.path as osp
from msa_sdk import constants
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.lookup import Lookup

dev_var = Variables()
dev_var.add('spreadsheets_directory', var_type='String')
dev_var.add('spreadsheets_extension', var_type='String')
dev_var.add('spreadsheet_list.0.spreadsheet', var_type='String')
dev_var.add('spreadsheet_list.0.is_selected', var_type='Boolean')
dev_var.add('spreadsheet_list.0.device_hostname', var_type='String')
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

def get_device_hostname_from_sheet(df, device_ref_row_index, column_filter):
    for key, value in df.iteritems():
        if key == column_filter:
            hostname = df.iloc[device_ref_row_index][key]
    return hostname

####################################################
#                                                  #
#                MAIN CODE                         #
#                                                  #
####################################################

#Constant variables
#
#Sheet name where is located the device external reference (Hostname)
SHEET_NAME_CONTAINING_DEVICE_HOSTNAME = 'Main'
#Sheet Columns key (name) where is located the device external reference (Hostname)
FILTER_COLUMN_NAME = 'Unnamed: 1'
#Sheet row index where is located the device external reference (Hostname)
SHEET_DEVICE_REF_ROW_INDEX = 2
NO_FOUND_DEVICE_MESSAGE = 'NOT FOUND'

context['no_found_device_message'] = NO_FOUND_DEVICE_MESSAGE

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

context['instanceid_hostname'] = context['SERVICEINSTANCEID'] + '_NoDeviceSelected' # we don't have yet the device selected


# check if at least one spreadsheet file is available. If not exit and return failed.
if not spreadsheet_list:
    MSA_API.task_error('No spreadsheed file found from \'' + spreadsheets_directory + '\' directory.', context, True)

#spreadsheet_list_restructured = [dict(spreadsheet=st, is_selected='false') for st in spreadsheet_list]
spreadsheet_list_restructured = []

#get all devices for the customer
lookup = Lookup()

#Get all devices available
lookup.look_list_device_ids()
all_devices = lookup.response.json()
device_ref_by_hostname = {}
for device in all_devices:
  # device = {'id': 125, 'prefix': 'RAB', 'ubiId': 'RAB125', 'externalReference': 'RAB125', 'name': 'CISCO-IOS'}
  device_ref_by_hostname[device['name']] = device['externalReference']

for st in spreadsheet_list:
    df = pandas.read_excel('file:' + st, sheet_name=SHEET_NAME_CONTAINING_DEVICE_HOSTNAME)
    #defined the position of the device reference from the sheet name 'Main'
    #device_ext_ref = get_device_reference_from_sheet(df, SHEET_DEVICE_REF_ROW_INDEX, FILTER_COLUMN_NAME)
    device_hostname = get_device_hostname_from_sheet(df, SHEET_DEVICE_REF_ROW_INDEX, FILTER_COLUMN_NAME)
    #device_hostname is mandatory, if it is empty return FAILED.
    if not device_hostname:
        MSA_API.task_error('Device Hostname is empty from sheet called ' + SHEET_NAME_CONTAINING_DEVICE_HOSTNAME + '.', context, True)
    #create spreadsheet dictionaries list.
    spreadsheet_basename = osp.basename(st)
    if (device_ref_by_hostname.get(device_hostname)):
      device_external_ref = device_ref_by_hostname[device_hostname]
    else:
      #device_external_ref = 'Not found, hostname "xxx" corresponding managed entity'
      device_external_ref = NO_FOUND_DEVICE_MESSAGE
    spreadsheet_dict = dict(spreadsheet=spreadsheet_basename, is_selected='false', device_external_ref=device_external_ref, device_hostname=device_hostname)
    spreadsheet_list_restructured.append(spreadsheet_dict)
#store in the context 'device_external_ref' and 'spreadsheet_list'
context['spreadsheet_list'] = spreadsheet_list_restructured


MSA_API.task_success('Spreadsheet list acquisition is done successfully.', context, True)

