no service config
no ip tftp source-interface
service timestamps debug datetime msec localtime show-timezone
service timestamps log datetime msec localtime show-timezone
service password-encryption
platform console serial
license boot level %boot_level%
license smart enable
enable secret Passw0rd
aaa new-model

hostname csr1000v
username admin password Passw0rd
ip domain-name example.com
interface GigabitEthernet1
ip address %vnf_address% %vnf_netmask%
no cdp enable
no shutdown
exit
line con 0
 password Passw0rd
exit
line vty 0 4
 transport input ssh
 password Passw0rd
exit
ip ssh version 2
crypto key generate rsa modulus 1024
ip access-list extended BLOCK-FILTER
 deny tcp any host %vnf_address% eq 22
 deny udp any host %vnf_address% eq snmp
 permit ip any any
exit
ip prefix-list MSA deny %vnf_network_address%
end
