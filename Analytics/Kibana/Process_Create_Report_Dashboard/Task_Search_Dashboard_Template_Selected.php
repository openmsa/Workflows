<?php
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';


// List all the parameters required by the task
function list_args()
{
  
 create_var_def('ipAddress', 'IpAddress');
 create_var_def('type', 'String');
 create_var_def('template_id', 'String');
 create_var_def('searchingURI', 'String');
 create_var_def('Hash', 'String');
 create_var_def('dashboardName', 'String');
 create_var_def('basePath', 'String');
 create_var_def('kibanaUrl', 'String');
 create_var_def('kibanaPort', 'Integer');
 create_var_def('kibanaIpAddress', 'IpAddress');
}

$context['kibanaIpAddress']="msa_kibana";
$context['kibanaPort']="5601";

/**
curl -XPOST "10.30.18.116:5601/kibana/api/saved_objects/_export" -H 'kbn-xsrf: true' -H 'Content-Type: application/json' -d'
{
  "objects": [
    {
      "type": "dashboard",
      "id": "template_dashboard"
    }
  ]
}
'
**/

$context['ipAddress']="msa_kibana";
/* ** Set basePath ** */
$context['basePath']="/kibana";

/* ** Url and Method to Find selected Dashboard **** */ 
$context['searchingURI']='http://'.$context['ipAddress'].':'.$context['kibanaPort'].$context['basePath'].'/api/saved_objects/_export';
$context['Hash']=$context['template_id'];
$context['kibanaUrl']='http://'.$context['kibanaIpAddress'].':'.$context['kibanaPort'].'/kibana/app/kibana#/dashboard/'.$context['Hash'].'/';

$body_request='
{
  "objects": [
    {
      "type": "'.$context['type'].'",
      "id": "'.$context['template_id'].'"
    }
  ],
  "excludeExportDetails": true
}
';

$ci = curl_init();
    curl_setopt($ci, CURLOPT_URL,$context['searchingURI']);
    curl_setopt($ci, CURLOPT_TIMEOUT, 200);
    curl_setopt($ci, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ci, CURLOPT_FORBID_REUSE, 0);
    curl_setopt($ci, CURLOPT_CUSTOMREQUEST, 'POST');
    curl_setopt($ci, CURLOPT_POSTFIELDS, $body_request);
    curl_setopt($ci, CURLOPT_HTTPHEADER, array('kbn-xsrf: true','Content-Type: application/json','Authorization: Basic c3VwZXJ1c2VyOnheWnl1R002fnU9K2ZZMkc='));
    $result= curl_exec($ci);

/* Store the result in a variable      */    
$context['result']=$result;	

$check=json_decode($result,true);
if(!isset($check['statusCode'])){

    task_exit(ENDED, 'Template ID '.$context['template_id'].' has been found');
	 
}
else{

 	task_exit(WARNING, 'Template ID '.$context['template_id'].' has not been found => '.$result.'');
}
//task_exit(ENDED, $result);
?>