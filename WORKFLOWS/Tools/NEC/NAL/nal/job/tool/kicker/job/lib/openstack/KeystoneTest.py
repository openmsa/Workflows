import datetime
import os
import sys
import traceback

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../../../../../job/')
from conf import config
from lib import logger
from lib.openstack.keystone import roles, tenants, tokens, users


# endpoint = 'http://localhost:8080/api_nal/Stubs/OpenStackClient/index.php?/v2.0'
endpoint = 'http://10.58.70.69:5000/v2.0'
admin_user_name = 'admin'
admin_password = 'i-portal'
tenant_name = 'admin'
tenant_id = '9ba7d56906cc4d0cbe055e06971b12a7'
user_name = 'test_user'
user_password = 'user_pass"123'


config = config.JobConfig()
log = logger.LibLogger(config)

try:
    OscTokens = tokens.OscTokens(config)
    OscTenants = tenants.OscTenants(config)
    OscUsers = users.OscUsers(config)
    OscRoles = roles.OscRoles(config)

    # create_token
    print('create_token')
    token = OscTokens.create_token(admin_user_name, admin_password, endpoint)
    print(type(token))
    print(token)
    print()

    # get_endpoints
    print('get_endpoints(tenant_name)')
    endpoint_array = OscTokens.get_endpoints(
        endpoint, token, admin_user_name, admin_password, tenant_name)
    print(type(endpoint_array))
    print(endpoint_array)
    print()

    print('get_endpoints(tenant_id)')
    endpoint_array = OscTokens.get_endpoints(
        endpoint, token, admin_user_name, admin_password, '', tenant_id)
    print(type(endpoint_array))
    print(endpoint_array)
    print()

    print('list_tenants')
    result = OscTenants.list_tenants(endpoint_array)
    print(type(result))
    print(result)
    print()

    print('create_tenant')
    tenant_name_new = tenant_name + datetime.datetime.today(
                                        ).strftime('%Y%m%d%H%M%S')
    print(tenant_name_new)
    result = OscTenants.create_tenant(endpoint_array, tenant_name_new)
    tenant_id_new = result['tenant']['id']
    print(type(result))
    print(result)
    print(type(tenant_id_new))
    print(tenant_id_new)
    print()

    print('list_tenants')
    result = OscTenants.list_tenants(endpoint_array)
    print(type(result))
    print(result)
    print()

    print('create_user')
    user_name_new = user_name + datetime.datetime.today(
                                        ).strftime('%Y%m%d%H%M%S')
    result = OscUsers.create_user(endpoint_array, user_name_new, user_password, tenant_id_new)
    user_id_new = result['user']['id']
    print(type(result))
    print(result)
    print(type(user_id_new))
    print(user_id_new)
    print()

    print('list_users(tenant)')
    result = OscUsers.list_users(endpoint_array, tenant_id_new)
    print(type(result))
    print(result)
    print()

    print('get_user')
    result = OscUsers.get_user(endpoint_array, user_id_new)
    print(type(result))
    print(result)
    print()

    print('update_user')
    user_name_upd = user_name_new + 'upd'
    result = OscUsers.update_user(endpoint_array, user_id_new, '', user_name_upd, '')
    print(type(result))
    print(result)
    print()

    print('get_user')
    result = OscUsers.get_user(endpoint_array, user_id_new)
    print(type(result))
    print(result)
    print()

    print('update_user_enabled')
    result = OscUsers.update_user_enabled(endpoint_array, user_id_new, False)
    print(type(result))
    print(result)
    print()

    print('get_user')
    result = OscUsers.get_user(endpoint_array, user_id_new)
    print(type(result))
    print(result)
    print()

    print('update_user_password')
    result = OscUsers.update_user_password(endpoint_array, user_id_new, 'newpass123')
    print(type(result))
    print(result)
    print()

    print('get_user')
    result = OscUsers.get_user(endpoint_array, user_id_new)
    print(type(result))
    print(result)
    print()

    print('list_roles')
    result = OscRoles.list_roles(endpoint_array)
    print(type(result))
    print(result)
    print()

    print('list_roles for user')
    result = OscRoles.list_roles_for_user(endpoint_array, user_id_new, tenant_id_new)
    print(type(result))
    print(result)
    print()

    print('add_role_to_user')
    result = OscRoles.add_role_to_user(endpoint_array, user_id_new, tenant_id_new, '448b6262a6d34ace9d673c7ac184500c')
    print(type(result))
    print(result)
    print()

    print('remove_role_from_user')
    result = OscRoles.remove_role_from_user(endpoint_array, user_id_new, tenant_id_new, '448b6262a6d34ace9d673c7ac184500c')
    print(type(result))
    print(result)
    print()

    print('delete_user')
    result = OscUsers.delete_user(endpoint_array, user_id_new)
    print(type(result))
    print(result)
    print()

    print('list_users(tenant)')
    result = OscUsers.list_users(endpoint_array, tenant_id_new)
    print(type(result))
    print(result)
    print()

    print('update_tenant')
    tenant_name_upd = tenant_name_new + 'upd'
    print('tenant_name_upd')
    result = OscTenants.update_tenant(endpoint_array, tenant_id_new, tenant_name_upd)
    print(type(result))
    print(result)
    print()

    print('get_tenant')
    result = OscTenants.get_tenant(endpoint_array, tenant_id_new)
    print(type(result))
    print(result)
    print()

    print('delete_tenant')
    result = OscTenants.delete_tenant(endpoint_array, tenant_id_new)
    print(type(result))
    print(result)
    print()

except:
    print('NG')
    msg = traceback.format_exc()
    print(msg)
    log.log_error(__name__, msg)
