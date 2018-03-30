#!/usr/bin/env python

#VNF Name:FortiGate VM
#Date    :2017/08/04(r2)

import pexpect
import sys
import time

########## Validation ##########
argv = sys.argv
argc = len(argv)
if (argc != 23):
    print 'Usage: %s controller_node_address server_user_name server_password key_path keystone_server_addres openstack_user openstack_passwords vnf_name vnf_user vnf_password vnf_address_1 vnf_address_2 dns_address proxy_server_address proxy_server_port tftp_server_address license_file_name vnf_new_password default_gateway default_gateway_device openstack_tenant region_name' %argv[0]
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
vnf_address_1 = sys.argv[11]
vnf_address_2 = sys.argv[12]
dns_address = sys.argv[13]
proxy_server_address = sys.argv[14]
proxy_server_port = sys.argv[15]
tftp_server_address = sys.argv[16]
license_file_name = sys.argv[17]
vnf_new_password = sys.argv[18]
default_gateway = sys.argv[19]
default_gateway_device = sys.argv[20]
openstack_tenant = sys.argv[21]
region_name = sys.argv[22]
WAIT_TIME=5
GETURL_WAIT_COUNT=60
CONSOLE_TIMEOUT = 3000

########## Set Enviroment Parameter #######
setcommand1 = "unset OS_SERVICE_TOKEN"
setcommand2 = "export OS_USERNAME=" + openstack_user
setcommand3 = "export OS_PASSWORD=" + openstack_password
setcommand4 = "export OS_AUTH_URL=http://" + keystone_server_address  + ":5000/v2.0"
setcommand5 = "export PS1='[\u@\h \W(keystone_" + openstack_user + ")]\$ '"
setcommand6 = "export OS_TENANT_NAME=" + openstack_tenant
setcommand7 = "export OS_ENDPOINT_TYPE=internalURL"
setcommand8 = "export OS_REGION_NAME=" + region_name
getserialURL = "nova get-serial-console " + vnf_name +" | grep serial | awk -F '|' '{print $3}'"
novaconsolePass = "/home/" + server_user_name + "/novaconsole/console-client-poll.py"
ssh_option = "-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i " + key_path

###### VNF Zero Touch CLI #########
vnf_command1 = "config system interface"
vnf_command2_1 = "edit port1"
vnf_command2_2 = "edit port2"
vnf_command3_1 = "set mode static"
vnf_command3_2 = "set ip " + vnf_address_1
vnf_command3_3 = "set ip " + vnf_address_2
vnf_command4 = "set allowaccess ping https ssh http telnet"
vnf_command5 = "end"
vnf_command6 = "config system dns"
vnf_command7 = "set primary " + dns_address
vnf_command8 = "config system autoupdate tunneling"
vnf_command9 = "set address " + proxy_server_address
vnf_command10 = "set port " + proxy_server_port
vnf_command11 = "set status enable"
vnf_command12 = "execute restore vmlicense tftp" + " " + license_file_name + " " + tftp_server_address
vnf_command13 = "y"
vnf_command14 = "config system admin"
vnf_command15 = "edit admin"
vnf_command16 = "set password " + vnf_new_password
vnf_command17 = "execute update-now"
vnf_command18 = "config router static"
vnf_command19 = "edit 1"
vnf_command20 = "set gateway " + default_gateway
vnf_command21 = "set device " + default_gateway_device 

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
console.expect("connecte")
console.sendline("\r\n")
console.expect("login")
console.sendline(vnf_user)
console.expect("assword")
if "" == vnf_password :
    console.sendline("\r\n")
else:
    console.sendline(vnf_password)
console.expect("#")
print "Fortigate Login OK"

######### Set VNF Zero Touch Config ######
console.sendline(vnf_command1)
console.expect("\(interface\) #")
console.sendline(vnf_command2_1)
console.expect("\(port1\) #")
console.sendline(vnf_command3_1)
console.expect("\(port1\) #")
console.sendline(vnf_command3_2)
console.expect("\(port1\) #")
console.sendline(vnf_command4)
console.expect("\(port1\) #")
console.sendline(vnf_command5)
console.expect("#")

console.sendline(vnf_command1)
console.expect("\(interface\) #")
console.sendline(vnf_command2_2)
console.expect("\(port2\) #")
console.sendline(vnf_command3_1)
console.expect("\(port2\) #")
console.sendline(vnf_command3_3)
console.expect("\(port2\) #")
console.sendline(vnf_command4)
console.expect("\(port2\) #")
console.sendline(vnf_command5)
console.expect("#")

console.sendline(vnf_command18)
console.expect("\(static\) #")
console.sendline(vnf_command19)
console.expect("\(1\) #")
console.sendline(vnf_command20)
console.expect("\(1\) #")
console.sendline(vnf_command21)
console.expect("\(1\) #")
console.sendline(vnf_command5)
console.expect("#")

console.sendline(vnf_command6)
console.expect("\(dns\) #")
console.sendline(vnf_command7)
console.expect("\(dns\) #")
console.sendline(vnf_command5)
console.expect("#")
console.sendline(vnf_command8)
console.expect("\(tunneling\) #")
console.sendline(vnf_command9)
console.expect("\(tunneling\) #")
console.sendline(vnf_command10)
console.expect("\(tunneling\) #")
console.sendline(vnf_command11)
console.expect("\(tunneling\) #")
console.sendline(vnf_command5)
console.expect("#")
console.sendline(vnf_command12)
console.expect("\(y\/n\)")
console.sendline(vnf_command13)
print "Restarting..."
console.expect("login")
console.sendline(vnf_user)
console.expect("assword")
if "" == vnf_password :
    console.sendline("\r\n")
else:
    console.sendline(vnf_password)
console.expect("#")

console.sendline(vnf_command17)

#------------------------------------------------------------------------
# When you enter the update-now command,
#  "enable engine? no
#   enable engine? yes"
#  message is output
# In the subsequent processing, add this message to the keyword of
#  the character string queuing processing
#------------------------------------------------------------------------
######## login ########
while True:
    cmd_ret = console.expect(["login", "enable engine\? yes"])
    if cmd_ret == 0:
        console.sendline(vnf_user)
    elif cmd_ret == 1:
        print "dbg_log(login):enable engine? yes"
        console.sendline("\r\n")
        continue

    cmd_ret = console.expect(["assword", "login", "enable engine\? yes"])
    if cmd_ret == 0:
        if "" == vnf_password :
            console.sendline("\r\n")
        else:
            console.sendline(vnf_password)
        break
    elif cmd_ret == 1:
        print "dbg_log(password):login: -> Relogin"
        console.sendline("\r\n")
    elif cmd_ret == 2:
        print "dbg_log(password):enable engine? yes"
        console.sendline("\r\n")

######## vnf_command14 ########
while True:
    cmd_ret = console.expect(["#", "enable engine\? yes"])
    if cmd_ret == 0:
        console.sendline(vnf_command14)
        break
    elif cmd_ret == 1:
        print "dbg_log(vnf_command14):enable engine? yes"
        console.sendline("\r\n")

######## vnf_command15 ########
while True:
    cmd_ret = console.expect(["\(admin\) #", "enable engine\? yes"])
    if cmd_ret == 0:
        console.sendline(vnf_command15)
        break
    elif cmd_ret == 1:
        print "dbg_log(vnf_command15):enable engine? yes"
        console.sendline("\r\n")

######## vnf_command16 ########
while True:
    cmd_ret = console.expect(["\(admin\) #", "enable engine\? yes"])
    if cmd_ret == 0:
        console.sendline(vnf_command16)
        break
    elif cmd_ret == 1:
        print "dbg_log(vnf_command16):enable engine? yes"
        console.sendline("\r\n")

######## vnf_command5 ########
while True:
    cmd_ret = console.expect(["\(admin\) #", "enable engine\? yes"])
    if cmd_ret == 0:
        console.sendline(vnf_command5)
        break
    elif cmd_ret == 1:
        print "dbg_log(vnf_command5):enable engine? yes"
        console.sendline("\r\n")

######## exit ########
while True:
    cmd_ret = console.expect(["#", "enable engine\? yes"])
    if cmd_ret == 0:
        console.sendline("exit")
        break
    elif cmd_ret == 1:
        print "dbg_log(exit):enable engine? yes"
        console.sendline("\r\n")

######## login ########
while True:
    cmd_ret = console.expect(["login", "enable engine\? yes"])
    if cmd_ret == 0:
        console.sendline(vnf_user)
    elif cmd_ret == 1:
        print "dbg_log(relogin):enable engine? yes"
        console.sendline("\r\n")
        continue

    cmd_ret = console.expect(["assword", "login", "enable engine\? yes"])
    if cmd_ret == 0:
        console.sendline(vnf_new_password)
        break
    elif cmd_ret == 1:
        print "dbg_log(new password):login: -> Relogin"
        console.sendline("\r\n")
    elif cmd_ret == 2:
        print "dbg_log(new password):enable engine? yes"
        console.sendline("\r\n")

######### VNF Console Auto Logout ###########
while True:
    cmd_ret = console.expect(["#", "enable engine\? yes"])
    if cmd_ret == 0:
        print "password change OK"
        print "Config OK"
        console.sendline("exit")
        break
    elif cmd_ret == 1:
        print "dbg_log(Logout):enable engine? yes"
        console.sendline("\r\n")

while True:
    cmd_ret = console.expect(["login", "enable engine\? yes"])
    if cmd_ret == 0:
        console.sendline("~.")
        break
    elif cmd_ret == 1:
        print "dbg_log(Console Auto Logout):enable engine? yes"
        console.sendline("\r\n")

######### VNF Interact Mode ############
while True:
    cmd_ret = console.expect([pexpect.EOF, "enable engine\? yes"])
    if cmd_ret == 0:
        break
    elif cmd_ret == 1:
        print "dbg_log(Interact Mode):enable engine? yes"
        console.sendline("\r\n")

