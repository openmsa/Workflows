import copy
import pandas
import glob
import json
import numpy as np
from re import search
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

dev_var = Variables()
dev_var.add('spreadsheet_list.0.spreadsheet', var_type='String')
dev_var.add('spreadsheet_list.0.is_selected', var_type='Boolean')
dev_var.add('spreadsheet_list.0.device_external_ref', var_type='String')

context = Variables.task_call(dev_var)

####################################################
#                                                  #
#                FUNCTIONS                         #
#                                                  #
####################################################

'''
Get rows indexes by value in specific column.

@param df
    Dataframe.
@param ot
    Row/column value (Order type) (e.g: 'ADD', 'DEL', 'Tag').
@param ot_column
    Sheet column name where order_type is located (e.g: 'Unnamed: 2').
return
    dictionary containing index of rows.
'''
def get_rows_indexes_by_value(df, ot, ot_column):
    rows = []
    #Get cells rows indexes by value from specific column.
    for key, value in df.iteritems():
        #df = df.replace(np.nan, '', regex=True)
        # Column name where the ORDER_TYPE is located.
        if key == ot_column:
            rows = df.index[df[key] == ot].tolist()

    return rows
'''
Get configuration row list from excel sheet.

@param df
    Dataframe.
@param rows
    Table header rows indexes dictionary.
return
        list of dictionary containing rows of configuration.
'''
def get_config_row_list_by_order_type(df, rows):
    config_row_dict_list = []
    config_row_dict = {}
    df = df.replace(np.nan, '', regex=True)

    # creating a list of dataframe columns
    columns = list(df)

    # loops to select row values by column
    for x in rows:
        count = 0
        config_row_dict.clear()
        for y in columns:
            config_row_dict[str(count)] = df.iloc[x][y]
            count += 1
        # insert config row in list and clear the list for the next row handling
        config_row_dict_list.append(config_row_dict.copy())

    return config_row_dict_list

def static_routing_replace_item_key_by_sheet_header_name(config_row_list, tab_header_row_index_list):
    count = 0
    for config_row_dict in config_row_list:
        while count < len(config_row_dict):
            key = tab_header_row_index_list[0].get(str(count))
            new_key = key.lower().replace(' ', '_').replace('-', '_')
            old_key = str(count)
            config_row_dict[new_key] = config_row_dict.pop(old_key)
            count += 1
        else:
            count = 0

    return config_row_list

def acl_replace_item_key_by_sheet_header_name(config_row_list, tab_header_row_index_list):
    count = 0
    for config_row_dict in config_row_list:
        count = 0
        while count < len(config_row_dict):
            if config_row_list.index(config_row_dict) == 0:
                key = tab_header_row_index_list[0].get(str(count))
                new_key = key.lower().replace(' ', '_').replace('-', '_')
            else:
                key = tab_header_row_index_list[1].get(str(count))
                new_key = key.lower().replace(' ', '_').replace('-', '_')
                #avoid aggreation of items with same key.
                if count == 5:
                    new_key = 'source_wildcardmask'
                if count == 6:
                    new_key = 'source_port'
                if count == 8:
                    new_key = 'destination_wildcardmask'
                if count == 9:
                    new_key = 'destination_port'
            old_key = str(count)
            config_row_dict[new_key] = config_row_dict.pop(old_key)
            count += 1

    return config_row_list

def policy_map_replace_item_key_by_sheet_header_name(config_row_list, tab_header_row_index_list):
    count = 0
    for config_row_dict in config_row_list:
        count = 0
        while count < len(config_row_dict):
            if config_row_list.index(config_row_dict) == 0:
                key = tab_header_row_index_list[0].get(str(count))
                new_key = key.lower().replace(' ', '_').replace('-', '_')
            else:
                key = tab_header_row_index_list[1].get(str(count))
                new_key = key.lower().replace(' ', '_').replace('-', '_')

                #avoid aggreation of items with same key.
                if count == 3:
                    new_key = 'cir_before'
                if count == 4:
                    new_key = 'cir_after'
                if count == 5:
                    new_key = 'bc_before'
                if count == 6:
                    new_key = 'bc_after'
                if count == 7:
                    new_key = 'be_before'
                if count == 8:
                    new_key = 'be_after'
            old_key = str(count)
            config_row_dict[new_key] = config_row_dict.pop(old_key)
            count += 1
    return config_row_list
    

####################################################
#                                                  #
#                MAIN CODE                         #
#                                                  #
####################################################

#Constant variables
STATIC_ROUTING = 'StaticRouting'
ACL = 'ACL'
SERVICE_POLICY = 'ServicePolicy'
CLASS_MAP = 'ClassMap'
POLICY_MAP = 'PolicyMap'
FILTER_TAB_FLAG = 'Flag'
FILTER_COLUMN_NAME = 'Unnamed: 1'
ORDER_TYPE = 'ADD'
context['order_type'] = ORDER_TYPE

# Check multiple or missing spreadsheet file selection.
selected_number = 0
spreadsheet_list_json= json.dumps(context['spreadsheet_list'])
spreadsheet_list = json.loads(spreadsheet_list_json)

if spreadsheet_list:
    for st in spreadsheet_list:
        if st.get('is_selected') == True:
            selected_number += 1
else:
	ret = MSA_API.process_content('FAILED', 'Spreadsheet list is empty.', context, True)
	print(ret)
    
# Retrieve selected spreadsheet_filename from the list.
spreadsheet_filename = ''
if selected_number == 1:
	for st in context.get('spreadsheet_list'):
		if st.get('is_selected') == True:
			if st.get('spreadsheet'):
                #spreadsheets_dir = context['spreadsheets_directory']
				spreadsheet_filename = context['spreadsheets_directory'] + '/' + st.get('spreadsheet')
			else:
				ret = MSA_API.process_content('FAILED', 'Selected spreadsheet filename is empty from the service instance context.', context, True)
				print(ret)
			break
else:
	ret = MSA_API.process_content('FAILED', 'Only one spreadsheet must and allows to be selected.', context, True)
	print(ret)
  
# List sheet name in spreadsheet 
#spreadsheet_filename = '/opt/fmc_repository/Datafiles/GWAN_RAB/UBIQUBE_MSA_configuration_sheet_20200918.xlsx'
sheet_names = ''

if spreadsheet_filename:
    xl = pandas.ExcelFile('file:' + spreadsheet_filename)
    sheet_names = xl.sheet_names  # see all sheet names
    
# unset configurations dictionaries in context before to read the spreadsheet
context.pop('ACL')
context.pop('ServicePolicy')
context.pop('ClassMap')
context.pop('policyMaps')
context.pop('StaticRouting')

# Read sheet to json
acl_rules_dict = {}
policy_map_dict = {}
sheet_name_patterns = [STATIC_ROUTING, ACL, SERVICE_POLICY, CLASS_MAP, POLICY_MAP]
for sheet_name in sheet_names:
  	for pattern in sheet_name_patterns:
            is_sheet_name_exist = search(pattern, sheet_name)
            if is_sheet_name_exist:
                df = pandas.read_excel('file:' + spreadsheet_filename, sheet_name=sheet_name)

                # SELECT tab_header_row_index_list FROM columns WHERE col_name='Unnamed: 1 AND cell_val = '''
                header_row_indexes = get_rows_indexes_by_value(df, FILTER_TAB_FLAG, FILTER_COLUMN_NAME)
                tab_header_row_index_list = get_config_row_list_by_order_type(df, header_row_indexes)

                # SELECT tab_header_row_index_list FROM columns WHERE col_name='Unnamed: 1'
                config_row_indexes = get_rows_indexes_by_value(df, ORDER_TYPE, FILTER_COLUMN_NAME)
                config_row_list = get_config_row_list_by_order_type(df, config_row_indexes)

                # Add tab header values as config values keys
                if sheet_name == STATIC_ROUTING or sheet_name == SERVICE_POLICY or sheet_name == CLASS_MAP:
                    config_list = static_routing_replace_item_key_by_sheet_header_name(config_row_list, tab_header_row_index_list)
                    # add staticRouting or ServicePolicy or ClassMap configurations in WF service context DB.
                    context[sheet_name] = config_list
                #                 
                elif search(ACL, sheet_name):
                    acl_rules_list = acl_replace_item_key_by_sheet_header_name(config_row_list, tab_header_row_index_list)
                    acl_rules_dict.update({sheet_name: acl_rules_list})

                elif search(POLICY_MAP, sheet_name):
                    policy_map_list = policy_map_replace_item_key_by_sheet_header_name(config_row_list, tab_header_row_index_list)
                    policy_map_dict.update({sheet_name: policy_map_list})

context['ACL'] = acl_rules_dict
context['policyMaps'] = policy_map_dict
context['spreadsheet_filename'] = spreadsheet_filename

ret = MSA_API.process_content('ENDED', 'Spreadsheet file is parsed successfully.', context, True)
print(ret)
