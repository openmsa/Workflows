#!/usr/bin/env bash

echo $1 | openssl aes-256-cbc -d -a -pbkdf2 -iter 100000 -salt -pass pass:$2
