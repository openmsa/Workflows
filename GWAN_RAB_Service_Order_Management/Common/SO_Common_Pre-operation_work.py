from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

dev_var = Variables()
dev_var.add('check_config_first', var_type='Boolean')

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
    acl_config = context['ACL'] 
    service_policy_config = context['ServicePolicy']
    class_map_config = context['ClassMap']
    policy_map_config = context['policyMaps']
    static_routing_config = context['StaticRouting']
    
    #filename is created based-on the device external reference
    http_repo_path = '/app/repos/'
    device_external_ref = context['device_external_ref']
    file_extension = '.json'
    file_name = 'gwan_rab_configs_' + device_external_ref + file_extension
    
    #create file in http server directory.
    file = open(http_repo_path + file_name, "w+") 
    file.write(static_routing_config)
    file.write(service_policy_config)
    file.write(class_map_config)
    file.write(policy_map_config)
    file.write(acl_config)
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
    file_name = write_configs_to_http_repo()
    #example of URL.
    configs_http_url = 'http://127.0.0.1/' + file_name
    #store the configuration filename and http URL.
    context['configs_file_name'] = file_name
    context['configs_http_url'] = configs_http_url
    
    #display to the GUI the configuration file URL.
    ret = MSA_API.process_content('PAUSE', 'Check conf: ' + configs_http_url, context, True)
    print(ret)

ret = MSA_API.process_content('ENDED', 'Task OK ', context, True)
print(ret)
    