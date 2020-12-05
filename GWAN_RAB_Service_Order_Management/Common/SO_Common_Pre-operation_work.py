import json
import os
import errno
from json2html import *
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

dev_var = Variables()
dev_var.add('check_config_first', var_type='Boolean')
dev_var.add('parsed_config', var_type='Link')

context = Variables.task_call(dev_var)


####################################################
#                                                  #
#                FUNCTIONS                         #
#                                                  #
####################################################
'''
Write in http server repository file the configurations from the context.

'''
def write_configs_to_http_repo():
    #retrieve configuration from the context.
    acl_config = json.dumps(context['ACL'])
    acl_config = json2html.convert(json = acl_config)
    service_policy_config = json.dumps(context['ServicePolicy'])
    service_policy_config = json2html.convert(json = service_policy_config)
    class_map_config = json.dumps(context['ClassMap'])
    class_map_config = json2html.convert(json = class_map_config)
    policy_map_config = json.dumps(context['policyMaps'])
    policy_map_config = json2html.convert(json = policy_map_config)
    static_routing_config = json.dumps(context['StaticRouting'])
    static_routing_config = json2html.convert(json = static_routing_config)
    
    #filename is created based-on the device external reference
    path_separator = '/'
    repo_base = '/opt/fmc_repository'
    repo_path = '/Datafiles/GWAN_RAB/Configurations'
    device_external_ref = context['device_external_ref']
    service_instance_id = context['SERVICEINSTANCEID']
    file_extension = '.html'
    file_name = repo_path + path_separator + device_external_ref + '_configuration_' + service_instance_id + file_extension
    filename_full_path = repo_base + file_name
    #create file in http server directory.
    if not os.path.exists(os.path.dirname(filename_full_path)):
        try:
            os.makedirs(os.path.dirname(filename_full_path))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    with open(filename_full_path, "w") as file:
        file.write("<h1>Static Routing</h1>")
        file.write("<p>")
        file.write(static_routing_config)
        file.write("</p>")
        file.write("<h1>Service Policy</h1>")
        file.write("<p>")
        file.write(service_policy_config)
        file.write("<h1>Class Map</h1>")
        file.write("<p>")
        file.write(class_map_config)
        file.write("</p>")
        file.write("<h1>Policy Map</h1>")
        file.write("<p>")
        file.write(policy_map_config)
        file.write("</p>")
        file.write("<h1>Access list (ACL)</h1>")
        file.write("<p>")
        file.write(acl_config)
        file.write("</p>")
        file.close()
    
    return file_name
    

####################################################
#                                                  #
#                MAIN CODE                         #
#                                                  #
####################################################

skip_config_review = 'False'
if 'check_config_first' in context:
    skip_config_review = str(context['check_config_first'])

if skip_config_review == 'False':
    
    #wirte parsed configurations in repository Datafile.
    file_name = write_configs_to_http_repo()

    #set link value in the context varible 'parsed_config'.
    context['parsed_config'] = file_name
    
    #display to the GUI the configuration file URL.
    ret = MSA_API.process_content('PAUSE', 'To review the configuration, click on the "Parsed Configuration" link.' , context, True)
    print(ret)

ret = MSA_API.process_content('ENDED', 'Task OK ', context, True)
print(ret)
    