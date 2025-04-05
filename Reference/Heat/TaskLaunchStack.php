<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args()
{
  create_var_def('vimid', 'Device');
  create_var_def('stackid', 'String');
  create_var_def('stackname', 'String');
  create_var_def('flavor', 'String');
  create_var_def('image', 'String');
  create_var_def('management_network_name', 'String');
  create_var_def('public_net', 'String');
  create_var_def('stackURL', 'String');
}

if (!empty($context['vimid'])){
	$devicelongid = substr($context['vimid'], 3);
	$create=_obmf_create('{"stack":{"'.$context['stackname'].'":{"object_id":"'.$context['stackname'].'","_order":"1464700354799","parameters":[{"paramname":"flavor","paramvalue":"'.$context['flavor'].'"},{"paramname":"image","paramvalue":"'.$context['image'].'"},{"paramname":"management_network_name","paramvalue":"'.$context['management_network_name'].'"},{"paramname":"public_net","paramvalue":"'.$context['public_net'].'"}],"template_url":"'.$context['stackURL'].'"}}}',$devicelongid);
	$message="";
	if(_openstack_stack_getApiStatusFromObmfAnswer($create)=="ERROR"){
		echo prepare_json_response(FAILED, _openstack_stack_getApiMessageFromObmfAnswer($create), '');
	}else{
		//stack is launched
		$message.="Stack is launched \n";
		update_asynchronous_task_details($context, $message);
		//get ID
		sleep(4);
		$ID=_openstack_stack_getStackIdFromName($devicelongid,$context['stackname']);
		$context['stackid']=$ID;
		//check result
		$stat="CREATE_IN_PROGRESS";
		$message.="Deployment status: ".$stat;
    		while ($stat=="CREATE_IN_PROGRESS") {
			//wait 3 seconds
			sleep(3);
			//get new status
			$stat = _openstack_stack_getStackStatus($devicelongid,$context['stackid']);
			$message.=".";
			update_asynchronous_task_details($context, $message);
		}
		$message.="\n";
		if ($stat=="CREATE_COMPLETE"){
			echo prepare_json_response(ENDED,"Stack is deployed with id ".$context['stackid'],$context, true);
		}else{
			echo prepare_json_response(FAILED, _openstack_stack_getStackStatusReason($devicelongid,$context['stackid']), '');
		}
	}
}else{
    echo prepare_json_response(FAILED, 'Missing parameters', '');
}
?>