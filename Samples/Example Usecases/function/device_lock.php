<?php

function device_lock($device_id) {
  
  $lock_device = '/tmp/lock_device_' . $device_id . '.lock';
  if(!$fp_device = fopen($lock_device, "w")){
    return FALSE;
  }

  flock($fp_device, LOCK_EX);

  return array('fp' => $fp_device, 'fn' => $lock_device);

}

?>
