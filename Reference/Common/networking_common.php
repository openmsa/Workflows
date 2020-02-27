<?php 

/**
 * Generate a list of all IP addresses between $start and $end (inclusive).
 * For Ex. [1.1.1.1, 1.1.1.5] => 1.1.1.1, 1.1.1.2, 1.1.1.3, 1.1.1.4, 1.1.1.5
 *
 * @param unknown $start
 * @param unknown $end
 */
function get_ip_range ($start, $end) {
	$start = ip2long($start);
	$end = ip2long($end);
	return array_map('long2ip', range($start, $end));
}

/**
 * Get the Start and End Address of the IP range from CIDR
 * For Ex. [10.0.0.0/24] => 10.0.0.0 - 10.0.0.255
 *
 * @param unknown $cidr
 * @return Array:Start and End IP Address
 */
function cidr_to_range($cidr) {

	$range = array();
	$cidr = explode('/', $cidr);
	$range[0] = long2ip((ip2long($cidr[0])) & ((-1 << (32 - (int)$cidr[1]))));
	$range[1] = long2ip((ip2long($cidr[0])) + pow(2, (32 - (int)$cidr[1])) - 1);
	return $range;
}

/**
 * Check if 2 CIDRs are over-lapping
 * For Ex. : $cidr1 = 100.64.0.0/10 and $cidr2 = 100.0.0.0/9 => true
 *         : $cidr1 = 100.64.0.0/10 and $cidr2 = 100.128.0.0/9 => false
 *
 * @param unknown $cidr1
 * @param unknown $cidr2
 * @return boolean
 */
function is_overlapping_cidr($cidr1, $cidr2) {

	$range1 = cidr_to_range($cidr1);
	$startIpNum = ip2long($range1[0]);
	$endIpNum = ip2long($range1[1]);

	$range2 = cidr_to_subnet_and_subnetmask_address($cidr2);
	$netnum  = ip2long($range2['subnet_ip']);
	$masknum = ip2long($range2['subnet_mask']);
	for ($i = $startIpNum; $i < $endIpNum; $i++) {
		if (($i & $masknum) === ($netnum & $masknum)) {
			return TRUE;
		}
	}
	return FALSE;
}

/**
 * Match IP address in a CIDR
 *
 * @param unknown $ip
 * @param unknown $cidr
 * @return boolean
 */
function cidr_match ($ip, $cidr) {

	list ($subnet, $mask) = explode ('/', $cidr);
	if ((ip2long($ip) & ~((1 << (32 - $mask)) - 1) ) == ip2long($subnet)) {
		return true;
	}
	return false;
}

/**
 * Convert Netmask to CIDR prefix
 * For ex. 255.255.255.0 -> 24
 *
 * @param unknown $netmask
 * @return number
 */
function netmask_to_cidr ($netmask) {
	$cidr = 0;
	foreach (explode('.', $netmask) as $number) {
		for (;$number > 0; $number = ($number << 1) % 256) {
			$cidr++;
		}
	}
	return $cidr;
}

/**
 * Check if the String is in CIDR format
 * For ex. 101.0.0.100/24
 *
 * @param unknown $string
 */
function is_cidr ($string) {

	$regex = '/^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])(\/([0-9]|[1-2][0-9]|3[0-2]))$/';
	return (preg_match($regex, $string) > 0);
}

/**
 * Convert CIDR to Subnet and Mask address
 * For ex. if CIDR is 10.0.0.0/24 => 10.0.0.0 255.255.255.0
 *
 * @param unknown $cidr
 * @return multitype:string multitype:
 */
function cidr_to_subnet_and_subnetmask_address ($cidr) {

	list ($subnet_ip, $prefix) = explode ('/', $cidr);
	// Take all 1s upto the prefix and rest of the 32-bits as 0s
	$binary_mask = "";
	for ($i = 0; $i < $prefix; $i++) {
		$binary_mask = $binary_mask . "1";
	}
	for ($i = $prefix; $i < 32; $i++) {
		$binary_mask = $binary_mask . "0";
	}

	// Out of 32-bits,convert each 8-bits in integer form
	// Add a "." after first 3 integers
	$binary_octect = "";
	$subnet_mask = "";
	for ($i = 0; $i < 32; $i = $i + 8) {
		$binary_octect = substr($binary_mask, $i, 8);
		$subnet_mask = $subnet_mask . intval($binary_octect, 2);
		if ($i != 24) {
			$subnet_mask = $subnet_mask . ".";
		}
		$binary_octect = "";
	}
	$response = array('subnet_ip' => $subnet_ip, 'subnet_mask' => $subnet_mask);
	return $response;
}

/** 
 * check if address is in network
 * 
 * @param unknown $addr
 * @param unknown $net
 * @param string $mask
 * @return boolean
 */
function address_is_in_network($addr, $net, $mask = '255.255.255.255')
{
	// case where IP is with /32 CIDR
	if (strpos($addr, '/')) {
		$tmp = explode('/', $addr);
		$addr = $tmp[0];
	}

	$addrnum = ip2long($addr);
	$netnum  = ip2long($net);
	$masknum = ip2long($mask);

	return (($addrnum & $masknum) === ($netnum & $masknum));
}

?>