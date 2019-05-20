<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/Common/curl_performer.php';

function list_args()
{

  create_var_def('interface', 'String');
  create_var_def('subinterface', 'String');
}


check_mandatory_param('interface');
check_mandatory_param('subinterface');

$ip = $context['device_ip_address'];
$interface = $context['interface'];
$subinterface = $context['subinterface'];

$host = "http://$ip:8080/restconf/data/ietf-interfaces:interfaces/interface=$interface.$subinterface";
$command = "curl --silent -H 'Content-Type:application/yang-data+json' -XDELETE $host";
$response = perform_curl_operation($command, "DELETE VLAN");
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
        $response = prepare_json_response(ENDED, ENDED_SUCCESSFULLY, $response['wo_newparams']['response_body']);
        echo $response;
	task_success('Task OK');
}
else{
	task_error('Task FAILED');
}
?>