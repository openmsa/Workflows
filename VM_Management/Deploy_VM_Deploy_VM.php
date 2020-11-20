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
  create_var_def('vm_num', 'String');
  create_var_def('server', 'Device');
  create_var_def('name', 'String');
  create_var_def('template', 'String');
  create_var_def('cpu', 'String');
  create_var_def('memory', 'String');
  create_var_def('host', 'String');
  create_var_def('datastore', 'String');
  create_var_def('folder', 'String');
  create_var_def('networks.0.network', 'String');
  create_var_def('networks.0.ip', 'String');
  //create_var_def('vms.0.device_id', 'String');
}

$PROCESSINSTANCEID = $context['PROCESSINSTANCEID'];
$EXECNUMBER = $context['EXECNUMBER'];
$TASKID = $context['TASKID'];
$process_params = array('PROCESSINSTANCEID' => $PROCESSINSTANCEID,'EXECNUMBER' => $EXECNUMBER,'TASKID' => $TASKID);

$input_name = $context['name'];
$template = $context['template'];
$cpu = $context['cpu'];
$memory = $context['memory'];
$host = $context['host'];
$datastore = $context['datastore'];
$folder = $context['folder'];
$input_networks = $context['networks'];
$server=$context['server'];
$server=getIdFromUbiId($server);
$vms=$context['vms'];
$num=$context['vm_num'];
//For list of devices, boot the VMs in batches
//Here batch size is 2
$batch_size=2;
$batch_iter=$num/$batch_size;
$batch_iter=floor($batch_iter);
$last_batch_size=$num%$batch_size;
$wo_comment="TotalVMS: $num, Total batches: $batch_iter, Last batch: $last_batch_size";
logToFile("$wo_comment");
update_asynchronous_task_details($process_params, $wo_comment);
//Identify the batch candidates by base template name and store them in context variables in the backend
/*$response = _obmf_get_object_variables($server, "VM_Templates", $template );
$response = json_decode($response, true);
if($response['wo_status'] !== ENDED)
{
    $device_data = prepare_json_response($response['wo_status'], "Failed to get template data", $response, true);
    echo $device_data;
    exit;
}
$template_name = $response['wo_newparams']['VM_Templates'][$template]['name'];
logToFile("Basename of the template: $template_name");
//still more to code, but for POC we hardocde
*/
//Currently hardcoding the template batch candidates
$cands=array($template,'c3ab957b-f412-485b-9764-d706d4e75e62');
$ips=array('10.31.1.161','10.31.1.198');

$batch_candidates=array();
$batch_item=array();
$batch_item['candidate']=$cands[0];
array_push($batch_candidates,$batch_item);

$batch_item=array();
$batch_item['candidate']=$cands[1];
array_push($batch_candidates,$batch_item);

$context['batch_candidates']=$batch_candidates;

//end of harcoding
$x=0;
$y=0;
for($i=0;$i<$batch_iter;$i++){
  for($j=0;$j<$batch_size;$j++){
    $me_name = "$input_name"."_"."$x";
    $tmpl_item=$batch_candidates[$j]['candidate'];
    $vm_params=array();
    $vm_params['name']=$me_name;
    $vm_params['template_id']=$tmpl_item;
    $vm_params['cpu_count']=$cpu;
    $vm_params['memory']=$memory;
    $vm_params['datastore']=$datastore;
    $vm_params['host']=$host;
    $vm_params['folder']=$folder;
    $networks=array();
    foreach($input_networks as $nw_item){
    	$nw=array();
    	$nw['network']=$nw_item['network'];
    	array_push($networks,$nw);
    }
    $vm_params['networks']=$networks;
    $cmd_obj=array("Template_VMs" => array("" => $vm_params));

    $response = execute_command_and_verify_response($server, CMD_CREATE, $cmd_obj, "VM CREATE");
    $x+=1;
  }
  $wo_comment="Batch $i of VMs Triggerred, waiting for the VMs to be UP";
  update_asynchronous_task_details($process_params, $wo_comment);
  //sleep(400);
  //wait until all VMs in this batch come up 
  $ms='vm';
  $z=$y;
  for($j=0;$j<$batch_size;$j++){
    $vm_name = "$input_name"."_"."$z";
    while(true){
      $res=import_objects($server,array($ms));
      $res=json_decode($res,true);
      if ($res['wo_status'] !== ENDED) {
        logToFile("Waiting for the batch $i of VMs to be up");
        sleep(30);
      }else{
        $vm_list=$res['wo_newparams']['vm'];
        foreach($vm_list as $key => $val){
          if($val['name'] === $vm_name){
            logToFile("ohoo my vm id is:  $key");
            $vms[$z]['vm_id']=$key;
            break;
          }
        }
        break;
      }
    }
    $z+=1;
  }
  $wo_comment="Batch $i of VMs are now UP";
  update_asynchronous_task_details($process_params, $wo_comment);
  //Check for reachability and then provision the MEs before proceeding to next batch
  for($j=0;$j<$batch_size;$j++){
    $ip=$ips[$j];
    $vmid=$vms[$j]['vm_id'];
    $wo_comment="Waiting to access vm $y: $vmid to be accessible";
    update_asynchronous_task_details($process_params, $wo_comment);
    //ping once the ip and if reachable go to provisioning if not reachable, reboot the VM and then ping 5 times after every 30 seconds
for($l=0;$l<2;$l++){
    $response = _device_do_ping($ip);
    $response = json_decode($response, true);
    $ping_status = $response['wo_newparams']['status'];
    logToFile("FIRST PING STATUS : $ping_status");
    if ($ping_status === FAILED) {
      //do reboot and try 10 times
	  //rebooting using the vm MS
      $wo_comment="Rebooting vm $y: $vmid $l times";
      update_asynchronous_task_details($process_params, $wo_comment);
	  $ms_params=array();
	  $ms_params['object_id']=$vmid;
	  $ms_params['power_state']="POWERED_OFF";
	  $ms_obj=array("vm" => array($vmid => $ms_params));
	  $response = execute_command_and_verify_response($server, CMD_UPDATE, $ms_obj, "VM OFF");
	  sleep(20);
	  $ms_params['power_state']="POWERED_ON";
	  $ms_obj=array("vm" => array($vmid => $ms_params));
	  $response = execute_command_and_verify_response($server, CMD_UPDATE, $ms_obj, "VM ON");
	  //wait to ping 5 times
      for($n=0;$n<10;$n++){
        $response = _device_do_ping($ip);
        $response = json_decode($response, true);
        $ping_status = $response['wo_newparams']['status'];
        logToFile("PING STATUS $n: $ping_status");
        $wo_comment="vm $y: $vmid : round $l PING STATUS $n: $ping_status";
        update_asynchronous_task_details($process_params, $wo_comment);
        if ($ping_status === FAILED) {
          sleep(20);
        }else{
          logToFile("Ping was successful, going to provision now");
          $wo_comment="vm $y: $vmid : is now reachable";
          update_asynchronous_task_details($process_params, $wo_comment);
          break;
        }
      }
	//Now either VM is reachable or not reachable even after rebooting waiting 
    }else{
      $wo_comment="vm $y: $vmid : is now reachable in round $l";
      update_asynchronous_task_details($process_params, $wo_comment);
      break;
    }
}
    //Assuming VM is now reachable, proceed provisioning with temporary IP
    $me_id=$vms[$y]['device_id'];
    $me_id=getIdFromUbiId($me_id);
    $msa_rest_api = "device/provisioning/{$me_id}?ip=$ip";
    $curl_cmd = create_msa_operation_request(OP_POST, $msa_rest_api);
    $response = perform_curl_operation($curl_cmd, "DO INITIAL PROVISIONING BY DEVICE ID and IP");
    $response = json_decode($response, true);
    if ($response['wo_status'] !== ENDED) {
	    $response = json_encode($response);
	    $vms[$y]['status']=$response;
    }
	$wo_comment="vm $y: $vmid : Provisioning Started";
    update_asynchronous_task_details($process_params, $wo_comment);
    $response = wait_for_provisioning_completion($me_id, $process_params);
    $response = json_decode($response, true);
    if ($response['wo_status'] !== ENDED) {
	    $response = json_encode($response);
	    $vms[$y]['status']=$response;
      	$wo_comment="vm $y: $vmid : Provisioning Failed - $response";
        update_asynchronous_task_details($process_params, $wo_comment);
    }else{
      $wo_comment="vm $y: $vmid : Provisioning Completed";
      update_asynchronous_task_details($process_params, $wo_comment);
    }
    logToFile("Provisioning of the VM: $y is completed" );
    $y+=1;
  }
}

if($last_batch_size >0){
  logToFile("Processing last batch");
  $wo_comment="Processing last batch";
  update_asynchronous_task_details($process_params, $wo_comment);
  //process the last batch
  for($j=0;$j<$last_batch_size;$j++){
    $me_name = "$input_name"."_"."$x";
    $tmpl_item=$batch_candidates[$j]['candidate'];
    $vm_params=array();
    $vm_params['name']=$me_name;
    $vm_params['template_id']=$tmpl_item;
    $vm_params['cpu_count']=$cpu;
    $vm_params['memory']=$memory;
    $vm_params['datastore']=$datastore;
    $vm_params['host']=$host;
    $vm_params['folder']=$folder;
    $networks=array();
    foreach($input_networks as $nw_item){
    	$nw=array();
    	$nw['network']=$nw_item['network'];
    	array_push($networks,$nw);
    }
    $vm_params['networks']=$networks;
    $cmd_obj=array("Template_VMs" => array("" => $vm_params));

    $response = execute_command_and_verify_response($server, CMD_CREATE, $cmd_obj, "VM CREATE");
    $x+=1;
  }
  $wo_comment="Last batch of VMs Triggerred, waiting for the VMs to be UP";
  update_asynchronous_task_details($process_params, $wo_comment);
 //wait until all VMs in this batch come up 
  $ms='vm';
  $z=$y;
  for($j=0;$j<$last_batch_size;$j++){
    $vm_name = "$input_name"."_"."$z";
    while(true){
      $res=import_objects($server,array($ms));
      $res=json_decode($res,true);
      if ($res['wo_status'] !== ENDED) {
        logToFile("Waiting for the batch of VMs to be up");
        sleep(30);
      }else{
        $vm_list=$res['wo_newparams']['vm'];
        foreach($vm_list as $key => $val){
          if($val['name'] === $vm_name){
            logToFile("ohoo my vm id is:  $key");
            $vms[$z]['vm_id']=$key;
            break;
          }
        }
        break;
      }
    }
    $z+=1;
  }
  $wo_comment="Last Batch of VMs are now UP";
  update_asynchronous_task_details($process_params, $wo_comment);
  //Check for reachability and then provision the MEs before proceeding to next batch
  for($j=0;$j<$last_batch_size;$j++){
    $ip=$ips[$j];
    $vmid=$vms[$j]['vm_id'];
    $wo_comment="Waiting to access vm $y: $vmid to be accessible";
    update_asynchronous_task_details($process_params, $wo_comment);
    //ping once the ip and if reachable go to provisioning if not reachable, reboot the VM and then ping 5 times after every 30 seconds
for($l=0;$l<2;$l++){ 
    $response = _device_do_ping($ip);
    $response = json_decode($response, true);
    $ping_status = $response['wo_newparams']['status'];
    logToFile("FIRST PING STATUS : $ping_status");
    if ($ping_status === FAILED) {
      //do reboot and try 10 times
	  //rebooting using the vm MS
      $wo_comment="Rebooting vm $y: $vmid $l times";
      update_asynchronous_task_details($process_params, $wo_comment);
	  $ms_params=array();
	  $ms_params['object_id']=$vmid;
	  $ms_params['power_state']="POWERED_OFF";
	  $ms_obj=array("vm" => array($vmid => $ms_params));
	  $response = execute_command_and_verify_response($server, CMD_UPDATE, $ms_obj, "VM OFF");
	  sleep(10);
	  $ms_params['power_state']="POWERED_ON";
	  $ms_obj=array("vm" => array($vmid => $ms_params));
	  $response = execute_command_and_verify_response($server, CMD_UPDATE, $ms_obj, "VM ON");
	  //wait to ping 5 times
      for($n=0;$n<10;$n++){
        $response = _device_do_ping($ip);
        $response = json_decode($response, true);
        $ping_status = $response['wo_newparams']['status'];
        logToFile("PING STATUS $n: $ping_status");
        $wo_comment="vm $y: $vmid : round $l PING STATUS $n: $ping_status";
        update_asynchronous_task_details($process_params, $wo_comment);
        if ($ping_status === FAILED) {
          sleep(30);
        }else {
          logToFile("Ping was successful, going to provision now");
           $wo_comment="vm $y: $vmid : is now reachable";
          update_asynchronous_task_details($process_params, $wo_comment);
          break;
        }
      }
	//Now either VM is reachable or not reachable even after rebooting waiting
    }else {
       $wo_comment="vm $y: $vmid : is now reachable in round $l";
       update_asynchronous_task_details($process_params, $wo_comment);
      break;
    }
}
    //Assuming VM is now reachable, proceed provisioning with temporary IP
    $me_id=$vms[$y]['device_id'];
    $me_id=getIdFromUbiId($me_id);
    $msa_rest_api = "device/provisioning/{$me_id}?ip=$ip";
    $curl_cmd = create_msa_operation_request(OP_POST, $msa_rest_api);
    $response = perform_curl_operation($curl_cmd, "DO INITIAL PROVISIONING BY DEVICE ID and IP");
    $response = json_decode($response, true);
    if ($response['wo_status'] !== ENDED) {
	    $response = json_encode($response);
	    $vms[$y]['status']=$response;
    }
	$wo_comment="vm $y: $vmid : Provisioning Started";
    update_asynchronous_task_details($process_params, $wo_comment);
    $response = wait_for_provisioning_completion($me_id, $process_params);
    $response = json_decode($response, true);
    if ($response['wo_status'] !== ENDED) {
	    $response = json_encode($response);
	    $vms[$y]['status']=$response;
        $wo_comment="vm $y: $vmid : Provisioning Failed - $response";
        update_asynchronous_task_details($process_params, $wo_comment);
    }else{
      $wo_comment="vm $y: $vmid : Provisioning Completed";
      update_asynchronous_task_details($process_params, $wo_comment);
    }
    logToFile("Provisioning of the VM: $y is completed" );
    $y+=1;
  }
}

$context['vms']=$vms;

task_success('VMs Deployment Successful');
?>