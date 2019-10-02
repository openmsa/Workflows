<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args()
{
	create_var_def('msa_templates_path', 'String');
}

check_mandatory_param('msa_templates_path');

$msa_templates_path = $context['msa_templates_path'];
$output_array = array();
exec("find " . TEMPLATES_HOME_DIR . $msa_templates_path . ' -type f', $output_array);
// Find give the full path + Hidden files

logToFile(debug_dump($output_array, "MSA Templates list from the given path :\n"));

$template_uris = array();
$template_index = 0;
$dir = "";
foreach ($output_array as $line) {
	
	if(strstr($line, "/.meta")) {
		continue;
	}
	
	$context['msa_templates'][$template_index++]['uri'] = substr($line, strlen(TEMPLATES_HOME_DIR));
}

logToFile(debug_dump($context['msa_templates'], "Context Template URIs :\n"));

$response = prepare_json_response(ENDED, "Templates fetched successfully from the given path", $context, true);
echo $response;

?>