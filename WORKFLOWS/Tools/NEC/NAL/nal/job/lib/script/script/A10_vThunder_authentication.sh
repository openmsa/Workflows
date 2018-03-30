#!/usr/bin/env python

#VNF Name:A10_vThunder
#Date    :2017/08/04(r1)

import pexpect
import sys
import time

########## Validation ##########
argv = sys.argv
argc = len(argv)
if (argc != 15):
    print 'Usage: %s controller_node_address server_user_name server_password key_path keystone_server_address openstack_user openstack_password vnf_name vnf_user vnf_password tftp_server_address license_file_name openstack_tenant region_name' %argv[0]
    quit()


############ Set Variables #############
controller_node_address = sys.argv[1]
server_user_name = sys.argv[2]
server_password = sys.argv[3]
key_path = sys.argv[4]
keystone_server_address = sys.argv[5]
openstack_user = sys.argv[6]
openstack_password = sys.argv[7]
vnf_name = sys.argv[8]
vnf_user = sys.argv[9]
vnf_password = sys.argv[10]
tftp_server_address = sys.argv[11]
license_file_name = sys.argv[12]
openstack_tenant = sys.argv[13]
region_name = sys.argv[14]
WAIT_TIME=5
GETURL_WAIT_COUNT=60
CONSOLE_TIMEOUT = 600

########## Set Enviroment Parameter #######
setcommand1 = "unset OS_SERVICE_TOKEN"
setcommand2 = "export OS_USERNAME=" + openstack_user
setcommand3 = "export OS_PASSWORD=" + openstack_password
setcommand4 = "export OS_AUTH_URL=http://" + keystone_server_address  + ":5000/v2.0"
setcommand5 = "export PS1='[\u@\h \W(keystone_" + openstack_user + ")]\$ '"
setcommand6 = "export OS_TENANT_NAME=" + openstack_tenant
setcommand7 = "export OS_ENDPOINT_TYPE=internalURL"
setcommand8 = "export OS_REGION_NAME=" + region_name
getserialURL = " nova get-serial-console " + vnf_name +" | grep serial | awk -F '|' '{print $3}'"
novaconsolePass = "/home/" + server_user_name + "/novaconsole/console-client-poll.py"
ssh_option = "-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i " + key_path


###### VNF Zero Touch CLI #########
enable = "enable"
config = "config"
vnf_command1 = "import glm-license license.txt " +  "tftp://" + tftp_server_address + "/" + license_file_name
exit = "exit"
write_memory = "write memory"


######## Host Server Auto Console Connect ###########
if server_password == "" and key_path != "":
    print "ssh public key login"
    console = pexpect.spawn ('ssh %s %s@%s' % (ssh_option, server_user_name, controller_node_address))
    console.timeout=CONSOLE_TIMEOUT
    i = console.expect_exact(['Enter passphrase for key', 'Permission denied', 'assword:', '#', '$'])
    if i == 0 or i == 1 or i == 2:
        print "Error: Incorect key_path"
        print "Error massages:"
        print "=============================="
        print console.before + console.after
        print "=============================="
        sys.exit(2)

elif server_password != "" and key_path == "":
    print "ssh password login"
    console = pexpect.spawn ('ssh %s@%s' % (server_user_name, controller_node_address))
    console.timeout=CONSOLE_TIMEOUT
    i = console.expect_exact(['yes', 'assword: '])
    if i == 0: # unknown ssh key
        console.sendline('yes')
        console.expect_exact('assword: ')
    console.sendline(server_password)
    i = console.expect_exact(['assword: ', '#', '$'])
    if i == 0:
        print "Error: Incorect server_password"
        sys.exit(2)

else:
    print "Error: Unacceptable combination of parameters"
    print "    +-----------------+-----------------------------------------------+"
    print "    |                 |               server_password                 |"
    print "    |                 +----------------------+------------------------+"
    print "    |                 |         SET          |         NULL           |"
    print "    +----------+------+----------------------+------------------------+"
    print "    |          | SET  |         NG           |          OK            |"
    print "    |          |      |                      | (ssh public key login) |"
    print "    | key_path +------+----------------------+------------------------+"
    print "    |          | NULL |         OK           |          NG            |"
    print "    |          |      | (ssh password login) |                        |"
    print "    +----------+------+----------------------+------------------------+"
    sys.exit(2)

console.sendline(setcommand1)
console.sendline(setcommand2)
console.sendline(setcommand3)
console.sendline(setcommand4)
console.sendline(setcommand5)
console.sendline(setcommand6)
console.sendline(setcommand7)
console.sendline(setcommand8)

######## Nova Console Login ########
loop_cnt=0
while True:
    console.expect(".*$")
    console.sendline(getserialURL)
    console.readline()
    cmd_ret = console.expect(['ws://.*', 'ERROR'])
    if cmd_ret == 0:
        print "getURL: OK"
        break
    else:
        loop_cnt = loop_cnt + 1
        time.sleep(WAIT_TIME)
        if loop_cnt == GETURL_WAIT_COUNT:
            print "T.O: getURL %dsec" % (loop_cnt * WAIT_TIME)
            sys.exit(1)

novaconsole = novaconsolePass + " " + console.after
console.sendline(novaconsole)


######## VNF Console Login #########
console.expect("to exit\)")
console.sendline("\r\n")
console.expect("login:")
console.sendline(vnf_user)
console.expect("assword:")
console.sendline(vnf_password)
console.expect(">")
console.sendline(enable)
console.expect("assword:")
console.sendline("\r\n")
console.expect("#")

######## Set VNF Zero Touch Config ##########

##import license license.txt
print "setting license NOW"
console.sendline(vnf_command1)
#print "%s" %vnf_command1
console.expect("#")
print "set license OK"
console.sendline(exit)
console.expect(">")
console.sendline(exit)
console.expect("quit")
console.sendline("y")
console.expect("login:")
console.sendline("\r\n")
console.expect("login:")
console.sendline("~.")
console.expect(pexpect.EOF)

