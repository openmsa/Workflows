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
  create_var_def('nic', 'String');
  create_var_def('vm_name', 'String');
  create_var_def('vm_size', 'String');
  create_var_def('image_offer', 'String');
  create_var_def('image_publisher', 'String');
  create_var_def('image_sku', 'String');
  create_var_def('image_version', 'String'); 
  create_var_def('admin_username', 'String');
  create_var_def('admin_password', 'String');
  create_var_def('operation', 'String');
  create_var_def('vm_status', 'String');
  create_var_def('signature', 'String');
  create_var_def('licenseTextLink', 'String');
  create_var_def('privacyPolicyLink', 'String');
  create_var_def('retrieveDatetime', 'String');
}

$context['operation']='Re Deploy VM '.$context['vm_name'].'';

if($context['image_publisher']=='fortinet'){

$authorization = 'Authorization: Bearer '.$context['token'].'';
$context['URL']='https://management.azure.com/subscriptions/'.$context['subscription_id'].'/providers/Microsoft.MarketplaceOrdering/offertypes/virtualmachine/publishers/'.$context['image_publisher'].'/offers/'.$context['image_offer'].'/plans/'.$context['image_sku'].'/agreements/current?api-version=2015-06-01';


$ci = curl_init();
    curl_setopt($ci, CURLOPT_HTTPHEADER, array('Content-Type: application/json' , $authorization ));
    curl_setopt($ci, CURLOPT_URL, $context['URL']);
    curl_setopt($ci, CURLOPT_TIMEOUT, 200);
    curl_setopt($ci, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ci, CURLOPT_FORBID_REUSE, 0);
    curl_setopt($ci, CURLOPT_CUSTOMREQUEST, 'GET');
    $response = curl_exec($ci);

$res = json_decode($response, true);
$context['signature']=$res['properties']['signature'];
$context['licenseTextLink']=$res['properties']['licenseTextLink'];
$context['privacyPolicyLink']=$res['properties']['privacyPolicyLink'];
$context['retrieveDatetime']=$res['properties']['retrieveDatetime'];


$doc='{"id": "/subscriptions/'.$context['subscription_id'].'/providers/Microsoft.MarketplaceOrdering/offertypes/virtualmachine/publishers/'.$context['image_publisher'].'/offers/'.$context['image_offer'].'/plans/'.$context['image_sku'].'","name": "'.$context['image_sku'].'","type": "Microsoft.MarketplaceOrdering/offertypes","properties": {"publisher": "'.$context['image_publisher'].'","product": "'.$context['image_offer'].'","plan": "'.$context['image_sku'].'","licenseTextLink":"'.$context['licenseTextLink'].'","privacyPolicyLink":"'.$context['privacyPolicyLink'].'","retrieveDatetime":"'.$context['retrieveDatetime'].'","signature":"'.$context['signature'].'","accepted": true}}';


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
}

else 
{
task_exit(ENDED, "No need license");
}
//$ret = prepare_json_response(ENDED, $response, true);
?>