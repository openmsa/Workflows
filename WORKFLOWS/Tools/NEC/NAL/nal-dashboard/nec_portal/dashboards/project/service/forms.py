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


import copy
import logging

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import messages

from nec_portal.api import nal_api
from nec_portal.dashboards.project.service import constants
from nec_portal.local import nal_portal_settings

from openstack_dashboard import api

LOG = logging.getLogger(__name__)
SERVICE_FUNCTION_TYPE_MAPPING = \
    getattr(nal_portal_settings, 'SERVICE_FUNCTION_TYPE_MAPPING', None)
SERVICE_CREATE_COLUMNS = \
    getattr(nal_portal_settings, 'SERVICE_CREATE_COLUMNS', None)
SERVICE_UPDATE_COLUMNS = \
    getattr(nal_portal_settings, 'SERVICE_UPDATE_COLUMNS', None)
SERVICE_DETAIL_DISPLAY_COLUMNS = \
    getattr(nal_portal_settings, 'SERVICE_DETAIL_DISPLAY_COLUMNS', None)
SERVICE_TYPE_MAPPING = \
    getattr(nal_portal_settings, 'SERVICE_TYPE_MAPPING', None)
SERVICE_TYPE_DETAIL_MAPPING = \
    getattr(nal_portal_settings, 'SERVICE_TYPE_DETAIL_MAPPING', None)
SERVICE_CREATE_DISPLAY_COLUMNS_LIST = \
    getattr(nal_portal_settings, 'SERVICE_CREATE_DISPLAY_COLUMNS_LIST', None)
SERVICE_UPDATE_DISPLAY_COLUMNS_LIST = \
    getattr(nal_portal_settings, 'SERVICE_UPDATE_DISPLAY_COLUMNS_LIST', None)
NAL_CONSTRUCT_SERVICE_TYPE = \
    getattr(nal_portal_settings, 'NAL_CONSTRUCT_SERVICE_TYPE', None)
SERVICE_BANDWIDTH_MAPPING = \
    getattr(nal_portal_settings, 'SERVICE_BANDWIDTH_MAPPING', None)
SERVICE_UPDATE_IPV6_DELETE_LIST = \
    getattr(nal_portal_settings, 'SERVICE_UPDATE_IPV6_DELETE_LIST', None)

SERVICE_TYPE_MAP = {}
for type, service_name in SERVICE_TYPE_MAPPING.iteritems():
    SERVICE_TYPE_MAP[service_name] = type

DISPLAY_CREATE_COLUMNS_MAP = {}
for service_type, columns in SERVICE_CREATE_DISPLAY_COLUMNS_LIST.iteritems():
    for column_name in columns:
        if column_name not in DISPLAY_CREATE_COLUMNS_MAP:
            DISPLAY_CREATE_COLUMNS_MAP[column_name] = []
        DISPLAY_CREATE_COLUMNS_MAP[column_name].append(service_type)

DISPLAY_UPDATE_COLUMNS_MAP = {}
for service_type, columns in SERVICE_UPDATE_DISPLAY_COLUMNS_LIST.iteritems():
    for column_name in columns:
        if column_name not in DISPLAY_UPDATE_COLUMNS_MAP:
            DISPLAY_UPDATE_COLUMNS_MAP[column_name] = []
        DISPLAY_UPDATE_COLUMNS_MAP[column_name].append(service_type)


def _get_network_list(request):
    try:
        tenant_id = request.user.tenant_id
        networks = api.neutron.network_list_for_tenant(request,
                                                       tenant_id)
    except Exception:
        msg = _('Failed to get network list.')
        redirect = reverse(constants.SERVICE_INDEX_URL)
        exceptions.handle(request, msg, redirect=redirect)

    return networks


def _get_subnet_list(request, network_id):
    try:
        subnets = api.neutron.subnet_list(request,
                                          network_id=network_id)
    except Exception:
        msg = _('Failed to get subnet list.')
        redirect = reverse(constants.SERVICE_INDEX_URL)
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
        msg = _('Failed to get network list.')
        redirect = reverse(constants.SERVICE_INDEX_URL)
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
        redirect = reverse(constants.SERVICE_INDEX_URL)
        exceptions.handle(request, msg, redirect=redirect)

    return subnet


class CreateServiceForm(forms.SelfHandlingForm):

    def __init__(self, request, *args, **kwargs):

        super(CreateServiceForm, self).__init__(request, *args, **kwargs)

        contract_type = NAL_CONSTRUCT_SERVICE_TYPE
        service_type_key = 'service_type_' + contract_type
        service_name = SERVICE_CREATE_COLUMNS['service_name']
        service_type = SERVICE_CREATE_COLUMNS[service_type_key]

        self.fields['service_name'] = getattr(forms, service_name['field'])(
            label=service_name['label'],
            required=service_name['required'])

        self.fields['service_type'] = getattr(forms, service_type['field'])(
            label=service_type['label'],
            choices=service_type['choices'],
            required=service_type['required'],
            widget=forms.Select(attrs={'class': 'sub_switchable',
                                       'id': 'service_type'}))

        for column in SERVICE_CREATE_COLUMNS['separate']:
            input_attrs = {}
            for input in DISPLAY_CREATE_COLUMNS_MAP[column[0]]:
                input_attrs['data-' + SERVICE_TYPE_MAP[input]] = \
                    column[1]['label']

            input_attrs['class'] = 'switched'
            input_attrs['id'] = column[0]

            if column[1]['field'] == 'ChoiceField':
                self.fields[column[0]] = getattr(forms, column[1]['field'])(
                    label=column[1]['label'],
                    choices=column[1]['choices'],
                    required=column[1]['required'],
                    widget=forms.Select(attrs=input_attrs))
            elif column[1]['field'] == 'BooleanField':
                self.fields[column[0]] = getattr(forms, column[1]['field'])(
                    label=column[1]['label'],
                    required=column[1]['required'],
                    widget=forms.CheckboxInput(attrs=input_attrs))
            else:
                self.fields[column[0]] = getattr(forms, column[1]['field'])(
                    label=column[1]['label'],
                    required=column[1]['required'],
                    widget=forms.TextInput(attrs=input_attrs))

        if 'IaaS_subnet_id' in self.fields:
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
                self.fields['IaaS_subnet_id'].choices = subnet_choices
            else:
                messages.error(request,
                               'There are no selectable subnets.')
                raise exceptions.NotAvailable

    def handle(self, request, data):
        try:
            service_type = data['service_type']
            service_type_name = SERVICE_TYPE_MAPPING[service_type]

            tenant_id = request.user.project_id
            services = nal_api.get_services(request, tenant_id,
                                            func_type='all_dcconnect')
            for service in services:
                if SERVICE_FUNCTION_TYPE_MAPPING[service.service_type] \
                        == 'dcconnect':
                    messages.error(request,
                                   'DC connection service is already created.')
                    raise exceptions.NotAvailable

            func_type = SERVICE_FUNCTION_TYPE_MAPPING[service_type]
            params = {'service_name': data['service_name'],
                      'service_type': service_type,
                      'function_type': func_type}

            for column in SERVICE_CREATE_COLUMNS['separate']:
                if service_type_name in DISPLAY_CREATE_COLUMNS_MAP[column[0]]:
                    if isinstance(data[column[0]], bool):
                        data[column[0]] = int(data[column[0]])
                    params[column[0]] = data[column[0]]

            service_detail = \
                SERVICE_TYPE_DETAIL_MAPPING.get(service_type_name, {})
            for key, value in service_detail.iteritems():
                params[key] = value

            if 'IaaS_subnet_id' in params:
                subnet_id = data['IaaS_subnet_id']
                subnet_detail = _get_subnet_detail(request, subnet_id)
                network = _get_network_detail(request,
                                              subnet_detail.network_id)
                params['IaaS_network_type'] = network['IaaS_network_type']
                params['IaaS_network_id'] = network['IaaS_network_id']
                params['IaaS_segmentation_id'] = \
                    network['IaaS_segmentation_id']
                params['network_name'] = network['network_name']

            service = nal_api.create_service(request, params)
            msg = _('Job of service creation is running.')
            LOG.debug(msg)
            messages.success(request, msg)
            return True

        except exceptions.NotAvailable:
            return False
        except Exception:
            redirect = reverse(constants.SERVICE_INDEX_URL)
            exceptions.handle(request, redirect=redirect)

    def clean(self):
        data = super(CreateServiceForm, self).clean()
        service_type = data['service_type']
        service_type_name = SERVICE_TYPE_MAPPING[service_type]
        for column in SERVICE_CREATE_COLUMNS['separate']:
            if column[1]['required'] and column[0] in self._errors:
                if service_type_name not in \
                        DISPLAY_CREATE_COLUMNS_MAP[column[0]]:
                    del self._errors[column[0]]
        return data


class UpdateServiceForm(forms.SelfHandlingForm):
    group_id = forms.CharField(widget=forms.HiddenInput())
    func_type = forms.CharField(widget=forms.HiddenInput())
    update_type = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, request, *args, **kwargs):
        super(UpdateServiceForm, self).__init__(request, *args, **kwargs)

        func_type = kwargs['initial']['obj_id'].split('|')[0]
        group_id = kwargs['initial']['obj_id'].split('|')[1]
        subnet_id = ''
        if len(kwargs['initial']['obj_id'].split('|')) == 3:
            subnet_id = kwargs['initial']['obj_id'].split('|')[2]
        update_type = kwargs['initial']['update_type']

        service = nal_api.get_services(self.request, group_id=group_id,
                                       func_type=func_type)
        self.fields['group_id'].initial = group_id
        self.fields['func_type'].initial = func_type
        self.fields['update_type'].initial = update_type

        if SERVICE_UPDATE_COLUMNS[update_type]['display_type'] == \
                'input_column':
            service_columns = SERVICE_DETAIL_DISPLAY_COLUMNS[func_type]
            detail_data = service[service_columns['detail_name']][0]
            network_list = service[service_columns['network_name']]

            for column in SERVICE_UPDATE_COLUMNS[update_type]['common']:
                input_attrs = {}
                for attr_key, attr_val in column[1]['widget'].items():
                    input_attrs[attr_key] = attr_val

                if column[1]['field'] == 'ChoiceField':
                    self.fields[column[0]] = getattr(forms,
                                                     column[1]['field'])(
                        label=column[1]['label'],
                        choices=column[1]['choices'],
                        required=column[1]['required'],
                        widget=forms.Select(attrs=input_attrs))
                else:
                    self.fields[column[0]] = getattr(forms,
                                                     column[1]['field'])(
                        label=column[1]['label'],
                        required=column[1]['required'],
                        widget=forms.TextInput(attrs=input_attrs))

                if hasattr(detail_data, column[0]):
                    if 'service_type' == column[0]:
                        self.fields['service_type'].initial = \
                            SERVICE_TYPE_MAPPING.get(
                                str(getattr(detail_data, column[0])),
                                getattr(detail_data, column[0]))
                    else:
                        self.fields[column[0]].initial = getattr(detail_data,
                                                                 column[0])

            for column in SERVICE_UPDATE_COLUMNS[update_type]['separate']:
                if SERVICE_TYPE_MAPPING[str(detail_data.service_type)] in \
                        DISPLAY_UPDATE_COLUMNS_MAP[column[0]]:
                    if column[1]['field'] == 'ChoiceField':
                        self.fields[column[0]] = getattr(forms,
                                                         column[1]['field'])(
                            label=column[1]['label'],
                            choices=column[1]['choices'],
                            help_text=column[1].get('help_text'),
                            required=column[1]['required'])
                    elif column[1]['field'] == 'BooleanField':
                        self.fields[column[0]] = getattr(forms,
                                                         column[1]['field'])(
                            label=column[1]['label'],
                            required=column[1]['required'])
                    else:
                        self.fields[column[0]] = getattr(forms,
                                                         column[1]['field'])(
                            label=column[1]['label'],
                            help_text=column[1].get('help_text'),
                            required=column[1]['required'])

            self._logic_by_update_type(request,
                                       update_type,
                                       detail_data,
                                       network_list,
                                       subnet_id)

    def handle(self, request, data):
        try:
            update_type = data['update_type']
            display_type = SERVICE_UPDATE_COLUMNS[update_type]['display_type']

            params = {'group_id': data['group_id'],
                      'function_type': data['func_type']}

            if display_type == 'input_column':

                for column in SERVICE_UPDATE_COLUMNS[update_type]['common']:
                    if column[0] == 'service_type':
                        common_value = SERVICE_TYPE_MAP[data[column[0]]]
                    else:
                        common_value = data[column[0]]
                    params[column[0]] = common_value

                for column in SERVICE_UPDATE_COLUMNS[update_type]['separate']:
                    if column[0] in data:
                        if isinstance(data[column[0]], bool):
                            data[column[0]] = int(data[column[0]])
                        params[column[0]] = data[column[0]]

                service_detail = \
                    SERVICE_TYPE_DETAIL_MAPPING.get(data['service_type'], {})
                for key, value in service_detail.iteritems():
                    params[key] = value

                if 'IaaS_subnet_id' in data:
                    subnet_id = data['IaaS_subnet_id']
                    subnet_detail = _get_subnet_detail(request, subnet_id)
                    network = _get_network_detail(request,
                                                  subnet_detail.network_id)
                    params['IaaS_subnet_id'] = subnet_id
                    params['IaaS_network_type'] = network['IaaS_network_type']
                    params['IaaS_network_id'] = network['IaaS_network_id']
                    params['IaaS_segmentation_id'] = \
                        network['IaaS_segmentation_id']
                    params['network_name'] = network['network_name']

            if SERVICE_UPDATE_COLUMNS[update_type]['method'] == 'create':
                nal_api.create_service(request, params)
                msg = _('Job of member creation is running.')
                LOG.debug(msg)
                messages.success(request, msg)
                return True
            else:
                if update_type == 'interface':
                    nal_api.update_service(request, params)
                    msg = _('Job of port creation is running.')
                elif update_type == 'serviceIPv6Add':
                    params['function_type'] = update_type
                    params['vrrp_address'] = data['vrrp_address']
                    params['ce1_address'] = data['ce1_address']
                    params['ce2_address'] = data['ce2_address']
                    nal_api.update_service(request, params)
                    msg = _('Job of add IPv6 Address is running.')
                elif update_type == 'bandwidth':
                    params['function_type'] = update_type
                    nal_api.update_service(request, params)
                    msg = _('Job of update bandwidth is running.')
                else:
                    params['function_type'] = update_type
                    nal_api.update_service(request, params)
                    msg = _('Job of update service setting is running.')
                LOG.debug(msg)
                messages.success(request, msg)
                return True

        except exceptions.NotAvailable:
            return False
        except Exception:
            redirect = reverse(constants.SERVICE_INDEX_URL)
            exceptions.handle(request, redirect=redirect)

    def clean(self):
        data = super(UpdateServiceForm, self).clean()
        return data

    def _get_unused_subnet_choices(self, request, network_list):

        networks = _get_network_list(request)
        used_subnet_list = [net.subnet_id for net in network_list]
        subnet_choices = []
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

        return subnet_choices

    def _get_used_subnet_choices(self, request, used_subnet_list, detail_data,
                                 subnet_id=''):

        my_dc_used_subnets = []
        subnet_choices = []
        for used_subnet in used_subnet_list:
            if used_subnet.dc_id == detail_data.my_dc_id:
                my_dc_used_subnets.append(used_subnet.subnet_id)

        networks = _get_network_list(request)
        for network_data in networks:
            subnets = _get_subnet_list(request, network_data.id)

            for subnet in subnets:
                if subnet.id in my_dc_used_subnets:
                    subnet_choices.append((subnet.id,
                                           network_data.name + ': ' +
                                           subnet.cidr +
                                           ' (' + subnet.name + ')'))

        if subnet_choices:
            subnet_choices.insert(0, ("", _("Select subnet")))

        return subnet_choices

    def _check_used_ipv6_subnet(self, network_list, my_dc_id):
        for used_network in network_list:
            if getattr(used_network, 'dc_id') == my_dc_id and \
                    len(used_network.subnet_id_v6) > 0:
                return True
        return False

    def _logic_by_update_type(self, request, update_type, detail_data,
                              network_list, subnet_id):

        if update_type == 'member_create':
            subnet_choices = \
                self._get_unused_subnet_choices(request, network_list)
            if subnet_choices:
                self.fields['IaaS_subnet_id'].choices = subnet_choices
            else:
                messages.error(request,
                               'There are no selectable subnets.')
                raise exceptions.NotAvailable

        elif update_type == 'interface':
            subnet_choices = \
                self._get_unused_subnet_choices(request, network_list)
            if subnet_choices:
                self.fields['IaaS_subnet_id'].choices = subnet_choices
            else:
                messages.error(request,
                               'There are no selectable subnets.')
                raise exceptions.NotAvailable

        elif update_type == 'bandwidth':
            for network_data in network_list:
                if getattr(network_data, 'dc_id') == getattr(detail_data,
                                                             'my_dc_id'):
                    old_bandwidth = getattr(network_data, 'bandwidth')
                    break

            bandwidth_list = \
                copy.deepcopy(self.fields['bandwidth'].choices)
            bandwidth_list.remove(
                (str(old_bandwidth),
                 SERVICE_BANDWIDTH_MAPPING[old_bandwidth]))
            self.fields['bandwidth'].choices = bandwidth_list

        elif update_type == 'serviceSetting':
            interface_choices = \
                self._get_used_subnet_choices(request, network_list,
                                              detail_data)

            interface_list = ['ntp_server_interface',
                              'snmp_server_interface',
                              'syslog_server_interface']
            for interface_key in interface_list:
                if interface_key in self.fields:
                    self.fields[interface_key].choices = interface_choices

        elif update_type == 'serviceIPv6Add':
            for used_network in network_list:
                if subnet_id == used_network.subnet_id:
                    update_network = used_network
                    break

            my_dc_id = getattr(detail_data, 'my_dc_id')
            if self._check_used_ipv6_subnet(network_list, my_dc_id):
                for delete_column in SERVICE_UPDATE_IPV6_DELETE_LIST:
                    del self.fields[delete_column]

            cider_vrrp = getattr(update_network, 'ip_address', '')
            ip_address = cider_vrrp.split('/')[0]
            cider_ce1 = getattr(update_network, 'ce1_address', '')
            ce1_address = cider_ce1.split('/')[0]
            cider_ce2 = getattr(update_network, 'ce2_address', '')
            ce2_address = cider_ce2.split('/')[0]

            self.fields['IaaS_subnet_id'] = \
                forms.CharField(widget=forms.HiddenInput(),
                                initial=update_network.subnet_id)
            self.fields['vrrp_address'] = \
                forms.CharField(widget=forms.HiddenInput(),
                                initial=ip_address,
                                required=False)
            self.fields['ce1_address'] = \
                forms.CharField(widget=forms.HiddenInput(),
                                initial=ce1_address,
                                required=False)
            self.fields['ce2_address'] = \
                forms.CharField(widget=forms.HiddenInput(),
                                initial=ce2_address,
                                required=False)

            network_data = _get_network_detail(request,
                                               update_network.network_id)
            subnets = _get_subnet_list(request,
                                       update_network.network_id)
            subnets = _get_filtering_subnet_list(subnets, 6)
            subnet_choices = []
            for subnet_data in subnets:
                subnet_choices.append(
                    (subnet_data.id,
                     network_data["network_name"] + ': ' +
                     subnet_data.cidr +
                     ' (' + subnet_data.name + ')'))

            if subnet_choices:
                subnet_choices.insert(0, ("", _("Select subnet")))
                self.fields['IaaS_subnet_id_v6'].choices = subnet_choices
            else:
                messages.error(request,
                               'There are no selectable subnets.')
                raise exceptions.NotAvailable
