<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args()
{
  create_var_def('customer_name', 'String');
  create_var_def('ipam_device_id', 'Device');
}

check_mandatory_param('customer_name');
check_mandatory_param('ipam_device_id');

//microservice_array contains microservice's description and name
$context['microservices_array'] = array('IPAM IPv4 addresses'			=> 'Netbox___IP_address',
                                        'IPAM IPv4 prefixes'			=> 'Netbox___Prefix',
                                        'IPAM Sites'					=> 'Netbox___Sites',
                                        'IPAM Tenants'      			=> 'NetBox___Tenant',
                                        'IPAM VLANs'            		=> 'Netbox___VLAN',
                                        'IPAM VRFs'             		=> 'Netbox___VRF',
                                        'IPAM Devices'          		=> 'Netbox___Devices',
                                        'IPAM Interfaces'       		=> 'Netbox___Interfaces',
                                        'IPAM Interface Connections'    => 'Netbox___Interface_connections',
                                        );

task_success('Success. All variables have been defined.');
?>