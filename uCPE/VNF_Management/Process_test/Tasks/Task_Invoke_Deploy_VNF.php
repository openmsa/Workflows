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
  
  create_var_def('device_id', 'String');
  create_var_def('vnfs.0.manufacturer_id', 'String');
  create_var_def('vnfs.0.model_id', 'String');
  create_var_def('vnfs.0.device_ip_address', 'String');
  create_var_def('vnfs.0.login', 'String');
  create_var_def('vnfs.0.password', 'String');
  create_var_def('vnfs.0.snmp_community', 'String');
  create_var_def('vnfs.0.conf_profile_reference', 'String');
  create_var_def('vnfs.0.mon_profile_reference', 'String');
  create_var_def('vnfs.0.vnfd', 'String');
  create_var_def('vnfs.0.ucpe_devices', 'String');
  create_var_def('vnfs.0.vnf_name', 'String');

   
  create_var_def('vnfs.0.nics.0.id', 'OBMFRef'); 
  create_var_def('vnfs.0.nics.0.type', 'String');  
  create_var_def('vnfs.0.nics.0.nicmodel', 'Composite'); 
  create_var_def('vnfs.0.nics.0.interfacename', 'OBMFRef');  
}

$ucpe_manager=$context['device_id'];

$json_obj=array("device_id" => "$ucpe_manager");

$json_body=json_encode($json_obj);

$external_ref=$context['UBIQUBEID'];
//------------------------------------------------------
$vnfs=$context['vnfs'];

foreach($vnfs as $vnf){

$process_name="Process/ENEA/VNF_Management/Process_New_Service";
$service_name="Process/ENEA/VNF_Management/VNF_Management";


//create a new WF instance

$response = _orchestration_execute_service_by_reference ($external_ref, "", $service_name, $process_name, $json_body);
 
//Now the returned info is accessed using the $response variable as shown below:
//Decode the json string into objects
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
    task_exit(FAILED, "Service $service_name execution failed.\n" . $response['wo_comment']);
}
$selfcare_instance_id=$response['wo_newparams']['serviceId']['id'];
//As per the above response, the $selfcare_instance_id would now have the value 6608
$selfcare_instance_ref=$response['wo_newparams']['serviceId']['serviceExternalReference'];

//trigger Deploy the VNF
$process_name="Process/ENEA/VNF_Management/Process_test";
$service_name="Process/ENEA/VNF_Management/VNF_Management";
//$ip_address =  $vnf['device_ip_address'];
$ip_address = "127.0.0.1";
$body = array(
      "device_id"            => $ucpe_manager,
      "vnf_descriptor"        => $vnf['vnfd'],
      "ucpe_devices" => $vnf['ucpe_devices'],
      "vnf_name"     => $vnf['vnf_name'],
      "customer_id"    => $external_ref,
      "manufacturer_id"    => $vnf['manufacturer_id'],
      "model_id"    => $vnf['model_id'],
      "device_ip_address"    =>$ip_address ,
      "login"    => $vnf['login'],
      "password"    => $vnf['password'],
      "new_password"    => $vnf['password'],
      "snmp_community"    => $vnf['snmp_community'],
      "conf_profile_reference"    => $vnf['conf_profile_reference'],
      "mon_profile_reference"    => $vnf['mon_profile_reference'],
      "nics"=> $vnf['nics']     
    );
$body = json_encode($body);
$external_ref=$context['UBIQUBEID'];
$response = _orchestration_execute_service_by_reference ($external_ref, $selfcare_instance_ref, $service_name, $process_name, $body);
 
//Now the returned info is accessed using the $response variable as shown below:
//Decode the json string into objects
$response = json_decode($response, true);
if ($response['wo_status'] !== ENDED) {
    task_exit(FAILED, "Service $service_name execution failed.\n" . $response['wo_comment']);
}

}
//---------------------------------------------------------------------------------

/**
 * End of the task (choose one)
 */
task_success('Task OK');
?>