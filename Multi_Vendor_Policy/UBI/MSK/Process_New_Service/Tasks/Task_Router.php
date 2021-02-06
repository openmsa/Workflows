<?php
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args()
{
}

//===========================================================
function getIpListFromSubnet($subnet_address){
	
	//the $subnet_address has to be in format like "a.d.c.d/30"
	list($ip, $mask) = explode('/', $subnet_address);
	//binary network mask in string
	$maskBinStr =str_repeat("1", $mask ) . str_repeat("0", 32-$mask );
	//invert the mask
	$inverseMaskBinStr = str_repeat("0", $mask ) . str_repeat("1",  32-$mask );
	$ipLong = ip2long( $ip );
	$ipMaskLong = bindec( $maskBinStr );
	$inverseIpMaskLong = bindec( $inverseMaskBinStr );
	$netWork = $ipLong & $ipMaskLong;
	//networkID/ networkIP, usually the first one in the subnet
	$start = $netWork;
	//ignore the broadcast IP, usually the last one in the subnet
	$end = ($netWork | $inverseIpMaskLong) -1 ;
	$range = array('firstIP' => $start, 'lastIP' => $end );
	$ip_list = array();
	for ($ip = $range['firstIP']; $ip <= $range['lastIP']; $ip++) {
		array_push($ip_list,long2ip($ip));
	}
	return $ip_list;
}
//===========================================================

function createNetmaskAddr ($bitcount) {

    $netmask = str_split (str_pad (str_pad ('', $bitcount, '1'), 32, '0'), 8);

    foreach ($netmask as &$element)
    {
      $element = bindec ($element);
    }

    return join ('.', $netmask);
}

//===========================================================
$device_id = substr($context['rtr_device'], 3);

$bitcunt       = $context['service_subnet_masklen'];
$cidr	       = $context['service_subnet_ip']."/".$context['service_subnet_masklen'];
$ipadrres_list = getIpListFromSubnet($cidr);
$subnet_mask   = createNetmaskAddr($bitcunt);

$micro_service_vars_array = array();
$micro_service_vars_array['object_id'] = $context['rtr_sw_int'];
$micro_service_vars_array['ipaddress'] = $ipadrres_list[1];
$micro_service_vars_array['mask'] = $subnet_mask;
$micro_service_vars_array['VLAN'] = $context['VLAN'];


//logToFile(debug_dump($ipadrres_list,"*************************\n"));
$managed_entity = array('RoutingSubinterface' => array(""=> $micro_service_vars_array));


$response = execute_command_and_verify_response($device_id, CMD_CREATE, $managed_entity , "CREATE RoutingSubinterface");
$response = json_decode($response, true);

logToFile(debug_dump($response,"*************************\n"));

if($response['wo_status'] !== ENDED)
{				
	$response = prepare_json_response($response['wo_status'], "Failed to update router", $context, true);	
	echo $response;
	exit;
}

$response = prepare_json_response($response['wo_status'], "Successfully updated router", $context, true);		
echo $response;
?>

