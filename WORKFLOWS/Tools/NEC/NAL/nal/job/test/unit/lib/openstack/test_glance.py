import unittest
import json

#sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../../../')
from job.conf import config
from job.lib.openstack.glance import images
from job.lib.openstack.keystone import tokens


class TestSelectAPI(unittest.TestCase):
    # Do a test of Select.

#     ENDPOINT_URL = 'http://10.58.79.171:35357/v3'
#     REGION_ID = 'RegionOne'
#     ADMIN_TENANT_ID = '8cc49b2e5ce04eebbcbfeb4eab05bd90'

    ENDPOINT_URL = 'http://localhost:80/rest_openstack/index.py/min/v3'
    REGION_ID = 'region_unit_test1'
    ADMIN_TENANT_ID = '9ba7d56906cc4d0cbe055e06971b12a7'

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

    def test_glance(self):

        endpoint = self.ENDPOINT_URL
        tenant_id = self.ADMIN_TENANT_ID
        admin_user_name = 'admin'
        admin_password = 'i-portal'

        job_config = config.JobConfig()

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

        endpoint_array['region_id'] = self.REGION_ID

        # Assertion
        self.assertGreaterEqual(len(endpoint_array), 1)

        # List Images
        res = images.OscGlanceImages(job_config).list_images(endpoint_array)
        print('list_images')
        print(json.dumps(res))

        # Assertion
        self.assertGreaterEqual(len(res), 1)

    def test_glance_endpoint_not_found(self):

        endpoint = self.ENDPOINT_URL
        tenant_id = self.ADMIN_TENANT_ID
        admin_user_name = 'admin'
        admin_password = 'i-portal'

        job_config = config.JobConfig()

        # Create Token
        token = tokens.OscTokens(job_config)\
                    .create_token(admin_user_name, admin_password, endpoint)

        # Assertion
        self.assertGreaterEqual(len(token), 1)

        # Get Endpoints
        endpoint_array = tokens.OscTokens(job_config).get_endpoints(
            endpoint, token, admin_user_name, admin_password, tenant_id)

        endpoint_array['region_id'] = 'regionNotfound'

        # Create Server
        try:
            images.OscGlanceImages(job_config).list_images(endpoint_array)

        except SystemError as e:
            if e.args[0] != images.OscGlanceImages.EXCEPT_MSG08:
                raise
