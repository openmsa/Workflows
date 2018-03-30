config system interface
edit port1
set mode static
set ip %vnf_address_1%
set allowaccess ping https ssh http telnet
end
config system interface
edit port2
set mode static
set ip  %vnf_address_2%
set allowaccess ping https ssh http telnet
end
config router static
edit 1
set gateway %default_gateway%
set device %default_gateway_device%
end
config system dns
set primary %dns_address%
end
config system autoupdate tunneling
set address %proxy_server_address%
set port %proxy_server_port%
set status enable
end
config system admin
edit admin
set password %vnf_new_password%
end
execute restore vmlicense tftp %license_file_name% %tftp_server_address%
