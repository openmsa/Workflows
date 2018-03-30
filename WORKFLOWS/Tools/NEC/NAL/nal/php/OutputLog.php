<?php
	# Parameter : className
	# function  : Simple log output
    $timeArray = explode('.',microtime(true));
    $ymd = date('Y/m/d H:i:s', $timeArray[0]) . '.' .$timeArray[1];

	if($argc == 2){
		$name = $argv[1];
	} else {
		$name = 'None';
	}
	$go=1;
	if(($inputpath=getenv("NAL_INPUTFILE")) === false) {
		$go=0;
	}
	if(($outputpath=getenv("NAL_OUTPUTFILE")) === false) {
		$go=0;
	}
	if($go == 1){
		# If there is input file and output file, this function reads those files and output to log
		$out='/var/log/nal/nal_job_trace.log';
		$data_in=file_get_contents($inputpath);
		$data_out=file_get_contents($outputpath);
		$data = $ymd . ' [IN]' . $data_in . '[OUT]' . $data_out . "\n";
		file_put_contents($out, $data, FILE_APPEND);
	}
