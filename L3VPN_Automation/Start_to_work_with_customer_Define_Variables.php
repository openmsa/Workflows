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
$context['microservices_array'] = 
  				array('IPAM IPv4 addresses'			=> 'ip_address',
                      'IPAM IPv4 prefixes'			=> 'prefix',
                      'IPAM Sites'					=> 'sites',
                      'IPAM Tenants'      			=> 'tenant',
                      'IPAM VLANs'            		=> 'vlan',
                      'IPAM VRFs'             		=> 'vrf',
                      'IPAM Devices'             	=> 'devices',
                      'IPAM Interfaces'             => 'interfaces',
                      'IPAM Interface Connections'  => 'interface_connections',
                      );

$context['device_models_array'] = array(
										'Juniper Networks' => array('manufacture_id' => '18',
                                                                    'model_id' => array(
                                                                      				  'rest' => '191191',
                                                                      				  'srx'  => '121'
                                                                    				  ),
                                                                    'deployment_settings' => array(
                                                                      				  'rest' => 'ds_juniper_rest_1'
                                                                    				  )
                                        							),
  										'Cisco Systems'	   => array('manufacture_id' => '1',
                                                                    'model_id' => array(
                                                                      				  'cli' => '113'
                                                                    				  )
                                        							),
                                                                      'deployment_settings' => array(
                                                                      				  'cli' => 'ds_cisco_isr_1'
                                                                    				  )
									   );

task_success('Success. All variables have been defined.');
?>