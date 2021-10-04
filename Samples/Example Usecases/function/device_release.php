<?php

function device_release($array){

  if($array === FALSE){
    return FALSE;
  }
  $fp = $array['fp'];
  $ret = fclose($fp);
  $fn = $array['fn'];
  @unlink ($fn);
  return $ret;
  
}

?>
