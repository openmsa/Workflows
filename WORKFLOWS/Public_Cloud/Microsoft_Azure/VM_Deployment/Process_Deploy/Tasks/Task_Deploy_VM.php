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
}

$context['operation']='Deploy VM '.$context['vm_name'].'';

$authorization = 'Authorization: Bearer '.$context['token'].'';
$context['URL']='https://management.azure.com/subscriptions/'.$context['subscription_id'].'/resourceGroups/'.$context['res_gr_name'].'/providers/Microsoft.Compute/virtualMachines/'.$context['vm_name'].'?api-version=2017-12-01';

/** Attach several private network interfaces **/

$attach_pv_int='';

if (!empty($context['private'])) {

foreach ($context['private'] as $private) {
$attach_pv_int.=',{"id": "/subscriptions/'.$context['subscription_id'].'/resourceGroups/'.$context['res_gr_name'].'/providers/Microsoft.Network/networkInterfaces/'.$private['nics'].'","properties": {"primary": false}}';
}

}

if($context['image_publisher']=='fortinet'){

$doc='{"location":"'.$context['location'].'","plan": {"name":"'.$context['image_sku'].'","publisher":"'.$context['image_publisher'].'","product":"'.$context['image_offer'].'"},"properties":{"hardwareProfile":{"vmSize":"'.$context['vm_size'].'"},"storageProfile":{"imageReference":{"offer":"'.$context['image_offer'].'","publisher":"'.$context['image_publisher'].'","sku":"'.$context['image_sku'].'","version":"'.$context['image_version'].'"}},"osProfile":{"adminUsername":"'.$context['admin_username'].'","computerName":"'.$context['vm_name'].'","adminPassword":"'.$context['admin_password'].'"},"networkProfile":{"networkInterfaces":[{"id":"/subscriptions/'.$context['subscription_id'].'/resourceGroups/'.$context['res_gr_name'].'/providers/Microsoft.Network/networkInterfaces/'.$context['nic'].'","properties":{"primary":true}}'.$attach_pv_int.']}},"name":"'.$context['vm_name'].'"}';
}

else {
$doc='{"location":"'.$context['location'].'","properties":{"hardwareProfile":{"vmSize":"'.$context['vm_size'].'"},"storageProfile":{"imageReference":{"offer":"'.$context['image_offer'].'","publisher":"'.$context['image_publisher'].'","sku":"'.$context['image_sku'].'","version":"'.$context['image_version'].'"}},"osProfile":{"adminUsername":"'.$context['admin_username'].'","computerName":"'.$context['vm_name'].'","adminPassword":"'.$context['admin_password'].'"},"networkProfile":{"networkInterfaces":[{"id":"/subscriptions/'.$context['subscription_id'].'/resourceGroups/'.$context['res_gr_name'].'/providers/Microsoft.Network/networkInterfaces/'.$context['nic'].'","properties":{"primary":true}}'.$attach_pv_int.']}},"name":"'.$context['vm_name'].'"}';
}

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