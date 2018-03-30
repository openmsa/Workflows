#!/usr/bin/env python

#VNF Name:A10_vThunder
#Date    :2017/08/04(r1)

import pexpect
import sys
import time

########## Validation ##########
argv = sys.argv
argc = len(argv)
if (argc != 16):
    print 'Usage: %s controller_node_address server_user_name server_password key_path keystone_server_address openstack_user openstack_password vnf_name vnf_user vnf_password vnf_mgmtip vnf_default_gateway vnf_root_password openstack_tenant region_name' %argv[0]
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
vnf_mgmtip = sys.argv[11]
vnf_default_gateway = sys.argv[12]
vnf_root_password = sys.argv[13]
openstack_tenant = sys.argv[14]
region_name = sys.argv[15]
WAIT_TIME=5
GETURL_WAIT_COUNT=60
LOADING_WAIT_COUNT=24
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
vnf_command1 = "admin admin password " + vnf_root_password
vnf_command2 = "interface management"
vnf_command3 = "ip address " + vnf_mgmtip
vnf_command4 = "ip default-gateway " + vnf_default_gateway
vnf_command5 = "ip control-apps-use-mgmt-port"
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
loop_cnt=0
while True:
    console.expect(".*$")
    console.sendline("\r\n")
    cmd_ret = console.expect(['login:', 'NOLICENSE'])
    if cmd_ret == 0:
        console.sendline(vnf_user)
    elif cmd_ret == 1:
        print "state: NOLICENSE"
        console.expect(">")
        break
    cmd_ret = console.expect(["assword:", 'Session close', 'login:', 'LOADING', 'NOLICENSE'])
    if cmd_ret == 0:
        console.sendline(vnf_password)
    elif cmd_ret == 1:
        #print "INFO1: Session closed -> Relogin"
        console.sendline("\r\n")
        continue
    elif cmd_ret == 2:
        #print "INFO1: login: -> Relogin"
        console.sendline("\r\n")
        continue
    elif cmd_ret == 3:
        console.sendline("\r\n")
    elif cmd_ret == 4:
        print "state: NOLICENSE"
        console.expect(">")
        break

    ## LOADING LOOP
    cmd_ret = console.expect(['Session close', 'login:', 'LOADING', 'NOLICENSE'])
    if cmd_ret == 0:
        #print "INFO2: Session closed -> Relogin"
        console.sendline("\r\n")
        continue
    elif cmd_ret == 1:
        #print "INFO2: login: -> Relogin"
        console.sendline("\r\n")
        continue
    elif cmd_ret == 2:
        print "Now LOADING..."
        while True:
            console.sendline("\r\n")
            cmd_ret = console.expect(['Session close', 'login:', 'LOADING', 'NOLICENSE'])
            if cmd_ret == 0 or cmd_ret == 1:
                print "...End LOADING"
                console.sendline("\r\n")
                break
            elif cmd_ret == 2:
                print "state: LOADING"
            elif cmd_ret == 3:
                print "Change state: LOADING -> NOLICENSE"

            loop_cnt = loop_cnt + 1
            time.sleep(WAIT_TIME)
            if loop_cnt == LOADING_WAIT_COUNT:
                ## Logout
                print "T.O: %dsec" % (loop_cnt * WAIT_TIME)
                console.sendline(exit)
                console.expect("quit")
                console.sendline("y")
                console.expect("login:")
                console.sendline("\r\n")
                console.expect("login:")
                console.sendline("~.")
                sys.exit(1)

    elif cmd_ret == 3:
        print "state: NOLICENSE"
        console.expect(">")
        break

## enable mode
console.sendline(enable)
console.expect("assword:")
console.sendline("\r\n")
console.expect("#")

## show process system
console.sendline("terminal length 0")
console.expect("#")

while True:
    console.sendline("show process system | include a10lb")
    console.expect("a10lb")
    cmd_ret = console.expect(['a10lb', '#'])
    if cmd_ret == 0:
        cmd_ret = console.expect(['not', '#'])
        if cmd_ret == 0:
            print "a10lb is not running"
            console.expect("#")
        elif cmd_ret == 1:
            print "a10lb is running"
            break
    elif cmd_ret == 1:
        print "a10lb does not exist"

    loop_cnt = loop_cnt + 1
    time.sleep(WAIT_TIME)
    if loop_cnt == LOADING_WAIT_COUNT:
        ## Logout
        print "T.O: %dsec" % (loop_cnt * WAIT_TIME)
        console.sendline(exit)
        console.expect(">")
        console.sendline(exit)
        console.expect("quit")
        console.sendline("y")
        console.expect("login:")
        console.sendline("\r\n")
        console.expect("login:")
        console.sendline("~.")
        sys.exit(1)

console.sendline(config)
console.expect("#")

######## Set VNF Zero Touch Config ##########

##admin admin password NEWPASSWORD
print "setting password NOW"
console.sendline(vnf_command1)
print "%s" %vnf_command1
console.expect("#")
print "set password OK"

print "setting interface NOW"
##interface management
console.sendline(vnf_command2)
print "%s" %vnf_command2
console.expect("#")

##ip address IP_ADDRESS
console.sendline(vnf_command3)
print "%s" %vnf_command3
console.expect("#")

##ip default-gateway DEFAULT_GW
console.sendline(vnf_command4)
print "%s" %vnf_command4
console.expect("#")

##ip control-apps-use-mgmt-port
#console.sendline(vnf_command5)
#print "%s" %vnf_command5
#console.expect("#")
console.sendline(exit)
console.expect("#")

##write memory
console.sendline(write_memory)
print "%s" %write_memory
console.expect("[OK]")
console.expect("#")

console.sendline(exit)
console.expect("#")
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

print "setting FINISH!!!"

