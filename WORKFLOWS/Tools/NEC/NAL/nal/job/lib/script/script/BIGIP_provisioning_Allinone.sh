#!/usr/bin/env python

import pexpect
import sys

########## Validation ##########
argv = sys.argv
argc = len(argv)
if (argc != 16):
    print 'Usage: %s controller_node_address server_user_name server_password keystone_server_addres openstack_user openstack_password vnf_name vnf_user vnf_password vnf_management_ip_address vnf_management_netmask vnf_default_route_name vnf_default_gateway vnf_root_password openstack_tenant' %argv[0]
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
vnf_management_ip_address = sys.argv[10]
vnf_management_netmask = sys.argv[11]
vnf_default_route_name = sys.argv[12]
vnf_default_gateway = sys.argv[13]
vnf_root_password = sys.argv[14]
openstack_tenant = sys.argv[15]

########## Set Enviroment Parameter #######
setcommand1 = "unset OS_SERVICE_TOKEN"
setcommand2 = "export OS_USERNAME=" + openstack_user
setcommand3 = "export OS_PASSWORD=" + openstack_password
setcommand4 = "export OS_AUTH_URL=http://" + keystone_server_address + ":5000/v2.0"
setcommand5 = "export PS1='[\u@\h \W(keystone_" + openstack_user + ")]\$ '"
setcommand6 = "export OS_TENANT_NAME=" + openstack_tenant
setcommand7 = "export OS_REGION_NAME=regionOne"
getserialURL = " nova get-serial-console " + vnf_name +" | grep serial | awk -F '|' '{print $3}'"
novaconsolePass = "/root/novaconsole/console-client-poll.py"


###### VNF Zero Touch CLI #########
vnf_command1 = "tmsh modify sys global-settings mgmt-dhcp disabled"
vnf_command2 = "tmsh create sys management-ip " + vnf_management_ip_address + "/" + vnf_management_netmask
vnf_command3 = "tmsh create sys management-route " + vnf_default_route_name + " gateway " + vnf_default_gateway + " network default"
vnf_command4 = "tmsh modify auth password root"


######## Host Server Auto Console Connect ###########
console = pexpect.spawn ('ssh %s@%s' % (server_user_name, controller_node_address))
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
console.sendline(vnf_command4)
console.expect("new password:")
console.sendline(vnf_root_password)
console.expect("confirm password:")
console.sendline(vnf_root_password)
console.expect("#")

######### VNF Console Auto Logout ###########
console.sendline("exit")
console.expect("login")
console.sendline("~.")

######### VNF Interact Mode ############
console.interact()

