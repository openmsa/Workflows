<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args()
{
	create_var_def('msa_templates_path', 'String');
}

check_mandatory_param('msa_templates_path');

$msa_templates_path = $context['msa_templates_path'];
$output_array = array();
exec("ls -lR " . TEMPLATES_HOME_DIR . $msa_templates_path, $output_array);

logToFile(debug_dump($output_array, "MSA Templates list from the given path :\n"));

$template_uris = array();
$template_index = 0;
$dir = "";
foreach ($output_array as $line) {
	if (strpos($line, TEMPLATES_HOME_DIR) === 0) {
		$dir = substr($line, strlen(TEMPLATES_HOME_DIR), strlen($line) - strlen(TEMPLATES_HOME_DIR) - 1);
		logToFile("Dir : $dir");
	}
	else if (strpos($line, "-") === 0) {
		$line_elements = explode(" ", $line);
		$context['msa_templates'][$template_index++]['uri'] = $dir . "/" . $line_elements[count($line_elements) - 1];
	}
	else if ($line === "") {
		$dir = "";
	}
}

logToFile(debug_dump($context['msa_templates'], "Context Template URIs :\n"));

$response = prepare_json_response(ENDED, "Templates fetched successfully from the given path", $context, true);
echo $response;

?>