<?php 

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args()
{
}

check_mandatory_param('device_id');
check_mandatory_param('device_ip_address');

$ip_address = $context['device_ip_address'];
$device_id=$context['device_id'];
$device_id=getIdFromUbiId ($device_id);
	
$response = _device_update_management_ip_address($device_id, $ip_address);
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
	$response = json_encode($response);
	echo $response;
	exit;
}

//check if ip is update in the sec-engine side
$sec_ip_address = "";
for($i=0; $i<5; $i++){
    sleep(2);
    $output = shell_exec("/opt/dms/bin/oradns --id ".$context['device_id']);
    //example output - ECL480 ip 10.30.19.237 ext ip 10.30.19.237 interface type E (port1-port1) ip type S (UP 31 sec old - 6 pings left)
    if($output != null){
        $details = explode(" ", $output);
        $sec_ip_address = $details[2];
        if($sec_ip_address == $ip_address){
            break;
        }
    }
}

if($sec_ip_address != $ip_address){
    $response = prepare_json_response(FAILED, "Update Management IP $ip_address failed on Sec Engine side, check batchupdate", $context, true);
    echo $response;
    exit;
}
	
$response = prepare_json_response(ENDED, "Management IP $ip_address updated successfully on MSA Device $device_id.", $context, true);
echo $response;

?>