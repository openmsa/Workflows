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

}

$authorization = 'Authorization: Bearer '.$context['token'].'';


if ($context['private_network']=='true')

{

foreach ($context['private'] as $private) {


$context['URL']='https://management.azure.com/subscriptions/'.$context['subscription_id'].'/resourceGroups/'.$context['res_gr_name'].'/providers/Microsoft.Network/networkInterfaces/'.$private['nics'].'?api-version=2018-06-01';


$ci = curl_init();
    curl_setopt($ci, CURLOPT_HTTPHEADER, array('Content-Type: application/json' , $authorization ));
    curl_setopt($ci, CURLOPT_URL, $context['URL']);
    curl_setopt($ci, CURLOPT_TIMEOUT, 200);
    curl_setopt($ci, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ci, CURLOPT_FORBID_REUSE, 0);
    curl_setopt($ci, CURLOPT_CUSTOMREQUEST, 'DELETE');
    
    $response = curl_exec($ci);

/** To check if the deletion is completed **/

$deleted=false;
do {
$ci = curl_init();
    curl_setopt($ci, CURLOPT_HTTPHEADER, array('Content-Type: application/json' , $authorization ));
    curl_setopt($ci, CURLOPT_URL, $context['URL']);
    curl_setopt($ci, CURLOPT_TIMEOUT, 200);
    curl_setopt($ci, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ci, CURLOPT_FORBID_REUSE, 0);
    curl_setopt($ci, CURLOPT_CUSTOMREQUEST, 'GET');
    $response = curl_exec($ci);

$res = json_decode($response, true);
if (isset($res['error']['code'])){	
  $check=$res['error']['code'];
  if($check=='ResourceNotFound'){
  $deleted=true;
  }
 }
} while($deleted==false);

$rsp='Status : '.$check.'';

}

task_exit(ENDED, $rsp);

}

else {

task_exit(ENDED, "No Private Network Interfaces to delete");

}
//$ret = prepare_json_response(ENDED, $response, true);
?>