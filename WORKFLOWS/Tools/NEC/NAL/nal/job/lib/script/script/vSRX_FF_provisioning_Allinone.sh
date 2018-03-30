#!/usr/bin/env python

import pexpect
import sys

########## Validation ##########
argv = sys.argv
argc = len(argv)
if (argc != 13):
    print 'Usage: %s controller_node_address server_user_name server_password keystone_server_address openstack_user openstack_password vnf_name vnf_user vnf_password vnf_mgmtif vnf_mgmtip openstack_tenant' %argv[0]
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
vnf_mgmtif = sys.argv[10]
vnf_mgmtip = sys.argv[11]
openstack_tenant = sys.argv[12]


########## Set Enviroment Parameter #######
setcommand1 = "unset OS_SERVICE_TOKEN"
setcommand2 = "export OS_USERNAME=" + openstack_user
setcommand3 = "export OS_PASSWORD=" + openstack_password
setcommand4 = "export OS_AUTH_URL=http://" + keystone_server_address  + ":5000/v2.0"
setcommand5 = "export PS1='[\u@\h \W(keystone_" + openstack_user + ")]\$ '"
setcommand6 = "export OS_TENANT_NAME=" + openstack_tenant
setcommand7 = "export OS_REGION_NAME=RegionOne"
setenvcommand= ". overcloudrc" 
getserialURL = " nova get-serial-console " + vnf_name +" | grep serial | awk -F '|' '{print $3}'"
novaconsolePass = "/root/novaconsole/console-client-poll.py"


###### VNF Zero Touch CLI #########
vnf_changemode1 = "cli"
vnf_changemode2 = "configure"
vnf_command1 = "set system root-authentication plain-text-password"
vnf_command2 = vnf_password
vnf_command3 = "set interfaces " + vnf_mgmtif + " unit 0 family inet address " + vnf_mgmtip
vnf_command4 = "delete security"
vnf_command5 = "set security forwarding-options family mpls mode packet-based"
vnf_command6 = "run request system reboot"
vnf_command7 = "yes"
commit_check = "commit check"
commit = "commit"


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
console.expect("connect")
console.sendline("\r\n")
i = console.expect_exact(['login', '@', '>', '#'])
if i == 0:
    console.sendline(vnf_user)
    console.expect("@")
    console.sendline(vnf_changemode1)
    console.expect(">")
    console.sendline(vnf_changemode2)
    console.expect("#")
elif i == 1:
    console.sendline(vnf_changemode1)
    console.expect(">")
    console.sendline(vnf_changemode2)
    console.expect("#")
elif i == 2:
    console.sendline(vnf_changemode2)
    console.expect("#")


######## Set VNF Zero Touch Config ##########
print "setting password NOW"
console.sendline(vnf_command1)
console.expect("New password:")
console.sendline(vnf_command2)
console.expect("Retype new password:")
console.sendline(vnf_command2)
console.expect("[edit]")
console.expect("#")
console.sendline(commit_check)
console.expect("[edit]")
console.expect("#")
console.sendline(commit)
console.expect("[edit]")
console.expect("#")
console.sendline(vnf_command3)
print "set password OK"
print "setting interface NOW"
console.expect("[edit]")
console.expect("#")
console.sendline(commit_check)
console.expect("[edit]")
console.expect("#")
console.sendline(commit)
console.expect("[edit]")
console.expect("#")
print "set interface OK"
print "setting modechange NOW"
console.sendline(vnf_command4)
console.expect("[edit]")
console.expect("#")
console.sendline(vnf_command5)
console.expect("[edit]")
console.expect("#")
console.sendline(commit_check)
console.expect("[edit]")
console.expect("#")
console.sendline(commit)
console.expect("[edit]")
console.expect("#")
print "set modechange OK"
console.sendline(vnf_command6)
console.expect("[yes,no]")
console.sendline(vnf_command7)
print "reboot now"

######### VNF Console Auto Logout ###########
console.expect("login")
print "reboot OK"
console.sendline("~.")

######### VNF Interact Mode ############
#console.interact()

