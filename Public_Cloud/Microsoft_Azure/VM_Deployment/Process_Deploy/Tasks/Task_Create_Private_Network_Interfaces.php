<?php

/**
 * This file is necessary to include to use all the in-built libraries of /opt/fmc_repository/Reference/Common
 */
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

/**
 * List all the parameters required by the task
 */
function list_args()
{
  /** 
   * You can use var_name convention for your variables
   * They will display automaticaly as "Var Name"
   * The allowed types are:
   *    'String', 'Boolean', 'Integer', 'Password', 'IpAddress',
   *    'IpMask', 'Ipv6Address', 'Composite', 'OBMFRef', 'Device'
   *
   * Add as many variables as needed
   */
  create_var_def('URL', 'String');
  create_var_def('token', 'String');
  create_var_def('subscription_id', 'String');
  create_var_def('res_gr_name', 'String');
  create_var_def('public_address', 'String');
  create_var_def('subnet_name', 'String');
  create_var_def('interface_name', 'String');
  create_var_def('nic', 'String');
  create_var_def('virtu_net', 'String');
  create_var_def('network_sec_gr_name', 'String');
  create_var_def('vm_name', 'String');


  create_var_def('private_network', 'Boolean');
  create_var_def('private.0.subnet_names', 'String');
  create_var_def('private.0.interface_names', 'String');
  create_var_def('private.0.nics', 'String');
  create_var_def('private.0.virtu_nets', 'String');
  create_var_def('private.0.network_sec_gr_names', 'String');
  //create_var_def('private.0.ips', 'IpAddress');
  
}

if ($context['private_network']=='true')

{

sleep(6);
$authorization = 'Authorization: Bearer '.$context['token'].'';

foreach ($context['private'] as $private) {

$private['interface_names']='intf_'.$private['nics'].'';

$context['URL']='https://management.azure.com/subscriptions/'.$context['subscription_id'].'/resourceGroups/'.$context['res_gr_name'].'/providers/Microsoft.Network/networkInterfaces/'.$private['nics'].'?api-version=2018-06-01';
$doc='{"location":"'.$context['location'].'","properties":{"enableAcceleratedNetworking":true,"networkSecurityGroup":{"id":"/subscriptions/'.$context['subscription_id'].'/resourceGroups/'.$context['res_gr_name'].'/providers/Microsoft.Network/networkSecurityGroups/'.$private['network_sec_gr_names'].'"},"ipConfigurations":[{"name":"'.$private['interface_names'].'","properties":{"privateIPAddress":"10.0.1.3","subnet":{"id":"/subscriptions/'.$context['subscription_id'].'/resourceGroups/'.$context['res_gr_name'].'/providers/Microsoft.Network/virtualNetworks/'.$private['virtu_nets'].'/subnets/'.$private['subnet_names'].'"}}}]}}';


$ci = curl_init();
    curl_setopt($ci, CURLOPT_HTTPHEADER, array('Content-Type: application/json' , $authorization ));
    curl_setopt($ci, CURLOPT_URL, $context['URL']);
    curl_setopt($ci, CURLOPT_TIMEOUT, 200);
    curl_setopt($ci, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ci, CURLOPT_FORBID_REUSE, 0);
    curl_setopt($ci, CURLOPT_CUSTOMREQUEST, 'PUT');
    curl_setopt($ci, CURLOPT_POSTFIELDS, $doc);
    $response = curl_exec($ci);

}
sleep(5);
task_exit(ENDED, $response);

}

else{
task_exit(ENDED, "Private Network Interface disabled");
}
//$ret = prepare_json_response(ENDED, $response, true);
?>