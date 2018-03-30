<?php
$uuid = md5(uniqid(mt_rand(), true));

$ret = json_encode(array('uuid'=>$uuid));

print($ret);

exit(0);
