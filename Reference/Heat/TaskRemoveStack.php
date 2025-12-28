<?php

require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

function list_args()
{
	create_var_def('vimid', 'Device');
	create_var_def('stackid', 'String');
}


if (!empty($context['vimid']) && !empty($context['stackid']) ){
	$devicelongid = substr($context['vimid'], 3);
	_obmf_delete('{"stacklist":"'.$context['stackid'].'"}',$devicelongid);
	echo prepare_json_response(ENDED,"Stack is deleted",$context, true);
}else{
	echo prepare_json_response(FAILED, 'Missing parameters', '');
}

?>