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


from django.conf.urls import patterns
from django.conf.urls import url

from nec_portal.dashboards.admin.resource import views

RESOURCE = r'^(?P<resource_id>[^/]+)/%s$'

urlpatterns = patterns(
    '',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<func_type>[^\|]+)\|(?P<resource_key>[^\|]+)\|'
        'license_table/detail$',
        views.LicenseDetailView.as_view(), name='license_detail'),
    url(r'^(?P<func_type>[^\|]+)\|(?P<resource_key>[^\|]+)\|'
        'pnf_table/detail$',
        views.PnfDetailView.as_view(), name='pnf_detail'),
    url(r'^(?P<func_type>[^\|]+)\|(?P<resource_key>[^\|]+)\|'
        'vlan_table/detail$',
        views.VlanDetailView.as_view(), name='vlan_detail'),
    url(r'^(?P<func_type>[^\|]+)\|(?P<resource_key>[^\|]+)\|'
        'pod_list_table/detail$',
        views.PodListDetailView.as_view(), name='pod_list_detail'),
    url(r'^(?P<func_type>[^\|]+)\|(?P<resource_key>[^\|]+)\|'
        '(?P<pod_id>[^\|]+)\|pod_detail_table/detail$',
        views.PodDetailView.as_view(), name='pod_detail'),
    url(RESOURCE % 'detail', views.LicenseDetailView.as_view(), name='detail'),
)
