<?php

function getStatus($device_id) {
	$info = json_decode(_device_get_status($device_id), true);
	$status = $info ["wo_newparams"];
	
	if (empty($status) || $status == "") {
		return "Managed Entity with id " . $device_id . " was not found";
	} else {
		return $status;
	}
}

function get_customer_ref() {
	global $context;

	// read the customer and get the external reference
	$customer_db_id = substr($context ["UBIQUBEID"],4);
	$response = _customer_read_by_id($customer_db_id);
	$response = json_decode($response, true);
	if ($response['wo_status'] !== ENDED) {
		$response = json_encode($response);
		echo $response;
		exit;
	 }
		  
	$customer_ref = $response['wo_newparams']['externalReference'];
	return $customer_ref;
}

?>