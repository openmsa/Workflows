<?php
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';


// List all the parameters required by the task
function list_args()
{
  
 create_var_def('ipAddress', 'IpAddress');
 create_var_def('port', 'Integer');
 create_var_def('type', 'String');
 create_var_def('template name', 'String');
 create_var_def('searchingURI', 'String');
 create_var_def('uriPutES', 'String');
 create_var_def('customer_id', 'Integer');
 create_var_def('Hash', 'String');
 create_var_def('dashboardName', 'String');


 //create_var_def('kibanaUrl', 'String');
 create_var_def('kibanaPort', 'Integer');
 create_var_def('kibanaIpAddress', 'IpAddress');



 create_var_def('filterType', 'String');
 
 create_var_def('advancedFilter', 'Composite');
 create_var_def('advancedFilterEmpty', 'Composite');

 create_var_def('basicFilterEmpty', 'Composite');
 // create_var_def('basicFilter', 'Composite');

 create_var_def('filter.0.field', 'Composite');
 create_var_def('filter.0.value', 'Composite');
 create_var_def('filter.0.operator', 'Composite');

 create_var_def('filter.0.resultBasictFilter', 'String');

create_var_def('filter.0.apply', 'Composite');



create_var_def('levelView', 'String');

create_var_def('device_id', 'Device');

create_var_def('device_ip', 'IpAddress');




}

// ENTER YOUR CODE HERE
// Update $context array for output variables


if ($context['filterType']=='Advanced'){
	
	if(!empty($context['advancedFilter'])){
	$context['advancedFilterEmpty']='false';
	}
	else{

	$context['advancedFilterEmpty']='true';
	}

}

else {
	
	if(empty($context['filter']))
	{
	  $context['basicFilter'] ='';
	}

	
	else {

	foreach ($context['filter'] as $filter) {
		
			if($filter['apply']=="true"){
				
          			$filter['resultBasicFilter']=' '.$filter['operator'].' '.$filter['field'].':'.$filter['value'];
				
				$context['basicFilter'].=$filter['resultBasicFilter'];
			}
				
		
	}
	
	
	$context['basicFilter'] = substr($context['basicFilter'], 3);
	
	}

	
	if(!empty($context['basicFilter'])){
	$context['basicFilterEmpty']='false';
	}
	else{

	$context['basicFilterEmpty']='true';
	}
}


/* to recover device ip address */

if($context['levelView']=='device') {

preg_match('/(?<digit>\d+)/',$context['device_id'],$device_id_number);
$context['device_id_number']=$device_id_number[1];
$context['cmd']="/opt/ubi-jentreprise/bin/api/device/readDeviceById.sh ".$context['device_id_number'];
$response_cmd= shell_exec($context['cmd']);
preg_match('#<ipAddress>\n<address>(.*)</address>\n<mask>#',$response_cmd, $out);
$context['device_ip']=$out[1];

}




/* Recover IP Address for Kibana */

define('HOST_KIBANA', 'UBI_ES_KIBANA_IP');
$_KIBANA=get_vars_value(HOST_KIBANA);
preg_match('#(.*):#',$_KIBANA,$_KIBANA);
$context['kibanaIpAddress']=$_KIBANA[1];


/* Recover Port Number for Kibana */

$_KIBANA=get_vars_value(HOST_KIBANA);
preg_match('#:(.*)#',$_KIBANA,$_KIBANA);
$context['kibanaPort']=$_KIBANA[1];


/**
curl -XPOST "10.30.18.116:5601/api/saved_objects/_export" -H 'kbn-xsrf: true' -H 'Content-Type: application/json' -d'
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

/* ***   Recove ES ip address   **** */ 
define('HOST_ES', 'UBI_ES_WEBPORTAL_ENDPOINT');
$_H=get_vars_value(HOST_ES);
$context['ipAddress']=$_H;



/* ** recove customer_id) ** */
preg_match('/(?<digit>\d+)/',$context['UBIQUBEID'],$matches);
$context['customer_id']=$matches[1];


/* ***** to hash Url Customer Dashboard ***** */
$context['Hash']=sha1(uniqid($context['customer_id'] . mt_rand(), true));



/* ** Url and Method to Find selected Dashboard **** */ 
$context['searchingURI']='http://'.$context['ipAddress'].':'.$context['port'].'/api/saved_objects/_export';

$body_request='
{
  "objects": [
    {
      "type": "'.$context['type'].'",
      "id": "'.$context['template name'].'"
    }
  ]
}
';



$context['f']='/tmp/file_kibana_'.$context['Hash'].'.ndjson';
$fp = fopen($context['f'], "w");

$ci = curl_init();
    curl_setopt($ci, CURLOPT_URL,$context['searchingURI']);
    curl_setopt($ci, CURLOPT_TIMEOUT, 200);
    curl_setopt($ci, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ci, CURLOPT_FORBID_REUSE, 0);
    curl_setopt($ci, CURLOPT_CUSTOMREQUEST, 'POST');
    curl_setopt($ci, CURLOPT_POSTFIELDS, $body_request);
    curl_setopt($ci, CURLOPT_HTTPHEADER, array('kbn-xsrf: true','Content-Type: application/json'));
    $result= curl_exec($ci);
    fwrite($fp, $result);

/* Store the result in a variable      */    
$context['result']=$result;	



/* ** Store Kibana  Url  ***/ 

$context['kibanaUrl']='http://'.$context['kibanaIpAddress'].':'.$context['kibanaPort'].'/app/kibana#/dashboard/'.$context['Hash'].'/';


$check=json_decode($result,true);
if(!isset($check['statusCode'])){
 	
	 task_exit(ENDED, "Template ID found");
}

 else{
 	
	 task_exit(WARNING, 'Template ID not found => '.$result.'');
}

//task_exit(ENDED, $result);

?>