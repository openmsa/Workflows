import datetime
import json
import unittest

#sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../../../')
from job.conf import config
from job.lib.openstack.keystone import roles
from job.lib.openstack.keystone import tenants
from job.lib.openstack.keystone import tokens
from job.lib.openstack.keystone import users


class TestSelectAPI(unittest.TestCase):
    # Do a test of Select.

#     ENDPOINT_URL = 'http://10.58.79.171:35357/v3'
#     REGION_ID = 'RegionOne'
#     ADMIN_TENANT_ID = '8cc49b2e5ce04eebbcbfeb4eab05bd90'
#     ADMIN_ROLE_ID = 'bf2fd8b743ca41ab91c6435d344e6928'

    ENDPOINT_URL = 'http://localhost:80/rest_openstack/index.py/min/v3'
    REGION_ID = 'region_unit_test1'
    ADMIN_TENANT_ID = '9ba7d56906cc4d0cbe055e06971b12a7'
    ADMIN_ROLE_ID = '448b6262a6d34ace9d673c7ac184500c'

    def setUp(self):

        # Establish a clean test environment.
        super(TestSelectAPI, self).setUp()

        # Insert test data
        self.create_fixtures()

    def tearDown(self):
        """Clear the test environment"""
        super(TestSelectAPI, self).tearDown()
        self.destroy_fixtures()

    def create_fixtures(self):

        pass

    def destroy_fixtures(self):

        pass

    def test_keystone(self):

        endpoint = self.ENDPOINT_URL
        admin_user_name = 'admin'
        admin_password = 'i-portal'
        tenant_name = 'test_tenant'
        tenant_id = self.ADMIN_TENANT_ID
        user_name = 'test_user'
        user_password = 'user_pass"123'
        role_id = self.ADMIN_ROLE_ID

        job_config = config.JobConfig()

        # Create Token
        token = tokens.OscTokens(job_config)\
                    .create_token(admin_user_name, admin_password, endpoint,
                                  tokens.OscTokens.DOMAIN_NAME_DEFAULT)
        print('create_token')
        print(token)

        # Assertion
        self.assertGreaterEqual(len(token), 1)

        # Get Endpoints
        endpoint_array = tokens.OscTokens(job_config).get_endpoints(
            endpoint, token, admin_user_name, admin_password, tenant_id,
                                  tokens.OscTokens.DOMAIN_NAME_DEFAULT)
        print('get_endpoints')
        print(json.dumps(endpoint_array))

        # Assertion
        self.assertGreaterEqual(len(endpoint_array), 1)

        # Create Token
        token = tokens.OscTokens(job_config)\
                    .create_token(admin_user_name, admin_password, endpoint)
        print('create_token')
        print(token)

        # Assertion
        self.assertGreaterEqual(len(token), 1)

        # Get Endpoints
        endpoint_array = tokens.OscTokens(job_config).get_endpoints(
            endpoint, token, admin_user_name, admin_password, tenant_id)
        print('get_endpoints')
        print(json.dumps(endpoint_array))

        # Assertion
        self.assertGreaterEqual(len(endpoint_array), 1)

        endpoint_array['region_id'] = self.REGION_ID

        # Create Tenant
        tenant_name_new1 = tenant_name + '1-' + datetime.datetime.today(
                                                    ).strftime('%Y%m%d%H%M%S')
        res = tenants.OscTenants(job_config)\
                            .create_tenant(endpoint_array, tenant_name_new1)
        print('create_tenant')
        print(json.dumps(res))
        tenant_id_new1 = res['project']['id']

        # Assertion
        self.assertGreaterEqual(len(res), 1)

        tenant_name_new2 = tenant_name + '2-' + datetime.datetime.today(
                                                    ).strftime('%Y%m%d%H%M%S')
        res = tenants.OscTenants(job_config)\
                .create_tenant(endpoint_array,
                               tenant_name_new2,
                               'test KeystoneV3',
                               False,
                               tenants.OscTenants.DOMAIN_ID_DEFAULT,
                               False)
        print('create_tenant')
        print(json.dumps(res))
        tenant_id_new2 = res['project']['id']

        # Assertion
        self.assertGreaterEqual(len(res), 1)

        # Get Tenant
        res = tenants.OscTenants(job_config)\
                            .get_tenant(endpoint_array, tenant_id_new1)
        print('get_tenant')
        print(json.dumps(res))

        # Assertion
        self.assertGreaterEqual(len(res), 1)

        # Update Tenant
        res = tenants.OscTenants(job_config).update_tenant(
                    endpoint_array, tenant_id_new1, tenant_name_new1 + 'upd')
        print('update_tenant')
        print(json.dumps(res))

        # Assertion
        self.assertGreaterEqual(len(res), 1)

        res = tenants.OscTenants(job_config).update_tenant(
                    endpoint_array, tenant_id_new2, tenant_name_new2 + 'upd',
                    'update',
                    True,
                    tenants.OscTenants.DOMAIN_ID_DEFAULT,
                    False)

        print('update_tenant')
        print(json.dumps(res))

        # Assertion
        self.assertGreaterEqual(len(res), 1)

        # List Tenants
        res = tenants.OscTenants(job_config).list_tenants(endpoint_array)
        print('list_tenants')
        print(json.dumps(res))

        # Assertion
        self.assertGreaterEqual(len(res), 1)

        # Create User
        user_name_new1 = user_name + '1-' + datetime.datetime.today(
                                                    ).strftime('%Y%m%d%H%M%S')
        res = users.OscUsers(job_config).create_user(
                endpoint_array, user_name_new1, user_password, tenant_id_new1)
        print('create_user')
        print(json.dumps(res))
        user_id_new1 = res['user']['id']

        # Assertion
        self.assertGreaterEqual(len(res), 1)

        # Create User
        user_name_new2 = user_name + '2-' + datetime.datetime.today(
                                                    ).strftime('%Y%m%d%H%M%S')
        res = users.OscUsers(job_config).create_user(
                                    endpoint_array,
                                    user_name_new2,
                                    user_password,
                                    tenant_id_new2,
                                    'test@kspsys.co.jp',
                                    True,
                                    users.OscUsers.DOMAIN_ID_DEFAULT)
        print('create_user')
        print(json.dumps(res))
        user_id_new2 = res['user']['id']

        # Assertion
        self.assertGreaterEqual(len(res), 1)

        # Get User
        res = users.OscUsers(job_config).get_user(
                                                endpoint_array, user_id_new1)
        print('get_user')
        print(json.dumps(res))

        # Assertion
        self.assertGreaterEqual(len(res), 1)

        # Get User
        res = users.OscUsers(job_config).get_user(
                                                endpoint_array, user_id_new2)
        print('get_user')
        print(json.dumps(res))

        # Assertion
        self.assertGreaterEqual(len(res), 1)

        # List Role For User
        res = roles.OscRoles(job_config)\
            .list_roles_for_user(endpoint_array, user_id_new1, tenant_id_new1)
        print('list_roles_for_user')
        print(json.dumps(res))

        # Assertion
        self.assertGreaterEqual(len(res), 1)

        # Update User
        res = users.OscUsers(job_config).update_user(
                                    endpoint_array,
                                    user_id_new1,
                                    None,
                                    user_name_new1 + 'upd')
        print('update_user')
        print(json.dumps(res))

        # Assertion
        self.assertGreaterEqual(len(res), 1)

        # Update User
        res = users.OscUsers(job_config).update_user(
                                    endpoint_array,
                                    user_id_new2,
                                    tenant_id,
                                    user_name_new2 + 'upd',
                                    'testupdate@kspsys.co.jp',
                                    'pass-update',
                                    False,
                                    users.OscUsers.DOMAIN_ID_DEFAULT)
        print('update_user')
        print(json.dumps(res))

        # Assertion
        self.assertGreaterEqual(len(res), 1)

        # Get User
        res = users.OscUsers(job_config).get_user(
                                                endpoint_array, user_id_new1)
        print('get_user')
        print(json.dumps(res))

        # Assertion
        self.assertGreaterEqual(len(res), 1)

        # Get User
        res = users.OscUsers(job_config).get_user(
                                                endpoint_array, user_id_new2)
        print('get_user')
        print(json.dumps(res))

        # Assertion
        self.assertGreaterEqual(len(res), 1)

        # List Users
        res = users.OscUsers(job_config).list_users(endpoint_array)
        print('list_users')
        print(json.dumps(res))

        # Assertion
        self.assertGreaterEqual(len(res), 1)

        # List Role
        res = roles.OscRoles(job_config).list_roles(endpoint_array)
        print('list_roles')
        print(json.dumps(res))

        # Assertion
        self.assertGreaterEqual(len(res), 1)

        # Add Role To User
        res = roles.OscRoles(job_config).add_role_to_user(
                    endpoint_array, user_id_new1, tenant_id_new1, role_id)
        print('add_role_to_user')
        print(json.dumps(res))

        # Assertion
        self.assertEqual(len(res), 0)

        # List Role For User
        res = roles.OscRoles(job_config)\
            .list_roles_for_user(endpoint_array, user_id_new1, tenant_id_new1)
        print('list_roles_for_user')
        print(json.dumps(res))

        # Assertion
        self.assertGreaterEqual(len(res), 1)

        # Remove Role From User
        res = roles.OscRoles(job_config).remove_role_from_user(
                    endpoint_array, user_id_new1, tenant_id_new1, role_id)
        print('remove_role_from_user')
        print(json.dumps(res))

        # Assertion
        self.assertEqual(len(res), 0)

        # List Role For User
        res = roles.OscRoles(job_config)\
            .list_roles_for_user(endpoint_array, user_id_new1, tenant_id_new1)
        print('list_roles_for_user')
        print(json.dumps(res))

        # Assertion
        self.assertGreaterEqual(len(res), 1)

        # Delete User
        res = users.OscUsers(job_config)\
                                .delete_user(endpoint_array, user_id_new1)
        print('delete_user')
        print(json.dumps(res))

        # Delete User
        res = users.OscUsers(job_config)\
                                .delete_user(endpoint_array, user_id_new2)
        print('delete_user')
        print(json.dumps(res))

        # Assertion
        self.assertEqual(len(res), 0)

        # List Users
        res = users.OscUsers(job_config).list_users(
                        endpoint_array, users.OscUsers.DOMAIN_ID_DEFAULT)
        print('list_users')
        print(json.dumps(res))

        # Delete Tenant
        res = tenants.OscTenants(job_config)\
                                .delete_tenant(endpoint_array, tenant_id_new1)
        print('delete_tenant')
        print(json.dumps(res))

        res = tenants.OscTenants(job_config)\
                                .delete_tenant(endpoint_array, tenant_id_new2)
        print('delete_tenant')
        print(json.dumps(res))

        # Assertion
        self.assertEqual(len(res), 0)

    def test_tokens_create_token_validation_error(self):

        endpoint = self.ENDPOINT_URL
        admin_user_name = 'admin'
        admin_password = 'i-portal'

        job_config = config.JobConfig()

        try:
            tokens.OscTokens(job_config)\
                    .create_token('', admin_password, endpoint)

        except SystemError as e:
            if e.args[0] != tokens.OscTokens.EXCEPT_MSG01:
                raise

        try:
            tokens.OscTokens(job_config)\
                    .create_token(admin_user_name, '', endpoint)

        except SystemError as e:
            if e.args[0] != tokens.OscTokens.EXCEPT_MSG01:
                raise

        try:
            tokens.OscTokens(job_config)\
                    .create_token(admin_user_name, admin_password, '')

        except SystemError as e:
            if e.args[0] != tokens.OscTokens.EXCEPT_MSG01:
                raise

    def test_tokens_get_endpoints_validation_error(self):

        endpoint = self.ENDPOINT_URL
        admin_user_name = 'admin'
        admin_password = 'i-portal'
        tenant_id = self.ADMIN_TENANT_ID
        token = 'aaa'

        job_config = config.JobConfig()

        try:
            tokens.OscTokens(job_config).get_endpoints(
                '', token, admin_user_name, admin_password, tenant_id)

        except SystemError as e:
            if e.args[0] != tokens.OscTokens.EXCEPT_MSG01:
                raise

        try:
            tokens.OscTokens(job_config).get_endpoints(
                endpoint, '', admin_user_name, admin_password, tenant_id)

        except SystemError as e:
            if e.args[0] != tokens.OscTokens.EXCEPT_MSG01:
                raise

        try:
            tokens.OscTokens(job_config).get_endpoints(
                endpoint, token, '', admin_password, tenant_id)

        except SystemError as e:
            if e.args[0] != tokens.OscTokens.EXCEPT_MSG01:
                raise

        try:
            tokens.OscTokens(job_config).get_endpoints(
                endpoint, token, admin_user_name, '', tenant_id)

        except SystemError as e:
            if e.args[0] != tokens.OscTokens.EXCEPT_MSG01:
                raise

        try:
            tokens.OscTokens(job_config).get_endpoints(
                endpoint, token, admin_user_name, admin_password, '')

        except SystemError as e:
            if e.args[0] != tokens.OscTokens.EXCEPT_MSG01:
                raise

    def test_tenants_list_tenants_validation_error(self):

        job_config = config.JobConfig()

        try:
            tenants.OscTenants(job_config).list_tenants({})

        except SystemError as e:
            if e.args[0] != tenants.OscTenants.EXCEPT_MSG01:
                raise

    def test_tenants_get_tenant_validation_error(self):

        endpoint_array = {'token': {}}
        tenant_id = self.ADMIN_TENANT_ID

        job_config = config.JobConfig()

        try:
            tenants.OscTenants(job_config).get_tenant(
                                            {}, tenant_id)

        except SystemError as e:
            if e.args[0] != tenants.OscTenants.EXCEPT_MSG01:
                raise

        try:
            tenants.OscTenants(job_config).get_tenant(
                                            endpoint_array, '')

        except SystemError as e:
            if e.args[0] != tenants.OscTenants.EXCEPT_MSG01:
                raise

    def test_tenants_create_tenant_validation_error(self):

        endpoint_array = {'token': {}}
        tenant_name = 'test_tenant'

        job_config = config.JobConfig()

        try:
            tenants.OscTenants(job_config).create_tenant(
                                            {}, tenant_name)

        except SystemError as e:
            if e.args[0] != tenants.OscTenants.EXCEPT_MSG01:
                raise

        try:
            tenants.OscTenants(job_config).create_tenant(
                                            endpoint_array, '')

        except SystemError as e:
            if e.args[0] != tenants.OscTenants.EXCEPT_MSG01:
                raise

    def test_tenants_update_tenant_validation_error(self):

        endpoint_array = {'token': {}}
        tenant_id = self.ADMIN_TENANT_ID

        job_config = config.JobConfig()

        try:
            tenants.OscTenants(job_config).update_tenant(
                                            {}, tenant_id)

        except SystemError as e:
            if e.args[0] != tenants.OscTenants.EXCEPT_MSG01:
                raise

        try:
            tenants.OscTenants(job_config).update_tenant(
                                            endpoint_array, '')

        except SystemError as e:
            if e.args[0] != tenants.OscTenants.EXCEPT_MSG01:
                raise

        try:
            tenants.OscTenants(job_config).update_tenant(
                                            endpoint_array, tenant_id)

        except SystemError as e:
            if e.args[0] != tenants.OscTenants.EXCEPT_MSG01:
                raise

    def test_tenants_delete_tenant_validation_error(self):

        endpoint_array = {'token': {}}
        tenant_id = self.ADMIN_TENANT_ID

        job_config = config.JobConfig()

        try:
            tenants.OscTenants(job_config).delete_tenant(
                                            {}, tenant_id)

        except SystemError as e:
            if e.args[0] != tenants.OscTenants.EXCEPT_MSG01:
                raise

        try:
            tenants.OscTenants(job_config).delete_tenant(
                                            endpoint_array, '')

        except SystemError as e:
            if e.args[0] != tenants.OscTenants.EXCEPT_MSG01:
                raise

    def test_users_list_users_validation_error(self):

        job_config = config.JobConfig()

        try:
            users.OscUsers(job_config).list_users({})

        except SystemError as e:
            if e.args[0] != users.OscUsers.EXCEPT_MSG01:
                raise

    def test_users_get_user_validation_error(self):

        endpoint_array = {'token': {}}
        user_id = 'abcdefg'

        job_config = config.JobConfig()

        try:
            users.OscUsers(job_config).get_user({}, user_id)

        except SystemError as e:
            if e.args[0] != users.OscUsers.EXCEPT_MSG01:
                raise

        try:
            users.OscUsers(job_config).get_user(endpoint_array, '')

        except SystemError as e:
            if e.args[0] != users.OscUsers.EXCEPT_MSG01:
                raise

    def test_users_create_user_validation_error(self):

        endpoint_array = {'token': {}}
        tenant_id = self.ADMIN_TENANT_ID
        user_name = 'test_user'
        password = 'test_user'

        job_config = config.JobConfig()

        try:
            users.OscUsers(job_config).create_user(
                        {}, user_name, password, tenant_id)

        except SystemError as e:
            if e.args[0] != users.OscUsers.EXCEPT_MSG01:
                raise

        try:
            users.OscUsers(job_config).create_user(
                        endpoint_array, '', password, tenant_id)

        except SystemError as e:
            if e.args[0] != users.OscUsers.EXCEPT_MSG01:
                raise

        try:
            users.OscUsers(job_config).create_user(
                        endpoint_array, user_name, '', tenant_id)

        except SystemError as e:
            if e.args[0] != users.OscUsers.EXCEPT_MSG01:
                raise

        try:
            users.OscUsers(job_config).create_user(
                        endpoint_array, user_name, password, '')

        except SystemError as e:
            if e.args[0] != users.OscUsers.EXCEPT_MSG01:
                raise

    def test_users_update_user_validation_error(self):

        endpoint_array = {'token': {}}
        user_id = 'test_user'

        job_config = config.JobConfig()

        try:
            users.OscUsers(job_config).update_user({}, user_id)

        except SystemError as e:
            if e.args[0] != users.OscUsers.EXCEPT_MSG01:
                raise

        try:
            users.OscUsers(job_config).update_user(endpoint_array, '')

        except SystemError as e:
            if e.args[0] != users.OscUsers.EXCEPT_MSG01:
                raise

        try:
            users.OscUsers(job_config).update_user(endpoint_array, user_id)

        except SystemError as e:
            if e.args[0] != users.OscUsers.EXCEPT_MSG01:
                raise

    def test_users_delete_user_validation_error(self):

        endpoint_array = {'token': {}}
        user_id = 'test_user'

        job_config = config.JobConfig()

        try:
            users.OscUsers(job_config).delete_user({}, user_id)

        except SystemError as e:
            if e.args[0] != users.OscUsers.EXCEPT_MSG01:
                raise

        try:
            users.OscUsers(job_config).delete_user(endpoint_array, '')

        except SystemError as e:
            if e.args[0] != users.OscUsers.EXCEPT_MSG01:
                raise

    def test_roles_list_roles_validation_error(self):

        job_config = config.JobConfig()

        # Get Endpoints
        try:
            roles.OscRoles(job_config).list_roles({})

        except SystemError as e:
            if e.args[0] != roles.OscRoles.EXCEPT_MSG01:
                raise

    def test_roles_list_roles_for_user_validation_error(self):

        endpoint_array = {'token': {}}
        tenant_id = self.ADMIN_TENANT_ID
        user_id = 'test_user'

        job_config = config.JobConfig()

        try:
            roles.OscRoles(job_config).list_roles_for_user(
                                        {}, user_id, tenant_id)

        except SystemError as e:
            if e.args[0] != roles.OscRoles.EXCEPT_MSG01:
                raise

        try:
            roles.OscRoles(job_config).list_roles_for_user(
                                        endpoint_array, '', tenant_id)

        except SystemError as e:
            if e.args[0] != roles.OscRoles.EXCEPT_MSG01:
                raise

        try:
            roles.OscRoles(job_config).list_roles_for_user(
                                        endpoint_array, user_id, '')

        except SystemError as e:
            if e.args[0] != roles.OscRoles.EXCEPT_MSG01:
                raise

    def test_roles_add_role_for_user_validation_error(self):

        endpoint_array = {'token': {}}
        tenant_id = self.ADMIN_TENANT_ID
        user_id = 'test_user'
        role_id = 'test_role'

        job_config = config.JobConfig()

        try:
            roles.OscRoles(job_config).add_role_to_user(
                            {}, user_id, tenant_id, role_id)

        except SystemError as e:
            if e.args[0] != roles.OscRoles.EXCEPT_MSG01:
                raise

        try:
            roles.OscRoles(job_config).add_role_to_user(
                            endpoint_array, '', tenant_id, role_id)

        except SystemError as e:
            if e.args[0] != roles.OscRoles.EXCEPT_MSG01:
                raise

        try:
            roles.OscRoles(job_config).add_role_to_user(
                            endpoint_array, user_id, '', role_id)

        except SystemError as e:
            if e.args[0] != roles.OscRoles.EXCEPT_MSG01:
                raise

        try:
            roles.OscRoles(job_config).add_role_to_user(
                            endpoint_array, user_id, tenant_id, '')

        except SystemError as e:
            if e.args[0] != roles.OscRoles.EXCEPT_MSG01:
                raise

    def test_roles_remove_role_from_user_validation_error(self):

        endpoint_array = {'token': {}}
        tenant_id = self.ADMIN_TENANT_ID
        user_id = 'test_user'
        role_id = 'test_role'

        job_config = config.JobConfig()

        try:
            roles.OscRoles(job_config).remove_role_from_user(
                            {}, user_id, tenant_id, role_id)

        except SystemError as e:
            if e.args[0] != roles.OscRoles.EXCEPT_MSG01:
                raise

        try:
            roles.OscRoles(job_config).remove_role_from_user(
                            endpoint_array, '', tenant_id, role_id)

        except SystemError as e:
            if e.args[0] != roles.OscRoles.EXCEPT_MSG01:
                raise

        try:
            roles.OscRoles(job_config).remove_role_from_user(
                            endpoint_array, user_id, '', role_id)

        except SystemError as e:
            if e.args[0] != roles.OscRoles.EXCEPT_MSG01:
                raise

        try:
            roles.OscRoles(job_config).remove_role_from_user(
                            endpoint_array, user_id, tenant_id, '')

        except SystemError as e:
            if e.args[0] != roles.OscRoles.EXCEPT_MSG01:
                raise

    def test_keystone_endpoint_not_found(self):

        endpoint = self.ENDPOINT_URL
        admin_user_name = 'admin'
        admin_password = 'i-portal'
        tenant_id = self.ADMIN_TENANT_ID

        job_config = config.JobConfig()

        # Create Token
        token = tokens.OscTokens(job_config)\
                    .create_token(admin_user_name, admin_password, endpoint)

        # Get Endpoints
        endpoint_array = tokens.OscTokens(job_config).get_endpoints(
            endpoint, token, admin_user_name, admin_password, tenant_id)

        endpoint_array['region_id'] = 'regionNotfound'

        # Create Server
        try:
            tenants.OscTenants(job_config)\
                            .create_tenant(endpoint_array, 'tenant_name_new1')

        except SystemError as e:
            if e.args[0] != tenants.OscTenants.EXCEPT_MSG08:
                raise
