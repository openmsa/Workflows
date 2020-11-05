<?php
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/ENEA/VNF_Management/common.php';

function list_args()
{
	create_var_def('ucpe_devices', 'OMBFRef');
}

$device_id = substr($context['device_id'], 3);
$arr= array("VNF_connections");
$response = import_objects($device_id, $arr);
$response = json_decode($response, true);

if($response['wo_status'] !== ENDED)
{               
    $device_data = prepare_json_response($response['wo_status'], "Failed to get connection data", $response, true);   
    echo $device_data;
    exit;
}

$connection_data = $response['wo_newparams']['VNF_connections'];
$final_connections = array();
//loop through all connections
foreach($connection_data as $connection)
{
	$cons = array_unique($connection["default_name"],SORT_REGULAR);

	foreach($cons as $row)
	{
		$final_connections[] = $connection["vnfdName"]."-".$row["connection_name"];
	
	}
}
	logToFile(debug_dump($final_connections,"*********** Connection data**************\n"));	


$context['fin_connection_values'] = $final_connections;

task_exit(ENDED, "Connection data retreived");
?>