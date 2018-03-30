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
if (argc != 6):
    print 'Usage: %s user_id user_password ip_address nal_rsa_pub_dir command_path' %argv[0]
    quit()


############ Set Variables #############
user_id = sys.argv[1]
user_password = sys.argv[2]
ip_address = sys.argv[3]
nal_rsa_pub_dir = sys.argv[4]
command_path = sys.argv[5]


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


######## Execute Script(generateKey) ###########
console.sendline('sh ' + command_path)
time.sleep(10)
console.readline()
console.expect("\r\n")
output = console.before

console.sendline("echo $?")
console.expect("#")
#console.readline()
#status = console.buffer
#if status != 0:
#    console.sendline("exit")
#    exit(9)
console.sendline("exit")
console.expect(pexpect.EOF)

rsa = output.split(",")
if len(rsa) == 0:
    exit(9)


######## SCP From MSA Host(RSA Pub) ###########
scp = pexpect.spawn('scp %s@%s:%s %s' % (user_id, ip_address, rsa[1], nal_rsa_pub_dir))
#scp.logfile_read = sys.stdout
scp.timeout=60
scp.expect('.ssword:*')
scp.sendline(user_password)
scp.expect(pexpect.EOF)

rsa_pub = rsa[1].split("/")
nal_rsa_pub_path = nal_rsa_pub_dir + "/" + rsa_pub[len(rsa_pub)-1]
if os.path.exists(nal_rsa_pub_path) == False:
    exit(9)


######## Connect MSA Host ###########
console = pexpect.spawn ('ssh %s@%s' % (user_id, ip_address))
#console.logfile_read = sys.stdout
console.timeout=60
i = console.expect_exact(['yes', 'assword: '])
if i == 0: # unknown ssh key
    console.sendline('yes')
    console.expect_exact('assword: ')
console.sendline(user_password)


######## Remove RSA Pub ###########
console.sendline("rm -f " + rsa[1])
console.expect("#")
console.sendline("echo $?")
console.expect("#")
#console.readline()
#status = console.buffer
#if status != 0:
#    console.sendline("exit")
#    exit(9)
console.sendline("exit")
console.expect(pexpect.EOF)


######## Read RSA Pub(NAL) ###########
with open(nal_rsa_pub_path, 'r') as f:
    rsa_pub_content = f.read()


######## Remove RSA Pub(NAL) ###########
os.remove(nal_rsa_pub_path)


######## Output Result ###########
print(rsa[0])
print(rsa_pub_content)

exit(0)
