<?php
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args()
{

}


$device_id = substr($context['fw_device'], 3);

//1)
//import service objects and check if the input service/ports are already created in the firewall
//If the service/s is not present, create new service objects on the firewall
//For now we are just creating new service objects based on the user input and not check if it successful
$srv_arr=array();
$services=$context['services'];
foreach($services as $service){
$obj_arr=array();
$obj_arr['protocol']= $service['protocol'];
$obj_arr['object_id']= $service['service_name'];
$obj_arr['destport']= $service['service_port'];
array_push($srv_arr, array('service'=>$service['service_name']));
$ms_obj=array('services' => array($service['service_name'] => $obj_arr));
execute_command_and_verify_response($device_id, CMD_CREATE, $ms_obj , "CREATE Service");

}

//2)
//Create address object/s for destination address
//address_ip_netmask
//object_id
//address
//masklen
$obj_arr=array();
$obj_arr['address']= $context['service_subnet_ip'];
$obj_arr['object_id']= $context['service_id'];
$obj_arr['masklen']= $context['service_subnet_masklen'];

$ms_obj=array('address_ip_netmask' => array($context['service_id'] => $obj_arr));
execute_command_and_verify_response($device_id, CMD_CREATE, $ms_obj , "CREATE destination Address");

//Source address object has to be created as a prerequisite

//We will use default values for zones for now as the interfaces are not created a new for this usecase
//Source zone has to be external
//Destination zone is internal
//Firewall rulename will be same as service id of the workflow

//================================================================================================================
$micro_service2 = array();



$micro_service2['services']	= $srv_arr;

$micro_service2['zone_from']	= $context['source_zone'];
$micro_service2['src_address'] = $context['source_address'];
$micro_service2['zone_to'] = $context['destination_zone'];
$micro_service2['dst_address'] = $context['service_id'];
$micro_service2['object_id'] = $context['service_id'];
$micro_service2['action'] = 'allow';


$managed_entity2 = array('policy' => array($context['service_id'] => $micro_service2));

$response = execute_command_and_verify_response($device_id, CMD_CREATE, $managed_entity2 , "CREATE policy");
$response = json_decode($response, true);

logToFile(debug_dump($response,"*************************\n"));

if($response['wo_status'] !== ENDED)
{				
	$response = prepare_json_response($response['wo_status'], "Failed to create firewall policy", $context, true);	
	echo $response;
	exit;
}

$response = prepare_json_response($response['wo_status'], "Successfully created firewall policy", $context, true);		
echo $response;
?>

