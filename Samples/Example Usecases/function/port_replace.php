<?php

function port_replace($log_port, $import_port){
  
  $interface = "";
  
  $search_head = "";
  $search_tail = "";
  $list_head = "";
  $list_tail = "";
  $int_head = "";
  $int_tail = "";
  
  preg_match('/^(?P<int_head>[[:alpha:]]+)(?P<int_tail>.*)$/', $log_port, $matches);
  $search_head = strtolower($matches['int_head']);
  $search_tail = $matches['int_tail'];

  foreach($import_port as $k => $v){
    preg_match('/^(?P<int_head>[[:alpha:]]+)(?P<int_tail>.*)$/', $k, $matches);
    $list_head = strtolower($matches['int_head']);
    $list_tail = $matches['int_tail'];
    if(strpos($list_head, $search_head) !== FALSE && $list_tail == $search_tail){
      $interface = $k;
    }
  }
  
  return $interface;
  
}

?>