#!/usr/bin/env bash

echo $1 | openssl enc -aes-256-cbc -a -salt -pass pass:$2
