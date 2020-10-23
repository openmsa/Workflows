<?php

/**
 * This file is necessary to include to use all the in-built libraries of /opt/fmc_repository/Reference/Common
 */
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function create_new_customer($customer_name, $context) {
  	$ms_ipam_tenant = $context['microservices_array']['IPAM Tenants'];
	$ms_ipam_prefix = $context['microservices_array']['IPAM IPv4 prefixes'];
	$ipam_device_id = $context['ipam_device_id'];
  
  	$response = update_asynchronous_task_details($context, "Create tenant.... ");
    $micro_service_vars_array = array ();
	$micro_service_vars_array ['object_id'] = $customer_name;
	$ms_array = array($ms_ipam_tenant => array ($customer_name => $micro_service_vars_array));
	$response = json_decode(execute_command_and_verify_response ( $ipam_device_id, CMD_CREATE, $ms_array, "CREATE new teant"), True);
    if ($response['wo_status'] !== ENDED) {
        $response = json_encode($response);
        echo $response;
        exit;
	}
}

function create_subnets($customer_name, $context) {
  
    $ms_ipam_tenant = $context['microservices_array']['IPAM Tenants'];
	$ms_ipam_prefix = $context['microservices_array']['IPAM IPv4 prefixes'];
	$ipam_device_id = $context['ipam_device_id'];
  
   	$response = update_asynchronous_task_details($context, "Create subnets.... ");
	$response = json_decode(synchronize_objects_and_verify_response($ipam_device_id), true);
	if ($response['wo_status'] !== ENDED) {
	  echo $response;
	  exit;
	}
  	$response = json_decode(import_objects($ipam_device_id, array($ms_ipam_tenant)), True);
	$ms_objects_array = $response['wo_newparams'][$ms_ipam_tenant];
  
	$tenant_id = $ms_objects_array["id"];
    
	foreach (range(0,31) as $third_octet) {
      	$prefix = '11.11.'.$third_octet.'.0/24';
    	$micro_service_vars_array = array ();
		$micro_service_vars_array ['object_id'] = $prefix;
        $micro_service_vars_array ['status'] = 'reserved';
        $micro_service_vars_array ['tenant'] = $tenant_id;
      	$micro_service_vars_array ['tags'] = array(array("tag" => "lan"));
		$ms_array = array($ms_ipam_prefix  => array ($prefix => $micro_service_vars_array));
		$response = json_decode(execute_command_and_verify_response ( $ipam_device_id, CMD_CREATE, $ms_array, "CREATE new subnet"), True);
    	if ($response['wo_status'] !== ENDED) {
       		$response = json_encode($response);
       		echo $response;
       		exit;
		}
    }
  
    foreach (range(0,30,2) as $forth_octet) {
      	$prefix = '11.11.255.'.$forth_octet.'/31';
    	$micro_service_vars_array = array ();
		$micro_service_vars_array ['object_id'] = $prefix;
        $micro_service_vars_array ['status'] = 'reserved';
        $micro_service_vars_array ['tenant'] = $tenant_id;
      	$micro_service_vars_array ['tags'] = array(array("tag" => "p2p"));
		$ms_array = array($ms_ipam_prefix  => array ($prefix => $micro_service_vars_array));
		$response = json_decode(execute_command_and_verify_response ( $ipam_device_id, CMD_CREATE, $ms_array, "CREATE new subnet"), True);
    	if ($response['wo_status'] !== ENDED) {
       		$response = json_encode($response);
       		echo $response;
       		exit;
		}
    }
}



$ms_ipam_tenant = $context['microservices_array']['IPAM Tenants'];
$ms_ipam_prefix = $context['microservices_array']['IPAM IPv4 prefixes'];
$ipam_device_id = $context['ipam_device_id'];
$customer_name = $context['customer_name'];

$response = json_decode(synchronize_objects_and_verify_response($ipam_device_id), true);
if ($response['wo_status'] !== ENDED) {
  echo $response;
  exit;
}

$response = update_asynchronous_task_details($context, "Retrive information about current customers ");
$response = json_decode(import_objects($ipam_device_id, array($ms_ipam_tenant)), True);
$ms_objects_array = $response['wo_newparams'][$ms_ipam_tenant];

$does_tenant_exist = False;
foreach ($ms_objects_array as $tenant_name => $tenant_details) {
  if ($tenant_name === $customer_name) {
    $does_tenant_exist = True;
  }
}

if (!$does_tenant_exist) {
	$result = create_new_customer($customer_name, $context);
  	$result = create_subnets($customer_name, $context);
}

task_success('Task OK');
?>