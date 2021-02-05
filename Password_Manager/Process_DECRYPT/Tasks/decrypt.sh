#!/usr/bin/env bash

echo $1 | openssl aes-256-cbc -d -a -salt -pass pass:$2
