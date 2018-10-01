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
  create_var_def('vm_name', 'String');
 
  create_var_def('location', 'String');
  
}

$context['public_address']=''.$context['vm_name'].'_public_address_name';

$authorization = 'Authorization: Bearer '.$context['token'].'';
$context['URL']='https://management.azure.com/subscriptions/'.$context['subscription_id'].'/resourceGroups/'.$context['res_gr_name'].'/providers/Microsoft.Network/publicIPAddresses/'.$context['public_address'].'?api-version=2018-04-01';
$doc='{"location":"'.$context['location'].'","properties": {"publicIPAllocationMethod": "Static","idleTimeoutInMinutes": 10,"publicIPAddressVersion": "IPv4"},"sku": {"name": "Standard"}}';


$ci = curl_init();
    curl_setopt($ci, CURLOPT_HTTPHEADER, array('Content-Type: application/json' , $authorization ));
    curl_setopt($ci, CURLOPT_URL, $context['URL']);
    curl_setopt($ci, CURLOPT_TIMEOUT, 200);
    curl_setopt($ci, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ci, CURLOPT_FORBID_REUSE, 0);
    curl_setopt($ci, CURLOPT_CUSTOMREQUEST, 'PUT');
    curl_setopt($ci, CURLOPT_POSTFIELDS, $doc);
    $response = curl_exec($ci);


task_exit(ENDED, $response);
//$ret = prepare_json_response(ENDED, $response, true);
?>