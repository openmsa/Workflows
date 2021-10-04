#!/bin/bash

E_ALL=32767
E_DEPRECATED=8192

check_level=$(( E_ALL & ~E_DEPRECATED ))
#check_level=$E_ALL

# note: E_STRICT is included in E_ALL since PHP 5.4.0


find . -type f -name "*.php" -exec \
php -d error_reporting=${check_level} \
	-l "{}" \; \
	2>&1 > /dev/null |\
awk '{ print } END { if (NR) exit(1) }'
