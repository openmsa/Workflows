<?php


/*
The function is to compare arrays by 'order' key
*/
function compare_order($value_a, $value_b) {
  if ($value_a['order'] === $value_b['order']) {
    return 0;
  } elseif ($value_a['order'] < $value_b['order']) {
    return -1;
  } else {
    return 1;
  }
}


/*
The function is to obtian software stack version from a software component version.
The software component and pattern are defined in 'version' file in each model directory
Due PHP reqstrictions, pattern regexp in the file should have '#' insted '\'
*/

function get_version($model_dir_file_path, $current_sw_stack) {
  $version_description_path = $model_dir_file_path."version";
  logToFile(debug_dump($version_description_path, "DEBUG: VERSION DESCRIPTION PATH"));
  $version_description = json_decode(file_get_contents($version_description_path), True);
  logToFile(debug_dump($version_description, "DEBUG: VERSION DESCRIPTION"));
  $pattern = "/".str_replace('#', '\\', $version_description['pattern'])."/";
  logToFile(debug_dump($pattern, "DEBUG: VERSION pattern"));
  logToFile(debug_dump($current_sw_stack, "DEBUG: VERSION STACK"));
  preg_match($pattern, $current_sw_stack[$version_description['field']], $matches);
  logToFile(debug_dump($matches['current_sw_version'], "DEBUG: VERSION VERSION"));
  return $matches['current_sw_version'];
}

/*
The function is to get current software stack from ME
*/

function get_current_sw_stack($device_id, $ms_software_inventory) {
  $return_array = array();
  $response = json_decode(import_objects($device_id, array($ms_software_inventory)), True);
  $object_ids_array = $response['wo_newparams'][$ms_software_inventory];
  foreach ($object_ids_array as $object => $vars) {
    if (array_key_exists('version', $vars)) {
      $return_array[$vars['object_id']] = $vars['version'];
    }
  }
  return $return_array;
}

/*
The function is to get current software stack from ME, but for emulation
*/

function get_current_sw_stack_fake($sw_stack) {
  $return_array = array();
  logToFile(debug_dump($sw_stack, "DEBUG: SW STACK"));
  foreach ($sw_stack as $stack => $vars) {
    if (!empty($vars)) {
      $return_array[$stack] = $vars['new_version'];
    }
  }
  return $return_array;
}

/*
The function is walking through software stacks what are located in model directory
and prepares upgrade stages - intermediate steps to upgrade software stack from current 
to the latest one 
*/


function get_possible_sw_stack($model_dir_file_path, $current_version) {
  $return_array = array();
  $possible_stack = '';
  $latest_stack = rtrim(file_get_contents($model_dir_file_path."latest"));
  if ($current_version === $latest_stack) {
    $possible_stack = 'LATEST';
  } else {
    $stack = $latest_stack;
    array_unshift($return_array, $latest_stack);
  }
  $i = 1;
  while (($possible_stack === '') and ($stack !== "NULL") and ($i <10)) {
    $stack_description_path = $model_dir_file_path."".$stack."/stack_description.json";  
    $stack_description = json_decode(file_get_contents($stack_description_path), True);   
    if ($current_version === $stack_description['prerequisite']) {
      $possible_stack = $stack_description['version'];
      if (!in_array($possible_stack, $return_array)) {
        array_unshift($return_array, $possible_stack);
      }
    } else {
      $stack = $stack_description['prerequisite'];
      array_unshift($return_array, $stack);
    }
  $i++;
  }

  return $return_array;
}

/*
The function compares versions and prerequisites of two software stacks and identifies a possibility to upgrade from
 one to another
*/

function validate_upgrade_possibility($model_dir_file_path, $original_sw_stack, $new_sw_stack) {
  $is_valid = "True";
  $wrong_sw_array = array();
  $original_sw_stack_description_path = $model_dir_file_path.$original_sw_stack."/stack_description.json";
  $new_sw_stack_description_path      = $model_dir_file_path.$new_sw_stack."/stack_description.json";
  $original_sw_stack_description = json_decode(file_get_contents($original_sw_stack_description_path), True);
  $new_sw_stack_description      = json_decode(file_get_contents($new_sw_stack_description_path), True);
  foreach ($new_sw_stack_description['components'] as $new_num => $new_properties) {
    reset($original_sw_stack_description['components']);
    while ((list($original_num, $original_properties) = each($original_sw_stack_description['components']) and ($is_valid === "True"))) {
      if ($new_properties['type'] === $original_properties['type']) {
        if ($new_properties['prerequisite'] !== $original_properties['version']) {
          $is_valid = "False";
          $wrong_sw_array = array("sw_type" => $new_properties['type'], "original_version" => $original_properties['version'], "required_version" => $new_properties['prerequisite']);
        }
      }
    }
  }

  return $wrong_sw_array;
}

/*
The function compares current software stack with new one and identifies what
software components are met dependencies, what are not, and what are already have 
required version.
*/


function check_prerequisites($upgrade_stack_path, $current_sw_stack) {
  $return_array = array();
  $stack_description_path = $upgrade_stack_path."/stack_description.json";
  $stack_description = json_decode(file_get_contents($stack_description_path), True);

  foreach ($current_sw_stack as $sw_type => $version) {
    $temp_array = array();
    reset($stack_description['components']);
    while ((list($num, $properties) = each($stack_description['components']) and empty($temp_array))) {
      if ($properties['type'] === $sw_type) {
        $temp_array['original_version'] = $version;
        $temp_array['new_version'] = $properties['version'];
        $temp_array['required_version'] = $properties['prerequisite'];
        if ($temp_array['original_version'] === $temp_array['required_version']) {
          $temp_array['is_prerequisite_met'] = "True";
          $temp_array['will_be_upgraded'] = "True";
        } else {
          $temp_array['is_prerequisite_met'] = "False";
          $temp_array['will_be_upgraded'] = "False";        
        }
        if ($temp_array['original_version'] === $temp_array['new_version']) {
          $temp_array['is_prerequisite_met'] = "True";
          $temp_array['will_be_upgraded'] = "False";
        }
      }
    }
  $return_array[$sw_type] = $temp_array;
  logToFile(debug_dump($return_array, "DEBUG: RETURN ARRAY"));
  }
  return $return_array;
}

/*
The function retrives files, form names and post upgrade actions for 
software components what will be updated
*/

function prepare_upgrade($prerequisite_check, $upgrade_stack_path) {
  $return_array = array();
  $stack_description_path = $upgrade_stack_path."/stack_description.json";
  $stack_description = json_decode(file_get_contents($stack_description_path), True);
  foreach ($prerequisite_check as $sw_type => $vars) {
    if (!empty($vars)) {
      if ($vars['will_be_upgraded'] === "True") {
        reset($stack_description['components']);
        while ((list($num, $properties) = each($stack_description['components']) and empty($temp_array))) {
          if ($properties['type'] === $sw_type) {
            $return_array[$sw_type]['files'] = $properties['files'];
            $return_array[$sw_type]['order'] = $properties['order'];
            $return_array[$sw_type]['post_upgrade'] = $properties['post_upgrade'];
          }
        }

      }
    }
  }
  return $return_array;
}

/*
The function performs upgrade process for a single upgrade stage
*/

function make_upgrade($info_prefix, $context, $upgrade_array, $upgrade_stack_path) {
  $microservices_array = $context['microservices_array'];
  $ms_bios_params = $microservices_array['Software inventory'];
  $ms_server_power = $microservices_array['Server power managment'];
  $device_id = $context['device_id'];
  uasort($upgrade_array, 'compare_order');
  foreach ($upgrade_array as $sw_type => $vars) {
    if ($context['is_emulation'] === 'true') {
      $files = '';
      foreach ($vars['files'] as $key => $value) {
        $files .= $value['form'].": ".$upgrade_stack_path."/".$value['file']."\n";
      }
      $details = $info_prefix."Upgrade ".$sw_type." using the following files:\n".$files;
      $response = update_asynchronous_task_details($context, $details);
      sleep(5);
      $post_upgrade = make_post_upgrade_action($context, $info_prefix, $sw_type, $vars['post_upgrade']);
      } else {
        $micro_service_vars_array = array ();
        $micro_service_vars_array ['object_id'] = $sw_type;
        $micro_service_vars_array ['file_list'] = array();
        $micro_service_vars_array ['form_list'] = array();
        foreach ($vars['files'] as $key => $value) {
          $micro_service_vars_array ['file_list'][] = $upgrade_stack_path."/".$value['file'];
          $micro_service_vars_array ['form_list'][] = $value['form'];
        }
        $ms_array = array($ms_bios_params => array ($sw_type => $micro_service_vars_array));
        $response = json_decode(execute_command_and_verify_response ( $device_id, CMD_UPDATE, $ms_array, "UPDATE ".$sw_type), True);
          if ($response['wo_status'] !== ENDED) {
              $response = json_encode($response);
              echo $response;
              exit;
          }

      }
    }

    //When upgrade is finished, reboot server
    $response = update_asynchronous_task_details($context, $info_prefix."Upgrade process for the stage has been finished. Reboot server. Rebooting... ");
    if ($context['is_emulation'] === "true") {
      sleep(5);
      $response = update_asynchronous_task_details($context, $info_prefix."Upgrade process for the stage has been finished. Reboot server. Rebooting... DONE");
    } else {
      $action = 'ForceRestart';
      $micro_service_vars_array = array ();
      $micro_service_vars_array ['object_id'] = $action;
      $micro_service_vars_array ['action'] = $action;
      $ms_array = array($ms_server_power => array ($action => $micro_service_vars_array));
      $response = json_decode(execute_command_and_verify_response ( $device_id, CMD_CREATE, $ms_array, "CREATE server power state - ".$action), True);
      sleep(180);
      $response = update_asynchronous_task_details($context, $info_prefix."Upgrade process for the stage has been finished. Reboot server. Rebooting... DONE");
    }

  }

/*
The function preforms post upgrade actions. The actions are defined in stack_description.json file for each software component. 
*/


function make_post_upgrade_action($context, $info_prefix, $sw_type, $post_upgrade_actions_array) {
  uasort($post_upgrade_actions_array, 'compare_order');

  foreach ($post_upgrade_actions_array as $action_number => $action_vars) {
    if ($action_vars['action'] === 'wait') {
      $response = update_asynchronous_task_details($context, $info_prefix."Post-upgrade action for ".$sw_type." is wait ".$action_vars['value'].' seconds. Waiting... ');
      sleep($action_vars['value']);
      $response = update_asynchronous_task_details($context, $info_prefix."Post-upgrade action for ".$sw_type." is wait ".$action_vars['value'].' seconds. Waiting... DONE');
      sleep(3);
    } elseif ($action_vars['action'] === 'no') {
      $response = update_asynchronous_task_details($context, $info_prefix."Post-upgrade action for ".$sw_type." is nothing... DONE");
      sleep(3);
    }
  }
  return True;
}

?>