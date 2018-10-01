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
  //create_var_def('client_id', 'String');
  //create_var_def('client_secret', 'String');
  //create_var_def('tenant_id', 'String');
  //create_var_def('URL', 'String');
}

$context['URL']='https://login.microsoftonline.com/'.$context['tenant_id'].'/oauth2/token';
$doc='grant_type=client_credentials&client_id='.$context['client_id'].'&client_secret='.$context['client_secret'].'&resource=https%3A%2F%2Fmanagement.azure.com%2F';


$ci = curl_init();
    curl_setopt($ci, CURLOPT_URL, $context['URL']);
    curl_setopt($ci, CURLOPT_TIMEOUT, 200);
    curl_setopt($ci, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ci, CURLOPT_FORBID_REUSE, 0);
    curl_setopt($ci, CURLOPT_CUSTOMREQUEST, 'POST');
    curl_setopt($ci, CURLOPT_POSTFIELDS, $doc);
    $response = curl_exec($ci);

$res = json_decode($response, true);
$context['token']=$res['access_token'];

task_exit(ENDED, $response);
//$ret = prepare_json_response(ENDED, $response, true);
?>