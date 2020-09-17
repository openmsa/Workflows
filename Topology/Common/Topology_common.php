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


function calcMask($maskAdr) {
	$maskPart = explode(".", $maskAdr);
	$mask = "";
	foreach ($maskPart as $val) {
		$mask .= decbin(intval($val));
	}
	$result=0;
	$pos = strpos($mask, "0");
	if ($pos !== false) {
		$result = $pos;
	} else {
		$result = 32;
	}
	logTofile("calcMask ".$maskAdr." -> ".$result);
	return $result;
}

function getNetworkByAddressAndMask($address, $mask) {
	$addressParts = explode(".", $address);
	$networkAddressBinary = "";
	foreach ($addressParts as $val) {
		$morceauBinaire = decbin(intval($val));
		while (strlen($morceauBinaire) < 8) {
			$morceauBinaire = "0" . $morceauBinaire;
		}
		$networkAddressBinary .= $morceauBinaire;
	}
	
	$networkAddressBinary = substr($networkAddressBinary, 0, $mask);
	while (strlen($networkAddressBinary) < 32) {
		$networkAddressBinary .= "0";
	}
	
	$addressMasked = "";
	for($i = 0; $i < 32; $i = $i + 8) {
		$part = intval(substr($networkAddressBinary, $i, 8), 2);
		$addressMasked .= $part . ".";
	}
	
	$addressMasked = substr($addressMasked, 0, strlen($addressMasked) - 1);
	logTofile("getNetworkByAddressAndMask: ".$address." ".$mask." -> ".$addressMasked."\n");
	return $addressMasked;
}

?>