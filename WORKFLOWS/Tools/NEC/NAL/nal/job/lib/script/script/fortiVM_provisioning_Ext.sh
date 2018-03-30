#!/usr/bin/env python

import pexpect
import sys

########## Validation ##########
argv = sys.argv
argc = len(argv)
if (argc != 18):
    print 'Usage: %s controller_node_address server_user_name server_password keystone_server_addres openstack_user openstack_passwords vnf_name vnf_user vnf_password vnf_address_1 vnf_address_2 tftp_server_address license_file_name vnf_new_password default_gateway default_gateway_device openstack_tenant' %argv[0]
    quit()

############ Set Variables #############
controller_node_address = sys.argv[1]
server_user_name = sys.argv[2]
server_password = sys.argv[3]
keystone_server_address = sys.argv[4]
openstack_user = sys.argv[5]
openstack_password = sys.argv[6]
vnf_name = sys.argv[7]
vnf_user = sys.argv[8]
vnf_password = sys.argv[9]
vnf_address_1 = sys.argv[10]
vnf_address_2 = sys.argv[11]
#dns_address = sys.argv[12]
#proxy_server_address = sys.argv[13]
#proxy_server_port = sys.argv[14]
tftp_server_address = sys.argv[12]
license_file_name = sys.argv[13]
vnf_new_password = sys.argv[14]
default_gateway = sys.argv[15]
default_gateway_device = sys.argv[16]
openstack_tenant = sys.argv[17]

########## Set Enviroment Parameter #######
setcommand1 = "unset OS_SERVICE_TOKEN"
setcommand2 = "export OS_USERNAME=" + openstack_user
setcommand3 = "export OS_PASSWORD=" + openstack_password
setcommand4 = "export OS_AUTH_URL=http://" + keystone_server_address  + ":5000/v2.0"
setcommand5 = "export PS1='[\u@\h \W(keystone_" + openstack_user + ")]\$ '"
setcommand6 = "export OS_TENANT_NAME=" + openstack_tenant
setcommand7 = "export OS_REGION_NAME=regionOne"
getserialURL = "nova get-serial-console " + vnf_name +" | grep serial | awk -F '|' '{print $3}'"
novaconsolePass = "/home/heat-admin/novaconsole/console-client-poll.py"


###### VNF Zero Touch CLI #########
vnf_command1 = "config system interface"
vnf_command2_1 = "edit port1"
vnf_command2_2 = "edit port2"
vnf_command3_1 = "set mode static"
vnf_command3_2 = "set ip " + vnf_address_1
vnf_command3_3 = "set ip " + vnf_address_2
vnf_command4 = "set allowaccess ping https ssh http telnet"
vnf_command5 = "end"
#vnf_command6 = "config system dns"
#vnf_command7 = "set primary " + dns_address
#vnf_command8 = "config system autoupdate tunneling"
#vnf_command9 = "set address " + proxy_server_address
#vnf_command10 = "set port " + proxy_server_port
#vnf_command11 = "set status enable"
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
console = pexpect.spawn ('ssh %s@%s' % (server_user_name, controller_node_address))
console.timeout=3000
i = console.expect_exact(['yes', 'assword: '])
if i == 0: # unknown ssh key
    console.sendline('yes')
    console.expect_exact('assword: ')
console.sendline(server_password)
console.sendline(setcommand1)
console.sendline(setcommand2)
console.sendline(setcommand3)
console.sendline(setcommand4)
console.sendline(setcommand5)
console.sendline(setcommand6)
#console.sendline(setcommand7)
console.sendline(getserialURL)
console.expect("ws.*")
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

#console.sendline(vnf_command6)
#console.expect("\(dns\) #")
#console.sendline(vnf_command7)
#console.expect("\(dns\) #")
#console.sendline(vnf_command5)
#console.expect("#")
#console.sendline(vnf_command8)
#console.expect("\(tunneling\) #")
#console.sendline(vnf_command9)
#console.expect("\(tunneling\) #")
#console.sendline(vnf_command10)
#console.expect("\(tunneling\) #")
#console.sendline(vnf_command11)
#console.expect("\(tunneling\) #")
#console.sendline(vnf_command5)
#console.expect("#")
console.sendline(vnf_command12)
console.expect("\(y\/n\)")
console.sendline(vnf_command13)
print "Restarting..."
console.expect("login")
console.sendline(vnf_user)
console.expect("assword")
console.sendline(vnf_password)
console.expect("#")

console.sendline(vnf_command17)
console.expect("login")
console.sendline(vnf_user)
console.expect("assword")
console.sendline(vnf_password)
console.expect("#")

console.sendline(vnf_command14)
console.expect("\(admin\) #")
console.sendline(vnf_command15)
console.expect("\(admin\) #")
console.sendline(vnf_command16)
console.expect("\(admin\) #")
console.sendline(vnf_command5)
console.expect("#")
console.sendline("exit")
console.expect("login")
console.sendline(vnf_user)
console.expect("assword")
console.sendline(vnf_new_password)
console.expect("#")
print "password change OK"
print "Config OK"

######### VNF Console Auto Logout ###########
console.sendline("exit")
console.expect("login")
console.sendline("~.")

######### VNF Interact Mode ############
console.interact()


