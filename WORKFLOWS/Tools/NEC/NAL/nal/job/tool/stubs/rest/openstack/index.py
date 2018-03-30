# -*- coding: utf-8 -*-

#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#  
#       http://www.apache.org/licenses/LICENSE-2.0
#  
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.
#  
#  COPYRIGHT  (C)  NEC  CORPORATION  2017
#  
import json
import os
import re
import sys
import traceback

sys.path.append(
    os.path.dirname(os.path.abspath(__file__)) + '/../../../../../')

from job.tool.stubs.rest.openstack.conf import config
from job.tool.stubs.rest.openstack.lib import utils


def application(environ, start_response):

    status = config.HTTP_STATUS_DEF['OK']
    response_headers = [('Content-type', 'application/json'),
                        ('charset', 'utf-8')]
    token = ''
    response_body = ''
    del_response_flg = False

    global error_path
    error_path = os.path.dirname(os.path.abspath(__file__)) \
                                                + '/log/error.log'
    global debug_path
    debug_path = os.path.dirname(os.path.abspath(__file__)) \
                                                + '/log/debug.log'

    try:

        # Get HTTP Method
        http_method = environ.get('REQUEST_METHOD')

        # Get URI
        uri = environ.get('REQUEST_URI')
        resource_info = uri.split('index.py/')
        resource_info = resource_info[-1].split('?')
        uri_params = resource_info[0].split('/')

        # Set ResponseFile Path
        location = uri_params.pop(0)
        response_dir = os.path.dirname(os.path.abspath(__file__)) \
                                        + '/response/' + location + '/'
        response_filename = http_method + '@' + '@'.join(uri_params)

        stub_url = environ.get('wsgi.url_scheme') + '://' \
            + environ.get('SERVER_NAME') + ':' \
            + environ.get('SERVER_PORT') \
            + environ.get('SCRIPT_NAME') + '/' + location

        # Get Parameters(Request Body)
        request_params = environ['wsgi.input'].read().decode('utf-8')
        if len(request_params) > 0:
            request_params = json.loads(request_params)

        # Set ResponseFile(Token)
        token = set_responsefile_token(
                response_dir, response_filename, request_params)

        # Set ResponseFile(Project)
        del_response_flg = set_responsefile_project(del_response_flg,
                response_dir, response_filename, request_params)

        # Set ResponseFile(User)
        del_response_flg = set_responsefile_user(del_response_flg,
                response_dir, response_filename, request_params)

        # Set ResponseFile(Role)
        del_response_flg = set_responsefile_role(del_response_flg,
                response_dir, response_filename, request_params)

        # Set ResponseFile(Network)
        del_response_flg = set_responsefile_network(del_response_flg,
                response_dir, response_filename, request_params)

        # Set ResponseFile(Subnet)
        del_response_flg = set_responsefile_subnet(del_response_flg,
                response_dir, response_filename, request_params)

        # Set ResponseFile(Port)
        del_response_flg = set_responsefile_port(del_response_flg,
                response_dir, response_filename, request_params)

        # Set ResponseFile(Server)
        del_response_flg = set_responsefile_server(del_response_flg,
                response_dir, response_filename, request_params, stub_url)

        response_path = response_dir + response_filename
        if os.path.exists(response_path):

            # Get Response Body
            with open(response_path, 'r') as f:
                response_body = f.read()

            # Delete ResponseFile
            if del_response_flg is True:
                os.remove(response_path)

        else:
            status = config.HTTP_STATUS_DEF['NOTFOUND']
            response_body = '{"error":"stub response file not found(' \
                + response_path.replace(
                                '\\', '\\\\').replace('"', '\\"') + ')"}'

            with open(error_path, 'w') as f:
                f.write(response_body)

    except:
        status = config.HTTP_STATUS_DEF['ERROR']
        response_body = '{"error":"' \
            + traceback.format_exc().replace(
                                '\\', '\\\\').replace('"', '\\"') + ')"}'

        with open(error_path, 'w') as f:
            f.write(response_body)

    # Return Response
    response_headers.append(('Content-Length', str(len(response_body))))

    if len(token) > 0:
        response_headers.append(('X-Subject-Token', token))

    start_response(status, response_headers)

    return [response_body.encode()]


def set_responsefile_token(
                response_dir, response_filename, request_params):

    token = ''
    response_path = response_dir + response_filename

    # When create_token Requested
    if response_filename == config.OS_RESPONSE_DEF['create_token']['file']:

        # Create Token
        token = utils.Utils().create_uuid(
                        config.CHAR_SET, config.SCRIPT_STDOUT_SEPARATER)

        # Get RequestParams
        project_id = utils.Utils().get_dict_value(request_params,
                                    ['auth', 'scope', 'project', 'id'])
        user_name = utils.Utils().get_dict_value(request_params,
                        ['auth', 'identity', 'password', 'user', 'name'])

        # Get ResponseParams
        with open(response_path, 'r') as f:
            response_content = f.read()
        response_params = json.loads(response_content)

        # Set ResponseParams
        if project_id is not None:
            response_params['token']['project']['id'] = project_id

        if user_name is not None:
            response_params['token']['user']['name'] = user_name

        # Update ResponseFile
        with open(response_path, 'w') as f:
            f.write(json.dumps(response_params))

    return token


def set_responsefile_project(del_response_flg,
                response_dir, response_filename, request_params):

    response_path = response_dir + response_filename

    # When list_tenants Requested
    if response_filename == config.OS_RESPONSE_DEF['list_tenants']['file']:

        if os.path.exists(response_path) == False:
            with open(response_path, 'w') as f:
                f.write(config.OS_RESPONSE_DEF['list_tenants']['resp'])

    # When create_tenant Requested
    elif response_filename == config.OS_RESPONSE_DEF['create_tenant']['file']:

        # Get ResponseParams(list_tenants)
        response_params_list_tenants = json.loads(config.OS_RESPONSE_DEF[
                                                    'list_tenants']['resp'])
        response_path_list_tenants = response_dir \
                            + config.OS_RESPONSE_DEF['list_tenants']['file']

        if os.path.exists(response_path_list_tenants):
            with open(response_path_list_tenants, 'r') as f:
                response_content = f.read()
            response_params_list_tenants = json.loads(response_content)

        # Create UUID
        project_id = utils.Utils().create_uuid(
                        config.CHAR_SET, config.SCRIPT_STDOUT_SEPARATER)

        # Set ResponseParams
        response_params_new_tenant = {'project': request_params['project']}
        response_params_new_tenant['project']['id'] = project_id
        response_params_new_tenant['project']['parent_id'] = request_params[
                                                        'project']['domain_id']
        response_params_new_tenant['project']['links'] = {'self': ''}
        response_params_new_tenant['project']['is_domain'] \
            = utils.Utils().get_dict_value(
                            request_params, ['project', 'is_domain'], False)

        # Update ResponseFile
        response_new_tenant = json.dumps(response_params_new_tenant)
        with open(response_path, 'w') as f:
            f.write(response_new_tenant)

        # Create ResponseFile(get_tenant)
        with open(response_dir \
            + config.OS_RESPONSE_DEF['get_tenant']['file'].replace(
                '%project_id%', project_id), 'w') as f:
            f.write(response_new_tenant)

        # Create ResponseFile(update_tenant)
        response_params_update_tenant = response_params_new_tenant
        response_params_update_tenant['project'].update({'extra': {}})
        with open(response_dir \
            + config.OS_RESPONSE_DEF['update_tenant']['file'].replace(
                '%project_id%', project_id), 'w') as f:
            f.write(json.dumps(response_params_update_tenant))

        # Create ResponseFile(delete_tenant)
        with open(response_dir \
            + config.OS_RESPONSE_DEF['delete_tenant']['file'].replace(
                '%project_id%', project_id), 'w') as f:
            f.write('')

        # Update ResponseFile(list_tenants)
        response_params_list_tenants['projects'].append(
                                        response_params_new_tenant['project'])

        with open(response_path_list_tenants, 'w') as f:
            f.write(json.dumps(response_params_list_tenants))

        # Create ResponseFile(create_user)
        response_params_create_user = json.loads(
                                config.OS_RESPONSE_DEF['create_user']['resp'])
        response_params_create_user['user']['id'] = config.OS_USER_ID_ADMIN
        response_params_create_user['user']['name'] = config.OS_USER_NAME_ADMIN
        response_params_create_user['user']['default_project_id'] = project_id

        with open(response_dir \
            + config.OS_RESPONSE_DEF['create_user']['file'], 'w') as f:
            f.write(json.dumps(response_params_create_user))

        # Create ResponseFile(get_user)
        with open(response_dir \
            + config.OS_RESPONSE_DEF['get_user']['file'].replace(
                '%user_id%', config.OS_USER_ID_ADMIN), 'w') as f:
            f.write(json.dumps(response_params_create_user))

        # Create ResponseFile(update_user)
        response_params_update_user = response_params_create_user
        response_params_update_user['user'].update({'extra': {}})
        with open(response_dir \
            + config.OS_RESPONSE_DEF['update_user']['file'].replace(
                '%user_id%', config.OS_USER_ID_ADMIN), 'w') as f:
            f.write(json.dumps(response_params_update_user))

        # Create ResponseFile(delete_user)
        with open(response_dir \
            + config.OS_RESPONSE_DEF['delete_user']['file'].replace(
                '%user_id%', config.OS_USER_ID_ADMIN), 'w') as f:
            f.write('')

        # Create/Update ResponseFile(list_users)
        response_path_list_users = response_dir \
                            + config.OS_RESPONSE_DEF['list_users']['file']
        if os.path.exists(response_path_list_users):
            with open(response_path_list_users, 'r') as f:
                response_content = f.read()
            response_params_list_users = json.loads(response_content)
        else:
            response_params_list_users = json.loads(config.OS_RESPONSE_DEF[
                                                    'list_users']['resp'])

        response_params_list_users['users'].append(
                                        response_params_create_user['user'])

        with open(response_path_list_users, 'w') as f:
            f.write(json.dumps(response_params_list_users))

        # Create ResponseFile(list_roles_for_user)
        with open(response_dir \
            + config.OS_RESPONSE_DEF['list_roles_for_user']['file'].replace(
                '%project_id%', project_id).replace(
                '%user_id%', config.OS_USER_ID_ADMIN), 'w') as f:
            f.write(config.OS_RESPONSE_DEF['list_roles_for_user']['resp'])

    # When update_tenant Requested
    matchOB = re.findall(
        config.OS_RESPONSE_DEF['update_tenant']['rexp'], response_filename)
    if len(matchOB) > 0:
        project_id = matchOB[0]

        # Get ResponseParams
        with open(response_path, 'r') as f:
            response_content = f.read()
        response_params_update_tenant = json.loads(response_content)

        # Update ResponseFile
        if 'name' in request_params['project']:
            response_params_update_tenant['project']['name'] \
                                        = request_params['project']['name']

        if 'description' in request_params['project']:
            response_params_update_tenant['project']['description'] \
                                = request_params['project']['description']

        if 'enabled' in request_params['project']:
            response_params_update_tenant['project']['enabled'] \
                                = request_params['project']['enabled']

        if 'domain_id' in request_params['project']:
            response_params_update_tenant['project']['domain_id'] \
                                = request_params['project']['domain_id']
            response_params_update_tenant['project']['parent_id'] \
                                = request_params['project']['domain_id']

        if 'is_domain' in request_params['project']:
            response_params_update_tenant['project']['is_domain'] \
                                = request_params['project']['is_domain']

        with open(response_path, 'w') as f:
            f.write(json.dumps(response_params_update_tenant))

        # Update ResponseFile(get_tenant)
        response_path_get_tenant = response_dir \
            + config.OS_RESPONSE_DEF['get_tenant']['file'].replace(
                '%project_id%', project_id)
        with open(response_path_get_tenant, 'r') as f:
            response_content = f.read()

        response_params_get_tenant = json.loads(response_content)
        response_params_get_tenant['project'] \
                                = response_params_update_tenant['project']
        del response_params_get_tenant['project']['extra']

        with open(response_path_get_tenant, 'w') as f:
            f.write(json.dumps(response_params_get_tenant))

        # Update ResponseFile(list_tenants)
        response_path_list_tenants = response_dir \
                            + config.OS_RESPONSE_DEF['list_tenants']['file']
        if os.path.exists(response_path_list_tenants):
            with open(response_path_list_tenants, 'r') as f:
                response_content = f.read()
            response_params_list_tenants = json.loads(response_content)

            for i, v in enumerate(response_params_list_tenants['projects']):
                if v['id'] == project_id:
                    response_params_list_tenants['projects'][i] \
                                        = response_params_get_tenant['project']
                    break

            with open(response_path_list_tenants, 'w') as f:
                f.write(json.dumps(response_params_list_tenants))

    # When delete_tenant Requested
    matchOB = re.findall(
        config.OS_RESPONSE_DEF['delete_tenant']['rexp'], response_filename)
    if len(matchOB) > 0:
        del_response_flg = True
        project_id = matchOB[0]

        # Delete ResponseFile(create_tenant)
        response_path_tenant = response_dir \
                            + config.OS_RESPONSE_DEF['create_tenant']['file']
        if os.path.exists(response_path_tenant):
            os.remove(response_path_tenant)

        # Delete ResponseFile(update_tenant)
        response_path_tenant = response_dir \
            + config.OS_RESPONSE_DEF['update_tenant']['file'].replace(
                                                '%project_id%', project_id)
        if os.path.exists(response_path_tenant):
            os.remove(response_path_tenant)

        # Delete ResponseFile(get_tenant)
        response_path_tenant = response_dir \
            + config.OS_RESPONSE_DEF['get_tenant']['file'].replace(
                                                '%project_id%', project_id)
        if os.path.exists(response_path_tenant):
            os.remove(response_path_tenant)

        # Delete ResponseFile(list_flavors)
        response_path_tenant = response_dir \
            + config.OS_RESPONSE_DEF['list_flavors']['file'].replace(
                                                '%project_id%', project_id)
        if os.path.exists(response_path_tenant):
            os.remove(response_path_tenant)

        # Update ResponseFile(list_tenants)
        response_path_list_tenants = response_dir \
                            + config.OS_RESPONSE_DEF['list_tenants']['file']

        with open(response_path_list_tenants, 'r') as f:
                response_content = f.read()
        response_params_list_tenants = json.loads(response_content)

        for i, v in enumerate(response_params_list_tenants['projects']):
            if v['id'] == project_id:
                response_params_list_tenants['projects'].pop(i)
                break

        with open(response_path_list_tenants, 'w') as f:
                f.write(json.dumps(response_params_list_tenants))

        # Delete ResponseFile(admin user)
        delete_responsefile_user_related(
                        response_dir, project_id, config.OS_USER_ID_ADMIN)

        response_path_user = response_dir \
                + config.OS_RESPONSE_DEF['delete_user']['file'].replace(
                '%user_id%', config.OS_USER_ID_ADMIN)
        if os.path.exists(response_path_user):
            os.remove(response_path_user)

    return del_response_flg


def set_responsefile_user(del_response_flg,
                response_dir, response_filename, request_params):

    response_path = response_dir + response_filename

    # When list_users Requested
    if response_filename == config.OS_RESPONSE_DEF['list_users']['file']:

        if os.path.exists(response_path) == False:
            with open(response_path, 'w') as f:
                f.write(config.OS_RESPONSE_DEF['list_users']['resp'])

    # When create_user Requested
    elif response_filename == config.OS_RESPONSE_DEF['create_user']['file']:

        # Get ResponseParams(list_users)
        response_params_list_users = json.loads(config.OS_RESPONSE_DEF[
                                                    'list_users']['resp'])
        response_path_list_users = response_dir \
                            + config.OS_RESPONSE_DEF['list_users']['file']
        if os.path.exists(response_path_list_users):
            with open(response_path_list_users, 'r') as f:
                response_content = f.read()
            response_params_list_users = json.loads(response_content)

        # Create UUID
        user_id = utils.Utils().create_uuid(
                            config.CHAR_SET, config.SCRIPT_STDOUT_SEPARATER)

        # Get project_id from RequestParams
        project_id = request_params['user']['default_project_id']

        # Set ResponseParams
        response_params_create_user = {'user': request_params['user']}
        response_params_create_user['user']['id'] = user_id
        response_params_create_user['user']['links'] = {'self': ''}
        response_params_create_user['user']['password_expires_at'] = None
        if 'email' not in response_params_create_user['user']:
            response_params_create_user['user']['email'] = ''
        del response_params_create_user['user']['password']

        # Update ResponseFile
        response_new_user = json.dumps(response_params_create_user)
        with open(response_path, 'w') as f:
            f.write(response_new_user)

        # Create ResponseFile(get_user)
        with open(response_dir \
            + config.OS_RESPONSE_DEF['get_user']['file'].replace(
                                        '%user_id%', user_id), 'w') as f:
            f.write(response_new_user)

        # Create ResponseFile(update_user)
        response_params_update_user = response_params_create_user
        response_params_update_user['user']['extra'] = {
                        'email': response_params_create_user['user']['email']}
        with open(response_dir \
            + config.OS_RESPONSE_DEF['update_user']['file'].replace(
                                        '%user_id%', user_id), 'w') as f:
            f.write(json.dumps(response_params_update_user))

        # Create ResponseFile(delete_user)
        with open(response_dir \
            + config.OS_RESPONSE_DEF['delete_user']['file'].replace(
                                        '%user_id%', user_id), 'w') as f:
            f.write('')

        # Update ResponseFile(list_users)
        response_params_list_users['users'].append(
                                        response_params_create_user['user'])

        with open(response_path_list_users, 'w') as f:
            f.write(json.dumps(response_params_list_users))

        # Create ResponseFile(list_roles_for_user)
        with open(response_dir \
            + config.OS_RESPONSE_DEF['list_roles_for_user']['file'].replace(
                '%project_id%', project_id).replace(
                '%user_id%', user_id), 'w') as f:
            f.write(config.OS_RESPONSE_DEF['list_roles_for_user']['resp'])

    # When update_user Requested
    matchOB = re.findall(
        config.OS_RESPONSE_DEF['update_user']['rexp'], response_filename)
    if len(matchOB) > 0:
        user_id = matchOB[0]

        # Get ResponseParams
        with open(response_path, 'r') as f:
            response_content = f.read()
        response_params_update_user = json.loads(response_content)

        # Update ResponseFile
        if 'name' in request_params['user']:
            response_params_update_user[
                        'user']['name'] = request_params['user']['name']

        if 'email' in request_params['user']:
            response_params_update_user[
                        'user']['email'] = request_params['user']['email']
            response_params_update_user[
                'user']['extra']['email'] = request_params['user']['email']

        if 'enabled' in request_params['user']:
            response_params_update_user[
                    'user']['enabled'] = request_params['user']['enabled']

        if 'domain_id' in request_params['user']:
            response_params_update_user[
                'user']['domain_id'] = request_params['user']['domain_id']

        if 'default_project_id' in request_params['user']:
            response_params_update_user[
            'user']['default_project_id'] = request_params[
                                            'user']['default_project_id']
        with open(response_path, 'w') as f:
            f.write(json.dumps(response_params_update_user))

        # Update ResponseFile(get_user)
        response_params_get_user = response_params_update_user
        del response_params_get_user['user']['extra']

        with open(response_dir \
            + config.OS_RESPONSE_DEF['get_user']['file'].replace(
                                        '%user_id%', user_id), 'w') as f:
            f.write(json.dumps(response_params_get_user))

        # Update ResponseFile(list_users)
        response_path_list_users = response_dir \
                            + config.OS_RESPONSE_DEF['list_users']['file']
        with open(response_path_list_users, 'r') as f:
            response_content = f.read()
        response_params_list_users = json.loads(response_content)

        for i, v in enumerate(response_params_list_users['users']):
            if v['id'] == user_id:
                response_params_list_users['users'][i] \
                                        = response_params_get_user['user']
                break

        with open(response_path_list_users, 'w') as f:
            f.write(json.dumps(response_params_list_users))

    # When delete_user Requested
    matchOB = re.findall(
        config.OS_RESPONSE_DEF['delete_user']['rexp'], response_filename)
    if len(matchOB) > 0:
        del_response_flg = True
        user_id = matchOB[0]

        # Get project_id from ResponseFile(get_user)
        response_path_user = response_dir \
            + config.OS_RESPONSE_DEF['get_user']['file'].replace(
                                        '%user_id%', user_id)
        with open(response_path_user, 'r') as f:
            response_content = f.read()
        response_params_get_user = json.loads(response_content)
        project_id = response_params_get_user['user']['default_project_id']

        # Delete ResponseFile(user)
        delete_responsefile_user_related(response_dir, project_id, user_id)

    return del_response_flg


def set_responsefile_role(del_response_flg,
                response_dir, response_filename, request_params):

    response_path = response_dir + response_filename

    # When list_roles_for_user Requested
    matchOB = re.findall(
        config.OS_RESPONSE_DEF[
                            'list_roles_for_user']['rexp'], response_filename)
    if len(matchOB) > 0:
        if os.path.exists(response_path) == False:
            with open(response_path, 'w') as f:
                f.write(config.OS_RESPONSE_DEF['list_roles_for_user']['resp'])

    # When add_role_to_user Requested
    matchOB = re.findall(
        config.OS_RESPONSE_DEF['add_role_to_user']['rexp'], response_filename)
    if len(matchOB) > 0:
        project_id = matchOB[0][0]
        user_id = matchOB[0][1]
        role_id = matchOB[0][2]

        # Create ResponseFile
        with open(response_path, 'w') as f:
            f.write('')

        # Create ResponseFile(remove_role_from_user)
        with open(response_dir \
            + config.OS_RESPONSE_DEF['remove_role_from_user']['file'].replace(
                '%project_id%', project_id).replace(
                '%user_id%', user_id).replace('%role_id%', role_id), 'w') as f:
            f.write('')

        # Get role name from ResponseFile(list_roles)
        with open(response_dir \
                  + config.OS_RESPONSE_DEF['list_roles']['file'], 'r') as f:
            response_content = f.read()
        response_params_list_roles = json.loads(response_content)

        role_name = ''
        for role in response_params_list_roles['roles']:
            if role['id'] == role_id:
                role_name = role['name']
                break

        # Update ResponseFile(list_roles_for_user)
        response_params_role = {'id': role_id,
                                'name': role_name,
                                'domain': None, 'links': {'self': ''}}
        response_path_list_roles_for_user = response_dir \
            + config.OS_RESPONSE_DEF['list_roles_for_user']['file'].replace(
                '%project_id%', project_id).replace(
                '%user_id%', user_id)

        if os.path.exists(response_path_list_roles_for_user):
            with open(response_path_list_roles_for_user, 'r') as f:
                response_content = f.read()
            response_params_list_roles_for_user = json.loads(response_content)
        else:
            response_params_list_roles_for_user = json.loads(
                        config.OS_RESPONSE_DEF['list_roles_for_user']['resp'])

        response_params_list_roles_for_user['roles'].append(
                                                        response_params_role)

        with open(response_path_list_roles_for_user, 'w') as f:
            f.write(json.dumps(response_params_list_roles_for_user))

    # When remove_role_from_user Requested
    matchOB = re.findall(
        config.OS_RESPONSE_DEF[
                        'remove_role_from_user']['rexp'], response_filename)
    if len(matchOB) > 0:
        del_response_flg = True
        project_id = matchOB[0][0]
        user_id = matchOB[0][1]
        role_id = matchOB[0][2]

        # Delete ResponseFile(add_role_to_user)
        os.remove(response_dir \
            + config.OS_RESPONSE_DEF['add_role_to_user']['file'].replace(
                '%project_id%', project_id).replace(
                '%user_id%', user_id).replace('%role_id%', role_id))

        # Update ResponseFile(list_roles_for_user)
        response_path_list_roles_for_user = response_dir \
            + config.OS_RESPONSE_DEF['list_roles_for_user']['file'].replace(
                '%project_id%', project_id).replace(
                '%user_id%', user_id)

        with open(response_path_list_roles_for_user, 'r') as f:
            response_content = f.read()
        response_params_list_roles_for_user = json.loads(response_content)

        for i, v in enumerate(response_params_list_roles_for_user['roles']):
            if v['id'] == role_id:
                response_params_list_roles_for_user['roles'].pop(i)

        with open(response_path_list_roles_for_user, 'w') as f:
            f.write(json.dumps(response_params_list_roles_for_user))

    return del_response_flg


def set_responsefile_network(del_response_flg,
                response_dir, response_filename, request_params):

    response_path = response_dir + response_filename

    # Get project_id from ResponseFile(create_token)
    with open(response_dir \
            + config.OS_RESPONSE_DEF['create_token']['file'], 'r') as f:
        response_content = f.read()
    response_params_token = json.loads(response_content)
    project_id = response_params_token['token']['project']['id']

    # When list_networks Requested
    if response_filename == config.OS_RESPONSE_DEF['list_networks']['file']:
        if os.path.exists(response_path) == False:
            with open(response_path, 'w') as f:
                f.write(config.OS_RESPONSE_DEF['list_networks']['resp'])

    # When create_network Requested
    elif response_filename == config.OS_RESPONSE_DEF['create_network']['file']:

        # Get ResponseParams(list_networks)
        response_params_list_networks = json.loads(
                        config.OS_RESPONSE_DEF['list_networks']['resp'])

        response_path_list_networks = response_dir \
            + config.OS_RESPONSE_DEF['list_networks']['file']

        if os.path.exists(response_path_list_networks):
            with open(response_path_list_networks, 'r') as f:
                response_content = f.read()
            response_params_list_networks = json.loads(response_content)

        # Create UUID
        network_id = utils.Utils().create_uuid(
                            config.CHAR_SET, config.SCRIPT_STDOUT_SEPARATER)

        # Set ResponseParams
        segmentation_id = config.OS_NETWORK_SEGMENT_ID_INI
        segmentation_id_max = 0
        for network in response_params_list_networks['networks']:

            provider_segmentation_id = network.get(
                                        'provider:segmentation_id', None)
            if provider_segmentation_id is None:
                provider_segmentation_id = 0
            if isinstance(provider_segmentation_id, int) == False:
                continue

            if provider_segmentation_id > segmentation_id_max:
                segmentation_id_max = network['provider:segmentation_id']

        if segmentation_id_max > segmentation_id:
            segmentation_id = segmentation_id_max + 1

        response_params = {'network': request_params['network']}
        response_params['network']['id'] = network_id
        response_params['network']['project_id'] = project_id
        response_params['network']['project_id'] = project_id
        response_params['network']['created_at'] = utils.Utils().get_sysdate()
        response_params['network']['updated_at'] = response_params[
                                                'network']['created_at']
        response_params['network']['availability_zone_hints'] = []
        response_params['network']['availability_zones'] = []
        response_params['network']['description'] = ''
        response_params['network']['ipv4_address_scope'] = None
        response_params['network']['ipv6_address_scope'] = None
        response_params['network']['mtu'] = config.OS_NETWORK_MTU
        response_params['network']['revision_number'] = 1
        response_params['network']['router:external'] = False
        response_params['network']['shared'] = False
        response_params['network']['status'] = config.OS_NETWORK_STATUS
        response_params['network']['subnets'] = []
        response_params['network']['tags'] = []

        response_params['network']['provider:network_type'] \
            = request_params['network'].get('provider:network_type', None)

        response_params['network']['provider:physical_network'] \
            = request_params['network'].get('provider:physical_network', None)

        response_params['network']['provider:segmentation_id'] \
            = request_params['network'].get(
                                'provider:segmentation_id', segmentation_id)

        # Create ResponseFile
        with open(response_path, 'w') as f:
            f.write(json.dumps(response_params))

        # Create ResponseFile(get_network)
        with open(response_dir \
            + config.OS_RESPONSE_DEF['get_network']['file'].replace(
                '%network_id%', network_id), 'w') as f:
            f.write(json.dumps(response_params))

        # Create ResponseFile(delete_network)
        with open(response_dir \
            + config.OS_RESPONSE_DEF['delete_network']['file'].replace(
                '%network_id%', network_id), 'w') as f:
            f.write('')

        # Update ResponseFile(list_networks)
        response_params_list_networks['networks'].append(
                                                request_params['network'])
        with open(response_path_list_networks, 'w') as f:
            f.write(json.dumps(response_params_list_networks))

    # When delete_network Requested
    matchOB = re.findall(
        config.OS_RESPONSE_DEF['delete_network']['rexp'], response_filename)
    if len(matchOB) > 0:
        del_response_flg = True
        network_id = matchOB[0]

        # Delete ResponseFile(create_network)
        response_path_network = response_dir \
            + config.OS_RESPONSE_DEF['create_network']['file']
        if os.path.exists(response_path_network):
            os.remove(response_path_network)

        # Delete ResponseFile(get_network)
        response_path_network = response_dir \
            + config.OS_RESPONSE_DEF['get_network']['file'].replace(
                '%network_id%', network_id)
        if os.path.exists(response_path_network):
            os.remove(response_path_network)

        # Update ResponseFile(list_networks)
        response_path_list_networks = response_dir \
            + config.OS_RESPONSE_DEF['list_networks']['file']

        if os.path.exists(response_path_list_networks):
            with open(response_path_list_networks, 'r') as f:
                response_content = f.read()
            response_params_list_networks = json.loads(response_content)

            for i, v in enumerate(response_params_list_networks['networks']):
                if v['id'] == network_id:
                    response_params_list_networks['networks'].pop(i)
                    break

            with open(response_path_list_networks, 'w') as f:
                    f.write(json.dumps(response_params_list_networks))

        # Delete ResponseFile(subnet)
        response_path_list_subnets = response_dir \
            + config.OS_RESPONSE_DEF['list_subnets']['file']

        if os.path.exists(response_path_list_subnets):
            with open(response_path_list_subnets, 'r') as f:
                response_content = f.read()
            response_params_list_subnets = json.loads(response_content)

            for i, v in enumerate(response_params_list_subnets['subnets']):
                if v['network_id'] == network_id:

                    # Delete ResponseFile(create_subnet)
                    response_path_subnet = response_dir \
                        + config.OS_RESPONSE_DEF['create_subnet']['file']
                    if os.path.exists(response_path_subnet):
                        os.remove(response_path_subnet)

                    # Delete ResponseFile(get_subnet)
                    response_path_subnet = response_dir \
                        + config.OS_RESPONSE_DEF['get_subnet']['file'].replace(
                            '%subnet_id%', v['id'])
                    if os.path.exists(response_path_subnet):
                        os.remove(response_path_subnet)

                    # Delete ResponseFile(delete_subnet)
                    response_path_subnet = response_dir \
                        + config.OS_RESPONSE_DEF['delete_subnet']['file']\
                            .replace('%subnet_id%', v['id'])
                    if os.path.exists(response_path_subnet):
                        os.remove(response_path_subnet)

                    response_params_list_subnets['subnets'].pop(i)
                    break

            # Update ResponseFile(list_subnets)
            with open(response_path_list_subnets, 'w') as f:
                    f.write(json.dumps(response_params_list_subnets))

        # Delete ResponseFile(port)
        response_path_list_ports = response_dir \
            + config.OS_RESPONSE_DEF['list_ports']['file']

        if os.path.exists(response_path_list_ports):
            with open(response_path_list_ports, 'r') as f:
                response_content = f.read()
            response_params_list_ports = json.loads(response_content)

            for i, v in enumerate(response_params_list_ports['ports']):
                if v['network_id'] == network_id:

                    # Delete ResponseFile(create_port)
                    response_path_port = response_dir \
                        + config.OS_RESPONSE_DEF['create_port']['file']
                    if os.path.exists(response_path_port):
                        os.remove(response_path_port)

                    # Delete ResponseFile(get_port)
                    response_path_port = response_dir \
                    + config.OS_RESPONSE_DEF['get_port']['file'].replace(
                            '%port_id%', v['id'])
                    if os.path.exists(response_path_port):
                        os.remove(response_path_port)

                    # Delete ResponseFile(update_port)
                    response_path_port = response_dir \
                    + config.OS_RESPONSE_DEF['update_port']['file'].replace(
                            '%port_id%', v['id'])
                    if os.path.exists(response_path_port):
                        os.remove(response_path_port)

                    # Delete ResponseFile(delete_port)
                    response_path_port = response_dir \
                    + config.OS_RESPONSE_DEF['delete_port']['file'].replace(
                            '%port_id%', v['id'])
                    if os.path.exists(response_path_port):
                        os.remove(response_path_port)

                    response_params_list_ports['ports'].pop(i)
                    break

            # Update ResponseFile(list_ports)
            with open(response_path_list_ports, 'w') as f:
                    f.write(json.dumps(response_params_list_ports))

    return del_response_flg


def set_responsefile_subnet(del_response_flg,
                response_dir, response_filename, request_params):

    response_path = response_dir + response_filename

    # Get project_id from ResponseFile(create_token)
    with open(response_dir \
            + config.OS_RESPONSE_DEF['create_token']['file'], 'r') as f:
        response_content = f.read()
    response_params_token = json.loads(response_content)
    project_id = response_params_token['token']['project']['id']

    # When list_subnets Requested
    if response_filename == config.OS_RESPONSE_DEF['list_subnets']['file']:
        if os.path.exists(response_path) == False:
            with open(response_path, 'w') as f:
                f.write(config.OS_RESPONSE_DEF['list_subnets']['resp'])

    # When create_subnet Requested
    elif response_filename == config.OS_RESPONSE_DEF['create_subnet']['file']:

        # Get ResponseParams(list_subnets)
        response_params_list_subnets = json.loads(
                        config.OS_RESPONSE_DEF['list_subnets']['resp'])

        response_path_list_subnets = response_dir \
            + config.OS_RESPONSE_DEF['list_subnets']['file']

        if os.path.exists(response_path_list_subnets):
            with open(response_path_list_subnets, 'r') as f:
                response_content = f.read()
            response_params_list_subnets = json.loads(response_content)

        # Create UUID
        subnet_id = utils.Utils().create_uuid(
                            config.CHAR_SET, config.SCRIPT_STDOUT_SEPARATER)

        # Get RequestParams
        network_id = request_params['subnet']['network_id']
        gateway_ip = request_params['subnet']['gateway_ip']
        cidr = request_params['subnet']['cidr']

        # Set ResponseParams
        response_params = {'subnet': request_params['subnet']}
        response_params['subnet']['id'] = subnet_id
        response_params['subnet']['ip_version'] \
                            = int(request_params['subnet']['ip_version'])
        response_params['subnet']['created_at'] = utils.Utils().get_sysdate()
        response_params['subnet']['updated_at'] = response_params[
                                                'subnet']['created_at']
        response_params['subnet']['description'] = ''
        response_params['subnet']['ipv6_address_mode'] = None
        response_params['subnet']['ipv6_ra_mode'] = None
        response_params['subnet']['revision_number'] = 1
        response_params['subnet']['service_types'] = []
        response_params['subnet']['subnetpool_id'] = None

        response_params['subnet']['name'] = request_params[
                                                'subnet'].get('name', '')
        response_params['subnet']['project_id'] = request_params[
                                    'subnet'].get('project_id', project_id)
        response_params['subnet']['allocation_pools'] = request_params[
                                    'subnet'].get('allocation_pools', [])
        response_params['subnet']['host_routes'] = request_params[
                                        'subnet'].get('host_routes', [])
        response_params['subnet']['dns_nameservers'] = request_params[
                                    'subnet'].get('dns_nameservers', [])

        if len(response_params['subnet']['allocation_pools']) == 0:
            allocation = utils.Utils().get_nw_from_cidr(cidr, gateway_ip)
            response_params['subnet']['allocation_pools'] = []
            response_params['subnet']['allocation_pools'].append(
                                            {'start': allocation['start'],
                                             'end': allocation['end']})

        # Create ResponseFile
        with open(response_path, 'w') as f:
            f.write(json.dumps(response_params))

        # Create ResponseFile(get_subnet)
        with open(response_dir \
            + config.OS_RESPONSE_DEF['get_subnet']['file'].replace(
                '%subnet_id%', subnet_id), 'w') as f:
            f.write(json.dumps(response_params))

        # Create ResponseFile(delete_subnet)
        with open(response_dir \
            + config.OS_RESPONSE_DEF['delete_subnet']['file'].replace(
                '%subnet_id%', subnet_id), 'w') as f:
            f.write('')

        # Update ResponseFile(list_subnets)
        response_params_list_subnets['subnets'].append(
                                            response_params['subnet'])

        with open(response_path_list_subnets, 'w') as f:
            f.write(json.dumps(response_params_list_subnets))

        # Update ResponseFile(get_network)
        response_path_get_network = response_dir \
            + config.OS_RESPONSE_DEF['get_network']['file'].replace(
                '%network_id%', network_id)

        with open(response_path_get_network, 'r') as f:
            response_content = f.read()
        response_params_get_network = json.loads(response_content)

        response_params_get_network['network']['subnets'].append(
                                                            subnet_id)
        with open(response_path_get_network, 'w') as f:
            f.write(json.dumps(response_params_get_network))

        # Update ResponseFile(list_networks)
        response_path_list_networks = response_dir \
            + config.OS_RESPONSE_DEF['list_networks']['file']

        with open(response_path_list_networks, 'r') as f:
            response_content = f.read()
        response_params_list_networks = json.loads(response_content)

        for i, v in enumerate(response_params_list_networks['networks']):
            if v['id'] == network_id:
                response_params_list_networks['networks'][i]['subnets']\
                                                        .append(subnet_id)
                break

        with open(response_path_list_networks, 'w') as f:
            f.write(json.dumps(response_params_list_networks))

    # When delete_subnet Requested
    matchOB = re.findall(
        config.OS_RESPONSE_DEF['delete_subnet']['rexp'], response_filename)
    if len(matchOB) > 0:
        del_response_flg = True
        subnet_id = matchOB[0]

        # Get network_id From ResponseFile(get_subnet)
        response_path_get_subnet = response_dir \
            + config.OS_RESPONSE_DEF['get_subnet']['file'].replace(
                '%subnet_id%', subnet_id)

        with open(response_path_get_subnet, 'r') as f:
            response_content = f.read()
        response_params_get_subnet = json.loads(response_content)

        network_id = response_params_get_subnet['subnet']['network_id']

        # Delete ResponseFile(create_subnet)
        response_path_subnet = response_dir \
            + config.OS_RESPONSE_DEF['create_subnet']['file']
        if os.path.exists(response_path_subnet):
            os.remove(response_path_subnet)

        # Delete ResponseFile(get_subnet)
        response_path_subnet = response_dir \
            + config.OS_RESPONSE_DEF['get_subnet']['file'].replace(
                '%subnet_id%', subnet_id)
        if os.path.exists(response_path_subnet):
            os.remove(response_path_subnet)

        # Update ResponseFile(list_subnets)
        response_path_list_subnets = response_dir \
            + config.OS_RESPONSE_DEF['list_subnets']['file']

        with open(response_path_list_subnets, 'r') as f:
            response_content = f.read()
        response_params_list_subnets = json.loads(response_content)

        for i, v in enumerate(response_params_list_subnets['subnets']):
            if v['id'] == subnet_id:
                response_params_list_subnets['subnets'].pop(i)
                break

        with open(response_path_list_subnets, 'w') as f:
            f.write(json.dumps(response_params_list_subnets))

        # Update ResponseFile(get_network)
        response_path_get_network = response_dir \
            + config.OS_RESPONSE_DEF['get_network']['file'].replace(
                '%network_id%', network_id)

        with open(response_path_get_network, 'r') as f:
            response_content = f.read()
        response_params_get_network = json.loads(response_content)

        for i, v in enumerate(
                    response_params_get_network['network']['subnets']):
            if v == subnet_id:
                response_params_get_network['network']['subnets'].pop(i)
                break

        with open(response_path_get_network, 'w') as f:
            f.write(json.dumps(response_params_get_network))

        # Update ResponseFile(list_networks)
        response_path_list_networks = response_dir \
            + config.OS_RESPONSE_DEF['list_networks']['file']

        with open(response_path_list_networks, 'r') as f:
            response_content = f.read()
        response_params_list_networks = json.loads(response_content)

        for i, v in enumerate(response_params_list_networks['networks']):
            if v['id'] == network_id:
                for i_subnet, v_subnet in enumerate(v['subnets']):
                    if v_subnet == subnet_id:
                        response_params_list_networks[
                                'networks'][i]['subnets'].pop(i_subnet)
                        break
                break

        with open(response_path_list_networks, 'w') as f:
            f.write(json.dumps(response_params_list_networks))

    return del_response_flg


def set_responsefile_port(del_response_flg,
                response_dir, response_filename, request_params):

    response_path = response_dir + response_filename

    # Get project_id from ResponseFile(create_token)
    with open(response_dir \
            + config.OS_RESPONSE_DEF['create_token']['file'], 'r') as f:
        response_content = f.read()
    response_params_token = json.loads(response_content)
    project_id = response_params_token['token']['project']['id']

    # When list_ports Requested
    if response_filename == config.OS_RESPONSE_DEF['list_ports']['file']:
        if os.path.exists(response_path) == False:
            with open(response_path, 'w') as f:
                f.write(config.OS_RESPONSE_DEF['list_ports']['resp'])

    # When create_port Requested
    elif response_filename == config.OS_RESPONSE_DEF['create_port']['file']:

        # Get RequestParams
        network_id = request_params['port']['network_id']

        # Get RequestParams(list_ports)
        response_params_list_ports = json.loads(
                config.OS_RESPONSE_DEF['list_ports']['resp'])

        response_path_list_ports = response_dir \
                + config.OS_RESPONSE_DEF['list_ports']['file']

        if os.path.exists(response_path_list_ports):
            with open(response_path_list_ports, 'r') as f:
                response_content = f.read()
            response_params_list_ports = json.loads(response_content)

        # Create UUID
        port_id = utils.Utils().create_uuid(
                            config.CHAR_SET, config.SCRIPT_STDOUT_SEPARATER)

        # Set ResponseParams
        response_params = {'port': request_params['port']}
        response_params['port']['id'] = port_id
        response_params['port']['project_id'] = project_id
        response_params['port']['created_at'] = utils.Utils().get_sysdate()
        response_params['port']['updated_at'] = response_params[
                                                        'port']['created_at']

        response_params['port']['allowed_address_pairs'] = []
        response_params['port']['description'] = ''
        response_params['port']['extra_dhcp_opts'] = []
        response_params['port']['binding:profile'] = {}
        response_params['port']['binding:vif_details'] = {}
        response_params['port']['binding:vif_type'] = config.OS_VIF_TYPE
        response_params['port']['revision_number'] = 1
        response_params['port']['status'] = config.OS_PORT_STATUS

        response_params['port']['name'] = request_params[
                                                    'port'].get('name', '')
        response_params['port']['fixed_ips'] = request_params[
                                                'port'].get('fixed_ips', [])
        response_params['port']['mac_address'] = request_params[
                'port'].get('mac_address', utils.Utils().create_mac_address())
        response_params['port']['device_id'] = request_params[
                                                'port'].get('device_id', '')
        response_params['port']['device_owner'] = request_params[
                                            'port'].get('device_owner', '')
        response_params['port']['security_groups'] = request_params[
                                            'port'].get('security_groups', [])
        response_params['port']['binding:host_id'] = request_params[
                            'port'].get('binding:host_id', config.OS_HOST_ID)
        response_params['port']['binding:vnic_type'] = request_params[
                        'port'].get('binding:vnic_type', config.OS_VNIC_TYPE)

        response_params['port']['fixed_ips'] \
            = set_response_params_port_fixed_ips(response_dir, network_id,
            response_params['port']['fixed_ips'], response_params_list_ports)

        # Create ResponseFile
        with open(response_path, 'w') as f:
            f.write(json.dumps(response_params))

        # Create ResponseFile(get_port)
        with open(response_dir \
            + config.OS_RESPONSE_DEF['get_port']['file'].replace(
                '%port_id%', port_id), 'w') as f:
            f.write(json.dumps(response_params))

        # Create ResponseFile(update_port)
        with open(response_dir \
            + config.OS_RESPONSE_DEF['update_port']['file'].replace(
                '%port_id%', port_id), 'w') as f:
            f.write(json.dumps(response_params))

        # Create ResponseFile(delete_port)
        with open(response_dir \
            + config.OS_RESPONSE_DEF['delete_port']['file'].replace(
                '%port_id%', port_id), 'w') as f:
            f.write('')

        # Create ResponseFile(list_ports)
        response_params_list_ports['ports'].append(response_params['port'])
        with open(response_path_list_ports, 'w') as f:
            f.write(json.dumps(response_params_list_ports))

    # When update_port Requested
    matchOB = re.findall(
        config.OS_RESPONSE_DEF['update_port']['rexp'], response_filename)
    if len(matchOB) > 0:
        port_id = matchOB[0]

        # Get ResponseFile
        with open(response_path, 'r') as f:
            response_content = f.read()
        response_params = json.loads(response_content)

        # Get ResponseFile(get_port)
        response_path_get_port = response_dir \
            + config.OS_RESPONSE_DEF['get_port']['file'].replace(
                '%port_id%', port_id)

        with open(response_path_get_port, 'r') as f:
            response_content = f.read()
        response_params_get_port = json.loads(response_content)

        # Get RequestParams(list_ports)
        response_path_list_ports = response_dir \
                + config.OS_RESPONSE_DEF['list_ports']['file']
        with open(response_path_list_ports, 'r') as f:
            response_content = f.read()
        response_params_list_ports = json.loads(response_content)

        # Set ResponseParams
        if 'name' in request_params['port']:
            response_params['port']['name'] = request_params['port']['name']
            response_params_get_port['port']['name'] \
                                            = request_params['port']['name']

        if 'admin_state_up' in request_params['port']:
            response_params['port']['admin_state_up'] \
                            = request_params['port']['admin_state_up']
            response_params_get_port['port']['admin_state_up'] \
                            = request_params['port']['admin_state_up']

        if 'fixed_ips' in request_params['port']:
            response_params['port']['fixed_ips'] \
                = set_response_params_port_fixed_ips(response_dir,
                                response_params_get_port['port']['network_id'],
                                        request_params['port']['fixed_ips'],
                                                response_params_list_ports)
            response_params_get_port['port']['fixed_ips'] \
                                        = response_params['port']['fixed_ips']

        if 'mac_address' in request_params['port']:
            response_params['port']['mac_address'] \
                            = request_params['port']['mac_address']
            response_params_get_port['port']['mac_address'] \
                            = request_params['port']['mac_address']

        if 'device_id' in request_params['port']:
            response_params['port']['device_id'] \
                            = request_params['port']['device_id']
            response_params_get_port['port']['device_id'] \
                            = request_params['port']['device_id']

        if 'device_owner' in request_params['port']:
            response_params['port']['device_owner'] \
                            = request_params['port']['device_owner']
            response_params_get_port['port']['device_owner'] \
                            = request_params['port']['device_owner']

        if 'security_groups' in request_params['port']:
            response_params['port']['security_groups'] \
                            = request_params['port']['security_groups']
            response_params_get_port['port']['security_groups'] \
                            = request_params['port']['security_groups']

        if 'binding:host_id' in request_params['port']:
            response_params['port']['binding:host_id'] \
                            = request_params['port']['binding:host_id']
            response_params_get_port['port']['binding:host_id'] \
                            = request_params['port']['binding:host_id']

        if 'binding:vnic_type' in request_params['port']:
            response_params['port']['binding:vnic_type'] \
                            = request_params['port']['binding:vnic_type']
            response_params_get_port['port']['binding:vnic_type'] \
                            = request_params['port']['binding:vnic_type']

        # Update ResponseFile
        with open(response_path, 'w') as f:
            f.write(json.dumps(response_params))

        # Update ResponseFile(get_port)
        with open(response_path_get_port, 'w') as f:
            f.write(json.dumps(response_params_get_port))

        # Update ResponseFile(list_ports)
        for i, v in enumerate(response_params_list_ports['ports']):
            if v['id'] == port_id:
                response_params_list_ports['ports'][i] \
                                = response_params_get_port['port']
                break

        with open(response_path_list_ports, 'w') as f:
            f.write(json.dumps(response_params_list_ports))

    # When delete_port Requested
    matchOB = re.findall(
        config.OS_RESPONSE_DEF['delete_port']['rexp'], response_filename)
    if len(matchOB) > 0:
        del_response_flg = True
        port_id = matchOB[0]

        # Delete ResponseFile(create_port)
        response_path_port = response_dir \
            + config.OS_RESPONSE_DEF['create_port']['file']
        if os.path.exists(response_path_port):
            os.remove(response_path_port)

        # Delete ResponseFile(get_port)
        response_path_port = response_dir \
            + config.OS_RESPONSE_DEF['get_port']['file'].replace(
                '%port_id%', port_id)
        if os.path.exists(response_path_port):
            os.remove(response_path_port)

        # Delete ResponseFile(update_port)
        response_path_port = response_dir \
            + config.OS_RESPONSE_DEF['update_port']['file'].replace(
                '%port_id%', port_id)
        if os.path.exists(response_path_port):
            os.remove(response_path_port)

        # Update ResponseFile(list_ports)
        response_path_list_ports = response_dir \
            + config.OS_RESPONSE_DEF['list_ports']['file']

        with open(response_path_list_ports, 'r') as f:
            response_content = f.read()
        response_params_list_ports = json.loads(response_content)

        for i, v in enumerate(response_params_list_ports['ports']):
            if v['id'] == port_id:
                response_params_list_ports['ports'].pop(i)
                break

        with open(response_path_list_ports, 'w') as f:
            f.write(json.dumps(response_params_list_ports))

    return del_response_flg


def set_responsefile_server(del_response_flg,
                response_dir, response_filename, request_params, stub_url):

    response_path = response_dir + response_filename

    # When list_servers Requested
    matchOB = re.findall(
        config.OS_RESPONSE_DEF['list_servers']['rexp'], response_filename)
    if len(matchOB) > 0:

        # Create ReaponseFile(list_servers)
        if os.path.exists(response_path) == False:
            with open(response_path, 'w') as f:
                f.write(config.OS_RESPONSE_DEF['list_servers']['resp'])

    # When list_flavors Requested
    matchOB = re.findall(
        config.OS_RESPONSE_DEF['list_flavors']['rexp'], response_filename)
    if len(matchOB) > 0:
        project_id = matchOB[0]

        # Create ReaponseFile(list_flavors)
        if os.path.exists(response_path) == False:
            with open(response_dir \
                + config.OS_RESPONSE_DEF['list_flavors']['file'], 'r') as f:
                response_content = f.read()
            with open(response_path, 'w') as f:
                f.write(response_content.replace(
                '%stub_url%', stub_url).replace('%project_id%', project_id))

    # When create_server Requested
    matchOB = re.findall(
        config.OS_RESPONSE_DEF['create_server']['rexp'], response_filename)
    if len(matchOB) > 0:
        project_id = matchOB[0]

        # Get RequestParams(list_servers)
        response_params_list_servers = json.loads(
                        config.OS_RESPONSE_DEF['list_servers']['resp'])

        response_path_list_servers = response_dir \
            + config.OS_RESPONSE_DEF['list_servers']['file'].replace(
                '%project_id%', project_id)

        if os.path.exists(response_path_list_servers):
            with open(response_path_list_servers, 'r') as f:
                response_content = f.read()
            response_params_list_servers = json.loads(response_content)

        # Create UUID
        server_id = utils.Utils().create_uuid(
                            config.CHAR_SET, config.SCRIPT_STDOUT_SEPARATER)

        # Get RequestParams
        name = request_params['server']['name']
        image_ref = request_params['server']['imageRef']
        flavor_ref = request_params['server']['flavorRef']
        networks = request_params['server']['networks']

        security_groups = request_params['server'].get(
                                    'security_groups', {'name': 'default'})
        availability_zone = request_params['server'].get(
                            'availability_zone', config.OS_AVAILABILITY_ZONE)

        config_drive = request_params['server'].get('config_drive', '')
        key_name = request_params['server'].get('key_name', None)
        metadata = request_params['server'].get('metadata', [])

        # Get user_id from ResponseParams(create_token)
        with open(response_dir \
                  + config.OS_RESPONSE_DEF['create_token']['file'], 'r') as f:
            response_content = f.read()
        response_params_token = json.loads(response_content)
        user_id = response_params_token['token']['user']['id']

        # Create ReaponseFile(list_flavors)
        response_path_list_flavors \
            = config.OS_RESPONSE_DEF['list_flavors']['file'].replace(
                                                '%project_id%', project_id)
        if os.path.exists(response_path_list_flavors) == False:
            with open(response_dir \
                + config.OS_RESPONSE_DEF['list_flavors']['file'], 'r') as f:
                response_content = f.read()
            with open(response_path_list_flavors, 'w') as f:
                f.write(response_content.replace(
                '%stub_url%', stub_url).replace('%project_id%', project_id))

        # Get Flavor From ResponseParams(list_flavors)
        with open(response_path_list_flavors, 'r') as f:
            response_content = f.read()
        response_params_list_flavors = json.loads(response_content)

        flavor_info = []
        for flavor in response_params_list_flavors['flavors']:
            if flavor['id'] == flavor_ref:
                flavor_info = flavor

        # Set Address, InterfaceAttachments
        addresses = {}
        interface_attachments = []

        for network in networks:
            network_id = network['uuid']
            port_id = network['port']

            # Get ResponseFile(get_network)
            response_path_get_network = response_dir \
                + config.OS_RESPONSE_DEF['get_network']['file'].replace(
                    '%network_id%', network_id)

            with open(response_path_get_network, 'r') as f:
                response_content = f.read()
            response_params_get_network = json.loads(response_content)

            # Get ResponseFile(get_port)
            response_path_get_port = response_dir \
                + config.OS_RESPONSE_DEF['get_port']['file'].replace(
                    '%port_id%', port_id)

            with open(response_path_get_port, 'r') as f:
                response_content = f.read()
            response_params_get_port = json.loads(response_content)

            network_name = response_params_get_network['network']['name']
            addresses[network_name] = []

            interface = {}
            interface['fixed_ips'] \
                        = response_params_get_port['port']['fixed_ips']
            interface['mac_addr'] \
                        = response_params_get_port['port']['mac_address']
            interface['net_id'] = network_id
            interface['port_id'] = port_id
            interface['port_state'] \
                            = response_params_get_port['port']['status']

            interface_attachments.append(interface)

            for fixed_ips in response_params_get_port['port']['fixed_ips']:

                # Get ResponseFile(get_subnet)
                response_path_get_subnet = response_dir \
                    + config.OS_RESPONSE_DEF['get_subnet']['file'].replace(
                        '%subnet_id%', fixed_ips['subnet_id'])

                with open(response_path_get_subnet, 'r') as f:
                    response_content = f.read()
                response_params_get_subnet = json.loads(response_content)

                addr = {}
                addr['OS-EXT-IPS-MAC:mac_addr'] \
                            = response_params_get_port['port']['mac_address']
                addr['OS-EXT-IPS:type'] = config.OS_EXT_IPS_TYPE
                addr['addr'] = fixed_ips['ip_address']
                addr['version'] \
                        = response_params_get_subnet['subnet']['ip_version']

                addresses[network_name].append(addr)

        # Set Links(Image)
        image_links = {'id': image_ref, 'links': []}
        image_links['links'].append(
            {'href': stub_url + '/' + project_id + '/images/' + image_ref,
             'rel': 'bookmark'})

        # Set Links(Server)
        server_links = []
        server_links.append(
            {'href': stub_url + '/v2.1/' + project_id \
                                                + '/servers/' + server_id,
             'rel': 'self'})
        server_links.append(
            {'href': stub_url + '/' + project_id + '/servers/' + server_id,
             'rel': 'bookmark'})

        # Set ResponseParams
        sysdate = utils.Utils().get_sysdate()
        response_params = {'server': {}}
        response_params['server']['id'] = server_id
        response_params['server']['OS-DCF:diskConfig'] \
                                        = config.OS_DCF_DISK_CONFIG
        response_params['server']['adminPass'] = 'admin' + sysdate
        response_params['server']['links'] = server_links
        response_params['server']['security_groups'] = security_groups

        # Set ResponseParams(get_server)
        response_params_get_server = {'server': {}}
        response_params_get_server['server']['id'] = server_id
        response_params_get_server['server']['OS-DCF:diskConfig'] \
                                            = config.OS_DCF_DISK_CONFIG
        response_params_get_server['server']['OS-EXT-AZ:availability_zone'] \
                                            = availability_zone
        response_params_get_server['server']['OS-EXT-SRV-ATTR:host'] \
                                            = config.OS_HOST_NAME
        response_params_get_server['server'][
                    'OS-EXT-SRV-hypervisor_hostname'] = config.OS_HOST_NAME
        response_params_get_server['server']['OS-EXT-SRV-instance_name'] \
                                        = utils.Utils().create_instance_name()
        response_params_get_server['server']['OS-EXT-STS:power_state'] \
                                            = config.OS_EXT_STS_POWER_STATE
        response_params_get_server['server']['OS-EXT-STS:task_state'] = None
        response_params_get_server['server']['OS-EXT-STS:vm_state'] \
                                                = config.OS_EXT_STS_VM_STATE
        response_params_get_server['server']['OS-SRV-USG:launched_at'] \
                                        = utils.Utils().get_sysdate('.000000')
        response_params_get_server['server']['OS-SRV-USG:terminated_at'] = None
        response_params_get_server['server']['accessIPv4'] = ''
        response_params_get_server['server']['accessIPv6'] = ''
        response_params_get_server['server']['addresses'] = addresses
        response_params_get_server['server']['config_drive'] = config_drive
        response_params_get_server['server']['created'] = sysdate
        response_params_get_server['server']['flavor'] = flavor_info
        response_params_get_server['server']['hostId'] = config.OS_HOST_ID
        response_params_get_server['server']['image'] = image_links
        response_params_get_server['server']['key_name'] = key_name
        response_params_get_server['server']['links'] = server_links
        response_params_get_server['server']['metadata'] = metadata
        response_params_get_server['server']['name'] = name
        response_params_get_server['server'][
                                'os-extended-volumes:volumes_attached'] = []
        response_params_get_server['server']['progress'] \
                                                = config.OS_SERVER_PROGRESS
        response_params_get_server['server']['security_groups'] \
                                                = security_groups
        response_params_get_server['server']['status'] \
                                                = config.OS_SERVER_STATUS
        response_params_get_server['server']['tenant_id'] = project_id
        response_params_get_server['server']['updated'] = sysdate
        response_params_get_server['server']['user_id'] = user_id

        # Create ResponseFile
        with open(response_path, 'w') as f:
            f.write(json.dumps(response_params))

        # Create ResponseFile(get_server)
        with open(response_dir \
            + config.OS_RESPONSE_DEF['get_server']['file'].replace(
                '%server_id%', server_id).replace(
                '%project_id%', project_id), 'w') as f:
            f.write(json.dumps(response_params_get_server))

        # Create ResponseFile(action_server)
        with open(response_dir \
            + config.OS_RESPONSE_DEF['action_server']['file'].replace(
                '%server_id%', server_id).replace(
                '%project_id%', project_id), 'w') as f:
            f.write('')

        # Create ResponseFile(delete_server)
        with open(response_dir \
            + config.OS_RESPONSE_DEF['delete_server']['file'].replace(
                '%server_id%', server_id).replace(
                '%project_id%', project_id), 'w') as f:
            f.write('')

        # Create ResponseFile(list_interfaces)
        with open(response_dir \
            + config.OS_RESPONSE_DEF['list_interfaces']['file'].replace(
                '%server_id%', server_id).replace(
                '%project_id%', project_id), 'w') as f:
            f.write(json.dumps({'interfaceAttachments': interface_attachments}))

        # Create ResponseFile(detach_interface)
        for interface_attachment in interface_attachments:
            with open(response_dir \
                + config.OS_RESPONSE_DEF['detach_interface']['file'].replace(
                    '%port_id%', interface_attachment['port_id']).replace(
                    '%server_id%', server_id).replace(
                    '%project_id%', project_id), 'w') as f:
                f.write('')

        # Update ResponseFile(list_servers)
        response_params_list_servers['servers'].append(
                                                response_params['server'])
        with open(response_path_list_servers, 'w') as f:
            f.write(json.dumps(response_params_list_servers))

    # When action_server Requested
    matchOB = re.findall(
        config.OS_RESPONSE_DEF['action_server']['rexp'], response_filename)
    if len(matchOB) > 0:
        project_id = matchOB[0][0]
        server_id = matchOB[0][1]

        response_content = ''

        if config.OS_VNC_CONSOLE_KEYNAME in request_params:
            response_params = {'console': {
                    'type': request_params[
                                    config.OS_VNC_CONSOLE_KEYNAME]['type'],
                    'url': stub_url + config.OS_VNC_CONSOLE_GET_URI \
                        + utils.Utils().create_uuid(
                            config.CHAR_SET, config.SCRIPT_STDOUT_SEPARATER)}}

            response_content = json.dumps(response_params)

        # Create ResponseFile(action_server)
        with open(response_path, 'w') as f:
            f.write(response_content)

    # When attach_interface Requested
    matchOB = re.findall(
        config.OS_RESPONSE_DEF['attach_interface']['rexp'], response_filename)
    if len(matchOB) > 0:
        project_id = matchOB[0][0]
        server_id = matchOB[0][1]

        # Get RequestParams
        port_id = utils.Utils().get_dict_value(
                    request_params, ['interfaceAttachment', 'port_id'], '')

        response_params = {'interfaceAttachment': {}}

        if len(port_id) > 0:

            # Get ResponseFile(get_port)
            response_path_get_port = response_dir \
                + config.OS_RESPONSE_DEF['get_port']['file'].replace(
                    '%port_id%', port_id)

            with open(response_dir \
                + config.OS_RESPONSE_DEF['get_port']['file'].replace(
                    '%port_id%', port_id), 'r') as f:
                response_content = f.read()
            response_params_get_port = json.loads(response_content)

            # Set ResponseParams
            response_params['interfaceAttachment'] = {
                'fixed_ips': response_params_get_port['port']['fixed_ips'],
                'mac_addr': response_params_get_port['port']['mac_address'],
                'net_id': response_params_get_port['port']['network_id'],
                'port_id': port_id,
                'port_state': response_params_get_port['port']['status'],
            }

        # Create ResponseFile(attach_interface)
        with open(response_path, 'w') as f:
            f.write(json.dumps(response_params))

        # Create ResponseFile(detach_interface)
        with open(response_dir \
            + config.OS_RESPONSE_DEF['detach_interface']['file'].replace(
                '%port_id%', port_id).replace(
                '%server_id%', server_id).replace(
                '%project_id%', project_id), 'w') as f:
            f.write('')

        # Update ResponseFile(list_interfaces)
        response_path_list_interfaces = response_dir \
            + config.OS_RESPONSE_DEF['list_interfaces']['file'].replace(
                '%server_id%', server_id).replace(
                '%project_id%', project_id)

        if os.path.exists(response_path_list_interfaces):
            with open(response_path_list_interfaces, 'r') as f:
                response_content = f.read()
            response_params_list_interfaces = json.loads(response_content)
        else:
            response_params_list_interfaces = json.loads(
                        config.OS_RESPONSE_DEF['list_interfaces']['resp'])

        response_params_list_interfaces['interfaceAttachments'].append(
                                    response_params['interfaceAttachment'])

        with open(response_path_list_interfaces, 'w') as f:
            f.write(json.dumps(response_params_list_interfaces))

    # When detach_interface Requested
    matchOB = re.findall(
        config.OS_RESPONSE_DEF['detach_interface']['rexp'], response_filename)
    if len(matchOB) > 0:
        del_response_flg = True
        project_id = matchOB[0][0]
        server_id = matchOB[0][1]
        port_id = matchOB[0][2]

        # Delete ResponseFile(attach_interface)
        response_path_attach_interface = response_dir \
            + config.OS_RESPONSE_DEF['attach_interface']['file'].replace(
                '%server_id%', server_id).replace(
                '%project_id%', project_id)

        if os.path.exists(response_path_attach_interface):
            os.remove(response_path_attach_interface)

        # Update ResponseFile(list_interfaces)
        response_path_list_interfaces = response_dir \
            + config.OS_RESPONSE_DEF['list_interfaces']['file'].replace(
                '%server_id%', server_id).replace(
                '%project_id%', project_id)

        if os.path.exists(response_path_list_interfaces):
            with open(response_path_list_interfaces, 'r') as f:
                response_content = f.read()
            response_params_list_interfaces = json.loads(response_content)

            for i, v in enumerate(response_params_list_interfaces[
                                                'interfaceAttachments']):
                if v['port_id'] == port_id:
                    response_params_list_interfaces[
                                            'interfaceAttachments'].pop(i)
                    break

            with open(response_path_list_interfaces, 'w') as f:
                f.write(json.dumps(response_params_list_interfaces))

    # When delete_server Requested
    matchOB = re.findall(
        config.OS_RESPONSE_DEF['delete_server']['rexp'], response_filename)
    if len(matchOB) > 0:
        del_response_flg = True
        project_id = matchOB[0][0]
        server_id = matchOB[0][1]

        # Delete ResponseFile(create_server)
        response_path_server = response_dir \
            + config.OS_RESPONSE_DEF['create_server']['file'].replace(
                '%project_id%', project_id)

        if os.path.exists(response_path_server):
            os.remove(response_path_server)

        # Delete ResponseFile(get_server)
        response_path_server = response_dir \
            + config.OS_RESPONSE_DEF['get_server']['file'].replace(
                '%server_id%', server_id).replace(
                '%project_id%', project_id)

        if os.path.exists(response_path_server):
            os.remove(response_path_server)

        # Delete ResponseFile(action_server)
        response_path_server = response_dir \
            + config.OS_RESPONSE_DEF['action_server']['file'].replace(
                '%server_id%', server_id).replace(
                '%project_id%', project_id)

        if os.path.exists(response_path_server):
            os.remove(response_path_server)

        # Delete ResponseFile(attach_interface)
        response_path_server = response_dir \
            + config.OS_RESPONSE_DEF['attach_interface']['file'].replace(
                '%server_id%', server_id).replace(
                '%project_id%', project_id)

        if os.path.exists(response_path_server):
            os.remove(response_path_server)

        # Delete ResponseFile(list_interfaces)
        response_path_list_interfaces = response_dir \
            + config.OS_RESPONSE_DEF['list_interfaces']['file'].replace(
                '%server_id%', server_id).replace(
                '%project_id%', project_id)

        if os.path.exists(response_path_list_interfaces):

            with open(response_path_list_interfaces, 'r') as f:
                response_content = f.read()
            response_params_list_interfaces = json.loads(response_content)

            for i, v in enumerate(response_params_list_interfaces[
                                                'interfaceAttachments']):

                # Delete ResponseFile(detach_interface)
                response_params_detach_interface = response_dir \
                    + config.OS_RESPONSE_DEF[
                        'detach_interface']['file'].replace(
                        '%port_id%', v['port_id']).replace(
                        '%server_id%', server_id).replace(
                        '%project_id%', project_id)

                if os.path.exists(response_params_detach_interface):
                    os.remove(response_params_detach_interface)

            os.remove(response_path_list_interfaces)

        # Update ResponseFile(list_servers)
        response_path_list_servers = response_dir \
            + config.OS_RESPONSE_DEF['list_servers']['file'].replace(
                '%project_id%', project_id)

        if os.path.exists(response_path_list_servers):
            with open(response_path_list_servers, 'r') as f:
                response_content = f.read()
            response_params_list_servers = json.loads(response_content)

            for i, v in enumerate(response_params_list_servers['servers']):
                if v['id'] == server_id:
                    response_params_list_servers['servers'].pop(i)
                    break

            with open(response_path_list_servers, 'w') as f:
                f.write(json.dumps(response_params_list_servers))

    return del_response_flg


def set_response_params_port_fixed_ips(
                    response_dir, network_id, fixed_ip_list, port_list):

    ip_address_inuse_list = {}
    allocation_pool_list = {}

    # Get RequestParams(list_subnets)
    subnet_list = json.loads(
                    config.OS_RESPONSE_DEF['list_subnets']['resp'])

    response_path_list_subnets = response_dir \
            + config.OS_RESPONSE_DEF['list_subnets']['file']

    if os.path.exists(response_path_list_subnets):
        with open(response_path_list_subnets, 'r') as f:
            response_content = f.read()
        subnet_list = json.loads(response_content)

    for port in port_list['ports']:

        if port['network_id'] == network_id:
            for fixed_ip in port['fixed_ips']:
                if 'subnet_id' in fixed_ip:
                    sbid = fixed_ip['subnet_id']
                    if sbid not in ip_address_inuse_list:
                        ip_address_inuse_list[sbid] = []
                    ip_address_inuse_list[sbid].append(fixed_ip['ip_address'])

    for subnet in subnet_list['subnets']:

        if subnet['network_id'] == network_id:
            allocation_pool_list[subnet['id']] = subnet['allocation_pools']

    if len(fixed_ip_list) > 0:

        for i, v in enumerate(fixed_ip_list):

            subnet_id = v.get('subnet_id', None)
            ip_address = v.get('ip_address', None)

            if subnet_id is not None:
                if ip_address is None:
                    ip = None
                    allocation_pool = allocation_pool_list.get(subnet_id, [])

                    for pool in allocation_pool:
                        pool['inuse'] = ip_address_inuse_list.get(
                                                            subnet_id, [])
                        ip = utils.Utils().get_ipaddress_not_inuse(pool)

                        if ip is not None:
                            break

                    fixed_ip_list[i]['ip_address'] = ip

            else:
                if ip_address is not None:
                    subnet_found = False
                    for sbid, allocation_pool in allocation_pool_list.items():
                        for pool in allocation_pool:
                            pool['ip'] = ip_address
                            pool['inuse'] = ip_address_inuse_list.get(
                                                                    sbid, [])

                            subnet_found \
                                = utils.Utils().is_ipaddress_usable(pool)

                            if subnet_found:
                                fixed_ip_list[i]['subnet_id'] = sbid
                                break

                        if subnet_found:
                            break
    else:
        for sbid, allocation_pool in allocation_pool_list.items():
            for pool in allocation_pool:
                pool['inuse'] = ip_address_inuse_list.get(sbid, [])
                ip = utils.Utils().get_ipaddress_not_inuse(pool)
                fixed_ip_list.append({'ip_address': ip, 'subnet_id': sbid})

    return fixed_ip_list


def delete_responsefile_user_related(response_dir, project_id, user_id):

    # Delete ResponseFile(get_user
    response_path_user = response_dir \
            + config.OS_RESPONSE_DEF['get_user']['file'].replace(
            '%user_id%', user_id)
    if os.path.exists(response_path_user):
        os.remove(response_path_user)

    # Delete ResponseFile(create_user)
    response_path_user = response_dir \
            + config.OS_RESPONSE_DEF['create_user']['file']
    if os.path.exists(response_path_user):
        os.remove(response_path_user)

    # Delete ResponseFile(update_user)
    response_path_user = response_dir \
            + config.OS_RESPONSE_DEF['update_user']['file'].replace(
            '%user_id%', user_id)
    if os.path.exists(response_path_user):
        os.remove(response_path_user)

    # Get Roles from ResponseFile(list_roles_for_user)
    response_path_list_roles_for_user = response_dir \
        + config.OS_RESPONSE_DEF['list_roles_for_user']['file'].replace(
            '%project_id%', project_id).replace(
            '%user_id%', user_id)

    if os.path.exists(response_path_list_roles_for_user):
        with open(response_path_list_roles_for_user, 'r') as f:
            response_content = f.read()

        response_params_list_roles_for_user = json.loads(response_content)

        for role in response_params_list_roles_for_user['roles']:

            # Delete ResponseFile(add_role_to_user)
            response_path_role = response_dir \
            + config.OS_RESPONSE_DEF['add_role_to_user']['file'].replace(
                '%project_id%', project_id).replace(
                '%user_id%', user_id).replace(
                '%role_id%', role['id'])
            if os.path.exists(response_path_role):
                os.remove(response_path_user)

            # Delete ResponseFile(remove_role_from_user)
            response_path_role = response_dir \
                + config.OS_RESPONSE_DEF[
                'remove_role_from_user']['file'].replace(
                    '%project_id%', project_id).replace(
                    '%user_id%', user_id).replace(
                    '%role_id%', role['id'])
            if os.path.exists(response_path_role):
                os.remove(response_path_user)

        # Delete ResponseFile(list_roles_for_user)
        os.remove(response_path_list_roles_for_user)

    # Update ResponseFile(list_users)
    response_path_list_users = response_dir \
                        + config.OS_RESPONSE_DEF['list_users']['file']

    with open(response_path_list_users, 'r') as f:
        response_content = f.read()
    response_params_list_users = json.loads(response_content)

    for i, v in enumerate(response_params_list_users['users']):
        if v['id'] == user_id:
            response_params_list_users['users'].pop(i)
            break

    with open(response_path_list_users, 'w') as f:
            f.write(json.dumps(response_params_list_users))
