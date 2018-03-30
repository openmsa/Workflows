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


import logging

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import messages

from nec_portal.api import nal_api
from nec_portal.dashboards.project.node import constants
from nec_portal.local import nal_portal_settings

from openstack_dashboard import api

LOG = logging.getLogger(__name__)
NODE_DETAIL_DISPLAY_COLUMNS = \
    getattr(nal_portal_settings, 'PROJECT_NODE_DETAIL_DISPLAY_COLUMNS', None)
NODE_CREATE_COLUMNS = \
    getattr(nal_portal_settings, 'NODE_CREATE_COLUMNS', None)
NODE_UPDATE_COLUMNS = getattr(nal_portal_settings, 'NODE_UPDATE_COLUMNS', None)
NODE_FUNCTION_TYPE_MAPPING = \
    getattr(nal_portal_settings, 'NODE_FUNCTION_TYPE_MAPPING', None)
DEVICE_TYPE_MAPPING = getattr(nal_portal_settings, 'DEVICE_TYPE_MAPPING', None)
NODE_CREATE_DISPLAY_COLUMNS_LIST = \
    getattr(nal_portal_settings, 'NODE_CREATE_DISPLAY_COLUMNS_LIST', None)
NODE_UPDATE_DISPLAY_COLUMNS_LIST = \
    getattr(nal_portal_settings, 'NODE_UPDATE_DISPLAY_COLUMNS_LIST', None)


FUNC_TYPE_MAP = {}
for apl_type, type_map in NODE_FUNCTION_TYPE_MAPPING.iteritems():
    for type, func_type in type_map.iteritems():
        FUNC_TYPE_MAP[func_type] = apl_type + '-' + type

DEVICE_TYPE_MAP = {}
for func_type, device_type_map in DEVICE_TYPE_MAPPING.iteritems():
    for device_type, device_name in device_type_map.iteritems():
        func_value = FUNC_TYPE_MAP[func_type]
        DEVICE_TYPE_MAP[device_name] = func_value + '-' + device_type

DISPLAY_CREATE_COLUMNS_MAP = {}
for device_name, columns in NODE_CREATE_DISPLAY_COLUMNS_LIST.iteritems():
    for column_name in columns:
        if column_name not in DISPLAY_CREATE_COLUMNS_MAP:
            DISPLAY_CREATE_COLUMNS_MAP[column_name] = []
        DISPLAY_CREATE_COLUMNS_MAP[column_name].append(device_name)

DISPLAY_UPDATE_COLUMNS_MAP = {}
for device_name, columns in NODE_UPDATE_DISPLAY_COLUMNS_LIST.iteritems():
    for column_name in columns:
        if column_name not in DISPLAY_UPDATE_COLUMNS_MAP:
            DISPLAY_UPDATE_COLUMNS_MAP[column_name] = []
        DISPLAY_UPDATE_COLUMNS_MAP[column_name].append(device_name)


def _get_network_list(request):
    try:
        tenant_id = request.user.tenant_id
        networks = api.neutron.network_list_for_tenant(request,
                                                       tenant_id)
    except Exception:
        msg = _('Failed to get network list.')
        exceptions.handle(request, msg)
        redirect = reverse(constants.NODE_INDEX_URL)
        exceptions.handle(request, msg, redirect=redirect)

    return networks


def _get_subnet_list(request, network_id):
    try:
        subnets = api.neutron.subnet_list(request,
                                          network_id=network_id)
    except Exception:
        msg = _('Failed to get subnet list.')
        redirect = reverse(constants.NODE_INDEX_URL)
        exceptions.handle(request, msg, redirect=redirect)

    return subnets


def _get_filtering_subnet_list(subnet_list, filter):

    filtering_subnet_list = []
    for subnet in subnet_list:
        if subnet.ip_version == filter:
            filtering_subnet_list.append(subnet)

    return filtering_subnet_list


def _get_network_detail(request, network_id):
    try:
        network = api.neutron.network_get(request, network_id)
    except Exception:
        msg = _('Failed to get network data.')
        redirect = reverse(constants.NODE_INDEX_URL)
        exceptions.handle(request, msg, redirect=redirect)

    return {'IaaS_network_type': network.provider__network_type,
            'IaaS_network_id': network.id,
            'IaaS_segmentation_id': network.provider__segmentation_id,
            'network_name': network.name,
            'network_type': network.router__external}


def _get_subnet_detail(request, subnet_id):
    try:
        subnet = api.neutron.subnet_get(request, subnet_id)
    except Exception:
        msg = _('Failed to get subnet data.')
        redirect = reverse(constants.NODE_INDEX_URL)
        exceptions.handle(request, msg, redirect=redirect)

    return subnet


class CreateNodeForm(forms.SelfHandlingForm):

    def __init__(self, request, *args, **kwargs):

        super(CreateNodeForm, self).__init__(request, *args, **kwargs)

        apl_type = NODE_CREATE_COLUMNS['apl_type']
        type = NODE_CREATE_COLUMNS['type']
        device_type = NODE_CREATE_COLUMNS['device_type']
        subnet = NODE_CREATE_COLUMNS['subnet']

        self.fields['apl_type'] = getattr(forms, apl_type['field'])(
            label=apl_type['label'],
            choices=apl_type['choices'],
            required=apl_type['required'],
            widget=forms.Select(attrs={'class': 'sub_switchable',
                                       'id': 'apl_type'}))

        self.fields['type'] = getattr(forms, type['field'])(
            label=type['label'],
            choices=type['choices'],
            required=type['required'],
            widget=forms.Select(attrs={'class': 'sub_switchable',
                                       'id': 'type'}))

        for key, column in device_type.items():
            self.fields['device_type-' + FUNC_TYPE_MAP[key]] = \
                getattr(forms, column['field'])(
                    label=column['label'],
                    choices=column['choices'],
                    required=column['required'],
                    widget=forms.Select(attrs={
                        'class': 'sub_switchable device_class',
                        'data-' + FUNC_TYPE_MAP[key]: column['label']}))

        self.fields['subnet'] = getattr(forms, subnet['field'])(
            label=subnet['label'],
            choices=subnet['choices'],
            required=subnet['required'],
            widget=forms.Select(attrs={'class': 'sub_switchable',
                                       'id': 'subnet'}))

        for column in NODE_CREATE_COLUMNS['separate']:
            input_attrs = {}
            for device_name in DISPLAY_CREATE_COLUMNS_MAP[column[0]]:
                name = 'data-' + DEVICE_TYPE_MAP[device_name]
                input_attrs[name] = column[1]['label']

            input_attrs['class'] = 'switched'
            input_attrs['id'] = column[0]

            if column[1]['field'] == 'ChoiceField':
                self.fields[column[0]] = getattr(forms, column[1]['field'])(
                    label=column[1]['label'],
                    choices=column[1]['choices'],
                    required=column[1]['required'],
                    help_text=column[1].get('help_text'),
                    widget=forms.Select(attrs=input_attrs))
            else:
                self.fields[column[0]] = getattr(forms, column[1]['field'])(
                    label=column[1]['label'],
                    required=column[1]['required'],
                    help_text=column[1].get('help_text'),
                    widget=forms.TextInput(attrs=input_attrs))

        networks = _get_network_list(request)
        subnet_choices = []
        for network_data in networks:
            subnets = _get_subnet_list(request, network_data.id)
            subnets = _get_filtering_subnet_list(subnets, 4)

            subnet_choices.extend([(subnet_data.id,
                                    network_data.name + ': ' +
                                    subnet_data.cidr +
                                    ' (' + subnet_data.name + ')')
                                   for subnet_data in subnets])

        if subnet_choices:
            subnet_choices.insert(0, ("", _("Select subnet")))
            self.fields['subnet'].choices = subnet_choices
        else:
            messages.error(request,
                           'There are no selectable subnets.')
            raise exceptions.NotAvailable

    def handle(self, request, data):
        try:
            apl_type = data['apl_type']
            type = data['type']
            device_type = data['device_type-' + apl_type + '-' + type]
            func_type = NODE_FUNCTION_TYPE_MAPPING[apl_type][type]
            device_name = DEVICE_TYPE_MAPPING[func_type][device_type]
            subnet_id = data['subnet']
            subnet_detail = _get_subnet_detail(request, subnet_id)
            network = _get_network_detail(request, subnet_detail.network_id)
            params = {'apl_type': apl_type,
                      'type': type,
                      'device_type': device_type,
                      'IaaS_network_type': network['IaaS_network_type'],
                      'IaaS_network_id': network['IaaS_network_id'],
                      'IaaS_segmentation_id': network['IaaS_segmentation_id'],
                      'network_name': network['network_name'],
                      'IaaS_subnet_id': subnet_id,
                      'function_type': func_type}

            for column in NODE_CREATE_COLUMNS['separate']:
                if device_name in DISPLAY_CREATE_COLUMNS_MAP[column[0]]:
                    params[column[0]] = data[column[0]]

            nal_api.create_node(request, params)
            msg = _('Job of node creation is running.')
            LOG.debug(msg)
            messages.success(request, msg)
            return True

        except exceptions.NotAvailable:
            return False
        except Exception:
            redirect = reverse(constants.NODE_INDEX_URL)
            exceptions.handle(request, redirect=redirect)

    def clean(self):
        data = super(CreateNodeForm, self).clean()
        apl_type = data['apl_type']
        type = data['type']
        device_type = data['device_type-' + apl_type + '-' + type]
        func_type = NODE_FUNCTION_TYPE_MAPPING[apl_type][type]
        device_name = DEVICE_TYPE_MAPPING[func_type][device_type]
        for column in NODE_CREATE_COLUMNS['separate']:
            if column[1]['required'] and column[0] in self._errors:
                if device_name not in DISPLAY_CREATE_COLUMNS_MAP[column[0]]:
                    del self._errors[column[0]]
        for key, value in NODE_CREATE_COLUMNS['device_type'].items():
            if value['required'] and 'device_type-' + FUNC_TYPE_MAP[key] \
                    in self._errors:
                if func_type != key:
                    del self._errors['device_type-' + FUNC_TYPE_MAP[key]]

        return data


class UpdateNodeForm(forms.SelfHandlingForm):
    node_id = forms.CharField(widget=forms.HiddenInput())
    function_type = forms.CharField(widget=forms.HiddenInput())
    update_type = forms.CharField(widget=forms.HiddenInput())
    device_type = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, request, *args, **kwargs):
        super(UpdateNodeForm, self).__init__(request, *args, **kwargs)

        func_type = kwargs['initial']['obj_id'].split('|')[0]
        node_id = kwargs['initial']['obj_id'].split('|')[1]
        port_id = ''
        if len(kwargs['initial']['obj_id'].split('|')) == 3:
            port_id = kwargs['initial']['obj_id'].split('|')[2]
        update_type = kwargs['initial']['update_type']

        node = nal_api.get_nodes(self.request, rec_id=node_id,
                                 func_type=func_type)
        detail_data = \
            node[NODE_DETAIL_DISPLAY_COLUMNS[func_type]['detail_name']][0]
        network_list = \
            node[NODE_DETAIL_DISPLAY_COLUMNS[func_type]['network_name']]

        self.fields['node_id'].initial = detail_data.node_id
        self.fields['function_type'].initial = func_type
        self.fields['update_type'].initial = update_type
        self.fields['device_type'].initial = detail_data.device_type

        if NODE_UPDATE_COLUMNS[update_type]['display_type'] == 'input_column':
            device_name = \
                DEVICE_TYPE_MAPPING[func_type][str(detail_data.device_type)]

            for key, val in NODE_UPDATE_COLUMNS[update_type]['common'].items():
                self.fields[key] = getattr(forms, val['field'])(
                    label=val['label'],
                    choices=val['choices'],
                    required=val['required'])

            for column in NODE_UPDATE_COLUMNS[update_type]['separate']:
                if device_name in DISPLAY_UPDATE_COLUMNS_MAP[column[0]]:
                    self.fields[column[0]] = getattr(forms,
                                                     column[1]['field'])(
                        label=column[1]['label'],
                        required=column[1]['required'],
                        help_text=column[1].get('help_text'))

            self._logic_by_update_type(request, update_type, device_name,
                                       detail_data, network_list, port_id)

        elif NODE_UPDATE_COLUMNS[update_type]['display_type'] == 'check':
            pass

        else:
            pass

    def handle(self, request, data):
        try:
            params = {'node_id': data['node_id'],
                      'device_type': data['device_type']}

            function_type = data['function_type']
            update_type = data['update_type']
            if NODE_UPDATE_COLUMNS[update_type]['display_type'] == \
                    'input_column':
                subnet_id = data['subnet']
                subnet_detail = _get_subnet_detail(request, subnet_id)
                network = _get_network_detail(request,
                                              subnet_detail.network_id)

                params['IaaS_subnet_id'] = subnet_id
                params['IaaS_network_type'] = network['IaaS_network_type']
                params['IaaS_network_id'] = network['IaaS_network_id']
                params['IaaS_segmentation_id'] = \
                    network['IaaS_segmentation_id']
                params['network_name'] = network['network_name']

                if update_type == 'interface':
                    params['function_type'] = function_type + '_port_p'
                elif update_type == 'IPv6Add':
                    params['function_type'] = function_type + update_type
                    params['port_id'] = data['port_id']
                    node_detail = FUNC_TYPE_MAP[function_type].split('-')
                    params['apl_type'] = node_detail[0]
                    params['type'] = node_detail[1]

                for key in \
                        NODE_UPDATE_COLUMNS[data['update_type']]['separate']:
                    if key[0] in data:
                        if isinstance(data[key[0]], bool):
                            data[key[0]] = int(data[key[0]])
                        params[key[0]] = data[key[0]]

            elif NODE_UPDATE_COLUMNS[update_type]['display_type'] == 'check':
                params['function_type'] = data['update_type']

            else:
                pass

            nal_api.update_node(request, params)
            msg = _('Job of port creation is running.')
            LOG.debug(msg)
            messages.success(request, msg)
            return True

        except exceptions.NotAvailable:
            return False
        except Exception:
            redirect = reverse(constants.NODE_INDEX_URL)
            exceptions.handle(request, redirect=redirect)

    def clean(self):
        data = super(UpdateNodeForm, self).clean()

        return data

    def _logic_by_update_type(self, request, update_type, device_name,
                              detail_data, network_list, port_id):

        if update_type == 'interface':
            subnet_choices = []
            networks = _get_network_list(request)
            used_subnet_list = [net.IaaS_subnet_id for net in network_list]
            for network_data in networks:
                subnets = _get_subnet_list(request, network_data.id)
                subnets = _get_filtering_subnet_list(subnets, 4)

                for subnet_data in subnets:
                    if subnet_data.id not in used_subnet_list:
                        subnet_choices.append(
                            (subnet_data.id,
                             network_data.name + ': ' +
                             subnet_data.cidr +
                             ' (' + subnet_data.name + ')'))

            if subnet_choices:
                subnet_choices.insert(0, ("", _("Select subnet")))
                self.fields['subnet'].choices = subnet_choices
            else:
                messages.error(request,
                               'There are no selectable subnets.')
                raise exceptions.NotAvailable

        elif update_type == 'IPv6Add':
            subnet_choices = []
            self.fields['port_id'] = \
                forms.CharField(initial=port_id, widget=forms.HiddenInput())

            exist_static_flg = '0'
            for used_network in network_list:
                if used_network.network_type_detail == '1' :
                    if used_network.ip_address_v6 != '' and exist_static_flg == '0':
                        if device_name in \
                                DISPLAY_UPDATE_COLUMNS_MAP['static_route_ip_ipv6']:
                            del self.fields['static_route_ip_ipv6']
                            exist_static_flg = '1'
                elif used_network.network_type_detail == '2' :
                    if used_network.ip_address_v6 != '':
                        del self.fields['ip_v6_ext_auto_set_flg']
                        del self.fields['fixed_ip_v6_ext']
                elif used_network.network_type_detail == '3' :
                    if used_network.ip_address_v6 != '':
                        del self.fields['ip_v6_pub_auto_set_flg']
                        del self.fields['fixed_ip_v6_pub']

            for used_network in network_list:
                if port_id == used_network.port_id:
                    network_data = \
                        _get_network_detail(request,
                                            used_network.IaaS_network_id)
                    subnets = _get_subnet_list(request,
                                               used_network.IaaS_network_id)
                    subnets = _get_filtering_subnet_list(subnets, 6)
                    break

            for subnet_data in subnets:
                subnet_choices.append(
                    (subnet_data.id,
                     network_data["network_name"] + ': ' +
                     subnet_data.cidr +
                     ' (' + subnet_data.name + ')'))

            if subnet_choices:
                subnet_choices.insert(0, ("", _("Select subnet")))
                self.fields['subnet'].choices = subnet_choices
            else:
                messages.error(request,
                               'There are no selectable subnets.')
                raise exceptions.NotAvailable
