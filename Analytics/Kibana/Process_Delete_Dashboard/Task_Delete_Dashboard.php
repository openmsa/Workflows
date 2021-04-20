<?php
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

// List all the parameters required by the task
function list_args()
{
 
}

/**

curl -XDELETE "localhost:5601/kibana/api/saved_objects/dashboard/1e57e98993aa04d700f3a754781adcb7babac109" -H 'kbn-xsrf: true'

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
    $check=json_decode($response2,true);

if(!isset($check['statusCode'])){
	 task_exit(ENDED, "The dashboard has been deleted : $response2");
}else{
	 task_exit(WARNING, $response2);
}
?>