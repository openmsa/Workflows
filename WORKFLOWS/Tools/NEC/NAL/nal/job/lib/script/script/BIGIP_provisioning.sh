#!/usr/bin/env python

#VNF Name:BIG-IP VE
#Date    :2017/08/04(r1)

import pexpect
import sys
import time
########## Validation ##########
argv = sys.argv
argc = len(argv)
if (argc != 22):
    print 'Usage: %s controller_node_address server_user_name server_password key_path keystone_server_addres openstack_user openstack_password vnf_name vnf_user vnf_password vnf_management_ip_address vnf_management_netmask vnf_default_route_name vnf_default_gateway vnf_root_password license_key vnf_trunkapl_ip_address vnf_trunkapl_netmask vnf_trunkapl_default_gateway openstack_tenant region_name' %argv[0]
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
vnf_management_ip_address = sys.argv[11]
vnf_management_netmask = sys.argv[12]
vnf_default_route_name = sys.argv[13]
vnf_default_gateway = sys.argv[14]
vnf_root_password = sys.argv[15]
license_key = sys.argv[16]
vnf_trunkapl_ip_address = sys.argv[17]
vnf_trunkapl_netmask = sys.argv[18]
vnf_trunkapl_default_gateway = sys.argv[19]
openstack_tenant = sys.argv[20]
region_name = sys.argv[21]
WAIT_TIME=5
GETURL_WAIT_COUNT=60
MCPD_WAIT_COUNT1=12
MCPD_WAIT_COUNT2=36
CONSOLE_TIMEOUT = 600

########## Set Enviroment Parameter #######
setcommand1 = "unset OS_SERVICE_TOKEN"
setcommand2 = "export OS_USERNAME=" + openstack_user
setcommand3 = "export OS_PASSWORD=" + openstack_password
setcommand4 = "export OS_AUTH_URL=http://" + keystone_server_address + ":5000/v2.0"
setcommand5 = "export PS1='[\u@\h \W(keystone_" + openstack_user + ")]\$ '"
setcommand6 = "export OS_TENANT_NAME=" + openstack_tenant
setcommand7 = "export OS_ENDPOINT_TYPE=internalURL"
setcommand8 = "export OS_REGION_NAME=" + region_name
getserialURL = " nova get-serial-console " + vnf_name +" | grep serial | awk -F '|' '{print $3}'"
novaconsolePass = "/home/" + server_user_name + "/novaconsole/console-client-poll.py"
ssh_option = "-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i " + key_path


###### VNF Zero Touch CLI #########
vnf_command1 = "tmsh modify sys global-settings mgmt-dhcp disabled"
vnf_command2 = "tmsh create sys management-ip " + vnf_management_ip_address + "/" + vnf_management_netmask
vnf_command3 = "tmsh create sys management-route " + vnf_default_route_name + " gateway " + vnf_default_gateway + " network default"

vnf_command4 = "tmsh create net vlan port1 interfaces add { 1.1 { untagged } }"
vnf_command5 = "tmsh create net self eth1 address " + vnf_trunkapl_ip_address + "/" + vnf_trunkapl_netmask + " vlan port1"
vnf_command6 = "tmsh create net route Default_Gateway network 0.0.0.0/0 gw " + vnf_trunkapl_default_gateway

vnf_command7 = "tmsh modify auth password root"

vnf_command8 = "tmsh install sys license registration-key " + license_key

vnf_command9 = "tmsh delete net route Default_Gateway"
vnf_command10 = "tmsh delete net self eth1"
vnf_command11 = "tmsh delete net vlan port1"

save = "tmsh save sys config"

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

## Nova Console Login
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
console.expect("connecte")
console.sendline("\r\n")
console.expect("login")
console.sendline(vnf_user)
console.expect("assword")
console.sendline(vnf_password)
console.expect("#")

######## Ready #########
loop_cnt=0
while True:
    console.sendline("tmsh show sys mcp")
    cmd_ret = console.expect_exact(['running', '#'])
    if cmd_ret == 0:
        print "mcpd ready OK"
        console.expect("#")
        break
    elif cmd_ret==1:
        print "mcpd is not running"
    loop_cnt = loop_cnt + 1
    time.sleep(WAIT_TIME)
    if loop_cnt == MCPD_WAIT_COUNT1:
        print "T.O: %dsec" % (loop_cnt * WAIT_TIME)
        ## Logout
        console.sendline("exit")
        console.expect("login")
        console.sendline("~.")
        sys.exit(1)

######### Set VNF Zero Touch Config ######
console.sendline(vnf_command1)
print "%s" %vnf_command1
console.expect("#")
console.sendline(vnf_command2)
print "%s" %vnf_command2
console.expect("#")
console.sendline(vnf_command3)
print "%s" %vnf_command3
console.expect("#")
console.sendline(vnf_command7)
console.expect("new password:")
console.sendline(vnf_root_password)
console.expect("confirm password:")
console.sendline(vnf_root_password)
console.expect("#")
console.sendline(save)
print "%s" %save
console.expect("#")

######### Set VNF Zero Touch Config ######
console.sendline(vnf_command4)
print "%s" %vnf_command4
console.expect("#")
console.sendline(vnf_command5)
print "%s" %vnf_command5
console.expect("#")
console.sendline(vnf_command6)
print "%s" %vnf_command6
console.expect("#")
##tmsh install sys license registration-key LICENSE_KEY
console.sendline(vnf_command8)
print "%s" %vnf_command8
console.expect("#")

######## Ready #########
loop_cnt=0
while True:
    console.sendline("tmsh show sys mcp")
    cmd_ret = console.expect_exact(['running', '#'])
    if cmd_ret == 0:
        print "mcpd ready OK"
        console.expect("#")
        break
    elif cmd_ret==1:
        print "mcpd is not running"
    loop_cnt = loop_cnt + 1
    time.sleep(WAIT_TIME)
    if loop_cnt == MCPD_WAIT_COUNT2:
        print "T.O: %dsec" % (loop_cnt * WAIT_TIME)
        ## Logout
        console.sendline("exit")
        console.expect("login")
        console.sendline("~.")
        sys.exit(1)

######### Delete VNF Zero Touch Config ######
console.sendline(vnf_command9)
print "%s" %vnf_command9
console.expect("#")
console.sendline(vnf_command10)
print "%s" %vnf_command10
console.expect("#")
console.sendline(vnf_command11)
print "%s" %vnf_command11
console.expect("#")
console.sendline(save)
print "%s" %save
console.expect("#")
######### VNF Console Auto Logout ###########
console.sendline("exit")
console.expect("login")
console.sendline("~.")

######### VNF Interact Mode ############
console.expect(pexpect.EOF)

