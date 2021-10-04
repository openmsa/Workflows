<?php
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';
require_once '/opt/fmc_repository/Process/ENEA/VNF_Management/common.php';

function list_args()
{
  create_var_def('vnf_name', 'vnf_name');     
}

check_mandatory_param('vnf_name');
$prop_f = array();

if(isset($context['cloud_init']))
{

    $contents = shell_exec("base64 -w 0 ".$context['cloud_init']); 
    $prop_f[] = array( 
                    "name"  => "cloudInit",
            "value" => $contents 
    );
}

//exit;
$HTTP_M = "POST";

$device_ip       = $context['device_ip'];
$port            = $context['port'];

//generate UUI for VNF id
$uuid            = uuid(openssl_random_pseudo_bytes(16));

//format required connection info


$nics = $context['nics'];
foreach($nics as $row)
{
    $name = explode("-",$row['id']);
    $bridge[] = array("name" => "bridge","value" =>$row["interfacename"]);

    $arr = array( 
           "name" => $name[1],
           "type" => $row['type'],
           "props" =>array(array("name" => "bridge",
                "value" =>$row["interfacename"]))
    );
    
    if($row['type'] == "Tap" && isset($row['nicmodel']) && $row['nicmodel'] != "")
    {
        $arr["model"] = $row['nicmodel'];
    }

    $connection_info_fin2[] = $arr;
}   

//========================================================================================
$device_ip = $context['device_ip'];
$port      = $context['port'];
$full_url  = "https://$device_ip$port/REST/v2/ServiceMethodExecution/modules/VnfManager/services/Configuration/methods/getVNFDescriptors";
$vnfd_list = curl_http_get($context['sessionToken'], $full_url,"", $HTTP_M);

if($vnfd_list['wo_status'] !== ENDED)
{               
    $vnfd_list = prepare_json_response($vnfd_list['wo_status'], "Failed to Import VNFD", $vnfd_list, true);   
    echo $vnfd_list;
    exit;
}

$vnfd_list = json_decode($vnfd_list['wo_newparams']['response_body'],TRUE);
$selected_vnfd = "";


foreach($vnfd_list as $row)
{
  
  //check if any vnfs matc the chosen descriptor.
  if($context['vnf_descriptor'] == $row["id"])
  {
    $selected_vnfd = $row;
    break;
  } 
}
//========================================================================================
$body = array(
  "vnfr"=>array(
      "id"            => $uuid,
      "vimEid"        => $context['device_data']['object_id'],
      "ecAutoRestart" => false,
      "ecManaged"     => false,
      "deviceName"    => $context['device_data']['name'],
      "connections"   => $connection_info_fin2 ,
      "props"=>$prop_f,
      "vnfdFlavour" => "Canonical",
      "vnfdVersion" => "1",
      "vnfd"     => $selected_vnfd,        
      "name"     => $context['vnf_name'],
      "_internal_objectType" => "VnfManager/VnfRecord"
    ));
$body = json_encode($body);

//TODO remove this once curl has been updated!!!
//create temporary file to put contents of bulk into.
$myfile = fopen("/opt/fmc_repository/Datafiles/datatemp_{$uuid}.txt", "w") or die("Unable to open file!");
fwrite($myfile, $body);
fclose($myfile);


$full_url  = "https://$device_ip$port/REST/v2/ServiceMethodExecution/modules/VnfManager/services/Configuration/methods/instantiateVNF";


$instnatiate_vnf= curl_http_get($context['sessionToken'], $full_url,"@/opt/fmc_repository/Datafiles/datatemp_{$uuid}.txt" , $HTTP_M);

//delete the temporary file
unlink("/opt/fmc_repository/Datafiles/datatemp_{$uuid}.txt");
$vnfr_id = json_decode($instnatiate_vnf['wo_newparams']['response_body'],true);

if($instnatiate_vnf['wo_status'] !== ENDED)
{               
    $instnatiate_vnf= prepare_json_response($instnatiate_vnf['wo_status'], "Failed to Instantiate VNF", $instnatiate_vnf, true);   
    echo $instnatiate_vnf;
    exit;
}

$context['instnatiate_vnf'] = $instnatiate_vnf;
$context['vnfr_id'] = $vnfr_id['_internal_objectId'] ;
task_exit(ENDED, "VNF instantiated");

?>