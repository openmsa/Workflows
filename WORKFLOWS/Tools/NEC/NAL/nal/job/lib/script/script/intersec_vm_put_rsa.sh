#!/usr/bin/env python

#VNF Name:IntersecVM
#Date    :2016/04/26(r0)

import os
import pexpect
import sys
import time

########## Validation ##########
argv = sys.argv
argc = len(argv)
if (argc != 7):
    print 'Usage: %s user_id user_password ip_address instance_name private_key command_path' %argv[0]
    quit()


############ Set Variables #############
user_id = sys.argv[1]
user_password = sys.argv[2]
ip_address = sys.argv[3]
instance_name = sys.argv[4]
private_key = sys.argv[5]
command_path = sys.argv[6]


######## Connect MSA Host ###########
console = pexpect.spawn ('ssh %s@%s' % (user_id, ip_address))
#console.logfile_read = sys.stdout

console.timeout=60
i = console.expect_exact(['yes', 'assword: '])
if i == 0: # unknown ssh key
    console.sendline('yes')
    console.expect_exact('assword: ')

console.sendline(user_password)
console.expect("#")

######## Execute Script(moveKey) ###########
console.sendline('sh ' + command_path + ' ' + instance_name + ' ' + private_key)
time.sleep(10)
console.expect("#")

console.sendline("echo $?")
console.expect("#")
#status = console.buffer
#if status != 0:
#    console.sendline("exit")
#    exit (9)
console.sendline("exit")
console.expect(pexpect.EOF)

exit(0)

