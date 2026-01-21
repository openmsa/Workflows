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
  create_var_def('total_of_devices', 'String'); 
  create_var_def('file', 'String');
}


$response = _lookup_list_device_ids();
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
    $response = prepare_json_response(FAILED, $response['wo_comment'], $context, true);
    echo $response;
    exit;
}

$devices = $response['wo_newparams'];

$counter=0;

$lines[] = array ('Device Name', 'Device ID', 'IP Address');

foreach($devices as $device) {
    
    $device_id = $device['id'];
    
    $response = _device_read_by_id($device_id);
    $response = json_decode($response, true);
   
    if ($response['wo_status'] === ENDED) {
    
                $name = $response['wo_newparams']['name'];
		
        	$management_address = $response['wo_newparams']['managementAddress'];
          
              	$lines[] = array ($name,$device['ubiId'], $management_address);
    }
 
$counter=$counter+1;  

}

$date=date("Y-m-d-h:i:s");
$context['total_of_devices']=$counter;
$lines[] = array ($date,'Total Number of devices', $counter );

$csv_file_path = "/tmp/device_list.csv";
$context['file']=$csv_file_path;

if (file_exists($csv_file_path)) {
	unlink($csv_file_path);
}

$file = fopen($csv_file_path,"w");

$delimiter=",";

// fprintf => to avoid error display characters (accent..) with excel file import

fprintf($file, chr(0xEF).chr(0xBB).chr(0xBF));

foreach($lines as $line){

fputcsv($file, $line,$delimiter);

}

fclose($file);


$res = prepare_json_response(ENDED, "Devices details fetched successfully.", $context, true);
echo $res;


?>