<?php

function same_port_lock($port, $date, $device_id) {

  $skip_port = '';
  
  $report = str_replace('/', '_', $port);
  $lock_port = '/tmp/' . $date . '_' . $device_id . '_' . $report;
  $fp_port = @fopen($lock_port, "x");

  if($fp_port === FALSE){
    $skip_port = $port;
  }
  
  @fclose($fp_port);
  
  return $skip_port;
  
}

?>