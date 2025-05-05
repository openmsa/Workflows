<?php
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

// List all the parameters required by the task
function list_args()
{
 
}

/**

curl -XDELETE "localhost:5601/api/saved_objects/dashboard/1e57e98993aa04d700f3a754781adcb7babac109" -H 'kbn-xsrf: true'

**/


$context['uriDeleteES']='http://'.$context['ipAddress'].':'.$context['port'].'/api/saved_objects/dashboard/'.$context['Hash'].'';

$ci = curl_init();
    curl_setopt($ci, CURLOPT_URL, $context['uriDeleteES']);
    curl_setopt($ci, CURLOPT_TIMEOUT, 200);
    curl_setopt($ci, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ci, CURLOPT_FORBID_REUSE, 0);
    curl_setopt($ci, CURLOPT_CUSTOMREQUEST, 'DELETE');
    curl_setopt($ci, CURLOPT_HTTPHEADER, array('kbn-xsrf: true','Content-Type: application/json'));
    $response2 = curl_exec($ci);

// End of the task do not modify after this point
/**
$ret = prepare_json_response(ENDED,$response, $context);
echo "$ret\n";
**/
task_exit(ENDED, "OK '.$response2.'");
?>