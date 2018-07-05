<?php

function _openstack_getPrivateIpFromInstanceName($devicelongid,$instanceName){
	logToFile("Get Private IP attached to ".$instanceName);
	$res=_obmf_import('{"servers":"0"}',$devicelongid);
	$st = substr($res,strpos($res, "&quot;name&quot;:&quot;".$instanceName)+23);
	$st = substr($res,strpos($res, "&quot;addr&quot;")+23);
	$st = substr($st,0,strpos($st, "&quot;"));
	logToFile("Private IP: ".$st);
	return $st;
}

function _openstack_getFloatingIpFromPrivateIp($devicelongid,$privateIp){
	logToFile("Get Floating IP attached to ".$privateIp);
	$import=_obmf_import('{"floatingips":"0"}',$devicelongid);
	//test status
	$status = substr($import,strpos($import, "<status>")+8);
	$status = substr($status,0,strpos($status, "</status>"));
	if($status!="OK"){
		echo prepare_json_response(ERROR,"Error while getting the floating IP","", true);
	}
	$st = substr($import,strpos($import, "fixed_ip_address&quot;:&quot;".$privateIp)+25);
	$st = substr($st,strpos($st, "floating_ip_addres")+32);
	$st = substr($st,0,strpos($st, "&quot;"));
	logToFile("Floating IP: ".$st);
	return $st;
}

function _openstack_stack_getApiStatusFromObmfAnswer($obmfAsnwer){
	logToFile("Answer from OBMF: ".$obmfAsnwer);
	$status=substr($obmfAsnwer,strpos($obmfAsnwer, "<status>")+8);
	$status=substr($status,0,strpos($status,"</status>"));
	logToFile("Status: ".$status);
	return $status;
}

function _openstack_stack_getApiMessageFromObmfAnswer($obmfAsnwer){
	logToFile("Answer from OBMF: ".$obmfAsnwer);
	$reason=substr($obmfAsnwer,strpos($obmfAsnwer, "<message>")+9);
	$reason=substr($reason,0,strpos($reason, "</message>"));
	logToFile("Message: ".$reason);
	return $reason;
}


/*
example:
{&quot;stacklist&quot;:{&quot;58fdcf39-0842-4e9c-ab33-e60c3d467a62&quot;:{&quot;stack_status_reason&quot;:&quot;Resource CREATE failed: ResourceInError: resources.fosinstance: Went to status ERROR due to \&quot;Message: Build of instance 0cd7ae74-c4d5-4f5e-afc4-45fa14658742 aborted: Flavor's disk is too small for requested image., Code: 500\&quot;&quot;,&quot;stack_status&quot;:&quot;CREATE_FAILED&quot;,&quot;stack_name&quot;:&quot;forti&quot;,&quot;object_id&quot;:&quot;58fdcf39-0842-4e9c-ab33-e60c3d467a62&quot;,&quot;creation_time&quot;:&quot;2016-06-15T09:20:42Z&quot;},&quot;9a6c7f11-8587-42bc-af2e-f14a2ace7b51&quot;:{&quot;stack_status_reason&quot;:&quot;Stack CREATE completed successfully&quot;,&quot;stack_status&quot;:&quot;CREATE_COMPLETE&quot;,&quot;stack_name&quot;:&quot;adtranDeployment&quot;,&quot;object_id&quot;:&quot;9a6c7f11-8587-42bc-af2e-f14a2ace7b51&quot;,&quot;creation_time&quot;:&quot;2016-06-15T08:48:25Z&quot;}}}
*/
function _openstack_stack_getStackIdFromName($devicelongid,$stackName){
	logToFile("Get Stack ID for stack: ".$stackName);
	$imp=_obmf_import('{"stacklist":"0"}',$devicelongid);
	$imp=substr($imp,strpos($imp, $stackName));
	$id = substr($imp,strpos($imp, "id&quo")+15);
	$id = substr($id,0,strpos($id, "&quot;"));
	logToFile("Stack ".$stackName."->".$id);
	return $id;
}	

function _openstack_stack_getStackStatus($devicelongid,$stackId){	
	logToFile("Get Stack Status for stack ID: ".$stackId,$devicelongid);
	$imp=_obmf_import('{"stacklist":"0"}',$devicelongid);
	$imp=substr($imp,strpos($imp, $stackId));
	$st = substr($imp,strpos($imp, "stack_status&quot")+25);
	$stat = substr($st,0,strpos($st, "&quot;"));
	logToFile("Stack ".$stackId."->".$stat);
	return $stat;
}	

function _openstack_stack_getStackStatusReason($devicelongid,$stackId){	
	logToFile("Get Stack Status Reason for stack ID: ".$stackId,$devicelongid);
	$imp=_obmf_import('{"stacklist":"0"}',$devicelongid);
	$imp=substr($imp,strpos($imp, $stackId));
	$st = substr($imp,strpos($imp, "ack_status_reason&quot")+30);
    $st = str_replace('\&quot;','"',$st);
    $stat = substr($st,0,strpos($st, "&quot;"));
	logToFile("Stack ".$stackId."->".$stat);
	return $stat;
}

?>