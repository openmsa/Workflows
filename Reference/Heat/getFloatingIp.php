<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args()
{
  create_var_def('vimid', 'Device');
  create_var_def('privateIpVnf', 'String');
}
$devicelongid = substr($context['vimid'], 3);
$fip=_openstack_getFloatingIpFromPrivateIp($devicelongid,$context['privateIpVnf']);
$context['device_ip_addressVNF']=$fip;

echo prepare_json_response(ENDED,"Floating IP VNF: ".$fip,$context, true);

?>