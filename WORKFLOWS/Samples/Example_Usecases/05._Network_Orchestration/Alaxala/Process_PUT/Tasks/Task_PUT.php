<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/Reference/Common/curl_performer.php';

function list_args()
{
  create_var_def('interface', 'String');
  create_var_def('subinterface', 'String');
}

function url_encode_ipop($input_string){

$output_string = str_replace(' ','%20',$input_string);
$output_string = str_replace('/','%2F',$output_string);

return $output_string;

}

check_mandatory_param('interface');
check_mandatory_param('subinterface');

$ip = $context['device_ip_address'];

/***   We do NOT use urlencode (see SUPFUJ-155)***/
//$interface = urlencode($context['interface']);
$interface = $context['interface'];
$interface_URL = url_encode_ipop($context['interface']);

$subinterface = $context['subinterface'];

$host = "/restconf/data/ietf-interfaces:interfaces/interface=$interface_URL.$subinterface";

$host = 'http://'.$ip.':8080'.$host;

$body = '{"ietf-interfaces:interface": [
  {
    "ietf-interfaces-common:parent-interface": "'."$interface".'",
    "type": "iana-if-type:l2vlan",
    "name": "'.$interface.'.'.$subinterface.'",
    "ietf-interfaces-common:encapsulation": {
      "ietf-flexible-encapsulation:flexible": {
        "match": {
          "dot1q-vlan-tagged": {
            "outer-tag": {
              "vlan-id": '.$subinterface.',
              "tag-type": "ieee802-dot1q-types:s-vlan"
            }
          }
        }  }  }  }]}';

$command = "curl --silent -H 'content-type:application/yang-data+json' -X PUT '$host' -d '$body'";

logToFile("create VLAN curl command:\n".$command);

$response = perform_curl_operation($command, "Create VLAN");
$response = json_decode($response, true);


if ($response['wo_status'] == ENDED) {
	
	task_success('Creation of the VLAN OK '.url_encode_ipop($interface));
}
else{
	task_error('Task FAILED');
}
?>