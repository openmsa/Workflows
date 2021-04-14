<?php
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';


function list_args()
{
 

}
					/** ******  this part is recovered from step 2  ****** **/

$i=$context['customer_id'];
//$context['result']=json_encode($filecontent);

$filecontent = file_get_contents($context['f']);

if(($context['levelView']=='service') || ($context['levelView']=='summary')) {

$filecontent=preg_replace('#title":"template_(\w+)#','title":"'.$context['dashboardName'].' '.$context['UBIQUBEID'].'', $filecontent);

}

if($context['levelView']=='device') {

$filecontent=preg_replace('#title":"template_(\w+)#','title":"'.$context['dashboardName'].' '.$context['UBIQUBEID'].' '.$context['device_id'].'', $filecontent);

}

/* if filter is empty you just apply customer_id filter , if it's not you add others filter fields */

	if($context['advancedFilterEmpty']=='true'){

		if(($context['levelView']=='service') || ($context['levelView']=='summary')) {

			$filecontent=preg_replace('#customer_id:(\w+)#','customer_id:'.$i.'',$filecontent);
			
	
			/** for netflow **/
			$var='*';
			$filecontent=preg_replace('#host:(\w+)#','host:'.$var.'',$filecontent);
	       }

	       if($context['levelView']=='device') {

			$filecontent=preg_replace('#customer_id:(\w+)#','customer_id:'.$i.' && device_id:'.$context['device_id'].'',$filecontent);
			
			/** for netflow **/
			$filecontent=preg_replace('#host:(\w+)#','host:'.$context['device_ip'].'',$filecontent);
	       }

	}


	elseif($context['advancedFilterEmpty']=='false'){
		
		if(($context['levelView']=='service') || ($context['levelView']=='summary')) {

		$filecontent=preg_replace('#customer_id:(\w+)#','customer_id:'.$i.' && ('.$context['advancedFilter'].')', $filecontent);
		
		/** for netflow **/
		$var='*';
		$filecontent=preg_replace('#host:(\w+)#','host:'.$var.' && ('.$context['advancedFilter'].')',$filecontent);
	        
		}

		if($context['levelView']=='device') {

		$filecontent=preg_replace('#customer_id:(\w+)#','customer_id:'.$i.' && device_id:'.$context['device_id'].' && ('.$context['advancedFilter'].')', $filecontent);



		/** for netflow **/
		
		$filecontent=preg_replace('#host:(\w+)#','host:'.$context['device_ip'].' && ('.$context['advancedFilter'].')',$filecontent);
	        
		}
	

	}



	elseif( $context['basicFilterEmpty']=='true'){

		if(($context['levelView']=='service') || ($context['levelView']=='summary')) {
		
		$filecontent=preg_replace('#customer_id:(\w+)#','customer_id:'.$i.'',$filecontent);
	
	
		/** for netflow **/
		$var='*';
		$filecontent=preg_replace('#host:(\w+)#','host:'.$var.'',$filecontent);
		
		}

		if($context['levelView']=='device') {
		
	
		$filecontent=preg_replace('#customer_id:(\w+)#','customer_id:'.$i.' && device_id:'.$context['device_id'].'',$filecontent);
	
	
		/** for netflow **/
		$filecontent=preg_replace('#host:(\w+)#','host:'.$context['device_ip'].'',$filecontent);
		
		}



	


	}


	elseif($context['basicFilterEmpty']=='false'){

		if(($context['levelView']=='service') || ($context['levelView']=='summary')) {

		$filecontent=preg_replace('#customer_id:(\w+)#','customer_id:'.$i.' && ('.$context['basicFilter'].')', $filecontent);

		/** for netflow **/
		$var='*';
		$filecontent=preg_replace('#host:(\w+)#','host:'.$var.' && ('.$context['basicFilter'].')',$filecontent);
	
	
		}

		if($context['levelView']=='device') {

		$filecontent=preg_replace('#customer_id:(\w+)#','customer_id:'.$i.' && device_id:'.$context['device_id'].' && ('.$context['basicFilter'].')', $filecontent);

		/** for netflow **/
		
		$filecontent=preg_replace('#host:(\w+)#','host:'.$context['device_ip'].' && ('.$context['basicFilter'].')',$filecontent);
	
	
		}




	}

$resp='Filtering';


$filecontent=preg_replace('#id":"(.*)","migrationVersion":{"dashboard":"7.0.0"}#','id":"'.$context['Hash'].'","migrationVersion":{"dashboard":"7.0.0"}', $filecontent);
file_put_contents($context['f'], $filecontent);

						/** ***** End *****/

/**
curl -XPOST "10.30.18.116:5601/kibana/api/kibana/dashboards/import?exclude=index-pattern" -H 'kbn-xsrf: true' -H 'Content-Type: application/json' -d'
{
  "objects": [
    {"attributes":{"description":"","hits":0,"kibanaSavedObjectMeta":{"searchSourceJSON":"{\"filter\":[{\"query\":{\"query_string\":{\"query\":\"customer_id:0\",\"analyze_wildcard\":true}}}]}"},"optionsJSON":"{\"darkTheme\":false}","panelsJSON":"[{\"col\":1,\"panelIndex\":2,\"row\":1,\"size_x\":8,\"size_y\":2,\"panelRefName\":\"panel_0\"},{\"col\":1,\"panelIndex\":4,\"row\":3,\"size_x\":8,\"size_y\":2,\"panelRefName\":\"panel_1\"},{\"col\":9,\"panelIndex\":6,\"row\":3,\"size_x\":4,\"size_y\":2,\"panelRefName\":\"panel_2\"},{\"col\":9,\"panelIndex\":7,\"row\":7,\"size_x\":4,\"size_y\":2,\"panelRefName\":\"panel_3\"},{\"col\":9,\"panelIndex\":8,\"row\":5,\"size_x\":4,\"size_y\":2,\"panelRefName\":\"panel_4\"},{\"col\":1,\"panelIndex\":9,\"row\":5,\"size_x\":8,\"size_y\":2,\"panelRefName\":\"panel_5\"},{\"col\":1,\"panelIndex\":10,\"row\":7,\"size_x\":8,\"size_y\":2,\"panelRefName\":\"panel_6\"},{\"panelIndex\":11,\"size_x\":4,\"size_y\":2,\"col\":9,\"row\":1,\"panelRefName\":\"panel_7\"}]","timeRestore":false,"title":"template_default","uiStateJSON":"{}","version":1},"id":"template_default","migrationVersion":{"dashboard":"7.0.0"},"references":[{"id":"default-Log-View-EVENTS-OVER-TIME","name":"panel_0","type":"visualization"},{"id":"default-Devices_ID","name":"panel_1","type":"visualization"},{"id":"default-Visualization_type","name":"panel_2","type":"visualization"},{"id":"default-count-devices","name":"panel_3","type":"visualization"},{"id":"default-Indexed-EVENTS","name":"panel_4","type":"visualization"},{"id":"default-TOP10-IpDest","name":"panel_5","type":"visualization"},{"id":"default-TOP10-IpSrc","name":"panel_6","type":"visualization"},{"id":"timeFilter","name":"panel_7","type":"visualization"}],"type":"dashboard","updated_at":"2019-07-12T12:53:34.410Z","version":"WzEwMjcsMV0="}
  ]
}
'

**/


$context['uriDeleteES']='http://'.$context['ipAddress'].':'.$context['port'].$context['basePath'].'/api/saved_objects/dashboard/'.$context['Hash'].'';

$ci = curl_init();
    curl_setopt($ci, CURLOPT_URL, $context['uriDeleteES']);
    curl_setopt($ci, CURLOPT_TIMEOUT, 200);
    curl_setopt($ci, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ci, CURLOPT_FORBID_REUSE, 0);
    curl_setopt($ci, CURLOPT_CUSTOMREQUEST, 'DELETE');
    curl_setopt($ci, CURLOPT_HTTPHEADER, array('kbn-xsrf: true','Content-Type: application/json'));
    $response2 = curl_exec($ci);


$context['uriPutES']='http://'.$context['ipAddress'].':'.$context['port'].$context['basePath'].'/api/kibana/dashboards/import?exclude=index-pattern';
$json_doc='{"objects": [ '.$filecontent.']}';



$ci = curl_init();
    curl_setopt($ci, CURLOPT_URL, $context['uriPutES']);
    curl_setopt($ci, CURLOPT_TIMEOUT, 200);
    curl_setopt($ci, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ci, CURLOPT_FORBID_REUSE, 0);
    curl_setopt($ci, CURLOPT_CUSTOMREQUEST, 'POST');
    curl_setopt($ci, CURLOPT_POSTFIELDS, $json_doc);
    curl_setopt($ci, CURLOPT_HTTPHEADER, array('kbn-xsrf: true','Content-Type: application/json'));
    $response = curl_exec($ci);

  unlink($context['f']);

$check=json_decode($response,true);
if(!isset($check['statusCode'])){
 	
	 task_exit(ENDED, "The dashboard has been updated");
}

 else{
 	
	 task_exit(WARNING, $response);
}
 //task_exit(ENDED, $response);
 

?>