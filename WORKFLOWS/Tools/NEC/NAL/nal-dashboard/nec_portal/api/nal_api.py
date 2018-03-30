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


from __future__ import absolute_import

import logging

from horizon import exceptions
from horizon import messages
from horizon.utils.memoized import memoized  # noqa

import nalclient
from nalclient import exc as client_exc
from nec_portal.local import nal_portal_settings

LOG = logging.getLogger(__name__)

HTT_ERROR_CODE = 68000
TIME_OUT = 60

ENDPOINT = getattr(nal_portal_settings, 'NAL_ENDPOINT', None)
NAL_ID_PASSWORD = getattr(nal_portal_settings, 'NAL_ID_PASSWORD', None)
NODE_RETURN_MAPPING = getattr(nal_portal_settings, 'NODE_RETURN_MAPPING', None)
SERVICE_RETURN_MAPPING = getattr(nal_portal_settings,
                                 'SERVICE_RETURN_MAPPING', None)
RESOURCE_RETURN_MAPPING = getattr(nal_portal_settings,
                                  'RESOURCE_RETURN_MAPPING', None)
RESOURCE_RETURN_ADMIN_MAPPING = getattr(nal_portal_settings,
                                        'RESOURCE_RETURN_ADMIN_MAPPING', None)
NAL_RESOURCES = getattr(nal_portal_settings,
                        'NAL_RESOURCES', None)
APL_TYPE_MAPPING = getattr(nal_portal_settings, 'APL_TYPE_MAPPING', None)
TYPE_MAPPING = getattr(nal_portal_settings, 'TYPE_MAPPING', None)


class Node(object):
    """Node class"""
    def __init__(self, return_obj, mapping):

        for key, value in mapping.iteritems():
            set_value = return_obj.get(value, '')
            self.__dict__[key] = set_value


class Service(object):
    """Service class"""
    def __init__(self, return_obj, mapping):

        for key, value in mapping.iteritems():
            set_value = return_obj.get(value, '')
            self.__dict__[key] = set_value


class Resource(object):
    """Resource class"""
    def __init__(self, return_obj, mapping):

        for key, value in mapping.iteritems():
            set_value = return_obj.get(value, '')
            self.__dict__[key] = set_value


@memoized
def client(request, version='1'):
    return nalclient.Client(version, ENDPOINT, token=request.user.token.id,
                            time_out=TIME_OUT, id_pass=NAL_ID_PASSWORD)


def get_nodes(request,
              IaaS_tenant_id=None,
              apl_type=None,
              type=None,
              device_type=None,
              rec_id=None,
              func_type='all_node'):

    params = {}
    if IaaS_tenant_id:
        params['IaaS_tenant_id'] = IaaS_tenant_id
    if apl_type:
        params['apl_type'] = apl_type
    if type:
        params['type'] = type
    if device_type:
        params['device_type'] = device_type
    if rec_id:
        params['ID'] = rec_id
    params['operation_id'] = request.user.id
    params['function_type'] = func_type

    node_list = client(request).node.get(params)

    if func_type == 'all_node':
        nodes = []
        for node_row in node_list:
            apl = node_row['apl_type']
            type = node_row['type']
            if type in TYPE_MAPPING.keys():
                node = Node(
                    node_row,
                    NODE_RETURN_MAPPING[func_type][APL_TYPE_MAPPING[str(apl)]])
                nodes.append(node)

        return nodes

    else:
        nodes = {}
        for key, value in NODE_RETURN_MAPPING[func_type].iteritems():
            if isinstance(value, dict):
                nodes[key] = []
                for node_row in node_list[key]:
                    nodes[key].append(Node(node_row, value))

        return nodes


def create_node(request, params):

    params['operation_id'] = request.user.id
    params['IaaS_tenant_id'] = request.user.project_id
    params['IaaS_tenant_name'] = request.user.project_name
    params['IaaS_region_id'] = request.user.services_region

    try:
        return client(request).node.create(params)
    except client_exc.NalBadRequest as e:
        LOG.warning(e)
        for err_msg in e.details.split('|'):
            messages.error(request, err_msg)
        raise exceptions.NotAvailable


def update_node(request, params):

    params['operation_id'] = request.user.id
    params['IaaS_tenant_id'] = request.user.project_id
    params['IaaS_tenant_name'] = request.user.project_name
    params['IaaS_region_id'] = request.user.services_region

    try:
        return client(request).node.update(params)
    except client_exc.NalBadRequest as e:
        LOG.warning(e)
        for err_msg in e.details.split('|'):
            messages.error(request, err_msg)
        raise exceptions.NotAvailable


def delete_node(request, func_type, node_id, device_type,
                job_cleaning_mode='0'):

    params = {'operation_id': request.user.id,
              'IaaS_tenant_id': request.user.project_id,
              'IaaS_region_id': request.user.services_region,
              'apl_table_rec_id': node_id,
              'device_type': device_type,
              'function_type': func_type,
              'job_cleaning_mode': job_cleaning_mode}

    return client(request).node.delete(params)


def get_services(request,
                 IaaS_tenant_id=None,
                 group_id=None,
                 func_type='all_dcconnect'):

    params = {}
    if IaaS_tenant_id:
        params['IaaS_tenant_id'] = IaaS_tenant_id
    if group_id:
        params['group_id'] = group_id
    params['operation_id'] = request.user.id
    params['function_type'] = func_type

    service_list = client(request).service.get(params)

    if func_type == 'all_dcconnect':
        services = []
        for service_row in service_list:
            service = Service(service_row,
                              SERVICE_RETURN_MAPPING['all_dcconnect'])
            services.append(service)
        return services
    else:
        services = {}
        for key, value in SERVICE_RETURN_MAPPING[func_type].iteritems():
            if isinstance(value, dict):
                services[key] = []
                if isinstance(service_list[key], list):
                    for row in service_list[key]:
                        services[key].append(Service(row, value))
                elif isinstance(service_list[key], dict):
                    my_dc_id = service_list[key].get('my_dc_id', None)
                    for group_key, group_value \
                            in service_list[key].iteritems():
                        if group_key == 'my_dc_id':
                            continue
                        else:
                            group_value['my_dc_id'] = my_dc_id
                        services[key].append(Service(group_value, value))
        return services


def create_service(request, params):

    params['operation_id'] = request.user.id
    params['IaaS_tenant_id'] = request.user.project_id
    params['IaaS_tenant_name'] = request.user.project_name
    params['IaaS_region_id'] = request.user.services_region

    try:
        return client(request).service.create(params)
    except client_exc.NalBadRequest as e:
        LOG.warning(e)
        for err_msg in e.details.split('|'):
            messages.error(request, err_msg)
        raise exceptions.NotAvailable


def update_service(request, params):

    params['operation_id'] = request.user.id
    params['IaaS_tenant_id'] = request.user.project_id
    params['IaaS_tenant_name'] = request.user.project_name
    params['IaaS_region_id'] = request.user.services_region

    try:
        return client(request).service.update(params)
    except client_exc.NalBadRequest as e:
        LOG.warning(e)
        for err_msg in e.details.split('|'):
            messages.error(request, err_msg)
        raise exceptions.NotAvailable


def delete_service(request, params):

    params['operation_id'] = request.user.id
    params['IaaS_tenant_id'] = request.user.project_id
    params['IaaS_region_id'] = request.user.services_region

    return client(request).service.delete(params)


def get_resources(request,
                  IaaS_tenant_id=None,
                  func_type='all_resource',
                  add_params=None):

    params = {}
    if IaaS_tenant_id:
        params['IaaS_tenant_id'] = IaaS_tenant_id
    params['operation_id'] = request.user.id
    params['function_type'] = func_type
    params['IaaS_region_id'] = request.user.services_region
    if add_params:
        params.update(add_params)

    resource_list = client(request).resource.get(params)

    resources = {}
    if isinstance(resource_list, dict):
        for ret_key, ret_val in resource_list.iteritems():
            if isinstance(ret_val, dict):
                resource = Resource(
                    ret_val,
                    RESOURCE_RETURN_MAPPING[func_type][ret_key])
                resources[ret_key] = resource
            else:
                resources[ret_key] = []
                for resource_row in ret_val:
                    resource = Resource(
                        resource_row,
                        RESOURCE_RETURN_MAPPING[func_type][ret_key])
                    resources[ret_key].append(resource)

    return resources


def create_resource(request, params):

    params['operation_id'] = request.user.id
    params['IaaS_tenant_id'] = request.user.project_id
    params['IaaS_tenant_name'] = request.user.project_name
    params['IaaS_region_id'] = request.user.services_region

    try:
        return client(request).resource.create(params)
    except client_exc.NalBadRequest as e:
        LOG.warning(e)
        for err_msg in e.details.split('|'):
            messages.error(request, err_msg)
        raise exceptions.NotAvailable


def update_resource(request, params):

    params['operation_id'] = request.user.id
    params['IaaS_tenant_id'] = request.user.project_id
    params['IaaS_tenant_name'] = request.user.project_name
    params['IaaS_region_id'] = request.user.services_region

    try:
        return client(request).resource.update(params)
    except client_exc.NalBadRequest as e:
        LOG.warning(e)
        for err_msg in e.details.split('|'):
            messages.error(request, err_msg)
        raise exceptions.NotAvailable


def delete_resource(request, func_type, resource_id):

    params = {'operation_id': request.user.id,
              'IaaS_tenant_id': request.user.project_id,
              'IaaS_region_id': request.user.services_region,
              'ID': resource_id,
              'function_type': func_type}

    return client(request).resource.delete(params)
