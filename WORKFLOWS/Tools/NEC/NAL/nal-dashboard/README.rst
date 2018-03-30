================
Develop Note
================
CREATE 2016/07/28


================
Setting policy.json
================
1) create policy.json
  command:
  $ cd /etc/openstack-dashboard
  $ vi nal_policy.json
    sample:
    --------------------
    {
        "nal_admin": "role:O__[Region Name]__Nal",
        "nal_member": "role:O__[Region Name]__Nal or role:role:T__[Region Name]__Nal",

        "nal:show_nodea_admin": "rule:nal_admin",
        "nal:show_nodea_project": "rule:nal_member",
        "nal:update_node_interface": "rule:nal_member",
        "nal:update_node_license": "rule:nal_member",
        "nal:delete_node": "rule:nal_member",
        "nal:create_node": "rule:nal_member",
        "nal:delete_node_network": "rule:nal_member"
    }
    --------------------

2)edit setting fail.
  command:
  $ cd /usr/share/openstack-dashboard/openstack_dashboard/
  $ vi settings.py
    sample:
    --------------------
    POLICY_FILES = {
        'identity': 'keystone_policy.json',
        'compute': 'nova_policy.json',
        'volume': 'cinder_policy.json',
        'image': 'glance_policy.json',
        'orchestration': 'heat_policy.json',
        'network': 'neutron_policy.json',
        'telemetry': 'ceilometer_policy.json',
        'nal': 'nal_policy.json'              #add
    }
    --------------------

3)Add role.
  To create the following roles in the role management screen.
    "O__[Region Name]__Nal"
    "T__[Region Name]__Nal" 

  Grant "O__[Region Name]__Nal" to administrator.
  Grant "T__[Region Name]__Nal" to members.
