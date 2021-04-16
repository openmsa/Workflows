<?php


function modify_microservice_to_read_playbook ($playbook_path, $microservice_file) {
	
	//The string that contain chosen playbook path
	$rewrite_string = '<operation>cat '.$playbook_path.' ';
	
	//Modify microservice file
	$sed_command = 'sed -i \'s@<operation>cat [^ ]* @'.$rewrite_string.'@\' '.$microservice_file;
	$result = shell_exec($sed_command);
	
	return $result;
}

function extract_variables ($device_id, $microservice_name) {
	
	//Read playbook file content
	$response = json_decode(import_objects($device_id, array($microservice_name)), True);
	$object_ids_array = $response['wo_newparams'][$microservice_name];
	$object_params = current($object_ids_array);
	
	//Create array from string
	$playbook_array = explode('|', $object_params['text']);
	
	//$vars_array is an array that contains strings with extra-args variables
	$vars_array = array();
	
	/*$playbook_variables contains extracted variables like 
	array("var_name1" => array("var_name2")
	*/
	$playbook_variables = array();
	
	//Just bool flag for parser
	$is_section = False;
	
	//Extract lines with extra args
	foreach ($playbook_array as $line) {
	  if ($is_section and preg_match("/$section_end_pattern/", $line) === 1) {
	      $is_section = False;    
	    }
	  if ($is_section) {
	      $vars_array[] = trim($line);
	    }
	  if (preg_match('/(\s+?)vars_prompt.+/', $line, $matches) === 1) {
	      $is_section = True;
	      $intention = $matches[1];
	      $section_end_pattern = '^'.$intention.'\S';
	    }
	}
	
	//Extract variables from var lines
	$var_name = '';
	foreach ($vars_array as $line) {
	  if (strpos($line, '- name') === 0) {
	    $temp_array = explode(':', $line);
	    $var_name = trim($temp_array[1]);
	    $playbook_variables[$var_name] = array();
	  } else {
	    $temp_array = explode(':', $line);
	    $playbook_variables[$var_name][trim($temp_array[0])] = trim(trim($temp_array[1]));
	  }
	}
	
	return $playbook_variables;
}

function playbook_attributes ($microservice_object) {
	$attributes_array = array();
	$attributes_array['path'] = $microservice_object['object_id'];
	$attributes_array['md5sum'] = $microservice_object['md5sum'];

	return $attributes_array;
}


function define_microservice_vars($playbook_attributes, $microservice_variables_array, $variable_skeleton) {

	//Modify string to create default value for playbook path in microservice
	$microservice_variables_array['var_playbook_path'] = sprintf($microservice_variables_array['var_playbook_path'], $playbook_attributes['path']);

	//Create varaible strings for microservice. Playbook's 'prompt' appears as displayName,
	//playbook's 'default' appears as default value for microservices variable.
	$microservice_create_vars = '';
	foreach ($playbook_attributes['variables'] as $var => $var_attributes) {
	  $current_variable = sprintf($variable_skeleton, $var_attributes['prompt'], $var, $var_attributes['default']);
	  $microservice_variables_array[$var] = $current_variable;
	  
	  //Add the new variable to command what used for CREATE method
	  $microservice_create_vars .= $var.'={$params.'.$var.'} ';
	}
	
	//Create a string that is used as command for CREATE method
	$microservice_create_line = '<operation>sudo ansible-playbook {$params.playbook_path} --extra-vars "'.$microservice_create_vars.'"</operation>';
	
	//Combine variables string to text block to put to file
	$variables_line = '  <variables frozen="0">\n';
	foreach ($microservice_variables_array as $var) {
	  $variables_line .= $var.'\n';
	}
	$variables_line .= '  </variables>\n';
	
	//Return both command and varables strings
	return (array('variables_line' => $variables_line,
				  'microservice_create_line' => $microservice_create_line
				  )
			);
}


function create_microservice_file($playbook_microservice_name, $playbook_attributes, $microservice_skeleton) {	

	//Gather microservice skeleton path and name
	$result = preg_match('|^(\S+?)([^/]+?\.xml)|', $microservice_skeleton, $matches);
	$microservice_skeleton_path = $matches[1];
	$microservice_skeleton_name = $matches[2];
	
	//Sanitize file name
	$playbook_microservice_file_name = $playbook_microservice_name;
	$playbook_microservice_file_name = preg_replace('/[| @()]/', '_', $playbook_microservice_file_name).'.xml';
	
	//Copy MS skeleton to new file
	$cp_command = '/bin/cp '.$microservice_skeleton.' '.$microservice_skeleton_path.$playbook_microservice_file_name;
	$cp_command .= '; /bin/cp '.$microservice_skeleton_path.'.meta_'.$microservice_skeleton_name.' '.$microservice_skeleton_path.'.meta_'.$playbook_microservice_file_name;
	$result = shell_exec($cp_command);
	
	//Write MS name to MS file

	$sed_command = '/bin/sed -i \'s@ansible_playbook_skeleton@'.$playbook_microservice_name.'@\' '.$microservice_skeleton_path.$playbook_microservice_file_name;
	$result = shell_exec($sed_command);
	
	//Write variables to MS file
	$sed_command = '/bin/sed -i \'s@<variables frozen="0"></variables>@'.$playbook_attributes['variables_line'].'@\' '.$microservice_skeleton_path.$playbook_microservice_file_name;
	$result = shell_exec($sed_command);
	
	//Write command to execute on CREATE step to MS file
	$sed_command = '/bin/sed -i \'s@<operation></operation>@'.$playbook_attributes['microservice_create_line'].'@\' '.$microservice_skeleton_path.$playbook_microservice_file_name;
	$result = shell_exec($sed_command);

	//Return new microservice path
	return $microservice_skeleton_path.$playbook_microservice_file_name;
}



function attach_file_to_deployment_settings($deployment_settings_id, $microservice_files_array) {
	$uris_array = array();
	foreach ($microservice_files_array as $number => $file) {
	  $uris_array[] = array("uri" => '/'.$file);
	}
	
	$response = json_decode(_profile_configuration_attach_files($deployment_settings_id, $uris_array), true);
	if ($response['wo_status'] !== ENDED) {
	  echo $response;
	  exit;
	}

	return True;
}


function re_create_microservice($device_id, $playbook_microservice_file_path, $playbook_file_path, $microservice_variables_array, $variable_skeleton, $microservice_skeleton, $microservice_file, $microservice_name) {
	
	//Sync out microservices
	$response = json_decode(synchronize_objects_and_verify_response($device_id), true);
	if ($response['wo_status'] !== ENDED) {
	  echo $response;
	  exit;
	}
	//Retrive playbook file list
	$response = json_decode(import_objects($device_id, array('Retrieve_playbook_files_list')), True);
	$object_ids_array = $response['wo_newparams']['Retrieve_playbook_files_list'];

	//Remove current MS
	$rm_command = '/bin/rm -f '.$playbook_microservice_file_path;
	$result = shell_exec($rm_command);
	
	//Find out modifyed microservice
	foreach ($object_ids_array as $object_id => $object_details) {
	  $current_playbook_file_path = $object_details['object_id'];
	  logToFile(debug_dump(md5($current_playbook_file_path), "DEBUG: CURRENT MD5"));
	  logToFile(debug_dump(md5($playbook_file_path), "DEBUG: MODIFYED MD5"));
	  if (md5($playbook_file_path) === md5($current_playbook_file_path)) {
	  	//Export attributes and variables
	  	$playbook_attributes = playbook_attributes($object_details);
	  	$result = modify_microservice_to_read_playbook($playbook_file_path, $microservice_file);
	  	//Sync out Ansible host to read playbook file list
	  	$response = json_decode(synchronize_objects_and_verify_response($device_id), true);
	  	if ($response['wo_status'] !== ENDED) {
	  	  echo $response;
	  	  exit;
	  	}

	  	$playbook_attributes['variables'] = extract_variables ($device_id, $microservice_name);
	  }
	}
	logToFile(debug_dump($playbook_attributes, "DEBUG: playbook attrinbutes"));
	//Prepare command and variables strings
	$result = define_microservice_vars($playbook_attributes, $microservice_variables_array, $variable_skeleton);
	$playbook_attributes['variables_line'] = $result['variables_line'];
	$playbook_attributes['microservice_create_line'] = $result['microservice_create_line'];
  	
  	$result = preg_match('|^(\S+?)([^/]+?\.yml)|', $playbook_attributes['path'], $matches);
	$playbook_microservice_name = $microservice_name_prefix.' (based on '.str_replace('.yml', '', $matches[2]).')';

	//Create MS files
	logToFile(debug_dump($playbook_attributes, "DEBUG: playbook attrinbutes"));
	$$playbook_attributes['microservice_path'] = create_microservice_file($playbook_microservice_name, $playbook_attributes, $microservice_skeleton);

	return $playbook_attributes;
}


function create_microservice($device_id, $playbook_file_path, $microservice_variables_array, $variable_skeleton) {
	
	//Sync out microservices
	$response = json_decode(synchronize_objects_and_verify_response($device_id), true);
	if ($response['wo_status'] !== ENDED) {
	  echo $response;
	  exit;
	}
	//Retrive playbook file list
	$response = json_decode(import_objects($device_id, array('Retrieve_playbook_files_list')), True);
	$object_ids_array = $response['wo_newparams']['Retrieve_playbook_files_list'];
	
	//Find out modifyed microservice
	foreach ($object_ids_array as $object_id => $object_details) {
	  $current_playbook_file_path = $object_details['object_id'];
	  if (md5($playbook_file_path) === md5($current_playbook_file_path)) {
	  	//Export attributes and variables
	  	$playbook_attributes = playbook_attributes($object_details);
	  	$result = modify_microservice_to_read_playbook($playbook_file_path, $microservice_file);
	  	//Sync out Ansible host to read playbook file list
	  	$response = json_decode(synchronize_objects_and_verify_response($device_id), true);
	  	if ($response['wo_status'] !== ENDED) {
	  	  echo $response;
	  	  exit;
	  	}

	  	$playbook_attributes['variables'] = extract_variables ($device_id, $microservice_name);
	  }
	}
	//Prepare command and variables strings
	$result = define_microservice_vars($playbook_attributes, $microservice_variables_array, $variable_skeleton);
	$playbook_attributes['variables_line'] = $result['variables_line'];
	$playbook_attributes['microservice_create_line'] = $result['microservice_create_line'];
  	
  	$result = preg_match('|^(\S+?)([^/]+?\.yml)|', $playbook_attributes['path'], $matches);
	$playbook_microservice_name = $microservice_name_prefix.' (based on '.str_replace('.yml', '', $matches[2]).')';

	//Create MS files
	$$playbook_attributes['microservice_path'] = create_microservice_file($playbook_microservice_name, $playbook_attributes, $microservice_skeleton);

	return $playbook_attributes;
}


function remove_microservice($playbook_file_path) {

 //Remove current MS
  $rm_command = '/bin/rm -f '.$playbook_file_path;
  $result = shell_exec($rm_command);
  return $playbook_details;
}


?>
